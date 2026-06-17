"""
csv2img - Convert CSV files to PNG images.

This module provides functionality to convert CSV files into high-quality images
by first rendering them to PDF using fpdf2, then rendering each page as an image.

Supports Unicode (CJK, Arabic, Hebrew, Devanagari, etc.) via configurable TTF/OTF 
fonts.
"""

import csv
import os
import logging
from pathlib import Path
from typing import Optional, List, Union

try:
    from fpdf import FPDF
except ImportError:
    raise ImportError("fpdf2 is required. Install it with: pip install fpdf")

try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError("PyMuPDF is required. Install it with: pip install PyMuPDF")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Supported output formats
SUPPORTED_FORMATS = ["png", "jpeg", "jpg"]

# Default font paths — auto-detect from system
_DEFAULT_FONTS = {
    "latin": "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf",
    "cjk": "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "arabic": "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
    "hebrew": "/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf",
    "devanagari": "/usr/share/fonts/opentype/noto/NotoSansDevanagari-Regular.otf",
}


def _detect_unicode(text: str) -> Optional[str]:
    """Detect the dominant non-Latin script in text and return the best font path."""
    has_cjk = any('\u4e00' <= ch <= '\u9fff' or '\u3040' <= ch <= '\u309f' or '\u30a0' <= ch <= '\u30ff' for ch in text)
    has_arabic = any('\u0600' <= ch <= '\u06ff' or '\u0750' <= ch <= '\u077f' for ch in text)
    has_hebrew = any('\u0590' <= ch <= '\u05ff' for ch in text)
    has_devanagari = any('\u0900' <= ch <= '\u097f' for ch in text)
    has_latin_ext = any('\u0080' <= ch <= '\u024f' for ch in text)

    if has_cjk:
        font = _DEFAULT_FONTS["cjk"]
        if os.path.exists(font):
            return font
    if has_arabic:
        font = _DEFAULT_FONTS["arabic"]
        if os.path.exists(font):
            return font
    if has_hebrew:
        font = _DEFAULT_FONTS["hebrew"]
        if os.path.exists(font):
            return font
    if has_devanagari:
        font = _DEFAULT_FONTS["devanagari"]
        if os.path.exists(font):
            return font
    if has_latin_ext:
        font = _DEFAULT_FONTS["latin"]
        if os.path.exists(font):
            return font
    return None


def _build_pdf(
    csv_path: Path,
    pdf_path: Path,
    delimiter: str = ",",
    font_path: Optional[str] = None,
    landscape: bool = True,
) -> None:
    """Render a CSV to PDF using fpdf2 with Unicode support."""
    # Read all data
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=delimiter)
        rows = list(reader)

    if not rows:
        # Empty CSV — create empty PDF
        pdf = FPDF(orientation='L')
        pdf.add_page()
        pdf.output(str(pdf_path))
        return

    max_cols = max(len(r) for r in rows)
    if max_cols == 0:
        max_cols = 1

    # Create PDF in landscape for wide tables
    orientation = 'L' if landscape else 'P'
    pdf = FPDF(orientation=orientation)
    pdf.add_page()  # fpdf2 requires explicit page creation

    # Register font(s) if provided
    if font_path and os.path.exists(font_path):
        # Register both regular and bold variants for fpdf2
        pdf.add_font("csvfont", "", font_path)
        pdf.add_font("csvfont", "B", font_path)

    # Calculate page width and margins
    margin = 10
    page_w = pdf.w - 2 * margin
    col_w = page_w / max_cols
    line_h = pdf.font_size * 2.2

    # Header row (bold)
    if font_path and os.path.exists(font_path):
        pdf.set_font("csvfont", size=10, style="B")
    else:
        pdf.set_font("Courier", size=10, style="B")

    for cell in rows[0]:
        pdf.multi_cell(col_w, line_h, str(cell), align="C", border=1)
    pdf.ln(line_h)

    # Data rows (regular)
    if font_path and os.path.exists(font_path):
        pdf.set_font("csvfont", size=9)
    else:
        pdf.set_font("Courier", size=9)

    for row in rows[1:]:
        padded = row + [''] * (max_cols - len(row))
        for cell in padded:
            pdf.multi_cell(col_w, line_h, str(cell), align="L", border=1)
        pdf.ln(line_h)

    pdf.output(str(pdf_path))


