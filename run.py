"""
Simple run script for the Mind Journal application
Run this script to start the application locally with:
python run.py
"""

from app import app

if __name__ == "__main__":
    print("Starting Mind Journal Application...")
    print("Open your browser and navigate to: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)