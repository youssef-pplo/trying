#!/usr/bin/env python3

import sys
import os
import platform
import threading
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path
from typing import List

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QLineEdit, QTextEdit, QProgressBar,
        QComboBox, QFileDialog, QMessageBox, QFrame, QGroupBox
    )
    from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, Signal, QObject
    from PySide6.QtGui import QFont, QPalette, QColor, QIcon
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image, ImageEnhance, ImageFilter
except ImportError as e:
    print(f"Error: Missing required package: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


class WorkerSignals(QObject):
    progress = Signal(float)
    status = Signal(str)
    text_update = Signal(str)
    finished = Signal(str, int, int)
    error = Signal(str)


class ArabicPDFOCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pdf_path = ""
        self.output_path = ""
        self.language = "ara"
        self.dpi = 400
        self.num_passes = 3
        self.is_processing = False
        self.signals = WorkerSignals()
        self.setup_ui()
        self.setup_connections()
        self.check_prerequisites()
        self.center_window()
    
    def setup_ui(self):
        self.setWindowTitle("Arabic PDF to Text OCR")
        self.setGeometry(100, 100, 900, 600)
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                color: #ffffff;
                border: 2px solid #3a3a3a;
                border-radius: 10px;
                margin-top: 8px;
                padding-top: 12px;
                background-color: #252525;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px;
            }
            QLabel {
                color: #ffffff;
            }
            QLineEdit {
                background-color: #2d2d2d;
                border: 2px solid #3a3a3a;
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
                font-size: 12px;
            }
            QLineEdit:focus {
                border: 2px solid #0ea5e9;
            }
            QPushButton {
                background-color: #0ea5e9;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0284c7;
            }
            QPushButton:pressed {
                background-color: #0369a1;
            }
            QPushButton:disabled {
                background-color: #475569;
                color: #94a3b8;
            }
            QTextEdit {
                background-color: #1e1e1e;
                border: 2px solid #3a3a3a;
                border-radius: 8px;
                padding: 10px;
                color: #ffffff;
                font-size: 13px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QProgressBar {
                border: 2px solid #3a3a3a;
                border-radius: 8px;
                text-align: center;
                color: white;
                font-weight: bold;
                background-color: #2d2d2d;
                height: 30px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0ea5e9, stop:1 #06b6d4);
                border-radius: 6px;
            }
            QComboBox {
                background-color: #2d2d2d;
                border: 2px solid #3a3a3a;
                border-radius: 8px;
                padding: 8px;
                color: #ffffff;
                font-size: 12px;
            }
            QComboBox:hover {
                border: 2px solid #0ea5e9;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                border: 2px solid #3a3a3a;
                selection-background-color: #0ea5e9;
                color: #ffffff;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 15, 20, 15)
        
        header = QLabel("Arabic PDF to Text OCR")
        header.setFont(QFont("Segoe UI", 32, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #0ea5e9; margin-bottom: 10px;")
        main_layout.addWidget(header)
        
        subtitle = QLabel("Convert PDF documents with maximum accuracy")
        subtitle.setFont(QFont("Segoe UI", 14))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #94a3b8; margin-bottom: 20px;")
        main_layout.addWidget(subtitle)
        
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        file_layout.setSpacing(10)
        
        pdf_layout = QHBoxLayout()
        pdf_label = QLabel("PDF File:")
        pdf_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        pdf_label.setFixedWidth(120)
        pdf_layout.addWidget(pdf_label)
        
        self.pdf_input = QLineEdit()
        self.pdf_input.setPlaceholderText("Select a PDF file to process...")
        pdf_layout.addWidget(self.pdf_input)
        
        self.browse_pdf_btn = QPushButton("Browse")
        self.browse_pdf_btn.setFixedWidth(100)
        pdf_layout.addWidget(self.browse_pdf_btn)
        file_layout.addLayout(pdf_layout)
        
        output_layout = QHBoxLayout()
        output_label = QLabel("Output File:")
        output_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        output_label.setFixedWidth(120)
        output_layout.addWidget(output_label)
        
        self.output_input = QLineEdit()
        self.output_input.setPlaceholderText("Output text file (auto-generated if empty)...")
        output_layout.addWidget(self.output_input)
        
        self.browse_output_btn = QPushButton("Browse")
        self.browse_output_btn.setFixedWidth(100)
        output_layout.addWidget(self.browse_output_btn)
        file_layout.addLayout(output_layout)
        
        file_group.setLayout(file_layout)
        main_layout.addWidget(file_group)
        
        settings_group = QGroupBox("Settings")
        settings_layout = QVBoxLayout()
        settings_layout.setSpacing(10)
        
        accuracy_layout = QHBoxLayout()
        accuracy_label = QLabel("Accuracy:")
        accuracy_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        accuracy_label.setFixedWidth(120)
        accuracy_layout.addWidget(accuracy_label)
        
        self.accuracy_combo = QComboBox()
        self.accuracy_combo.addItems([
            "Standard (1 pass)",
            "High (2 passes)",
            "Very High (3 passes)",
            "Maximum (4 passes)"
        ])
        self.accuracy_combo.setCurrentIndex(2)
        accuracy_layout.addWidget(self.accuracy_combo)
        settings_layout.addLayout(accuracy_layout)
        
        lang_layout = QHBoxLayout()
        lang_label = QLabel("Language:")
        lang_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        lang_label.setFixedWidth(120)
        lang_layout.addWidget(lang_label)
        
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "Arabic",
            "Arabic + English",
            "English"
        ])
        self.language_combo.setCurrentIndex(0)
        lang_layout.addWidget(self.language_combo)
        settings_layout.addLayout(lang_layout)
        
        dpi_layout = QHBoxLayout()
        dpi_label = QLabel("Quality:")
        dpi_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        dpi_label.setFixedWidth(120)
        dpi_layout.addWidget(dpi_label)
        
        self.dpi_combo = QComboBox()
        self.dpi_combo.addItems([
            "Low (200 DPI)",
            "Medium (300 DPI)",
            "High (400 DPI)",
            "Very High (600 DPI)",
            "Ultra High (800 DPI)"
        ])
        self.dpi_combo.setCurrentIndex(2)
        dpi_layout.addWidget(self.dpi_combo)
        settings_layout.addLayout(dpi_layout)
        
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)
        
        self.process_btn = QPushButton("Process PDF")
        self.process_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.process_btn.setMinimumHeight(45)
        main_layout.addWidget(self.process_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Segoe UI", 11))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("color: #94a3b8; margin-top: 5px;")
        main_layout.addWidget(self.status_label)
        
        stats_layout = QHBoxLayout()
        self.pages_label = QLabel("Pages: 0")
        self.pages_label.setStyleSheet("color: #94a3b8;")
        stats_layout.addWidget(self.pages_label)
        
        self.passes_label = QLabel("Passes: 0")
        self.passes_label.setStyleSheet("color: #94a3b8;")
        stats_layout.addWidget(self.passes_label)
        
        stats_layout.addStretch()
        main_layout.addLayout(stats_layout)
        
        preview_group = QGroupBox("Extracted Text")
        preview_layout = QVBoxLayout()
        
        preview_header = QHBoxLayout()
        preview_header.addStretch()
        
        self.save_btn = QPushButton("Save Text")
        self.save_btn.setFixedWidth(120)
        preview_header.addWidget(self.save_btn)
        
        preview_layout.addLayout(preview_header)
        
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(False)
        preview_layout.addWidget(self.text_preview)
        
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)
    
    def setup_connections(self):
        self.browse_pdf_btn.clicked.connect(self.browse_pdf)
        self.browse_output_btn.clicked.connect(self.browse_output)
        self.process_btn.clicked.connect(self.start_processing)
        self.save_btn.clicked.connect(self.save_text)
        self.signals.progress.connect(self.update_progress)
        self.signals.status.connect(self.update_status)
        self.signals.text_update.connect(self.update_text_preview)
        self.signals.finished.connect(self.on_finished)
        self.signals.error.connect(self.on_error)
    
    def center_window(self):
        frame = self.frameGeometry()
        screen = QApplication.primaryScreen().geometry().center()
        frame.moveCenter(screen)
        self.move(frame.topLeft())
    
    def find_tesseract_windows(self):
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Tesseract-OCR\tesseract.exe",
            os.path.join(os.path.dirname(sys.executable), "tesseract", "tesseract.exe"),
            os.path.join(os.path.dirname(sys.executable), "Tesseract-OCR", "tesseract.exe"),
        ]
        for path in common_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return path
        return None
    
    def install_tesseract_windows_auto(self):
        try:
            app_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
            tesseract_dir = app_dir / "Tesseract-OCR"
            tesseract_exe = tesseract_dir / "tesseract.exe"
            
            if tesseract_exe.exists():
                pytesseract.pytesseract.tesseract_cmd = str(tesseract_exe)
                return True
            
            reply = QMessageBox.question(
                self,
                "Tesseract Not Found",
                "Tesseract OCR is required but not found.\n\n"
                "Would you like to download and install it automatically?\n\n"
                "This will download ~50MB and install Tesseract OCR.",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.No:
                QMessageBox.information(
                    self,
                    "Manual Installation",
                    "Please install Tesseract OCR manually:\n\n"
                    "1. Download from: https://github.com/UB-Mannheim/tesseract/wiki\n"
                    "2. Install to default location\n"
                    "3. Restart this application"
                )
                return False
            
            QMessageBox.information(
                self,
                "Download Required",
                "Automatic installation requires manual download.\n\n"
                "Please:\n"
                "1. Download Tesseract from:\n"
                "   https://github.com/UB-Mannheim/tesseract/wiki\n"
                "2. Install it\n"
                "3. Restart this application\n\n"
                "The app will auto-detect it after installation."
            )
            return False
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to setup Tesseract: {e}")
            return False
    
    def check_prerequisites(self):
        system = platform.system()
        
        if system == "Windows":
            tesseract_path = self.find_tesseract_windows()
            if not tesseract_path:
                try:
                    pytesseract.get_tesseract_version()
                except Exception:
                    self.install_tesseract_windows_auto()
        else:
            try:
                pytesseract.get_tesseract_version()
            except Exception:
                QMessageBox.warning(
                    self,
                    "Tesseract Not Found",
                    "Tesseract OCR is not installed.\n\n"
                    "Installation:\n"
                    "Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-ara\n"
                    "Fedora: sudo dnf install tesseract tesseract-langpack-ara\n"
                    "Arch: sudo pacman -S tesseract tesseract-data-ara"
                )
    
    def browse_pdf(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select PDF File",
            "",
            "PDF Files (*.pdf);;All Files (*)"
        )
        if filename:
            self.pdf_input.setText(filename)
            self.pdf_path = filename
            if not self.output_input.text():
                output = Path(filename).with_suffix('.txt')
                self.output_input.setText(str(output))
                self.output_path = str(output)
    
    def browse_output(self):
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Text As",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            self.output_input.setText(filename)
            self.output_path = filename
    
    def update_progress(self, value):
        self.progress_bar.setValue(int(value * 100))
    
    def update_status(self, message):
        self.status_label.setText(message)
    
    def update_text_preview(self, text):
        self.text_preview.setPlainText(text)
    
    def on_finished(self, output_path, pages, passes):
        self.is_processing = False
        self.process_btn.setEnabled(True)
        self.process_btn.setText("Process PDF")
        self.update_progress(1.0)
        self.update_status(f"Completed! {pages} pages processed with {passes} passes each")
        
        QMessageBox.information(
            self,
            "Success",
            f"PDF processed successfully!\n\n"
            f"Pages: {pages}\n"
            f"Passes per page: {passes}\n"
            f"Output: {output_path}"
        )
    
    def on_error(self, error_msg):
        self.is_processing = False
        self.process_btn.setEnabled(True)
        self.process_btn.setText("Process PDF")
        self.update_progress(0)
        self.update_status(f"Error: {error_msg}")
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_msg}")
    
    def start_processing(self):
        if self.is_processing:
            return
        
        self.pdf_path = self.pdf_input.text()
        output_text = self.output_input.text()
        self.output_path = output_text if output_text else str(Path(self.pdf_path).with_suffix('.txt'))
        
        accuracy_text = self.accuracy_combo.currentText()
        self.num_passes = int(accuracy_text.split('(')[1].split()[0])
        
        lang_text = self.language_combo.currentText()
        lang_map = {
            "Arabic": "ara",
            "Arabic + English": "ara+eng",
            "English": "eng"
        }
        self.language = lang_map.get(lang_text, "ara")
        
        dpi_text = self.dpi_combo.currentText()
        dpi_map = {
            "Low (200 DPI)": 200,
            "Medium (300 DPI)": 300,
            "High (400 DPI)": 400,
            "Very High (600 DPI)": 600,
            "Ultra High (800 DPI)": 800
        }
        self.dpi = dpi_map.get(dpi_text, 400)
        
        if not self.pdf_path:
            QMessageBox.warning(self, "Error", "Please select a PDF file.")
            return
        
        if not Path(self.pdf_path).exists():
            QMessageBox.warning(self, "Error", f"PDF file not found: {self.pdf_path}")
            return
        
        if not Path(self.pdf_path).suffix.lower() == '.pdf':
            QMessageBox.warning(self, "Error", "Selected file is not a PDF.")
            return
        
        self.is_processing = True
        self.process_btn.setEnabled(False)
        self.process_btn.setText("Processing...")
        self.update_progress(0)
        self.update_status("Starting...")
        
        thread = threading.Thread(target=self.process_pdf, daemon=True)
        thread.start()
    
    def preprocess_image(self, image):
        processed = []
        processed.append(image.copy())
        enhancer = ImageEnhance.Contrast(image)
        processed.append(enhancer.enhance(1.5))
        enhancer = ImageEnhance.Sharpness(image)
        processed.append(enhancer.enhance(2.0))
        denoised = image.filter(ImageFilter.MedianFilter(size=3))
        processed.append(denoised)
        if image.mode != 'L':
            gray = image.convert('L')
            enhancer = ImageEnhance.Contrast(gray)
            processed.append(enhancer.enhance(2.0))
        return processed
    
    def ocr_multiple_passes(self, image, lang, num_passes):
        all_results = []
        psm_modes = [
            ('6', 'Uniform block'),
            ('3', 'Automatic'),
            ('11', 'Sparse text'),
            ('12', 'Sparse with OSD')
        ]
        processed_images = self.preprocess_image(image)
        
        for pass_num in range(num_passes):
            psm_mode, _ = psm_modes[pass_num % len(psm_modes)]
            processed_img = processed_images[pass_num % len(processed_images)]
            try:
                config = f'--psm {psm_mode}'
                text = pytesseract.image_to_string(processed_img, lang=lang, config=config)
                if text.strip():
                    all_results.append(text.strip())
            except Exception:
                continue
        
        if not all_results:
            return ""
        
        best_result = max(all_results, key=len)
        all_lines = []
        seen_lines = set()
        for result in all_results:
            lines = result.split('\n')
            for line in lines:
                line_clean = line.strip()
                if line_clean and line_clean not in seen_lines:
                    seen_lines.add(line_clean)
                    all_lines.append(line_clean)
        
        merged_result = '\n'.join(all_lines)
        if len(merged_result) > len(best_result) * 1.2:
            return merged_result
        
        return best_result
    
    def process_pdf(self):
        try:
            self.signals.progress.emit(0.05)
            self.signals.status.emit("Converting PDF to images...")
            
            images = convert_from_path(self.pdf_path, dpi=self.dpi)
            total_pages = len(images)
            
            self.signals.status.emit(f"Found {total_pages} pages")
            self.pages_label.setText(f"Pages: {total_pages}")
            self.passes_label.setText(f"Passes: {self.num_passes}")
            
            self.signals.progress.emit(0.1)
            all_text = []
            
            for i, image in enumerate(images, 1):
                page_progress = 0.1 + (i / total_pages) * 0.85
                self.signals.progress.emit(page_progress)
                self.signals.status.emit(f"Processing page {i}/{total_pages}...")
                
                text = self.ocr_multiple_passes(image, self.language, self.num_passes)
                all_text.append(f"\n{'='*60}\nPage {i}\n{'='*60}\n\n{text}\n")
                
                current_text = '\n'.join(all_text)
                self.signals.text_update.emit(current_text)
            
            full_text = '\n'.join(all_text)
            self.signals.progress.emit(0.95)
            
            output_path = Path(self.output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            
            self.signals.progress.emit(1.0)
            self.signals.finished.emit(str(output_path), total_pages, self.num_passes)
            
        except Exception as e:
            self.signals.error.emit(str(e))
    
    def save_text(self):
        text = self.text_preview.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Warning", "No text to save.")
            return
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Text As",
            "",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text)
                QMessageBox.information(self, "Success", f"Text saved to: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save file:\n{e}")


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = ArabicPDFOCRApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
