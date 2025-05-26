# VoiceForge Documentation

**Welcome to VoiceForge!** 🎵  
A powerful, modular text-to-speech application that converts text files to high-quality MP3 audio.

---

## 📚 Documentation Index

### 🚀 Getting Started
- **[Getting Started Guide](getting-started-guide.md)** - Complete tutorial for understanding Phase 1 development and using VoiceForge
- **[Quick Reference](quick-reference.md)** - Command reference card and common usage patterns
- **[Demo Script](../demo.py)** - Interactive demonstration of VoiceForge features

### 📖 User Guides
- **[Installation Guide](getting-started-guide.md#installation-guide)** - Step-by-step installation instructions
- **[Basic Usage Tutorial](getting-started-guide.md#basic-usage-tutorial)** - Your first text-to-speech conversion
- **[Advanced Features](getting-started-guide.md#advanced-features)** - Custom voices, output settings, and more
- **[Troubleshooting](getting-started-guide.md#troubleshooting)** - Common issues and solutions

### 🛠️ Developer Resources
- **[Phase 1 Summary](phase1-summary.md)** - Comprehensive development overview and architecture explanation
- **[Development Setup](getting-started-guide.md#development-setup)** - Setting up development environment
- **[Code Structure](getting-started-guide.md#understanding-the-code-structure)** - Understanding the codebase
- **[Adding TTS Providers](getting-started-guide.md#adding-a-new-tts-provider)** - Extending VoiceForge

### 📊 Project Information
- **[Project README](../README.md)** - Main project overview and features
- **[Development Progress](../progress.md)** - Current status and roadmap
- **[Development Plan](../TTS_tool/VoiceForge_Development_Plan_v1.0.md)** - Detailed development strategy

---

## 🎯 Quick Navigation

### For New Users
1. **Start Here**: [Getting Started Guide](getting-started-guide.md)
2. **Try the Demo**: Run `python demo.py` in the project root
3. **Quick Commands**: Check the [Quick Reference](quick-reference.md)

### For Developers
1. **Understand the Architecture**: [Phase 1 Summary](phase1-summary.md)
2. **Set Up Development**: [Development Setup](getting-started-guide.md#development-setup)
3. **Explore the Code**: [Code Structure](getting-started-guide.md#understanding-the-code-structure)

### For Project Managers
1. **Project Status**: [Development Progress](../progress.md)
2. **Technical Overview**: [Phase 1 Summary](phase1-summary.md)
3. **Future Plans**: [Development Plan](../TTS_tool/VoiceForge_Development_Plan_v1.0.md)

---

## 📋 Document Descriptions

### 📖 [Getting Started Guide](getting-started-guide.md)
**Length**: ~400 lines  
**Audience**: Users and Developers  
**Content**: Complete tutorial covering Phase 1 development understanding, installation, usage, advanced features, development setup, and troubleshooting.

### ⚡ [Quick Reference](quick-reference.md)
**Length**: ~200 lines  
**Audience**: All Users  
**Content**: Command reference card with common usage patterns, configuration locations, troubleshooting tips, and supported features.

### 🏗️ [Phase 1 Summary](phase1-summary.md)
**Length**: ~500 lines  
**Audience**: Developers and Technical Users  
**Content**: Comprehensive development overview, step-by-step architecture explanation, design decisions, data flow, and testing results.

### 🎬 [Demo Script](../demo.py)
**Length**: ~150 lines  
**Audience**: All Users  
**Content**: Interactive Python script that demonstrates VoiceForge functionality without requiring an API key.

---

## 🔧 Key Features Documented

### ✅ Core Functionality
- **Text-to-Speech Conversion**: Convert `.txt` files to `.mp3` audio
- **Multiple TTS Providers**: Fish Audio (with OpenAI and Google coming soon)
- **Cost Estimation**: Upfront cost calculation before conversion
- **Voice Selection**: Choose from available voices and models
- **Audio Quality**: Configurable MP3 bitrates (64-320 kbps)

### ✅ Configuration & Security
- **Secure API Key Storage**: Encrypted with Fernet cryptography
- **Cross-Platform Config**: Windows, macOS, and Linux support
- **Provider Management**: Easy switching between TTS services
- **Settings Validation**: Robust configuration validation

### ✅ User Experience
- **CLI Interface**: Professional command-line tool with Click framework
- **Rich Feedback**: Progress indicators, status messages, error handling
- **Help System**: Comprehensive help and documentation
- **Verbose Logging**: Detailed logging for debugging

### ✅ Developer Experience
- **Modular Architecture**: Clean separation of concerns
- **Extensible Design**: Easy to add new TTS providers
- **Design Patterns**: Factory, Strategy, Command, and Singleton patterns
- **Comprehensive Documentation**: Code comments and user guides

---

## 🚀 Getting Started in 3 Steps

### 1. Install VoiceForge
```bash
cd /path/to/VoiceForge
pip install -e .
```

### 2. Configure API Key
```bash
voiceforge config set-api-key fish_audio YOUR_API_KEY
```

### 3. Convert Text to Speech
```bash
echo "Hello, VoiceForge!" > test.txt
voiceforge convert --input test.txt
```

---

## 📞 Support & Community

### Getting Help
- **Built-in Help**: `voiceforge --help`
- **Documentation**: Browse the guides above
- **Demo Script**: Run `python demo.py` for interactive demo
- **Troubleshooting**: Check the [troubleshooting section](getting-started-guide.md#troubleshooting)

### Contributing
- **Development Setup**: Follow the [development guide](getting-started-guide.md#development-setup)
- **Adding Providers**: See [adding TTS providers](getting-started-guide.md#adding-a-new-tts-provider)
- **Code Standards**: Use black, mypy, and flake8 for code quality

### Project Links
- **GitHub Repository**: (Coming soon)
- **Issue Tracker**: Report bugs and request features
- **Discussions**: Community support and ideas
- **Releases**: Download stable versions

---

## 🎵 About VoiceForge

VoiceForge is a modern, extensible text-to-speech application built with Python. It provides both command-line and (future) GUI interfaces for converting text files to high-quality MP3 audio using advanced AI-powered TTS services.

**Key Principles:**
- **Modularity**: Clean, extensible architecture
- **Security**: Encrypted API key storage
- **Usability**: Intuitive CLI with rich feedback
- **Quality**: High-quality audio output
- **Cross-Platform**: Works everywhere Python runs

**Current Status:** Phase 1 Complete ✅  
**Next Phase:** Enhanced CLI features and additional TTS providers

---

**🎉 Welcome to VoiceForge!** Start with the [Getting Started Guide](getting-started-guide.md) and join us in building the future of text-to-speech conversion. 