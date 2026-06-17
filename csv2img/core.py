"""
csv2img - Convert CSV files to PNG images.

This module provides functionality to convert CSV files into high-quality images
by first converting them to PDF and then rendering each page as an image.
"""

import os
import logging
from pathlib import Path
from typing import Optional, List, Union

try:
    from csv2pdf import convert as csv_to_pdf
except ImportError:
    raise ImportError("csv2pdf is required. Install it with: pip install csv2pdf")

try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError("PyMuPDF is required. Install it with: pip install PyMuPDF")

# Supported output formats mapped to PyMuPDF's valid formats
SUPPORTED_FORMATS = {"png", "jpeg", "jpg", "pnm", "pgm", "ppm", "pbm", "pam", "psd", "ps"}

# Format display extensions
FORMAT_EXT = {
    "png": ".png",
    "jpeg": ".jpg",
    "jpg": ".jpg",
    "pnm": ".pnm",
    "pgm": ".pgm",
    "ppm": ".ppm",
    "pbm": ".pbm",
    "pam": ".pam",
    "psd": ".psd",
    "ps": ".ps",
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def saveas(
    source: Union[str, Path],
    dpi: int = 300,
    output_dir: Optional[str] = None,
    fmt: str = "png",
    delimiter: str = ",",
) -> List[str]:
    """
    Convert a CSV file to image(s).

    This function converts a CSV file to PDF format first, then renders each page
    as a high-quality image.

    Args:
        source: Path to the source CSV file (str or Path)
        dpi: Resolution for the output images (default: 300)
        output_dir: Directory to save output images (default: same directory as source)
        fmt: Output image format. Supported: png, jpeg, jpg, pnm, pgm, ppm, pbm, pam, psd, ps
        delimiter: Column delimiter for the CSV file (default: comma)

    Returns:
        List of paths to the generated image files

    Raises:
        ValueError: If source is None, file is not CSV, or format is unsupported
        FileNotFoundError: If the source CSV file doesn't exist
        IndexError: If the CSV file is empty (no header row)
        ImportError: If required dependencies are not installed

    Example:
        >>> from csv2img import saveas
        >>> output_files = saveas("data.csv")
        >>> print(f"Generated {len(output_files)} images")
    """
    if source is None:
        raise ValueError("Source file path cannot be None")

    source_path = Path(source)

    if not source_path.exists():
        raise FileNotFoundError(f"Source file not found: {source_path.absolute()}")

    if source_path.suffix.lower() != '.csv':
        raise ValueError(f"Expected a .csv file, got: {source_path.suffix}")

    fmt_lower = fmt.lower().strip()
    if fmt_lower not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported format '{fmt}'. Supported: {sorted(SUPPORTED_FORMATS)}"
        )

    ext = FORMAT_EXT.get(fmt_lower, f".{fmt_lower}")

    # Determine output directory and base name
    base_name = source_path.stem
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = source_path.parent

    logger.info(f"Converting {source_path.name} to {fmt_lower.upper()} images...")

    # Convert CSV to PDF
    pdf_path = output_path / f"{base_name}.pdf"
    try:
        csv_to_pdf(
            str(source_path),
            str(pdf_path),
            delimiter=delimiter,
        )
        logger.info(f"Created PDF: {pdf_path}")
    except IndexError:
        raise ValueError("CSV file is empty or contains no header row")
    except Exception as e:
        logger.error(f"Failed to convert CSV to PDF: {e}")
        raise

    # Convert PDF pages to images
    output_files = []
    try:
        doc = fitz.open(str(pdf_path))
        if len(doc) == 0:
            logger.warning("PDF has no pages — CSV file may be empty")
            return output_files

        logger.info(f"Processing {len(doc)} page(s)...")

        for page_num, page in enumerate(doc, start=1):
            pix = page.get_pixmap(dpi=dpi)
            output_file = output_path / f"{base_name}{page_num}{ext}"
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
    csv_file: Union[str, Path],
    output_dir: Optional[str] = None,
    dpi: int = 300,
    fmt: str = "png",
    delimiter: str = ",",
) -> List[str]:
    """
    Alias for saveas() function for backwards compatibility.

    Args:
        csv_file: Path to the CSV file
        output_dir: Output directory (optional)
        dpi: Resolution for output images
        fmt: Output image format
        delimiter: CSV delimiter

    Returns:
        List of generated image file paths
    """
    return saveas(csv_file, dpi=dpi, output_dir=output_dir, fmt=fmt, delimiter=delimiter)


def main():
    """Command-line entry point."""
    import sys

    if len(sys.argv) < 2 or sys.argv[1] in ('--help', '-h'):
        print("Usage: csv2img <csv_file> [output_dir] [dpi] [format] [delimiter]")
        print("Example:")
        print("  csv2img data.csv")
        print("  csv2img data.csv ./output 300 png ,")
        print("")
        print("Supported formats: png, jpeg, jpg, pnm, pgm, ppm, pbm, pam, psd, ps")
        print("Delimiter: , (comma), \\t (tab), ; (semicolon)")
        sys.exit(0)

    csv_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    fmt = sys.argv[4] if len(sys.argv) > 4 else "png"
    delimiter = sys.argv[5] if len(sys.argv) > 5 else ","

    try:
        output_files = saveas(csv_file, dpi=dpi, output_dir=output_dir, fmt=fmt, delimiter=delimiter)
        print(f"✓ Successfully converted {csv_file} to {fmt.upper()} images")
        for f in output_files:
            print(f"  - {f}")
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
