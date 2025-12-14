# Building Windows .exe File

## Important Note

**You cannot build a Windows .exe file on Linux.** You need to build it on a Windows machine.

## Option 1: Build on Windows (Recommended)

1. **Copy the project to a Windows machine**
   - Copy the entire `ocrapp` folder to Windows

2. **Install Python 3.8+ on Windows**
   - Download from: https://www.python.org/downloads/
   - Make sure to check "Add Python to PATH" during installation

3. **Open Command Prompt or PowerShell in the project folder**

4. **Run the build script:**
   ```cmd
   build_windows.bat
   ```

   Or manually:
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   python build_windows_exe.py
   ```

5. **The .exe file will be in the `dist` folder**

## Option 2: Use GitHub Actions / CI/CD

You can set up automated builds using GitHub Actions to build Windows executables automatically.

## Option 3: Use Docker with Windows Container

If you have Docker with Windows containers, you can build inside a Windows container.

## Current Linux Build

The file at `/win/arabic-pdf-ocr` is a **Linux executable**, not a Windows .exe file.

To get a Windows .exe:
- Build on a Windows machine using `build_windows.bat`
- Or use a Windows virtual machine
- Or use a CI/CD service that supports Windows builds

## Quick Windows Build Command

On Windows, run:
```cmd
build_windows.bat
```

This will:
1. Install PyInstaller
2. Build the .exe file
3. Copy it to `C:\win\arabic-pdf-ocr.exe`

