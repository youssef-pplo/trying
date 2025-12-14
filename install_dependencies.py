#!/usr/bin/env python3

import subprocess
import sys
import os
import platform
from pathlib import Path
import urllib.request
import zipfile
import shutil

def run_command(cmd, check=True):
    try:
        result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def install_python_deps():
    print("Installing Python dependencies...")
    success, _, _ = run_command(f"{sys.executable} -m pip install -r requirements.txt")
    if success:
        print("✓ Python dependencies installed")
    else:
        print("✗ Failed to install Python dependencies")
    return success

def check_tesseract():
    success, _, _ = run_command("tesseract --version")
    return success

def check_poppler():
    success, _, _ = run_command("pdftoppm -v")
    return success

def install_tesseract_windows():
    print("\nTesseract OCR installation for Windows:")
    print("=" * 50)
    print("Please download and install Tesseract OCR from:")
    print("https://github.com/UB-Mannheim/tesseract/wiki")
    print("\nAfter installation, add it to PATH or run:")
    print('setx PATH "%PATH%;C:\\Program Files\\Tesseract-OCR"')
    print("\nFor Arabic support, download:")
    print("https://github.com/tesseract-ocr/tessdata/raw/main/ara.traineddata")
    print("And place it in: C:\\Program Files\\Tesseract-OCR\\tessdata\\")
    return False

def install_poppler_windows():
    print("\nPoppler installation for Windows:")
    print("=" * 50)
    print("Please download Poppler from:")
    print("https://github.com/oschwartz10612/poppler-windows/releases")
    print("\nExtract and add to PATH or place in the same folder as the executable")
    return False

def install_tesseract_linux():
    print("\nInstalling Tesseract OCR...")
    system = platform.system().lower()
    
    if system == "linux":
        distro = platform.linux_distribution()[0].lower() if hasattr(platform, 'linux_distribution') else ""
        
        if "ubuntu" in distro or "debian" in distro:
            success, _, _ = run_command("sudo apt-get update && sudo apt-get install -y tesseract-ocr tesseract-ocr-ara")
        elif "fedora" in distro:
            success, _, _ = run_command("sudo dnf install -y tesseract tesseract-langpack-ara")
        elif "arch" in distro or "manjaro" in distro:
            success, _, _ = run_command("sudo pacman -S --noconfirm tesseract tesseract-data-ara")
        else:
            print("Please install Tesseract OCR manually for your distribution")
            return False
        
        if success:
            print("✓ Tesseract OCR installed")
            return True
        else:
            print("✗ Failed to install Tesseract OCR")
            return False
    
    return False

def install_poppler_linux():
    print("\nInstalling Poppler...")
    system = platform.system().lower()
    
    if system == "linux":
        distro = platform.linux_distribution()[0].lower() if hasattr(platform, 'linux_distribution') else ""
        
        if "ubuntu" in distro or "debian" in distro:
            success, _, _ = run_command("sudo apt-get install -y poppler-utils")
        elif "fedora" in distro:
            success, _, _ = run_command("sudo dnf install -y poppler-utils")
        elif "arch" in distro or "manjaro" in distro:
            success, _, _ = run_command("sudo pacman -S --noconfirm poppler")
        else:
            print("Please install Poppler manually for your distribution")
            return False
        
        if success:
            print("✓ Poppler installed")
            return True
        else:
            print("✗ Failed to install Poppler")
            return False
    
    return False

def main():
    print("Arabic PDF OCR - Dependency Installer")
    print("=" * 50)
    
    system = platform.system()
    print(f"Detected system: {system}")
    
    install_python_deps()
    
    if system == "Windows":
        if not check_tesseract():
            install_tesseract_windows()
        else:
            print("✓ Tesseract OCR found")
        
        if not check_poppler():
            install_poppler_windows()
        else:
            print("✓ Poppler found")
    
    elif system == "Linux":
        if not check_tesseract():
            install_tesseract_linux()
        else:
            print("✓ Tesseract OCR found")
        
        if not check_poppler():
            install_poppler_linux()
        else:
            print("✓ Poppler found")
    
    else:
        print(f"Automatic installation not supported for {system}")
        print("Please install Tesseract OCR and Poppler manually")
    
    print("\n" + "=" * 50)
    print("Installation complete!")
    print("\nYou can now run the application with:")
    print("  python3 app.py")

if __name__ == '__main__':
    main()

