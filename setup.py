"""
Setup script for csv2img package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read the contents of requirements.txt
requirements = (this_directory / "requirements.txt").read_text(encoding="utf-8").splitlines()
requirements = [r.strip() for r in requirements if r.strip() and not r.startswith("#")]

setup(
    name="csv2img",
    version="0.3.0",
    author="Calvin_Shun",
    author_email="calvin.shun@example.com",
    description="Convert CSV files to PNG images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shun-Calvin/csv2img",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "csv2img=csv2img.core:main",
        ],
    },
    keywords="csv image conversion png pdf visualization",
    project_urls={
        "Bug Reports": "https://github.com/Shun-Calvin/csv2img/issues",
        "Source": "https://github.com/Shun-Calvin/csv2img",
    },
)
