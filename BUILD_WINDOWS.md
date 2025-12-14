# Building Windows Executable

## Quick Start

### Option 1: Using the Python Script (Linux/Windows)

```bash
python3 build_windows_exe.py
```

### Option 2: Using the Batch File (Windows)

Double-click `build_exe.bat` or run:
```cmd
build_exe.bat
```

### Option 3: Manual Build

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name arabic-pdf-ocr app.py \
  --hidden-import PySide6.QtCore \
  --hidden-import PySide6.QtGui \
  --hidden-import PySide6.QtWidgets \
  --collect-all PySide6
```

## Requirements

1. **Python 3.8+** with all dependencies installed
2. **PyInstaller**: `pip install pyinstaller`
3. **Tesseract OCR** (for Windows): Download from https://github.com/UB-Mannheim/tesseract/wiki
4. **Poppler** (for Windows): Download from https://github.com/oschwartz10612/poppler-windows/releases

## Output

The executable will be created in the `dist/` folder as `arabic-pdf-ocr.exe`

## Important Notes

### For Windows Distribution

The executable requires:
- **Tesseract OCR** installed on the target system
- **Poppler** binaries in PATH or bundled with the app
- **Arabic language data** for Tesseract (`ara.traineddata`)

### Bundling Dependencies

To create a fully standalone executable, you may need to:

1. Bundle Tesseract OCR:
   ```bash
   pyinstaller --add-data "C:/Program Files/Tesseract-OCR;tesseract" app.py
   ```

2. Bundle Poppler:
   ```bash
   pyinstaller --add-data "path/to/poppler/bin;poppler" app.py
   ```

3. Set environment variables in your code to point to bundled paths

### Alternative: Portable Distribution

Instead of bundling, you can create a portable package:
- `arabic-pdf-ocr.exe`
- `tesseract/` folder (Tesseract binaries)
- `poppler/` folder (Poppler binaries)
- `README.txt` with installation instructions

## Troubleshooting

### "Module not found" errors
- Add missing modules with `--hidden-import`
- Use `--collect-all PySide6` to include all Qt modules

### Large executable size
- This is normal for PySide6 applications (usually 50-100MB)
- Use `--onefile` for single file or remove it for folder distribution

### App doesn't start
- Check if all Qt DLLs are included
- Verify Tesseract and Poppler are accessible
- Run from command line to see error messages

