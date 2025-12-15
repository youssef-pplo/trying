#!/usr/bin/env python3

import sys
import os
import io
import platform
import threading
from pathlib import Path
from typing import List

try:
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QPushButton, QLabel, QLineEdit, QTextEdit, QProgressBar,
        QComboBox, QFileDialog, QMessageBox, QFrame, QGroupBox, QDialog, QDialogButtonBox
    )
    from PySide6.QtCore import Qt, Signal, QObject, QUrl
    from PySide6.QtGui import QFont, QDesktopServices
    import fitz
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


class LinkMessageBox(QDialog):
    def __init__(self, parent, title, message, links=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumWidth(500)

        layout = QVBoxLayout()

        label = QLabel(message)
        label.setWordWrap(True)
        label.setOpenExternalLinks(True)
        label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        layout.addWidget(label)

        if links:
            for link_text, link_url in links.items():
                link_label = QLabel(f'<a href="{link_url}" style="color: #0ea5e9;">{link_text}</a>')
                link_label.setOpenExternalLinks(True)
                link_label.linkActivated.connect(lambda url: QDesktopServices.openUrl(QUrl(url)))
                layout.addWidget(link_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setLayout(layout)


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
        header.setFont(QFont("Segoe UI", 24, QFont.Bold))
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #0ea5e9; margin-bottom: 5px;")
        main_layout.addWidget(header)

        subtitle = QLabel("Convert PDF documents with Tesseract OCR")
        subtitle.setFont(QFont("Segoe UI", 11))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #94a3b8; margin-bottom: 10px;")
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