def saveas(
    source: Union[str, Path],
    dpi: int = 300,
    output_dir: Optional[str] = None,
    output_format: str = "png",
    delimiter: str = ",",
    font_path: Optional[str] = None,
) -> List[str]:
    """
    Convert a CSV file to image files.

    This function renders the CSV to PDF using fpdf2 (with Unicode font support),
    then renders each PDF page as an image.

    Args:
        source: Path to the source CSV file (str or Path)
        dpi: Resolution for the output images (default: 300)
        output_dir: Directory to save output images (default: same directory as source)
        output_format: Output format — 'png', 'jpeg', or 'jpg' (default: 'png')
        delimiter: CSV delimiter character (default: ',')
        font_path: Optional path to a TTF/OTF font file. If None, auto-detects
                   from system fonts based on CSV content.

    Returns:
        List of paths to the generated image files

    Raises:
        FileNotFoundError: If the source CSV file doesn't exist
        ValueError: If the source file is not a CSV file or format is unsupported
        ImportError: If required dependencies are not installed

    Example:
        >>> from csv2img import saveas
        >>> output_files = saveas("data.csv")
        >>> print(f"Generated {len(output_files)} images")

        # With custom font for CJK text:
        >>> output_files = saveas("chinese.csv", font_path="/path/to/font.ttf")

        # With semicolon delimiter:
        >>> output_files = saveas("data.tsv", delimiter=";", output_format="jpeg")
    """
    if source is None:
        raise ValueError("Source file path cannot be None")

    source_path = Path(source)

    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path.absolute()}")

    if source_path.suffix.lower() != '.csv':
        raise ValueError(f"Expected a .csv file, got: {source_path.suffix}")

    fmt = output_format.lower().lstrip('.')
    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format '{output_format}'. Supported: {SUPPORTED_FORMATS}")

    fmt_upper = fmt.upper()

    # Determine output directory and base name
    base_name = source_path.stem
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = source_path.parent

    logger.info(f"Converting {source_path.name} to {fmt_upper} images...")

    # Auto-detect font if not provided
    if font_path is None:
        # Read CSV content to detect script
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                csv_content = f.read()
            font_path = _detect_unicode(csv_content)
            if font_path:
                logger.info(f"Auto-detected font: {os.path.basename(font_path)}")
            else:
                logger.info("No special font needed (ASCII-only content)")
        except UnicodeDecodeError:
            logger.warning("Could not detect font (encoding issue), using default")

    # Convert CSV to PDF
    pdf_path = output_path / f"{base_name}.pdf"
    try:
        _build_pdf(source_path, pdf_path, delimiter=delimiter, font_path=font_path)
        logger.info(f"Created PDF: {pdf_path}")
    except Exception as e:
        logger.error(f"Failed to convert CSV to PDF: {e}")
        raise

    # Convert PDF pages to images
    output_files = []
    try:
        doc = fitz.open(str(pdf_path))
        logger.info(f"Processing {len(doc)} page(s)...")

        for page_num, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=dpi)
            ext = fmt if fmt != "jpg" else "jpeg"
            output_file = output_path / f"{base_name}{page_num}.{ext}"
            pix.save(str(output_file))
            output_files.append(str(output_file))
            logger.info(f"Created image: {output_file}")

        doc.close()
        logger.info(f"Successfully generated {len(output_files)} image(s)")

    except Exception as e:
        logger.error(f"Failed to convert PDF to images: {e}")
        raise
    finally:
        # Clean up temporary PDF
        if pdf_path.exists():
            try:
                pdf_path.unlink()
                logger.debug(f"Cleaned up temporary PDF: {pdf_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up temporary PDF: {e}")

    return output_files


def convert_file(
    csv_file: str,
    output_dir: Optional[str] = None,
    dpi: int = 300,
    output_format: str = "png",
    delimiter: str = ",",
    font_path: Optional[str] = None,
) -> List[str]:
    """
    Alias for saveas() function for backwards compatibility.

    Args:
        csv_file: Path to the CSV file
        output_dir: Output directory (optional)
        dpi: Resolution for output images
        output_format: Output format ('png', 'jpeg', 'jpg')
        delimiter: CSV delimiter character
        font_path: Optional font path for Unicode support

    Returns:
        List of generated image file paths
    """
    return saveas(
        csv_file, dpi=dpi, output_dir=output_dir,
        output_format=output_format, delimiter=delimiter, font_path=font_path
    )


def main():
    """Command-line entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: csv2img <csv_file> [output_dir] [dpi]")
        print("       csv2img <csv_file> [output_dir] [dpi] [--format png|jpeg] [--font path.ttf]")
        print("Example: csv2img data.csv ./output 300")
        sys.exit(1)

    csv_file = sys.argv[1]
    output_dir = None
    dpi = 300
    output_format = "png"
    delimiter = ","
    font_path = None

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--format' and i + 1 < len(sys.argv):
            output_format = sys.argv[i + 1]
            i += 2
        elif arg == '--font' and i + 1 < len(sys.argv):
            font_path = sys.argv[i + 1]
            i += 2
        elif arg == '--delimiter' and i + 1 < len(sys.argv):
            delimiter = sys.argv[i + 1]
            i += 2
        elif arg.replace('-', '').isdigit():
            dpi = int(arg)
            i += 1
        else:
            output_dir = arg
            i += 1

    try:
        output_files = saveas(csv_file, dpi=dpi, output_dir=output_dir,
                              output_format=output_format, delimiter=delimiter, font_path=font_path)
        print(f"\u2713 Successfully converted {csv_file} to {len(output_files)} image(s)")
        for f in output_files:
            print(f"  - {f}")
    except Exception as e:
        print(f"\u2717 Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
