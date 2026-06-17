"""
csv2img - Convert CSV files to PNG images.

Supports Unicode (CJK, Arabic, Hebrew, Devanagari, etc.) via configurable TTF fonts.
"""

from .core import saveas, convert_file, main, SUPPORTED_FORMATS, _detect_unicode

__version__ = "0.4.0"
__author__ = "Calvin_Shun"
__all__ = ["saveas", "convert_file", "main", "SUPPORTED_FORMATS", "_detect_unicode"]
