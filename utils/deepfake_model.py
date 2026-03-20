import torch
import torch.nn as nn
import timm

class DeepfakeDetector(nn.Module):
    def __init__(self, model_name='efficientnet_b0', pretrained=True, num_classes=2):
        super(DeepfakeDetector, self).__init__()
        # Load pretrained EfficientNet-B0
        self.model = timm.create_model(model_name, pretrained=pretrained)
        
        # Modify the classifier head for binary classification (Real vs Fake)
        # EfficientNet-B0 typically has 'classifier' as the head
        in_features = self.model.classifier.in_features
        self.model.classifier = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        return self.model(x)

def get_model(device=None):
    device = device if device else (torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu'))
    model = DeepfakeDetector()
    return model.to(device)

if __name__ == "__main__":
    model = get_model()
    print(f"Model loaded and moved to {next(model.parameters()).device}")
    # Dummy test
    x = torch.randn(1, 3, 224, 224).to(next(model.parameters()).device)
    output = model(x)
    print(f"Output shape: {output.shape}")
