#!/usr/bin/env python3

import subprocess
import sys
import os
from pathlib import Path

def check_pyinstaller():
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def build_exe():
    print("Building Windows executable...")
    print("-" * 50)
    
    if not check_pyinstaller():
        print("ERROR: PyInstaller is not installed.")
        print("Install it with: pip install pyinstaller")
        return False
    
    cmd = [
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--name', 'arabic-pdf-ocr',
        '--clean',
        '--noconfirm',
        '--hidden-import', 'PySide6.QtCore',
        '--hidden-import', 'PySide6.QtGui',
        '--hidden-import', 'PySide6.QtWidgets',
        '--hidden-import', 'pytesseract',
        '--hidden-import', 'pdf2image',
        '--hidden-import', 'PIL',
        '--hidden-import', 'PIL.Image',
        '--hidden-import', 'PIL.ImageEnhance',
        '--hidden-import', 'PIL.ImageFilter',
        '--exclude-module', 'torch',
        '--exclude-module', 'numpy',
        '--exclude-module', 'scipy',
        '--exclude-module', 'matplotlib',
        '--exclude-module', 'pandas',
        '--exclude-module', 'sklearn',
        '--exclude-module', 'tensorflow',
        '--exclude-module', 'cv2',
        '--exclude-module', 'PySide6.QtWebEngine',
        '--exclude-module', 'PySide6.QtWebEngineWidgets',
        '--exclude-module', 'PySide6.QtWebSockets',
        '--exclude-module', 'PySide6.QtQuick',
        '--exclude-module', 'PySide6.QtQml',
        '--exclude-module', 'PySide6.Qt3D',
        '--exclude-module', 'PySide6.QtCharts',
        '--exclude-module', 'PySide6.QtDataVisualization',
        '--exclude-module', 'PySide6.QtLocation',
        '--exclude-module', 'PySide6.QtMultimedia',
        '--exclude-module', 'PySide6.QtMultimediaWidgets',
        '--exclude-module', 'PySide6.QtNetwork',
        '--exclude-module', 'PySide6.QtOpenGL',
        '--exclude-module', 'PySide6.QtPositioning',
        '--exclude-module', 'PySide6.QtPrintSupport',
        '--exclude-module', 'PySide6.QtSensors',
        '--exclude-module', 'PySide6.QtSerialPort',
        '--exclude-module', 'PySide6.QtSql',
        '--exclude-module', 'PySide6.QtSvg',
        '--exclude-module', 'PySide6.QtTest',
        '--exclude-module', 'PySide6.QtTextToSpeech',
        '--exclude-module', 'PySide6.QtWebChannel',
        '--exclude-module', 'PySide6.QtXml',
        '--exclude-module', 'PySide6.QtXmlPatterns',
        '--icon=NONE',
        'app.py'
    ]
    
    print(f"Running: pyinstaller [options] app.py")
    print("Excluding unnecessary modules to reduce size...")
    print()
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n" + "=" * 50)
        print("Build completed successfully!")
        print(f"Executable location: dist/arabic-pdf-ocr.exe")
        print("\nNote: The executable still requires:")
        print("  - Tesseract OCR installed on Windows")
        print("  - Poppler binaries in PATH")
        print("\nFor fully standalone, see BUILD_WINDOWS.md")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed: {e}")
        return False
    except Exception as e:
        print(f"\nError: {e}")
        return False

if __name__ == '__main__':
    success = build_exe()
    sys.exit(0 if success else 1)
