#!/bin/bash

echo "Building Windows .exe on Linux using Wine"
echo "=========================================="
echo ""

if ! command -v wine &> /dev/null; then
    echo "ERROR: Wine is not installed"
    echo ""
    echo "Install Wine:"
    echo "  Ubuntu/Debian: sudo apt-get install wine"
    echo "  Fedora: sudo dnf install wine"
    echo "  Arch: sudo pacman -S wine"
    exit 1
fi

echo "Wine found: $(wine --version)"
echo ""

echo "This method requires Windows Python installed via Wine."
echo "Alternative: Use a Windows VM or build on actual Windows machine."
echo ""
echo "For now, let's try using pyinstaller with --target-arch option..."
echo ""

if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip3 install pyinstaller
fi

echo "Attempting to build with cross-platform options..."
echo "Note: This may not work perfectly - Windows build is recommended"
echo ""

pyinstaller --onefile --name arabic-pdf-ocr --clean --noconfirm \
  --hidden-import PySide6.QtCore \
  --hidden-import PySide6.QtGui \
  --hidden-import PySide6.QtWidgets \
  --hidden-import pytesseract \
  --hidden-import pdf2image \
  --hidden-import PIL \
  --hidden-import PIL.Image \
  --hidden-import PIL.ImageEnhance \
  --hidden-import PIL.ImageFilter \
  --exclude-module torch \
  --exclude-module numpy \
  --exclude-module scipy \
  --exclude-module matplotlib \
  --exclude-module pandas \
  --exclude-module sklearn \
  --exclude-module tensorflow \
  --exclude-module cv2 \
  --exclude-module PySide6.QtWebEngine \
  --exclude-module PySide6.QtWebEngineWidgets \
  --exclude-module PySide6.QtWebSockets \
  --exclude-module PySide6.QtQuick \
  --exclude-module PySide6.QtQml \
  --exclude-module PySide6.Qt3D \
  --exclude-module PySide6.QtCharts \
  --exclude-module PySide6.QtDataVisualization \
  --exclude-module PySide6.QtLocation \
  --exclude-module PySide6.QtMultimedia \
  --exclude-module PySide6.QtMultimediaWidgets \
  --exclude-module PySide6.QtNetwork \
  --exclude-module PySide6.QtOpenGL \
  --exclude-module PySide6.QtPositioning \
  --exclude-module PySide6.QtPrintSupport \
  --exclude-module PySide6.QtSensors \
  --exclude-module PySide6.QtSerialPort \
  --exclude-module PySide6.QtSql \
  --exclude-module PySide6.QtSvg \
  --exclude-module PySide6.QtTest \
  --exclude-module PySide6.QtTextToSpeech \
  --exclude-module PySide6.QtWebChannel \
  --exclude-module PySide6.QtXml \
  --exclude-module PySide6.QtXmlPatterns \
  app.py

echo ""
if [ -f "dist/arabic-pdf-ocr" ]; then
    echo "Build completed, but this is a Linux executable."
    echo "To create Windows .exe, you need:"
    echo "  1. Windows machine, OR"
    echo "  2. Windows VM, OR"
    echo "  3. GitHub Actions / CI/CD with Windows runner"
    echo ""
    echo "Copying Linux executable to /win anyway..."
    sudo mkdir -p /win
    sudo cp dist/arabic-pdf-ocr /win/arabic-pdf-ocr
    echo "Copied to /win/arabic-pdf-ocr (Linux executable)"
else
    echo "Build failed!"
fi

