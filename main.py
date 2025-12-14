#!/usr/bin/env python3
"""
Arabic PDF to Text Converter using Tesseract OCR
Converts PDF files to text using Tesseract OCR with Arabic language support.
"""

import os
import sys
import argparse
from pathlib import Path
from typing import List, Optional

try:
    from pdf2image import convert_from_path
    import pytesseract
    from PIL import Image
except ImportError as e:
    print(f"Error: Missing required package. Please install dependencies: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)


def check_tesseract_installed() -> bool:
    """Check if Tesseract OCR is installed on the system."""
    try:
        pytesseract.get_tesseract_version()
        return True
    except Exception:
        return False


def check_arabic_language() -> bool:
    """Check if Arabic language data is available for Tesseract."""
    try:
        # Try to get available languages
        langs = pytesseract.get_languages()
        return 'ara' in langs or 'ara+eng' in langs
    except Exception:
        return False


def pdf_to_images(pdf_path: str, dpi: int = 300) -> List[Image.Image]:
    """
    Convert PDF pages to images.
    
    Args:
        pdf_path: Path to the PDF file
        dpi: Resolution for image conversion (default: 300)
    
    Returns:
        List of PIL Image objects
    """
    try:
        print(f"Converting PDF to images (DPI: {dpi})...")
        images = convert_from_path(pdf_path, dpi=dpi)
        print(f"Successfully converted {len(images)} pages to images.")
        return images
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        raise


def ocr_image_to_text(image: Image.Image, lang: str = 'ara') -> str:
    """
    Perform OCR on an image and extract text.
    
    Args:
        image: PIL Image object
        lang: Tesseract language code (default: 'ara' for Arabic)
    
    Returns:
        Extracted text string
    """
    try:
        # Configure Tesseract for Arabic
        config = '--psm 6'  # Assume uniform block of text
        text = pytesseract.image_to_string(image, lang=lang, config=config)
        return text
    except Exception as e:
        print(f"Error during OCR: {e}")
        raise


def process_pdf(pdf_path: str, output_path: Optional[str] = None, lang: str = 'ara', dpi: int = 300) -> str:
    """
    Process a PDF file and extract Arabic text.
    
    Args:
        pdf_path: Path to input PDF file
        output_path: Path to output text file (optional)
        lang: Tesseract language code
        dpi: Resolution for PDF to image conversion
    
    Returns:
        Extracted text content
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    if not pdf_path.suffix.lower() == '.pdf':
        raise ValueError(f"File is not a PDF: {pdf_path}")
    
    print(f"\nProcessing PDF: {pdf_path.name}")
    print("-" * 50)
    
    # Convert PDF to images
    images = pdf_to_images(str(pdf_path), dpi=dpi)
    
    # Process each page
    all_text = []
    for i, image in enumerate(images, 1):
        print(f"Processing page {i}/{len(images)}...", end=' ', flush=True)
        text = ocr_image_to_text(image, lang=lang)
        all_text.append(f"\n{'='*50}\nPage {i}\n{'='*50}\n\n{text}")
        print("Done")
    
    full_text = '\n'.join(all_text)
    
    # Save to file if output path is specified
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        print(f"\nText saved to: {output_path}")
    else:
        # Default output: same name as PDF but with .txt extension
        default_output = pdf_path.with_suffix('.txt')
        with open(default_output, 'w', encoding='utf-8') as f:
            f.write(full_text)
        print(f"\nText saved to: {default_output}")
    
    return full_text


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='Convert PDF files to text using Tesseract OCR (Arabic language)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py document.pdf
  python main.py document.pdf -o output.txt
  python main.py document.pdf --dpi 400 --lang ara+eng
        """
    )
    
    parser.add_argument(
        'pdf_file',
        type=str,
        help='Path to the PDF file to process'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output text file path (default: same as PDF with .txt extension)'
    )
    
    parser.add_argument(
        '--lang',
        type=str,
        default='ara',
        help='Tesseract language code (default: ara for Arabic, use ara+eng for mixed)'
    )
    
    parser.add_argument(
        '--dpi',
        type=int,
        default=300,
        help='DPI for PDF to image conversion (default: 300, higher = better quality but slower)'
    )
    
    args = parser.parse_args()
    
    # Check prerequisites
    print("Checking prerequisites...")
    if not check_tesseract_installed():
        print("\nERROR: Tesseract OCR is not installed or not found in PATH.")
        print("\nInstallation instructions:")
        print("  Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-ara")
        print("  Fedora: sudo dnf install tesseract tesseract-langpack-ara")
        print("  Arch: sudo pacman -S tesseract tesseract-data-ara")
        sys.exit(1)
    
    if not check_arabic_language():
        print("\nWARNING: Arabic language data may not be installed.")
        print("Installation instructions:")
        print("  Ubuntu/Debian: sudo apt-get install tesseract-ocr-ara")
        print("  Fedora: sudo dnf install tesseract-langpack-ara")
        print("  Arch: sudo pacman -S tesseract-data-ara")
        print("\nContinuing anyway...")
    
    try:
        # Process the PDF
        process_pdf(
            pdf_path=args.pdf_file,
            output_path=args.output,
            lang=args.lang,
            dpi=args.dpi
        )
        print("\n✓ Conversion completed successfully!")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()


