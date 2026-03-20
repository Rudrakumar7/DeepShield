import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from utils.deepfake_model import get_model
from utils.deepfake_dataset import get_dataloader

def train_global_model(train_dir, val_dir, epochs=10, batch_size=16, lr=0.0001):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # We use the same EfficientNet-B0 backbone but focused on global features
    model = get_model(device)
    
    # Load previous weights if available to fine-tune
    weights_path = 'models/checkpoints/best_deepfake_model.pth'
    if os.path.exists(weights_path):
        print(f"Loading existing weights from {weights_path} to fine-tune for global detection...")
        try:
            model.load_state_dict(torch.load(weights_path, map_location=device))
        except:
            print("Existing weights incompatible or corrupted. Starting from pretrained.")
            
    train_loader = get_dataloader(train_dir, batch_size=batch_size, shuffle=True, train=True)
    val_loader = get_dataloader(val_dir, batch_size=batch_size, shuffle=False)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    best_acc = 0.0
    save_path = 'models/checkpoints/global_deepfake_model.pth'
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    for epoch in range(epochs):
        print(f"\nEpoch {epoch+1}/{epochs}")
        print("-" * 10)
        
        # Training Phase
        model.train()
        running_loss = 0.0
        running_corrects = 0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)
            
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
            running_corrects += torch.sum(preds == labels.data)
            
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = running_corrects.double() / len(train_loader.dataset)
        print(f"Train Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")
        
        # Validation Phase
        model.eval()
        val_loss = 0.0
        val_corrects = 0
        
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                loss = criterion(outputs, labels)
                
                val_loss += loss.item() * inputs.size(0)
                val_corrects += torch.sum(preds == labels.data)
                
        val_loss = val_loss / len(val_loader.dataset)
        val_acc = val_corrects.double() / len(val_loader.dataset)
        print(f"Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}")
        
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), save_path)
            print(f"Best model saved! (Acc: {best_acc:.4f})")

if __name__ == "__main__":
    TRAIN_DIR = r'datasets\processed_global\train'
    VAL_DIR = r'datasets\processed_global\val'
    
    # Increased epochs and smaller batch size for better convergence on global features
    train_global_model(TRAIN_DIR, VAL_DIR, epochs=10, batch_size=8, lr=0.00005)
    print("Global model training complete.")
