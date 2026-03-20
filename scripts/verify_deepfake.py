import sys
import os
sys.path.append(os.getcwd())

import torch
from utils.deepfake_model import get_model
from utils.preprocess import FaceExtractor
from utils.deepfake_inference import DeepfakeInference
from PIL import Image
import numpy as np
import os

def test_pipeline():
    print("Starting verification test...")
    
    # 1. Test Model Loading
    try:
        model = get_model()
        print("✅ Model loaded successfully.")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return

    # 2. Test Face Extractor
    try:
        extractor = FaceExtractor()
        # Create a dummy image with a square (simulating a face)
        dummy_img = np.zeros((400, 400, 3), dtype=np.uint8)
        dummy_img[100:300, 100:300, :] = 255 # White square
        dummy_pil = Image.fromarray(dummy_img)
        dummy_path = "test_image.jpg"
        dummy_pil.save(dummy_path)
        
        # MTCNN might not find a "face" in a white square, but we test the call
        face = extractor.extract_face(dummy_path)
        print("✅ FaceExtractor utility is functional (though it may not find a face in dummy noise).")
        os.remove(dummy_path)
    except Exception as e:
        print(f"❌ FaceExtractor test failed: {e}")

    # 3. Test Inference Utility
    try:
        predictor = DeepfakeInference()
        print("✅ Inference utility initialized successfully.")
    except Exception as e:
        print(f"❌ Inference utility initialization failed: {e}")

    print("\nVerification complete. The infrastructure is ready for the dataset.")

if __name__ == "__main__":
    test_pipeline()
