# Arabic PDF to Text OCR Converter

A Python application with a modern GUI that converts PDF files to text using Tesseract OCR with Arabic language support. Works on Linux for development/testing and can be packaged as a Windows executable.

## Features

- ✅ **Modern GUI** - User-friendly graphical interface
- ✅ Convert PDF files to text using OCR
- ✅ Arabic language support (with optional English)
- ✅ High-quality image conversion (configurable DPI)
- ✅ Real-time progress tracking
- ✅ Text preview in the application
- ✅ UTF-8 text output
- ✅ Command-line interface also available

## Quick Setup (Auto Install)

Run the auto-installer to install everything automatically:

```bash
./auto_install.sh
```

Or manually:
```bash
python3 install_dependencies.py
```

## Manual Setup

### System Dependencies (Linux)

1. **Tesseract OCR**
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install tesseract-ocr tesseract-ocr-ara
   
   # Fedora
   sudo dnf install tesseract tesseract-langpack-ara
   
   # Arch Linux
   sudo pacman -S tesseract tesseract-data-ara
   ```

2. **Poppler (for PDF to image conversion)**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install poppler-utils
   
   # Fedora
   sudo dnf install poppler-utils
   
   # Arch Linux
   sudo pacman -S poppler
   ```

### Python Dependencies

Install Python packages:
```bash
pip install -r requirements.txt
```

## Usage

### GUI Application (Recommended)

Launch the graphical interface:
```bash
python3 app.py
```

Or use the launcher script:
```bash
./run.sh
```

**GUI Features:**
- Browse and select PDF files
- Choose output location
- Select language (Arabic, Arabic+English, or English)
- Adjust DPI quality settings (200, 300, 400, or 600)
- Real-time progress bar
- Live text preview
- Save extracted text to file

### Command Line Interface

For command-line usage, use `main.py`:

**Basic Usage:**
```bash
python3 main.py document.pdf
```

**Specify Output File:**
```bash
python3 main.py document.pdf -o output.txt
```

**Adjust Quality (DPI):**
```bash
python3 main.py document.pdf --dpi 400
```

**Mixed Arabic/English:**
```bash
python3 main.py document.pdf --lang ara+eng
```

**Command Line Options:**
```
positional arguments:
  pdf_file              Path to the PDF file to process

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output text file path (default: same as PDF with .txt extension)
  --lang LANG           Tesseract language code (default: ara for Arabic)
  --dpi DPI             DPI for PDF to image conversion (default: 300)
```

## Packaging as Windows Executable

**IMPORTANT: Windows .exe files must be built on Windows!**

The Linux build creates a Linux executable, not a Windows .exe file.

### Building on Windows

1. **Copy the project to a Windows machine**

2. **Run the Windows build script:**
   ```cmd
   build_windows.bat
   ```

   This will:
   - Install PyInstaller
   - Build the .exe file
   - Copy it to `C:\win\arabic-pdf-ocr.exe`

3. **Or build manually:**
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller
   python build_windows_exe.py
   ```

### Building on Linux (for Linux executable)

```bash
python3 build_windows_exe.py
```

This creates a Linux executable, not a Windows .exe.

See `BUILD_WINDOWS_INSTRUCTIONS.md` for detailed instructions.

### 3. For Windows Distribution

When packaging for Windows, you'll need to:

1. **Include Tesseract OCR**: Bundle Tesseract with your executable or provide installation instructions
2. **Include Language Data**: Ensure Arabic language data (`ara.traineddata`) is included
3. **Include Poppler**: Bundle poppler binaries for PDF processing

### Advanced PyInstaller Command

```bash
pyinstaller \
  --onefile \
  --name arabic-pdf-ocr \
  --add-data "path/to/tesseract;tesseract" \
  --add-data "path/to/poppler;poppler" \
  --hidden-import pytesseract \
  --hidden-import pdf2image \
  main.py
```

**Note**: For Windows, you'll need to download:
- Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
- Poppler for Windows: https://github.com/oschwartz10612/poppler-windows/releases

## Troubleshooting

### "Tesseract not found"
- Ensure Tesseract is installed and in your PATH
- On Linux, verify with: `which tesseract`

### "Arabic language not found"
- Install Arabic language pack: `sudo apt-get install tesseract-ocr-ara`
- Verify with: `tesseract --list-langs`

### "Poppler not found"
- Install poppler-utils package
- Verify with: `which pdftoppm`

### Poor OCR Quality
- Increase DPI: `--dpi 400` or `--dpi 600`
- Ensure PDF has good quality images/text
- Try different PSM modes by modifying the code

## Project Structure

```
ocrapp/
├── app.py               # GUI application (main)
├── main.py              # Command-line application
├── run.sh               # Quick launcher for GUI
├── setup.sh             # Setup script
├── build_windows_exe.py # Windows executable builder
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues or pull requests for improvements.

