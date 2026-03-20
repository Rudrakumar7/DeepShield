import os
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image

class DeepfakeDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        """
        data_dir: path to directory containing 'real' and 'fake' folders.
        Each folder should contains images (frames extracted from videos).
        """
        self.data_dir = data_dir
        self.transform = transform
        self.samples = []
        
        for label, class_name in enumerate(['real', 'fake']):
            class_dir = os.path.join(data_dir, class_name)
            if not os.path.exists(class_dir):
                continue
            for img_name in os.listdir(class_dir):
                if img_name.endswith(('.jpg', '.jpeg', '.png')):
                    self.samples.append((os.path.join(class_dir, img_name), label))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
        
        return image, label

def get_transforms(train=False):
    if train:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(15),
            transforms.ColorJitter(brightness=0.1, contrast=0.1, saturation=0.1, hue=0.05),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

def get_dataloader(data_dir, batch_size=32, shuffle=True, train=False):
    dataset = DeepfakeDataset(data_dir, transform=get_transforms(train=train))
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=2)
