import cv2
import numpy as np
import os
import random
from PIL import Image, ImageChops, ImageEnhance, ExifTags
from utils.deepfake_inference import DeepfakeInference

# Initialize the Deepfake Models
# 1. Face-Specific Model
try:
    FACE_MODEL_PATH = 'models/checkpoints/best_deepfake_model.pth'
    face_predictor = DeepfakeInference(model_path=FACE_MODEL_PATH)
    print("✅ Face Deepfake Model integrated.")
except Exception as e:
    face_predictor = None
    print(f"⚠️ Face Model load failed: {e}")

# 2. Global Frame Model (New)
try:
    GLOBAL_MODEL_PATH = 'models/checkpoints/global_deepfake_model.pth'
    # Fallback to face model if global weights are still being trained/missing
    active_global_path = GLOBAL_MODEL_PATH if os.path.exists(GLOBAL_MODEL_PATH) else FACE_MODEL_PATH
    global_predictor = DeepfakeInference(model_path=active_global_path)
    print(f"✅ Global Image Model integrated (Weights: {os.path.basename(active_global_path)}).")
except Exception as e:
    global_predictor = None
    print(f"⚠️ Global Model load failed: {e}")

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

def detect_frequency_artifacts(path):
    """
    Uses Fast Fourier Transform (FFT) to detect periodic artifacts 
    common in generative AI and deepfake upscaling.
    """
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return 0.0
        
    dft = np.fft.fft2(img)
    dft_shift = np.fft.fftshift(dft)
    
    # Calculate Magnitude Spectrum
    magnitude_spectrum = 20 * np.log(np.abs(dft_shift) + 1)
    
    # High-frequency analysis
    rows, cols = img.shape
    crow, ccol = rows // 2 , cols // 2
    
    # Analyze the high-frequency quadrants for periodic noise
    # (Simplified: check standard deviation of high-freq areas)
    mask = np.ones((rows, cols), np.uint8)
    r = 30 # radius to exclude low-freq center
    mask[crow-r:crow+r, ccol-r:ccol+r] = 0
    
    high_freq_part = magnitude_spectrum * mask
    non_zero_high_freq = high_freq_part[high_freq_part > 0]
    
    std_val = np.std(non_zero_high_freq) if len(non_zero_high_freq) > 0 else 0
    
    # Generative AI often has unnaturally uniform or periodic high-freq noise (low std in mag spectrum)
    # or extreme high-freq spikes (high std). We normalize to a risk score.
    risk = min(100, std_val * 2) 
    return risk

def check_metadata(path):
    """
    Checks EXIF/Metadata for signatures of AI generation or editing tools.
    """
    try:
        img = Image.open(path)
        info = img.info
        exif = img.getexif()
        
        ai_signatures = ['DALL-E', 'Midjourney', 'Stable Diffusion', 'Adobe Firefly', 'ChatGPT', 'OpenAI', 'Generative AI', 'Photoshop']
        details = []
        risk = 0
        ai_generated_flag = False
        
        # 1. Check basic info/strings
        for key, value in info.items():
            if any(sig.lower() in str(value).lower() for sig in ai_signatures):
                risk += 80
                ai_generated_flag = True
                details.append(f"AI Signature found in metadata: {value}")
                
        # 2. Check EXIF tags
        if exif:
            for tag, value in exif.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                if any(sig.lower() in str(value).lower() for sig in ai_signatures):
                    risk += 80
                    ai_generated_flag = True
                    details.append(f"AI Signature in EXIF ({decoded}): {value}")
        
        # 3. Check for suspiciously missing EXIF (Generative images often lack camera info)
        if not exif or len(exif) < 3:
            # Not conclusive but adds to suspicion
            risk += 15
            details.append("Minimal EXIF metadata (Typical for AI or internet-saved images).")
            
        return min(100, risk), details, ai_generated_flag
    except:
        return 0, []

