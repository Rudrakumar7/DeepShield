import os
import sys

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from utils.deepfake_model import get_model
from utils.deepfake_dataset import get_dataloader
import time

def train_model(train_dir, val_dir, epochs=5, batch_size=4, lr=0.0001):
    device = torch.device('cuda' if torch.cuda.is_available() else torch.device('cpu'))
    print(f"Using device: {device}")
    
    model = get_model(device)
    
    # Check if we have previous weights to continue from
    checkpoint_path = 'models/checkpoints/best_deepfake_model.pth'
    if os.path.exists(checkpoint_path):
        print(f"Loading existing weights from {checkpoint_path}")
        model.load_state_dict(torch.load(checkpoint_path, map_location=device))
    
    train_loader = get_dataloader(train_dir, batch_size=batch_size, shuffle=True, train=True)
    val_loader = get_dataloader(val_dir, batch_size=batch_size, shuffle=False)
    
    print(f"Train samples: {len(train_loader.dataset)}")
    print(f"Val samples: {len(val_loader.dataset)}")
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)
    
    best_acc = 0.0
    
    for epoch in range(epochs):
        start_time = time.time()
        print(f"\nEpoch {epoch+1}/{epochs}")
        print("-" * 10)
        
        model.train()
        running_loss = 0.0
        running_corrects = 0
        
        processed_batches = 0
        total_batches = len(train_loader)
        
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
            
            processed_batches += 1
            if processed_batches % 10 == 0 or processed_batches == total_batches:
                print(f"\rBatch {processed_batches}/{total_batches} Loss: {loss.item():.4f}", end="")
            
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = running_corrects.double() / len(train_loader.dataset)
        
        print(f"\nTrain Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}")
        
        # Validation
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
        print(f"Time: {time.time() - start_time:.2f}s")
        
        if val_acc > best_acc:
            best_acc = val_acc
            save_path = 'models/checkpoints/best_deepfake_model_new.pth'
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            torch.save(model.state_dict(), save_path)
            print("New best model saved!")

if __name__ == "__main__":
    TRAIN_DIR = r'datasets\processed\train'
    VAL_DIR = r'datasets\processed\val'
    train_model(TRAIN_DIR, VAL_DIR, epochs=5, batch_size=4, lr=0.0001)
    print("\nTraining complete.")
