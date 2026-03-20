import os
import cv2
import random
import shutil
from tqdm import tqdm

def global_preprocess(raw_dirs, output_base, frame_interval=30):
    """
    Extracts full frames from videos for global manipulation detection.
    Processes the entire dataset without limits.
    """
    os.makedirs(output_base, exist_ok=True)
    
    for category in raw_dirs:
        cat_dirs = raw_dirs[category]
        output_cat_train = os.path.join(output_base, 'train', category)
        output_cat_val = os.path.join(output_base, 'val', category)
        os.makedirs(output_cat_train, exist_ok=True)
        os.makedirs(output_cat_val, exist_ok=True)
        
        # Collect all videos for this category
        all_videos = []
        for d in cat_dirs:
            if os.path.exists(d):
                videos = [os.path.join(d, f) for f in os.listdir(d) if f.endswith(('.mp4', '.avi', '.mov'))]
                all_videos.extend(videos)
        
        print(f"Found {len(all_videos)} videos for category: {category}")
        
        # Shuffle for random train/val distribution
        random.shuffle(all_videos)
        
        # Split into train/val (80/20)
        split_idx = int(len(all_videos) * 0.8)
        train_vids = all_videos[:split_idx]
        val_vids = all_videos[split_idx:]
        
        def extract_frames(video_list, output_dir):
            for v_path in tqdm(video_list, desc=f"Processing {category}"):
                cap = cv2.VideoCapture(v_path)
                frame_count = 0
                saved_count = 0
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    if frame_count % frame_interval == 0:
                        v_name = os.path.basename(v_path).split('.')[0]
                        out_path = os.path.join(output_dir, f"{v_name}_frame_{saved_count}.jpg")
                        cv2.imwrite(out_path, frame)
                        saved_count += 1
                        
                    frame_count += 1
                cap.release()

        print(f"Extracting training frames for {category} ({len(train_vids)} videos)...")
        extract_frames(train_vids, output_cat_train)
        print(f"Extracting validation frames for {category} ({len(val_vids)} videos)...")
        extract_frames(val_vids, output_cat_val)

if __name__ == "__main__":
    DATA_DIRS = {
        'real': [
            r'datasets\raw\FaceForensics++_C23\original',
            r'datasets\raw\archive (1)\Celeb-real',
            r'datasets\raw\archive (1)\YouTube-real'
        ],
        'fake': [
            r'datasets\raw\FaceForensics++_C23\Deepfakes',
            r'datasets\raw\archive (1)\Celeb-synthesis'
        ]
    }
    
    OUTPUT_PATH = r"datasets\processed_global"
    
    # Process ALL videos with 60 frame intervals to prevent extreme data bloat while capturing variation
    print("Initiating FULL dataset global preprocessing...")
    global_preprocess(DATA_DIRS, OUTPUT_PATH, frame_interval=60)
    print("Global preprocessing complete.")
