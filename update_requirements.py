# update_requirements.py
import subprocess
import sys

def update_requirements():
    packages = [
        "huggingface-hub==0.16.0",
        "transformers==4.30.0",
        "sentence-transformers==2.2.2",
        "torch==2.0.1",
        "accelerate==0.20.0"
    ]
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {e}")

if __name__ == "__main__":
    update_requirements()