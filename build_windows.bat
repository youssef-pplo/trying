@echo off
echo ========================================
echo Building Windows Executable (.exe)
echo ========================================
echo.

echo Step 1: Installing PyInstaller...
pip install pyinstaller
echo.

echo Step 2: Building executable...
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
  --exclude-module torch ^
  --exclude-module numpy ^
  --exclude-module scipy ^
  --exclude-module matplotlib ^
  --exclude-module pandas ^
  --exclude-module sklearn ^
  --exclude-module tensorflow ^
  --exclude-module cv2 ^
  --exclude-module PySide6.QtWebEngine ^
  --exclude-module PySide6.QtWebEngineWidgets ^
  --exclude-module PySide6.QtWebSockets ^
  --exclude-module PySide6.QtQuick ^
  --exclude-module PySide6.QtQml ^
  --exclude-module PySide6.Qt3D ^
  --exclude-module PySide6.QtCharts ^
  --exclude-module PySide6.QtDataVisualization ^
  --exclude-module PySide6.QtLocation ^
  --exclude-module PySide6.QtMultimedia ^
  --exclude-module PySide6.QtMultimediaWidgets ^
  --exclude-module PySide6.QtNetwork ^
  --exclude-module PySide6.QtOpenGL ^
  --exclude-module PySide6.QtPositioning ^
  --exclude-module PySide6.QtPrintSupport ^
  --exclude-module PySide6.QtSensors ^
  --exclude-module PySide6.QtSerialPort ^
  --exclude-module PySide6.QtSql ^
  --exclude-module PySide6.QtSvg ^
  --exclude-module PySide6.QtTest ^
  --exclude-module PySide6.QtTextToSpeech ^
  --exclude-module PySide6.QtWebChannel ^
  --exclude-module PySide6.QtXml ^
  --exclude-module PySide6.QtXmlPatterns ^
  app.py

echo.
echo ========================================
if exist "dist\arabic-pdf-ocr.exe" (
    echo Build SUCCESSFUL!
    echo.
    echo Executable location: dist\arabic-pdf-ocr.exe
    echo.
    echo Copying to /win directory...
    if not exist "C:\win" mkdir "C:\win"
    copy "dist\arabic-pdf-ocr.exe" "C:\win\arabic-pdf-ocr.exe"
    echo.
    echo Executable copied to: C:\win\arabic-pdf-ocr.exe
) else (
    echo Build FAILED!
    echo Check the error messages above.
)
echo ========================================
pause

