# Building Windows .exe on Linux

PyInstaller **cannot cross-compile** - it builds for the platform it runs on. However, here are practical solutions:

## Option 1: GitHub Actions (Recommended - FREE)

This is the easiest and free way to build Windows .exe from Linux:

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/ocrapp.git
   git push -u origin main
   ```

2. **GitHub Actions will automatically build:**
   - Go to your GitHub repository
   - Click "Actions" tab
   - The workflow will run automatically
   - Download the `.exe` from artifacts

3. **Or trigger manually:**
   - Go to Actions → "Build Windows Executable"
   - Click "Run workflow"

The workflow file is already created at `.github/workflows/build-windows.yml`

## Option 2: Use a Windows VM

1. Install VirtualBox or VMware
2. Install Windows in the VM
3. Copy project to VM
4. Run `build_windows.bat`

## Option 3: Use Windows Subsystem for Linux (WSL) - Reverse

If you have access to a Windows machine:
1. Use WSL to access your Linux files
2. Build on Windows host using the files

## Option 4: Use Docker (Limited)

Docker on Linux uses Linux containers. Windows containers require:
- Windows Server, OR
- Windows 10/11 Pro with Hyper-V

Not practical for most Linux setups.

## Quick Start with GitHub Actions

```bash
# If you have git repo
git push origin main

# Then go to GitHub → Actions → Download .exe
```

## Manual Build (Requires Windows)

If you have access to a Windows machine:
1. Copy entire `ocrapp` folder to Windows
2. Run `build_windows.bat`
3. Get `dist\arabic-pdf-ocr.exe`

---

**Bottom line:** The easiest way is GitHub Actions - it's free, automatic, and works from Linux!

