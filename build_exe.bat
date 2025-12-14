@echo off
echo Building Windows Executable...
echo.

pip install pyinstaller

pyinstaller --onefile --windowed --name arabic-pdf-ocr --clean --noconfirm ^
  --hidden-import PySide6.QtCore ^
  --hidden-import PySide6.QtGui ^
  --hidden-import PySide6.QtWidgets ^
  --hidden-import pytesseract ^
  --hidden-import pdf2image ^
  --hidden-import PIL ^
  --hidden-import PIL.Image ^
  --hidden-import PIL.ImageEnhance ^
  --hidden-import PIL.ImageFilter ^
  --collect-all PySide6 ^
  app.py

echo.
echo Build complete! Check the dist folder for arabic-pdf-ocr.exe
echo.
echo Note: You need to install Tesseract OCR and Poppler separately:
echo - Tesseract: https://github.com/UB-Mannheim/tesseract/wiki
echo - Poppler: https://github.com/oschwartz10612/poppler-windows/releases
pause

