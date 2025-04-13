#!/bin/bash

# Mind Journal Application Runner for macOS and Linux

echo "==================================="
echo "Mind Journal - Local Setup"
echo "==================================="
echo

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error creating virtual environment."
        echo "Please make sure Python 3 is installed."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error activating virtual environment."
    exit 1
fi

# Check if requirements are installed
if [ ! -d "venv/lib/python*/site-packages/flask" ]; then
    echo "Installing requirements..."
    pip install -r requirements_list.txt
    if [ $? -ne 0 ]; then
        echo "Error installing requirements."
        exit 1
    fi
fi

# Create instance directory if not exists
if [ ! -d "instance" ]; then
    echo "Creating instance directory..."
    mkdir instance
fi

# Run the application
echo
echo "Starting Mind Journal application..."
echo
echo "Access the application at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo
python run.py

# Deactivate virtual environment when done
deactivate