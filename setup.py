"""
Setup script for Mind Journal application
This script helps set up the necessary components for the Mind Journal application.
"""

import os
import subprocess
import sys
import nltk

def check_python_version():
    """Check if Python version is compatible."""
    required_version = (3, 8)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: Python {required_version[0]}.{required_version[1]} or higher is required")
        print(f"Current version: Python {current_version.major}.{current_version.minor}")
        return False
    
    print(f"✓ Python version check passed: {current_version.major}.{current_version.minor}.{current_version.micro}")
    return True

def install_requirements():
    """Install Python dependencies from requirements file."""
    try:
        print("Installing required packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_list.txt"])
        print("✓ Required packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to install required packages")
        return False

def download_nltk_data():
    """Download necessary NLTK data."""
    try:
        print("Downloading required NLTK data...")
        nltk.download('vader_lexicon')
        nltk.download('punkt')
        print("✓ NLTK data downloaded successfully")
        return True
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")
        return False

def download_spacy_model():
    """Download spaCy language model."""
    try:
        print("Downloading spaCy model...")
        subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
        print("✓ spaCy model downloaded successfully")
        return True
    except subprocess.CalledProcessError:
        print("Error: Failed to download spaCy model")
        return False

def create_instance_directory():
    """Create instance directory if it doesn't exist."""
    if not os.path.exists('instance'):
        os.makedirs('instance')
        print("✓ Created instance directory")
    else:
        print("✓ Instance directory already exists")
    return True

def main():
    """Run the setup process."""
    print("\n=== Mind Journal Application Setup ===\n")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create instance directory
    if not create_instance_directory():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Download NLTK data
    if not download_nltk_data():
        print("Warning: NLTK data download failed, but we'll continue.")
    
    # Download spaCy model
    if not download_spacy_model():
        print("Warning: spaCy model download failed, but we'll continue.")
    
    print("\n=== Setup completed successfully! ===")
    print("\nTo run the application:")
    print("1. Activate your virtual environment (if you're using one)")
    print("2. Run: python app.py")
    print("3. Open your browser and navigate to: http://localhost:5000")

if __name__ == "__main__":
    main()