def analyze_image(filepath):
    """
    Performs comprehensive analysis by combining:
    1. AI Deepfake Model (Face-specific)
    2. FFT Frequency Analysis (Global artifacts)
    3. ELA (Compression/Editing anomalies)
    4. Metadata/EXIF Scanning (AI Signatures)
    """
    try:
        details = []
        scores = {}
        
        # 1. AI Analysis: Face-Specific
        if face_predictor:
            probs, confidence = face_predictor.predict_image(filepath)
            if probs:
                scores['face_ai'] = int(probs['Fake'] * 100)
                details.append(f"Face Analysis: {probs['Fake']*100:.1f}% synthetic prob.")
            else:
                scores['face_ai'] = 0
                details.append("No face detected for specialized AI scan.")
        else:
            scores['face_ai'] = 0

        # 2. AI Analysis: Global Image Context (New)
        if global_predictor:
            # We use predict_global to check the entire frame for inconsistencies
            probs, confidence = global_predictor.predict_global(filepath)
            scores['global_ai'] = int(probs['Fake'] * 100)
            details.append(f"Global AI Context: {probs['Fake']*100:.1f}% manipulation prob.")
        else:
            scores['global_ai'] = 0

        # 2. Frequency Domain Analysis (Focus: AI Generation Patterns)
        fft_risk = detect_frequency_artifacts(filepath)
        scores['fft'] = fft_risk
        if fft_risk > 50:
            details.append(f"Frequency Analysis: High-frequency artifacts detected ({fft_risk:.1f}).")

        # 3. ELA Analysis (Focus: Modification/Resaving)
        ela_image = convert_to_ela_image(filepath, 90)
        ela_cv = cv2.cvtColor(np.array(ela_image), cv2.COLOR_RGB2BGR)
        gray_ela = cv2.cvtColor(ela_cv, cv2.COLOR_BGR2GRAY)
        mean_error = np.mean(gray_ela)
        ela_threshold = 25.0 
        scores['ela'] = min(100, (mean_error / ela_threshold) * 50)
        details.append(f"ELA Analysis: Mean error {mean_error:.2f}.")

        # 4. Metadata Analysis (Focus: AI Signatures)
        meta_risk, meta_details, has_ai_meta = check_metadata(filepath)
        scores['metadata'] = meta_risk
        details.extend(meta_details)

        # --- MULTI-CLASS CATEGORIZATION LOGIC ---
        
        classification = "Real"
        final_risk = 0.0
        
        # Feature values
        face_fakeness = scores.get('face_ai', 0)
        global_fakeness = scores.get('global_ai', 0)
        fft = scores.get('fft', 0)
        ela = scores.get('ela', 0)
        
        # 1. Definitively AI Generated (DALL-E, Midjourney, etc.)
        if has_ai_meta or (global_fakeness > 70 and fft > 60):
            classification = "AI Generated"
            final_risk = max(85, global_fakeness, meta_risk)
        
        # 2. Deepfake (Face Manipulation / Swap)
        elif face_fakeness > 65:
            classification = "Deepfake"
            final_risk = max(70, face_fakeness)
            
        # 3. AI Modified (Background Edits / Generative Fill / Inpainting)
        elif global_fakeness > 55 or ela > 40:
             # If face is real but global/ELA is highly suspicious, it's a local edit
             classification = "AI Modified"
             final_risk = max(60, global_fakeness, ela)
             
        # 4. Real or Mild Suspicion
        else:
            # Calculate a base risk from heuristics
            base_risk = (global_fakeness * 0.4) + (fft * 0.3) + (ela * 0.3)
            final_risk = base_risk
            if final_risk > 45:
                classification = "Suspicious"
            else:
                classification = "Real"

        # Finalize Confidence Values
        is_fake = classification in ["Deepfake", "AI Generated", "AI Modified", "Suspicious"]
        confidence = min(99.0, final_risk if is_fake else (100 - final_risk))
        risk_level = 'High' if classification in ["Deepfake", "AI Generated"] else ('Medium' if classification in ["AI Modified", "Suspicious"] else 'Low')
        
        return {
            'result': classification,
            'confidence': round(confidence, 2),
            'details': " | ".join(details) if details else "No obvious manipulation detected.",
            'risk_level': risk_level,
            'model_type': 'Multi-Class AI Engine'
        }
        
    except Exception as e:
        print(f"Error in analyze_image: {e}")
        return {
            'result': 'Error',
            'confidence': 0.0,
            'details': f"Analysis failed: {str(e)}",
            'risk_level': 'Unknown'
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
