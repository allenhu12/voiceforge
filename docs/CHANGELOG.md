# Changelog

All notable changes to VoiceForge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for Phase 2 (v1.1.0)
- Batch processing for multiple files
- OpenAI TTS provider integration
- Google Cloud TTS provider integration
- Voice preview functionality
- Enhanced configuration management
- Performance optimizations

### Planned for Phase 3 (v2.0.0)
- GUI application with modern interface
- Drag-and-drop file support
- Real-time cost estimation in GUI
- Voice playback and preview
- Advanced audio settings
- SSML support

## [1.0.0] - 2025-01-26

### Added - Phase 1: Foundation & Core CLI ✅

#### Core Architecture
- **Modular Architecture**: Extensible design with clear separation of concerns
- **Abstract Factory Pattern**: TTSServiceInterface for consistent provider behavior
- **Factory Pattern**: TTSServiceFactory for provider instantiation
- **Strategy Pattern**: Pluggable TTS providers
- **Command Pattern**: CLI commands with Click framework

#### TTS Integration
- **Fish Audio TTS Client**: Complete implementation with msgpack serialization
- **Bearer Token Authentication**: Secure API authentication
- **Cost Estimation**: Character-based cost calculation (~$0.015/1000 chars)
- **Voice Management**: Support for speech-1.6 and speech-1.4 models
- **Error Handling**: Comprehensive HTTP and API error management

#### Configuration Management
- **Secure API Key Storage**: Fernet encryption for sensitive data
- **Cross-Platform Support**: Windows, macOS, and Linux compatibility
- **Configuration Directories**: Platform-specific config locations
- **JSON-based Settings**: Structured configuration with validation
- **Dot Notation Access**: Easy nested configuration access

#### File Processing
- **Input Handler**: Text file reading with encoding detection (UTF-8, chardet)
- **File Validation**: Size limits, format checking, and error handling
- **Text Processing**: Cleaning and preparation for TTS
- **Character Counting**: Accurate statistics for cost estimation
- **Output Handler**: MP3 file management with proper naming conventions

#### CLI Interface
- **Click Framework**: Professional command-line interface
- **Hierarchical Commands**: `convert`, `config`, `list-voices`
- **Rich Options**: Input validation, default values, help text
- **Progress Indicators**: Status messages and user feedback
- **Interactive Prompts**: Confirmation dialogs for operations
- **Verbose Logging**: Detailed debugging information

#### Error Handling & Logging
- **Custom Exception Hierarchy**: VoiceForgeError, AuthenticationError, NetworkError, FileError
- **Comprehensive Logging**: Console and file output with configurable levels
- **API Request Logging**: Detailed logging without sensitive data
- **User-Friendly Messages**: Clear error descriptions and solutions

#### Documentation
- **Getting Started Guide**: Complete tutorial (598 lines)
- **Quick Reference**: Command reference card (260 lines)
- **Phase 1 Summary**: Development overview (510 lines)
- **Git Workflow Guide**: Version control guidelines
- **Demo Script**: Interactive demonstration without API key
- **Code Documentation**: Comprehensive docstrings and comments

#### Development Tools
- **Package Configuration**: Complete setup.py with dependencies
- **Requirements Management**: requirements.txt with core dependencies
- **Git Integration**: Repository setup with comprehensive .gitignore
- **Cross-Platform Testing**: Validated on macOS (additional platforms pending)

### Technical Specifications
- **Python Version**: 3.8+ (recommended 3.10+)
- **Dependencies**: 7 core packages (click, httpx, ormsgpack, pydantic, etc.)
- **Code Quality**: ~3,000 lines across 20+ files
- **Architecture**: Modular design with interfaces, services, core, CLI, utils
- **Security**: Encrypted API key storage, no plain text secrets
- **Performance**: Efficient file processing and API communication

### Testing & Validation
- **CLI Testing**: All commands functional and validated
- **Cost Estimation**: Accurate character-based calculations
- **File Processing**: Text reading, validation, and statistics
- **Configuration**: Secure storage and retrieval of settings
- **Error Handling**: Comprehensive exception management
- **Demo Script**: Interactive testing without API requirements

### Files Added
```
26 files changed, 4908 insertions(+)
├── .gitignore                                    # Git ignore rules
├── README.md                                     # Project overview
├── CHANGELOG.md                                  # Version history
├── demo.py                                       # Demo script
├── requirements.txt                              # Dependencies
├── setup.py                                     # Package config
├── docs/
│   ├── README.md                                # Documentation index
│   ├── getting-started-guide.md                # Complete tutorial
│   ├── quick-reference.md                       # Command reference
│   ├── phase1-summary.md                        # Development overview
│   └── git-workflow.md                          # Git guidelines
└── src/voiceforge/
    ├── __init__.py                              # Package init
    ├── cli/
    │   ├── __init__.py
    │   └── main.py                              # CLI interface
    ├── core/
    │   ├── __init__.py
    │   ├── config_manager.py                    # Configuration
    │   ├── input_handler.py                     # File input
    │   └── output_handler.py                    # File output
    ├── interfaces/
    │   ├── __init__.py
    │   └── tts_service_interface.py             # TTS contract
    ├── services/
    │   ├── __init__.py
    │   ├── fish_tts_client.py                   # Fish Audio client
    │   └── service_factory.py                   # Provider factory
    ├── utils/
    │   ├── __init__.py
    │   ├── exceptions.py                        # Custom exceptions
    │   └── logger.py                            # Logging utilities
    └── gui/
        └── __init__.py                          # GUI placeholder
```

### Installation & Usage
```bash
# Installation
pip install -e .

# Configuration
voiceforge config set-api-key fish_audio YOUR_API_KEY

# Basic usage
voiceforge convert --input text.txt

# Cost estimation
voiceforge convert --input text.txt --estimate-only

# Voice selection
voiceforge list-voices
voiceforge convert --input text.txt --voice speech-1.4
```

### Commit Information
- **Initial Commit**: `d366771`
- **Commit Message**: "Initial commit: VoiceForge Phase 1 - Foundation & Core CLI complete with modular architecture, Fish Audio integration, secure config, CLI interface, and comprehensive documentation"
- **Date**: January 26, 2025
- **Files**: 26 files
- **Lines**: ~4,900 lines of code

---

## Development Phases

### ✅ Phase 1: Foundation & Core CLI (v1.0.0)
**Status**: Completed  
**Duration**: 1 day  
**Focus**: Architecture, CLI, Fish Audio integration, documentation

### 🔄 Phase 2: CLI Enhancements (v1.1.0)
**Status**: Planned  
**Duration**: 2-3 weeks  
**Focus**: Batch processing, additional providers, enhanced features

### 📋 Phase 3: GUI Implementation (v2.0.0)
**Status**: Planned  
**Duration**: 1-2 months  
**Focus**: Desktop application, modern UI, advanced features

### 📦 Phase 4: Packaging & Distribution (v2.1.0)
**Status**: Planned  
**Duration**: 2-3 weeks  
**Focus**: Installers, releases, update mechanism

---

## Contributing

Please read our [Git Workflow Guide](docs/git-workflow.md) for details on our development process, commit guidelines, and how to submit pull requests.

## Support

- **Documentation**: Check the `docs/` directory
- **Issues**: Report bugs and request features via GitHub issues
- **Discussions**: Community support via GitHub discussions
- **Demo**: Run `python demo.py` for interactive demonstration 