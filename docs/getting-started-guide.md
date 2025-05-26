# VoiceForge Getting Started Guide

**Version:** 1.0.0  
**Last Updated:** January 26, 2025  
**Target Audience:** Developers and Users

---

## 📚 Table of Contents

1. [Understanding Phase 1 Development](#understanding-phase-1-development)
2. [Installation Guide](#installation-guide)
3. [Basic Usage Tutorial](#basic-usage-tutorial)
4. [Advanced Features](#advanced-features)
5. [Development Setup](#development-setup)
6. [Troubleshooting](#troubleshooting)

---

## 🏗️ Understanding Phase 1 Development

### What We Built in Phase 1

Phase 1 focused on creating a solid foundation for VoiceForge with a complete CLI interface. Here's what was accomplished:

#### 1. **Modular Architecture**
```
VoiceForge/
├── src/voiceforge/           # Main application package
│   ├── interfaces/           # Abstract base classes
│   ├── services/            # TTS provider implementations
│   ├── core/               # Core business logic
│   ├── cli/                # Command-line interface
│   ├── gui/                # GUI (placeholder for Phase 3)
│   └── utils/              # Utilities and helpers
├── tests/                  # Test suite (to be expanded)
├── docs/                   # Documentation
└── requirements.txt        # Dependencies
```

#### 2. **Key Components Explained**

**🔌 TTSServiceInterface** (`src/voiceforge/interfaces/tts_service_interface.py`)
- Abstract base class defining the contract for all TTS providers
- Ensures consistent behavior across different TTS services
- Methods: `get_name()`, `text_to_speech()`, `estimate_cost()`, etc.

**🐟 FishTTSClient** (`src/voiceforge/services/fish_tts_client.py`)
- Concrete implementation for Fish Audio TTS service
- Handles API communication, authentication, and audio generation
- Uses msgpack serialization for Fish Audio's specific requirements

**⚙️ ConfigManager** (`src/voiceforge/core/config_manager.py`)
- Manages application configuration and secure API key storage
- Cross-platform configuration directories
- Encrypted API key storage using Fernet cryptography

**📁 InputHandler** (`src/voiceforge/core/input_handler.py`)
- Handles text file reading and validation
- Character encoding detection and text processing
- Smart text chunking for large files

**💾 OutputHandler** (`src/voiceforge/core/output_handler.py`)
- Manages MP3 file output and directory operations
- File naming conventions and conflict resolution
- Cross-platform file operations

**🏭 TTSServiceFactory** (`src/voiceforge/services/service_factory.py`)
- Factory pattern for creating TTS service instances
- Auto-registration of available providers
- Extensible design for adding new providers

#### 3. **Design Patterns Used**

- **Abstract Factory Pattern**: TTSServiceInterface + concrete implementations
- **Factory Pattern**: TTSServiceFactory for provider instantiation
- **Strategy Pattern**: Pluggable TTS providers
- **Command Pattern**: CLI commands with Click framework
- **Singleton Pattern**: Configuration manager instance

---

## 🚀 Installation Guide

### Prerequisites

- **Python 3.8+** (recommended: Python 3.10+)
- **pip** package manager
- **Internet connection** for TTS API calls

### Step 1: Clone or Download VoiceForge

```bash
# If you have the source code
cd /path/to/VoiceForge

# Or clone from repository (when available)
# git clone https://github.com/voiceforge/voiceforge.git
# cd voiceforge
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### Step 3: Install VoiceForge

```bash
# Install in development mode (recommended for now)
pip install -e .

# Or install specific extras
pip install -e .[dev]  # Include development tools
pip install -e .[gui]  # Include GUI dependencies (for future)
```

### Step 4: Verify Installation

```bash
# Check if VoiceForge is installed
voiceforge --version

# Should output: VoiceForge, version 1.0.0

# Check available commands
voiceforge --help
```

---

## 📖 Basic Usage Tutorial

### Step 1: Understanding the CLI Structure

VoiceForge uses a hierarchical command structure:

```bash
voiceforge [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS]
```

**Global Options:**
- `--verbose, -v`: Enable detailed logging
- `--config-dir PATH`: Use custom configuration directory
- `--version`: Show version information
- `--help`: Show help message

**Main Commands:**
- `convert`: Convert text files to MP3
- `config`: Manage configuration and API keys
- `list-voices`: List available voices for TTS providers

### Step 2: Set Up Your First TTS Provider

Before converting any text, you need to configure a TTS provider. Currently, VoiceForge supports Fish Audio.

#### Get Fish Audio API Key

1. Visit [Fish Audio](https://fish.audio/)
2. Sign up for an account
3. Navigate to API settings
4. Generate an API key

#### Configure the API Key

```bash
# Set your Fish Audio API key
voiceforge config set-api-key fish_audio YOUR_API_KEY_HERE

# Example:
# voiceforge config set-api-key fish_audio fa-1234567890abcdef
```

**Expected Output:**
```
✅ API key set for fish_audio
✅ API key validated successfully
```

### Step 3: Check Your Configuration

```bash
# View current configuration
voiceforge config show
```

**Expected Output:**
```
VoiceForge Configuration:
  Default provider: fish_audio
  Output directory: /Users/yourname/workspace/VoiceForge/voiceforge_output
  Configured providers: 1
```

```bash
# List available providers
voiceforge config list-providers
```

**Expected Output:**
```
Available TTS providers:
  ⭐ fish_audio ✅
```

### Step 4: Create a Test Text File

```bash
# Create a simple test file
echo "Hello, this is a test of VoiceForge. It can convert text to speech using advanced AI models." > test.txt
```

### Step 5: Your First Conversion

#### Estimate Cost First (Recommended)

```bash
# Get cost estimate without converting
voiceforge convert --input test.txt --estimate-only
```

**Expected Output:**
```
📖 Reading input file: test.txt
📊 Text statistics:
   Characters: 95
   Words: 17
   Lines: 1
💰 Estimated cost: ~$0.01 (95 chars)
✅ Cost estimation complete.
```

#### Perform the Conversion

```bash
# Convert the text file to MP3
voiceforge convert --input test.txt
```

**Expected Output:**
```
📖 Reading input file: test.txt
📊 Text statistics:
   Characters: 95
   Words: 17
   Lines: 1
💰 Estimated cost: ~$0.01 (95 chars)
Convert using fish_audio with voice 'speech-1.6'? [y/N]: y
🔄 Converting text to speech...
   Provider: fish_audio
   Voice: speech-1.6
   Output: /path/to/voiceforge_output/test_fish_audio_speech-1.6.mp3
✅ Conversion successful!
   Output file: /path/to/voiceforge_output/test_fish_audio_speech-1.6.mp3
   File size: 0.15 MB
Open output directory? [y/N]: y
```

### Step 6: Explore Available Voices

```bash
# List available voices for Fish Audio
voiceforge list-voices
```

**Expected Output:**
```
🔄 Fetching voices for fish_audio...

Available voices for Fish Audio:
  • Speech 1.6 (speech-1.6)
    Latest Fish Audio speech model
    Languages: en, zh, ja, ko, fr, de, es, ar

  • Speech 1.4 (speech-1.4)
    Previous generation speech model
    Languages: en, zh, ja
```

---

## 🔧 Advanced Features

### Custom Voice Selection

```bash
# Use a specific voice
voiceforge convert --input test.txt --voice speech-1.4

# Use a specific provider (when multiple are available)
voiceforge convert --input test.txt --provider fish_audio --voice speech-1.6
```

### Custom Output Directory

```bash
# Specify custom output directory
voiceforge convert --input test.txt --output-dir ./my-audio

# The directory will be created if it doesn't exist
```

### Audio Quality Settings

```bash
# Set MP3 bitrate (64, 128, 192, 320)
voiceforge convert --input test.txt --bitrate 192
```

### Overwrite Existing Files

```bash
# Overwrite existing output files
voiceforge convert --input test.txt --overwrite
```

### Verbose Logging

```bash
# Enable detailed logging for troubleshooting
voiceforge --verbose convert --input test.txt
```

### Configuration Management

```bash
# Remove an API key
voiceforge config remove-api-key fish_audio

# Reset configuration to defaults
voiceforge config reset

# Use custom configuration directory
voiceforge --config-dir ./my-config config show
```

---

## 🛠️ Development Setup

### For Developers Who Want to Extend VoiceForge

#### Step 1: Development Installation

```bash
# Clone the repository
git clone https://github.com/voiceforge/voiceforge.git
cd voiceforge

# Create development environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e .[dev]
```

#### Step 2: Development Tools

```bash
# Format code
black src/

# Type checking
mypy src/

# Linting
flake8 src/

# Run tests
pytest
```

#### Step 3: Adding a New TTS Provider

1. **Create Provider Client**:
   ```python
   # src/voiceforge/services/my_tts_client.py
   from ..interfaces.tts_service_interface import TTSServiceInterface
   
   class MyTTSClient(TTSServiceInterface):
       def get_name(self) -> str:
           return "My TTS Service"
       
       # Implement all required methods...
   ```

2. **Register Provider**:
   ```python
   # In src/voiceforge/services/service_factory.py
   from .my_tts_client import MyTTSClient
   TTSServiceFactory.register_provider("my_tts", MyTTSClient)
   ```

3. **Test Your Provider**:
   ```bash
   voiceforge config list-providers  # Should show your provider
   voiceforge config set-api-key my_tts YOUR_API_KEY
   voiceforge convert --input test.txt --provider my_tts
   ```

---

## 🔍 Understanding the Code Structure

### Key Files to Understand

#### 1. **Main CLI Entry Point**
```python
# src/voiceforge/cli/main.py
@cli.command()
def convert(ctx, input_file, output_dir, provider, voice, bitrate, overwrite, estimate_only):
    # Main conversion logic
    # 1. Load configuration
    # 2. Create TTS service
    # 3. Read input file
    # 4. Estimate cost
    # 5. Perform conversion
    # 6. Save output
```

#### 2. **TTS Service Interface**
```python
# src/voiceforge/interfaces/tts_service_interface.py
class TTSServiceInterface(ABC):
    @abstractmethod
    def text_to_speech(self, api_key, text, output_file_path, voice_or_model, mp3_bitrate, extra_settings):
        # Convert text to speech and save as MP3
        pass
```

#### 3. **Configuration Management**
```python
# src/voiceforge/core/config_manager.py
class ConfigManager:
    def set_api_key(self, provider, api_key):
        # Encrypt and store API key securely
        encrypted_bytes = self._cipher.encrypt(api_key.encode())
```

### Data Flow

1. **User runs command**: `voiceforge convert --input test.txt`
2. **CLI parses arguments**: Click framework processes options
3. **Configuration loaded**: ConfigManager reads settings and API keys
4. **TTS service created**: Factory creates appropriate provider instance
5. **Input processed**: InputHandler reads and validates text file
6. **Cost estimated**: TTS service calculates estimated cost
7. **Conversion performed**: TTS service calls API and gets audio data
8. **Output saved**: OutputHandler saves MP3 file with proper naming

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### 1. **Installation Issues**

**Problem**: `pip install -e .` fails
```bash
# Solution: Update pip and setuptools
pip install --upgrade pip setuptools

# Try installation again
pip install -e .
```

**Problem**: Missing dependencies
```bash
# Solution: Install dependencies manually
pip install click httpx ormsgpack pydantic python-dotenv cryptography chardet
```

#### 2. **Configuration Issues**

**Problem**: "No API key found for fish_audio"
```bash
# Solution: Set your API key
voiceforge config set-api-key fish_audio YOUR_API_KEY

# Verify it's set
voiceforge config show
```

**Problem**: Configuration file corruption
```bash
# Solution: Reset configuration
rm -rf ~/.config/voiceforge  # On Linux/macOS
# Or delete %LOCALAPPDATA%\VoiceForge on Windows

# Reconfigure
voiceforge config set-api-key fish_audio YOUR_API_KEY
```

#### 3. **API Issues**

**Problem**: "Authentication failed for Fish Audio"
```bash
# Solution: Verify your API key
# 1. Check Fish Audio dashboard
# 2. Regenerate API key if needed
# 3. Update VoiceForge configuration
voiceforge config set-api-key fish_audio NEW_API_KEY
```

**Problem**: "Network operation failed"
```bash
# Solution: Check network connectivity
# 1. Verify internet connection
# 2. Check if Fish Audio API is accessible
curl -I https://api.fish.audio/v1/models

# Try with verbose logging
voiceforge --verbose convert --input test.txt
```

#### 4. **File Issues**

**Problem**: "File does not exist"
```bash
# Solution: Check file path
ls -la test.txt  # Verify file exists
pwd              # Check current directory

# Use absolute path
voiceforge convert --input /full/path/to/test.txt
```

**Problem**: "Directory is not writable"
```bash
# Solution: Check permissions
ls -la voiceforge_output/

# Create directory manually
mkdir -p ./my-output
voiceforge convert --input test.txt --output-dir ./my-output
```

### Debug Mode

```bash
# Enable maximum verbosity for debugging
voiceforge --verbose convert --input test.txt

# Check log files (if configured)
tail -f ~/.config/voiceforge/logs/voiceforge.log
```

### Getting Help

```bash
# Command-specific help
voiceforge convert --help
voiceforge config --help

# General help
voiceforge --help
```

---

## 🎯 Next Steps

### For Users
1. **Experiment with different voices** using `--voice` option
2. **Try different file types** (currently supports .txt)
3. **Explore batch processing** (coming in Phase 2)

### For Developers
1. **Add unit tests** for your components
2. **Implement additional TTS providers** (OpenAI, Google, etc.)
3. **Contribute to the GUI development** (Phase 3)

### Phase 2 Preview
Coming soon:
- **Batch processing**: Convert multiple files at once
- **Additional TTS providers**: OpenAI TTS, Google Cloud TTS
- **Enhanced voice management**: Favorites, filtering, preview
- **Advanced configuration**: Profiles, custom settings

---

**🎉 Congratulations!** You now understand how VoiceForge was built and how to use it effectively. The modular architecture makes it easy to extend and customize for your specific needs.

For more information, check out:
- `README.md` - Project overview and features
- `progress.md` - Development progress and roadmap
- `TTS_tool/VoiceForge_Development_Plan_v1.0.md` - Detailed development plan 