# csv2img

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/Shun-Calvin/csv2img/actions/workflows/test.yml/badge.svg)](https://github.com/Shun-Calvin/csv2img/actions)

Convert CSV files to high-quality PNG/JPEG images with full Unicode support (CJK, Arabic, Hebrew, Devanagari, etc.).

## Features

- **Simple API**: Convert CSV to PNG/JPEG with one line of code
- **High Quality**: Configurable DPI (default 300) for crisp output
- **Full Unicode**: Auto-detects scripts and uses appropriate fonts — CJK, Arabic, Hebrew, Devanagari, Latin Extended
- **Multi-page Support**: Automatically handles CSV files that span multiple pages
- **Flexible Formats**: Output as PNG or JPEG
- **Custom Delimiters**: Supports TSV, semicolon-separated, or any delimiter
- **CLI Support**: Use from command line or as a Python library
- **Zero csv2pdf dependency**: Pure fpdf2 + PyMuPDF

## Installation

### From PyPI (recommended)

```bash
pip install csv2img
```

### From Source

```bash
git clone https://github.com/Shun-Calvin/csv2img.git
cd csv2img
pip install -e .
```

## Usage

### Python Library

#### Basic Usage

```python
from csv2img import saveas

# Convert a CSV file to PNG images
output_files = saveas("data.csv")
print(f"Generated {len(output_files)} images: {output_files}")
```

#### Unicode (CJK) — Auto-Detected

```python
from csv2img import saveas

# Chinese/Japanese/Korean text is auto-detected and rendered with Noto Sans CJK
output_files = saveas("chinese_data.csv")
# Output: chinese_data1.png (with proper CJK characters)
```

#### Custom Format & DPI

```python
from csv2img import saveas

# Convert to JPEG at 600 DPI
output_files = saveas("report.csv", dpi=600, output_format="jpeg")
```

#### Custom Delimiter (TSV, semicolon, etc.)

```python
from csv2img import saveas

# Tab-separated values
output_files = saveas("data.tsv", delimiter="\t")

# Semicolon-separated (common in European locales)
output_files = saveas("data.csv", delimiter=";")
```

#### Custom Font

```python
from csv2img import saveas

# Use your own TTF/OTF font file
output_files = saveas("data.csv", font_path="/path/to/your/font.ttf")
```

#### Using the Alternative Function Name

```python
from csv2img import convert_file

output_files = convert_file("data.csv", output_dir="./images", dpi=300)
```

### Command Line Interface

After installation, you can use the `csv2img` command:

```bash
# Basic usage
csv2img data.csv

# Specify output directory
csv2img data.csv ./output

# Specify output directory and DPI
csv2img data.csv ./output 600

# Specify output format
csv2img data.csv ./output 300 --format jpeg

# Specify delimiter (TSV)
csv2img data.csv ./output 300 --delimiter $'\t'

# Custom font
csv2img data.csv ./output 300 --font /path/to/font.ttf
```

## API Reference

### `saveas(source, dpi=300, output_dir=None, output_format="png", delimiter=",", font_path=None)`

Convert a CSV file to image files.

**Parameters:**
- `source` (str | Path): Path to the source CSV file (required)
- `dpi` (int): Resolution for output images (default: 300)
- `output_dir` (str, optional): Directory to save output images (default: same as source)
- `output_format` (str): Output format — `'png'` or `'jpeg'` (default: `'png'`)
- `delimiter` (str): CSV delimiter character (default: `','`)
- `font_path` (str, optional): Path to a TTF/OTF font file. If `None`, auto-detects from system fonts based on CSV content.

**Returns:**
- `List[str]`: List of paths to the generated image files

**Raises:**
- `FileNotFoundError`: If the source CSV file doesn't exist
- `ValueError`: If the source file is not a CSV file or format is unsupported
- `ImportError`: If required dependencies are not installed

### `SUPPORTED_FORMATS`

A list of supported output formats: `["png", "jpeg", "jpg"]`

## Unicode Font Support

csv2img auto-detects the dominant script in your CSV and uses the appropriate font:

| Script | Unicode Range | Font Used |
|--------|--------------|-----------|
| CJK (Chinese/Japanese/Korean) | `\u4e00-\u9fff`, `\u3040-\u30ff` | Noto Sans CJK |
| Arabic | `\u0600-\u06ff` | Noto Sans Arabic |
| Hebrew | `\u0590-\u05ff` | Noto Sans Hebrew |
| Devanagari (Hindi, etc.) | `\u0900-\u097f` | Noto Sans Devanagari |
| Latin Extended | `\u0080-\u024f` | Noto Sans Mono |

You can override auto-detection by passing `font_path` explicitly.

## How It Works

1. The CSV file is parsed using Python's built-in `csv` module (supports any delimiter)
2. fpdf2 renders the table to a PDF with Unicode-aware TTF fonts
3. PyMuPDF (fitz) renders each PDF page as a high-quality image
4. The temporary PDF file is automatically cleaned up

**Example:**
- Input: `data.csv`
- Output: `data1.png`, `data2.png`, `data3.png` (if the CSV spans 3 pages)

## Requirements

- Python 3.7+
- fpdf2 (PDF rendering with Unicode font support)
- PyMuPDF (PDF to image rendering)

## Troubleshooting

### Font Missing for Specific Script

If your CSV contains characters not covered by the auto-detected font, pass a custom font:

```python
from csv2img import saveas

# Use a font that covers your specific characters
output_files = saveas("data.csv", font_path="/path/to/font.ttf")
```

### Permission Errors

Ensure you have write permissions in the output directory. If specifying a custom output directory, it will be created automatically if it doesn't exist.

### Memory Issues

For very large CSV files:
- Reduce the DPI setting (e.g., use 150 instead of 300)
- Ensure sufficient disk space for temporary PDF and output images

## Testing

```bash
pip install pytest
python -m pytest tests/ -v
```

## Changelog

### Version 0.4.0 (2026-06-17)
- ✨ **Removed csv2pdf dependency** — pure fpdf2 + PyMuPDF implementation
- ✨ **Full Unicode support** — auto-detects CJK, Arabic, Hebrew, Devanagari, Latin Extended
- ✨ **JPEG output format** — PNG and JPEG both supported
- ✨ **Custom delimiter** — TSV, semicolon, or any separator
- ✨ **Custom font path** — pass your own TTF/OTF font file
- ✨ **Path object support** — `source` accepts `str` or `Path`
- ✨ **Empty CSV handling** — returns `[]` instead of crashing
- ✨ **Output validation** — verifies generated files exist and are non-empty
- 🐛 **Fixed PDF cleanup** — removes temp PDF after return, not in finally
- 📦 **Updated dependencies** — `csv2pdf>=1.0.0` → `fpdf2>=2.5.0`

### Version 0.3.0 (2026-04-07)
- Added JPEG and PNG format support
- Added delimiter parameter
- Improved error handling and output validation

### Version 0.2.0 (2026-04-07)
- ✨ Added comprehensive error handling and input validation
- ✨ Added type hints and docstrings
- ✨ Added logging support
- ✨ Added command-line interface
- ✨ Added `setup.py` for proper package installation
- ✨ Added `requirements.txt`
- ✨ Improved documentation with examples
- 🐛 Fixed temporary PDF cleanup
- 📦 Added proper package structure

### Version 0.1.0 (2022)
- Initial release
- Basic CSV to PNG conversion functionality

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
