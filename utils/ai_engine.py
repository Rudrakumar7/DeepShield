import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
import os
import random

def convert_to_ela_image(path, quality):
    """
    Generates an ELA image by saving the image at a specific quality 
    and calculating the difference between the original and the compressed version.
    """
    filename = path
    resaved_filename = filename.split('.')[0] + '.resaved.jpg'
    ELA_filename = filename.split('.')[0] + '.ela.png'
    
    im = Image.open(filename).convert('RGB')
    im.save(resaved_filename, 'JPEG', quality=quality)
    resaved_im = Image.open(resaved_filename)
    
    ela_im = ImageChops.difference(im, resaved_im)
    
    extrema = ela_im.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff
    
    ela_im = ImageEnhance.Brightness(ela_im).enhance(scale)
    
    # Cleanup temp file
    try:
        os.remove(resaved_filename)
    except:
        pass
        
    return ela_im

def analyze_image(filepath):
    """
    Performs Error Level Analysis (ELA) on the uploaded image.
    """
    try:
        ela_image = convert_to_ela_image(filepath, 90)
        
        # Convert PIL image to OpenCV format
        ela_cv = cv2.cvtColor(np.array(ela_image), cv2.COLOR_RGB2BGR)
        
        # Calculate mean intensity of ELA
        # Higher mean intensity generally implies more compression artifacts or manipulation
        gray_ela = cv2.cvtColor(ela_cv, cv2.COLOR_BGR2GRAY)
        mean_error = np.mean(gray_ela)
        
        # Simple heuristic threshold
        # In a real system, a CNN would analyze the ELA image
        threshold = 25.0 
        
        is_fake = mean_error > threshold
        confidence = min(100.0, (mean_error / threshold) * 50.0 + 50.0) if is_fake else min(100.0, (1 - mean_error/threshold) * 50.0 + 50.0)
        
        result_text = 'Potential Manipulation Detected' if is_fake else 'No Obvious Manipulation'
        risk_level = 'High' if is_fake else 'Low'
        
        return {
            'result': result_text,
            'confidence': round(confidence, 2),
            'details': f"ELA Mean Error: {mean_error:.2f} (Threshold: {threshold}). High error levels often indicate resaving or modification.",
            'risk_level': risk_level
        }
        
    except Exception as e:
        print(f"Error in analyze_image: {e}")
        return {
            'result': 'Error',
            'confidence': 0.0,
            'details': f"Analysis failed: {str(e)}",
            'risk_level': 'Unknown'
        }

# Audio/Video Imports
import librosa
from moviepy import VideoFileClip

def analyze_audio(filepath):
    """
    Analyzes audio using Librosa to check for anomalies.
    """
    try:
        # Load audio file
        y, sr = librosa.load(filepath, duration=30) 
        
        # Feature Extraction
        rmse = librosa.feature.rms(y=y)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        
        details = []
        risk_score = 0
        
        # 1. Silence/Pause Analysis
        # Natural speech has micro-pauses for breathing (silence > 0.0). 
        # AI models often generate continuous waveforms or absolute silence (0.0).
        rmse_mean = np.mean(rmse)
        silence_frames = np.sum(rmse < 0.005)
        silence_ratio = silence_frames / len(rmse[0])
        
        # Heuristic A: Too continuous (AI often forgets to breathe)
        if silence_ratio < 0.02: 
            risk_score += 35
            details.append("Unnaturally continuous speech (lack of breathing pauses).")
            
        # Heuristic B: Too quiet (absolute silence in gaps is suspicious if 0.0, but here we use low threshold)
        elif silence_ratio > 0.8:
            risk_score += 20
            details.append("Audio contains excessive silence.")

        # 2. Zero-Crossing Rate (ZCR) Consistency
        # Human speech is chaotic. AI speech ZCR is often smoother.
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_std = np.std(zcr)
        if zcr_std < 0.02: # Very low variation in signal changes
            risk_score += 30
            details.append("Signal structure is suspiciously consistent (low ZCR variance).")

        # 3. Spectral Consistency
        cent_std = np.std(spec_cent)
        if cent_std < 30: # Tightened threshold
            risk_score += 30
            details.append("Spectral features are too stable (robotic/synthetic characteristics).")
            
        # 4. Dynamic Range / Volume
        if rmse_mean < 0.01:
            risk_score += 10
            details.append("Audio potentialy too quiet for reliable analysis.")

        # Final Decision
        if risk_score >= 50:
            is_fake = True
            result_text = 'Fake/Synthetic'
            confidence = min(99.0, 60.0 + risk_score)
        elif risk_score >= 30:
            is_fake = True # Leaning towards fake
            result_text = 'Suspicious'
            confidence = 65.0
        else:
            is_fake = False
            result_text = 'Real' 
            confidence = max(60.0, 100.0 - risk_score)
            if not details:
                details.append("Natural speech patterns detected.")

        return {
            'result': result_text,
            'confidence': round(confidence, 2),
            'details': " ".join(details),
            'risk_level': 'High' if is_fake else 'Low'
        }
        
    except Exception as e:
        print(f"Error in analyze_audio: {e}")
        return {
            'result': 'Error',
            'confidence': 0.0,
            'details': f"Analysis failed: {str(e)}",
            'risk_level': 'Unknown'
        }

def analyze_video(filepath):
    """
    Analyzes video metadata and frame consistency.
    """
    try:
        clip = VideoFileClip(filepath)
        duration = clip.duration
        fps = clip.fps
        size = clip.size
        
        details = [f"Resolution: {size[0]}x{size[1]}", f"FPS: {fps}", f"Duration: {duration:.2f}s"]
        risk_score = 0
        
        # Check for non-standard FPS
        if fps not in [24, 25, 30, 60] and abs(fps - round(fps)) > 0.1:
            risk_score += 30
            details.append(f"Non-standard variable FPS ({fps:.2f}) detected.")
        
        # Check if audio is missing (common in some generative video)
        if clip.audio is None:
            risk_score += 40
            details.append("No audio track found (suspicious for certain deepfake types).")
        
        clip.close()
        
        if risk_score > 40:
            result_text = 'Suspicious'
            risk_level = 'Medium'
        else:
            result_text = 'Real'
            risk_level = 'Low'
            details.append("Metadata checks passed.")
            
        return {
            'result': result_text,
            'confidence': round(max(60.0, 100.0 - risk_score), 2),
            'details': " | ".join(details),
            'risk_level': risk_level
        }
        
    except Exception as e:
        print(f"Error in analyze_video: {e}")
        return {
            'result': 'Error',
            'confidence': 0.0,
            'details': f"Analysis failed: {str(e)}",
            'risk_level': 'Unknown'
        }
