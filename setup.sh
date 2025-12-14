#!/bin/bash

set -e

echo "Arabic PDF OCR - Setup Script"
echo "=============================="
echo ""

# Check if running on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Warning: This script is designed for Linux"
fi

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check for pip
if ! command -v pip3 &> /dev/null && ! command -v pip &> /dev/null; then
    echo "ERROR: pip is not installed"
    exit 1
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt || pip install -r requirements.txt
echo "✓ Python dependencies installed"
echo ""

# Check for Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "WARNING: Tesseract OCR is not installed"
    echo ""
    echo "Please install Tesseract OCR:"
    echo "  Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-ara"
    echo "  Fedora: sudo dnf install tesseract tesseract-langpack-ara"
    echo "  Arch: sudo pacman -S tesseract tesseract-data-ara"
    echo ""
else
    echo "✓ Tesseract OCR found: $(tesseract --version | head -n 1)"
    
    # Check for Arabic language
    if tesseract --list-langs 2>/dev/null | grep -q "ara"; then
        echo "✓ Arabic language data found"
    else
        echo "WARNING: Arabic language data not found"
        echo "  Install with: sudo apt-get install tesseract-ocr-ara"
    fi
    echo ""
fi

# Check for Poppler
if ! command -v pdftoppm &> /dev/null; then
    echo "WARNING: Poppler is not installed"
    echo ""
    echo "Please install Poppler:"
    echo "  Ubuntu/Debian: sudo apt-get install poppler-utils"
    echo "  Fedora: sudo dnf install poppler-utils"
    echo "  Arch: sudo pacman -S poppler"
    echo ""
else
    echo "✓ Poppler found: $(pdftoppm -v 2>&1 | head -n 1)"
    echo ""
fi

echo "=============================="
echo "Setup complete!"
echo ""
echo "Usage:"
echo "  python3 main.py your_document.pdf"
echo ""


