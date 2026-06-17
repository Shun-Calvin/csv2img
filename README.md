# csv2img

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://img.shields.io/pypi/v/csv2img.svg)](https://pypi.org/project/csv2img/)
[![Tests](https://github.com/Shun-Calvin/csv2img/actions/workflows/test.yml/badge.svg)](https://github.com/Shun-Calvin/csv2img/actions)

Convert CSV files to high-quality PNG/JPEG images with a single function call.

## Features

- **Simple API**: Convert CSV to image with one line of code
- **High Quality**: Configurable DPI (default 300) for crisp output
- **Multi-format**: Supports PNG (default) and JPEG output
- **Multi-page Support**: Automatically handles CSV files that span multiple pages
- **Flexible Output**: Specify custom output directory and format
- **Custom Delimiters**: Support for comma, tab, or semicolon-separated CSVs
- **CLI Support**: Use from command line or as a Python library
- **Path Support**: Accept both `str` and `Path` objects

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

### Manual Installation

Install the required dependencies:

```bash
pip install csv2pdf PyMuPDF
```

## Usage

### Python Library

#### Basic Usage (PNG)

```python
from csv2img import saveas

# Convert a CSV file to PNG images
output_files = saveas("data.csv")
print(f"Generated {len(output_files)} images: {output_files}")
```

#### Custom DPI and Output Directory

```python
from csv2img import saveas

# Convert with custom DPI and output directory
output_files = saveas(
    source="data.csv",
    dpi=600,  # Higher resolution
    output_dir="./output_images"  # Custom output directory
)
```

#### JPEG Output

```python
from csv2img import saveas

# Convert to JPEG (default quality: 95)
output_files = saveas("data.csv", fmt="jpeg")
# Specify custom quality (1-100)
output_files = saveas("data.csv", fmt="jpeg", jpeg_quality=85)
```

#### Custom Delimiter (TSV, Semicolon)

```python
from csv2img import saveas

# Tab-separated values
output_files = saveas("data.tsv", delimiter="\t")

# Semicolon-separated (common in European locales)
output_files = saveas("data.csv", delimiter=";")
```

#### Using Path Objects

```python
from pathlib import Path
from csv2img import saveas

# Accepts both str and Path
output_files = saveas(Path("data.csv"))
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

# Specify format (PNG or JPEG)
csv2img data.csv ./output 300 jpeg

# Specify delimiter (comma, tab, semicolon)
csv2img data.csv ./output 300 png --delimiter "\t"

# Show help
csv2img --help
```

## API Reference

### `saveas(source, dpi=300, output_dir=None, fmt="png", jpeg_quality=95, delimiter=",")`

Convert a CSV file to image images.

**Parameters:**

- `source` (str | Path): Path to the source CSV file (required)
- `dpi` (int): Resolution for output images (default: 300). Range: 1–1200
- `output_dir` (str | Path | None): Directory to save output images (default: same directory as source)
- `fmt` (str): Output format — `"png"` (default) or `"jpeg"`. Case-insensitive.
- `jpeg_quality` (int): JPEG quality, 1–100 (default: 95). Only applies when `fmt="jpeg"`.
- `delimiter` (str): CSV delimiter character (default: `","`). Common values: `","`, `"\t"`, `";"`

**Returns:**

- `List[str]`: List of paths to the generated image files

**Raises:**

- `ValueError`: If source is None, file is not .csv, unsupported format, or invalid DPI/quality
- `FileNotFoundError`: If the source CSV file doesn't exist
- `RuntimeError`: If output file generation fails or produces empty files

**Example:**

```python
from csv2img import saveas

try:
    files = saveas("report.csv", dpi=300, fmt="jpeg", jpeg_quality=85)
    print(f"Success! Generated {len(files)} images")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Invalid input: {e}")
except RuntimeError as e:
    print(f"Conversion failed: {e}")
```

## Supported Formats

| Format | Extension | Supported |
|--------|-----------|-----------|
| PNG | `.png` | ✅ Yes (default) |
| JPEG | `.jpg`, `.jpeg` | ✅ Yes |
| TIFF | `.tif` | ❌ Not supported by PyMuPDF |
| WebP | `.webp` | ❌ Not supported by PyMuPDF |

## How It Works

1. The CSV file is converted to PDF format using `csv2pdf`
2. Each PDF page is rendered as a high-quality image using `PyMuPDF` (fitz)
3. The temporary PDF file is automatically cleaned up
4. Output files are named as `{original_name}{page_number}.{ext}`

**Example:**

- Input: `data.csv`
- Output (PNG): `data1.png`, `data2.png`, `data3.png` (if the CSV spans 3 pages)
- Output (JPEG): `data1.jpeg`, `data2.jpeg`

## Requirements

- Python 3.7+
- csv2pdf >= 0.1.0
- PyMuPDF >= 1.19.0

## Limitations

### Unicode / Non-Latin Characters

The underlying `csv2pdf` library uses the Courier font which only supports **Latin-1** characters. CSV files with Chinese, Japanese, Korean, Arabic, emoji, or other non-Latin characters will fail.

**Workarounds:**

1. Use a CSV editor to convert text to Latin-1 compatible characters
2. Pre-process your data with a tool like `iconv` to transliterate characters
3. Consider using a different library that supports Unicode fonts (future improvement)

### Empty CSV Files

An entirely empty CSV file (zero bytes) will return an empty list — no images are generated. A CSV with only a header row will generate one blank-page image.

### Large Files

For very large CSV files:
- Reduce the DPI setting (e.g., use 150 instead of 300)
- Ensure sufficient disk space for temporary PDF and output images
- Consider splitting the CSV into smaller chunks

## Troubleshooting

### Import Errors

If you encounter import errors with `fitz` or `PyMuPDF`:

```bash
pip uninstall fitz PyMuPDF
pip install PyMuPDF
```

**Note:** Install `PyMuPDF` only (not `fitz` separately). The `fitz` module is included in PyMuPDF.

### Permission Errors

Ensure you have write permissions in the output directory. If specifying a custom output directory, it will be created automatically if it doesn't exist.

### Deprecation Warning from csv2pdf

You may see a deprecation warning from `csv2pdf` about the `ln` parameter. This is a known issue in the upstream library and does not affect functionality. It will be resolved when `csv2pdf` updates to the latest `fpdf2` API.

## Development

### Running Tests

```bash
python -m pytest tests/ -v
```

### Building the Package

```bash
python setup.py sdist bdist_wheel
```

### Installing in Development Mode

```bash
pip install -e .
```

### Adding a New Format

To add support for a new image format:

1. Check if PyMuPDF supports it (see `Pixmap.save()` valid_formats)
2. Add the extension to `SUPPORTED_FORMATS` in `csv2img/core.py`
3. Add the corresponding test in `tests/test_csv2img.py`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Changelog

### Version 0.3.0 (2026-06-17)

- ✨ Added JPEG output format support
- ✨ Added custom delimiter support (tab, semicolon)
- ✨ Added `fmt` and `jpeg_quality` parameters to `saveas()`
- ✨ Added `delimiter` parameter to `saveas()` and CLI
- ✨ Added support for `Path` objects as input
- ✨ Added empty CSV handling (returns empty list)
- ✨ Added output file validation (checks for empty files)
- ✨ Added `--help` flag to CLI
- ✨ Added comprehensive test suite (38 tests)
- ✨ Added GitHub Actions CI
- ✨ Added `pyproject.toml` for modern packaging
- 🐛 Fixed PDF cleanup — moved to finally block to prevent leaks
- 🐛 Fixed requirements.txt version constraint (csv2pdf>=0.1.0,<1.0.0)
- 🐛 Fixed module shadowing bug (csv2img.py → csv2img/core.py)
- 📝 Updated README with full API docs, format support table, limitations, and troubleshooting

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

## Author

- **Calvin_Shun** — [GitHub](https://github.com/Shun-Calvin)

## Acknowledgments

- [csv2pdf](https://pypi.org/project/csv2pdf/) — CSV to PDF conversion
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF rendering and manipulation
