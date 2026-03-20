import torch
import torch.nn.functional as F
from PIL import Image
from utils.deepfake_model import get_model
from utils.deepfake_dataset import get_transforms
from utils.preprocess import FaceExtractor
import os

class DeepfakeInference:
    def __init__(self, model_path=None, device=None):
        self.device = device if device else (torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'))
        self.model = get_model(self.device)
        
        if model_path and os.path.exists(model_path):
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))
            self.model.eval()
            print(f"Loaded model from {model_path}")
        else:
            print("Warning: Running with untrained model weights!")
            self.model.eval()
            
        self.face_extractor = FaceExtractor(device=self.device)
        self.transforms = get_transforms()

    def predict_image(self, image_path):
        """
        Face-specific prediction (Legacy/Face-focused)
        """
        face_img = self.face_extractor.extract_face(image_path)
        if face_img is None:
            return None, 0.0
        return self._predict_transformed(face_img)

    def predict_global(self, image_path):
        """
        Whole-image prediction (Analyzes the entire frame)
        """
        img = Image.open(image_path).convert('RGB')
        return self._predict_transformed(img)

    def _predict_transformed(self, pil_img):
        """
        Core inference logic on a PIL image.
        """
        input_tensor = self.transforms(pil_img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            output = self.model(input_tensor)
            probabilities = F.softmax(output, dim=1).cpu().numpy()[0]
            
        probs_dict = {
            'Real': float(probabilities[0]),
            'Fake': float(probabilities[1])
        }
        max_prob = float(max(probabilities))
        return probs_dict, max_prob

if __name__ == "__main__":
    # Example usage
    predictor = DeepfakeInference()
    print("Inference utility ready.")
