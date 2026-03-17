#!/usr/bin/env python3
"""
KOKAO Engine v3.0.4 — Setup Script

Biologically Plausible Cognitive Architecture based on 
Kosyakov's Theory of Functionally-Independent Structures.

Authors:
    Vital Kalinouski / Виталий Калиновский
    V. Ovseychik / В. Овсейчик

Organization: newmathphys
Email: newmathphys@gmail.com

Based on ideas from Yu.B. Kosyakov's book "My Brain" (1999).
Основано на идеях из книги Ю.Б. Косякова "Мой мозг" (1999).

Note: The mathematical method is in the public domain 
      (Russian Patent №2109332 expired).
"""

from setuptools import setup, find_packages
from pathlib import Path
import re

# Чтение README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Чтение версии из __init__.py
def get_version():
    init_file = this_directory / "kokao" / "__init__.py"
    with open(init_file, "r", encoding="utf-8") as f:
        content = f.read()
        match = re.search(r'__version__ = "([^"]+)"', content)
        if match:
            return match.group(1)
    return "3.0.4"

# Чтение requirements
requirements = []
req_file = this_directory / "requirements.txt"
if req_file.exists():
    with open(req_file, "r", encoding="utf-8") as f:
        requirements = [
            line.strip() for line in f 
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="kokao-engine",
    version=get_version(),
    author="Vital Kalinouski, V. Ovseychik",
    author_email="newmathphys@gmail.com",
    description="Biologically Plausible Cognitive Architecture achieving 92.92% accuracy on UCR datasets. Based on Kosyakov's Theory (1999).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/newmathphys/kokao-engine",
    project_urls={
        "Bug Tracker": "https://github.com/newmathphys/kokao-engine/issues",
        "Documentation": "https://kokao-engine.readthedocs.io/",
        "Source": "https://github.com/newmathphys/kokao-engine",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Natural Language :: Russian",
    ],
    keywords=[
        "machine-learning",
        "bio-inspired",
        "neural-networks",
        "ucr",
        "time-series",
        "kosyakov",
        "cognitive-architecture",
        "functionally-independent-structures",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "mypy>=0.950",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "benchmarks": [
            "pandas>=1.3.0",
            "scikit-learn>=1.0.0",
        ],
    },
    include_package_data=True,
    package_data={
        "kokao": ["py.typed"],
    },
    entry_points={
        "console_scripts": [
            "kokao=kokao.main:main",
        ],
    },
    license="MIT",
    license_files=["LICENSE"],
)
