#!/bin/bash

# Setup script for Medical Chatbot API

echo "Setting up Medical Chatbot API..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Check for dataset directory
if [ ! -d "../Dataset" ] && [ ! -d "/Users/thrishithreddy/Desktop/Dataset" ]; then
    echo "Warning: Dataset directory not found. Make sure PDF files are in the Dataset folder."
fi

echo ""
echo "Setup complete!"
echo "To run the API server:"
echo "  python3 app.py"
echo ""
echo "Or with uvicorn:"
echo "  uvicorn app:app --host 0.0.0.0 --port 8000"

