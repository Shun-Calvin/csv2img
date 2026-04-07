# csv2img

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Convert CSV files to high-quality PNG images with a single function call.

## Features

- **Simple API**: Convert CSV to PNG with one line of code
- **High Quality**: Configurable DPI (default 300) for crisp output
- **Multi-page Support**: Automatically handles CSV files that span multiple pages
- **Flexible Output**: Specify custom output directory
- **CLI Support**: Use from command line or as a Python library

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

#### Basic Usage

```python
from csv2img import saveas

# Convert a CSV file to PNG images
output_files = saveas("data.csv")
print(f"Generated {len(output_files)} images: {output_files}")
```

#### Advanced Usage

```python
from csv2img import saveas

# Convert with custom DPI and output directory
output_files = saveas(
    source="data.csv",
    dpi=600,  # Higher resolution
    output_dir="./output_images"  # Custom output directory
)
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
```

## API Reference

### `saveas(source, dpi=300, output_dir=None)`

Convert a CSV file to PNG images.

**Parameters:**
- `source` (str): Path to the source CSV file (required)
- `dpi` (int): Resolution for output images in dots per inch (default: 300)
- `output_dir` (str, optional): Directory to save output images (default: same as source file)

**Returns:**
- `List[str]`: List of paths to the generated PNG files

**Raises:**
- `FileNotFoundError`: If the source CSV file doesn't exist
- `ValueError`: If the source file is not a CSV file or source is None
- `ImportError`: If required dependencies are not installed

**Example:**
```python
from csv2img import saveas

try:
    files = saveas("report.csv", dpi=300)
    print(f"Success! Generated {len(files)} images")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except Exception as e:
    print(f"Error: {e}")
```

## How It Works

1. The CSV file is first converted to PDF format using `csv2pdf`
2. Each PDF page is rendered as a high-quality PNG image using `PyMuPDF` (fitz)
3. The temporary PDF file is automatically cleaned up
4. Output files are named as `{original_name}{page_number}.png`

**Example:**
- Input: `data.csv`
- Output: `data1.png`, `data2.png`, `data3.png` (if the CSV spans 3 pages)

## Requirements

- Python 3.7+
- csv2pdf
- PyMuPDF (fitz)

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

### Memory Issues

For very large CSV files:
- Reduce the DPI setting (e.g., use 150 instead of 300)
- Ensure sufficient disk space for temporary PDF and output images

## Development

### Running Tests

```bash
python -m pytest tests/
```

### Building the Package

```bash
python setup.py sdist bdist_wheel
```

### Installing in Development Mode

```bash
pip install -e .
```

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

- **Calvin_Shun** - [GitHub](https://github.com/Shun-Calvin)

## Acknowledgments

- [csv2pdf](https://pypi.org/project/csv2pdf/) - CSV to PDF conversion
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF rendering and manipulation
