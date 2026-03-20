import os
import sys
# Resolve potential DLL conflicts on Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "True"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import random
import shutil
from tqdm import tqdm

# Add project root to path
sys.path.append(os.getcwd())
from utils.preprocess import FaceExtractor

def bulk_process(raw_dirs, output_base, frame_interval=30, split_ratio=0.8):
    """
    raw_dirs: dict with key 'real' or 'fake' and value as list of directories
    output_base: where to save processed images
    """
    extractor = FaceExtractor()
    print(f"Starting bulk preprocessing on {extractor.device}...")

    # Create directory structure
    for split in ['train', 'val']:
        for cat in ['real', 'fake']:
            os.makedirs(os.path.join(output_base, split, cat), exist_ok=True)

    for cat, dirs in raw_dirs.items():
        print(f"Processing category: {cat}")
        all_videos = []
        for d in dirs:
            if os.path.exists(d):
                videos = [os.path.join(d, f) for f in os.listdir(d) if f.endswith(('.mp4', '.avi', '.mkv'))]
                all_videos.extend(videos)
        
        # Shuffle for random distribution
        random.shuffle(all_videos)
        
        split_idx = int(len(all_videos) * split_ratio)
        train_videos = all_videos[:split_idx]
        val_videos = all_videos[split_idx:]

        # Process Train
        print(f"  Extracting faces for {cat} - Train ({len(train_videos)} videos)")
        for v in tqdm(train_videos):
            out_dir = os.path.join(output_base, 'train', cat)
            extractor.process_video(v, out_dir, frame_interval=frame_interval)

        # Process Val
        print(f"  Extracting faces for {cat} - Val ({len(val_videos)} videos)")
        for v in tqdm(val_videos):
            out_dir = os.path.join(output_base, 'val', cat)
            extractor.process_video(v, out_dir, frame_interval=frame_interval)

if __name__ == "__main__":
    # Define dataset paths
    DATA_DIRS = {
        'real': [
            r"datasets\raw\FaceForensics++_C23\original",
            r"datasets\raw\archive (1)\Celeb-real",
            r"datasets\raw\archive (1)\YouTube-real"
        ],
        'fake': [
            r"datasets\raw\FaceForensics++_C23\Deepfakes",
            r"datasets\raw\FaceForensics++_C23\Face2Face",
            r"datasets\raw\archive (1)\Celeb-synthesis"
        ]
    }
    
    OUTPUT_PATH = r"datasets\processed"
    
    # Process ALL videos for maximum accuracy
    print("Initiating FULL dataset face preprocessing...")
    bulk_process(DATA_DIRS, OUTPUT_PATH, frame_interval=30)
    print("Bulk face preprocessing complete.")
