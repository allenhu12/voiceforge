"""
VoiceForge Setup Configuration

Setup script for installing VoiceForge - Text-to-Speech File Converter.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
else:
    requirements = [
        "click>=8.0.0",
        "httpx>=0.24.0", 
        "ormsgpack>=1.2.0",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "cryptography>=3.4.0",
        "chardet>=5.0.0"
    ]

setup(
    name="voiceforge",
    version="1.0.0",
    description="Convert text files to MP3 audio using advanced TTS services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="VoiceForge Team",
    author_email="contact@voiceforge.dev",
    url="https://github.com/voiceforge/voiceforge",
    project_urls={
        "Bug Reports": "https://github.com/voiceforge/voiceforge/issues",
        "Source": "https://github.com/voiceforge/voiceforge",
        "Documentation": "https://github.com/voiceforge/voiceforge/wiki",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "voiceforge=voiceforge.cli.main:main",
        ],
    },
    install_requires=requirements,
    extras_require={
        "gui": [
            "customtkinter>=5.0.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pytest-cov>=4.0.0",
        ],
        "all": [
            "customtkinter>=5.0.0",
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    keywords="tts text-to-speech audio mp3 fish-audio voice synthesis",
    python_requires=">=3.8",
    include_package_data=True,
    zip_safe=False,
    platforms=["any"],
) 