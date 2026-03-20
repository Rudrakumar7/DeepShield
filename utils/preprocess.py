import os
import cv2
import torch
from facenet_pytorch import MTCNN
from PIL import Image
import numpy as np

class FaceExtractor:
    def __init__(self, image_size=224, margin=20, device=None):
        self.device = device if device else (torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'))
        # post_process=False to get raw image before normalization for our custom pipeline
        self.mtcnn = MTCNN(
            image_size=image_size, 
            margin=margin, 
            post_process=False, 
            device=self.device
        )
        self.image_size = image_size

    def extract_face(self, image_path, save_path=None):
        """
        Detects, crops, and resizes face from an image.
        Returns the processed face as a PIL Image.
        """
        try:
            img = Image.open(image_path).convert('RGB')
            # detect and return cropped face
            face = self.mtcnn(img)
            
            if face is not None:
                # MTCNN with post_process=False returns a tensor [3, H, W] in range [0, 255]
                face_np = face.permute(1, 2, 0).numpy().astype(np.uint8)
                face_img = Image.fromarray(face_np)
                
                if save_path:
                    os.makedirs(os.path.dirname(save_path), exist_ok=True)
                    face_img.save(save_path)
                
                return face_img
            else:
                print(f"No face detected in {image_path}")
                return None
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None

    def process_video(self, video_path, output_dir, frame_interval=30):
        """
        Extracts faces from video frames at specified interval.
        """
        v_cap = cv2.VideoCapture(video_path)
        v_len = int(v_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        video_name = os.path.basename(video_path).split('.')[0]
        count = 0
        
        for i in range(v_len):
            success = v_cap.grab()
            if not success:
                break
                
            if i % frame_interval == 0:
                success, frame = v_cap.retrieve()
                if not success:
                    break
                    
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_pil = Image.fromarray(frame)
                
                save_path = os.path.join(output_dir, f"{video_name}_frame_{i}.jpg")
                face = self.mtcnn(frame_pil, save_path=save_path)
                if face is not None:
                    count += 1
        
        v_cap.release()
        print(f"Extracted {count} faces from {video_path}")
        return count

if __name__ == "__main__":
    # Example usage
    extractor = FaceExtractor()
    print(f"Running FaceExtractor on {extractor.device}")
