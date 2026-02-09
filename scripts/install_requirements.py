import subprocess
import sys


def install_packages():
    """Install required packages"""
    packages = [
        'matplotlib>=3.7.0',
        'seaborn>=0.12.0',
        'numpy>=1.24.0',
        'pandas>=2.0.0',
        'scikit-learn>=1.3.0',
        'tensorflow>=2.13.0',
        'keras-tuner>=1.3.0',
        'flask>=2.3.0',
        'flask-cors>=4.0.0',
        'pathlib'
    ]

    print("Installing required packages...")
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✓ Installed: {package}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")


if __name__ == "__main__":
    install_packages()