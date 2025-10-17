#!/bin/bash
# Oracle Samuel Setup Script for Mac/Linux
# © 2025 Dowek Analytics Ltd.

echo "========================================"
echo "ORACLE SAMUEL - THE REAL ESTATE MARKET PROPHET"
echo "Setup Script"
echo "========================================"
echo ""

echo "Step 1: Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi
echo "✓ Virtual environment created"
echo ""

echo "Step 2: Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

echo "Step 3: Upgrading pip..."
pip install --upgrade pip
echo "✓ Pip upgraded"
echo ""

echo "Step 4: Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run Oracle Samuel:"
echo "  1. Activate venv: source venv/bin/activate"
echo "  2. Run app: streamlit run app.py"
echo ""

