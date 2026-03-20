import os
import subprocess
import sys

def main():
    print("="*50)
    print("🚀 Initiating DeepShield Master Training Pipeline")
    print("="*50)
    
    print("\n[1/2] Starting Global AI Image Model Training...")
    try:
        subprocess.run([sys.executable, "scripts/train_global_detector.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Global training failed or was interrupted.")
        return

    print("\n[2/2] Starting Specialized Face AI Model Training...")
    try:
        subprocess.run([sys.executable, "scripts/train_deepfake.py"], check=True)
    except subprocess.CalledProcessError:
        print("❌ Face model training failed or was interrupted.")
        return

    print("\n✅ All AI Models have been successfully trained on the full dataset!")

if __name__ == "__main__":
    main()
