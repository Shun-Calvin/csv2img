"""
csv2img - Convert CSV files to PNG/JPEG images.

Supports Unicode (CJK, Arabic, Hebrew, Devanagari, etc.) via configurable TTF/OTF fonts
with cross-platform font detection (Windows, macOS, Linux).
"""

from .core import (
    saveas,
    convert_file,
    main,
    SUPPORTED_FORMATS,
    _detect_unicode,
    _find_fallback_font,
)

__version__ = "0.5.0"
__author__ = "Calvin_Shun"
__all__ = [
    "saveas",
    "convert_file",
    "main",
    "SUPPORTED_FORMATS",
    "_detect_unicode",
    "_find_fallback_font",
]
