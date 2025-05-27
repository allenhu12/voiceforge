# VoiceForge

Convert text files to high-quality MP3 audio using advanced Text-to-Speech services.

## Features

- 🎯 **Simple CLI Interface** - Easy-to-use command-line tool
- 📦 **Standalone Executables** - No Python installation required for end users
- 🎭 **Speech Type Presets** - 12 optimized presets for different use cases (audiobook, podcast, presentation, etc.)
- 🗣️ **Natural Speech Mode** - Enhanced text preprocessing with proper pauses and natural flow
- 📈 **Real-Time Progress Tracking** - Smooth progress bars with live status updates
- 🔌 **Pluggable TTS Providers** - Support for Fish Audio, with more providers coming
- 💰 **Cost Estimation** - Know the cost before conversion
- 📁 **Batch Processing** - Convert multiple files efficiently
- 🌍 **Cross-Platform** - Works on Windows, macOS, and Linux
- 🔒 **Secure API Key Management** - Encrypted storage of sensitive credentials
- 📊 **Detailed Statistics** - Character counts, file sizes, and conversion metrics

## Quick Start

### Installation

#### Option 1: Python Package (Developers)
```bash
# Install VoiceForge
pip install voiceforge

# Or install with GUI support (coming soon)
pip install voiceforge[gui]
```

#### Option 2: Standalone Executable (End Users)
**No Python Required!** Download the pre-built executable for your platform:

- **Windows**: Download `VoiceForge.exe` 
- **macOS**: Download `VoiceForge` binary
- **Linux**: Download `VoiceForge` binary

Or build your own using the instructions in [Building Standalone Executables](#building-standalone-executables).

### Basic Usage

1. **Set up your API key** (Fish Audio example):
   ```bash
   voiceforge config set-api-key fish_audio YOUR_API_KEY
   ```

2. **Convert a text file** (uses high-quality female voice + natural speech by default):
   ```bash
   voiceforge convert --input story.txt
   ```

3. **Use speech type presets** for optimized results:
   ```bash
   voiceforge convert --input story.txt --speech-type female-narrator
   ```

4. **List available voices and speech types**:
   ```bash
   voiceforge list-voices
   voiceforge list-speech-types
   ```

## Supported TTS Providers

### Fish Audio
- **Models**: AI models (speech-1.6, speech-1.5) + Human voice models
- **Default Voice**: High-quality female narrator (professional audiobook quality)
- **Languages**: English, Chinese, Japanese, Korean, French, German, Spanish, Arabic
- **Pricing**: ~$0.015 per 1,000 characters
- **Setup**: Get your API key from [Fish Audio](https://fish.audio/)

## CLI Commands

### Convert Text to Speech

#### Basic Conversion
```bash
# Basic conversion (high-quality female voice + natural speech enabled by default)
voiceforge convert --input file.txt

# Specify custom output filename
voiceforge convert --input file.txt --output my_audio

# Custom output directory
voiceforge convert --input file.txt --output-dir ./audio
```

#### Speech Type Presets (Recommended)
```bash
# Female narrator for audiobooks
voiceforge convert --input novel.txt --speech-type female-narrator

# Male narrator for documentaries
voiceforge convert --input documentary.txt --speech-type male-narrator

# Professional presentation
voiceforge convert --input slides.txt --speech-type presentation

# Educational content
voiceforge convert --input lesson.txt --speech-type educational

# Meditation guide
voiceforge convert --input meditation.txt --speech-type meditation

# Podcast episode
voiceforge convert --input episode.txt --speech-type podcast

# List all available presets
voiceforge list-speech-types
```

#### Advanced Options
```bash
# Specify provider and voice
voiceforge convert --input file.txt --provider fish_audio --voice speech-1.6

# Fine-tune natural speech parameters
voiceforge convert --input file.txt --speech-speed 0.8 --temperature 0.6

# Disable natural speech for basic TTS
voiceforge convert --input file.txt --no-natural

# Estimate cost only
voiceforge convert --input file.txt --estimate-only
```

### Configuration Management
```bash
# Set API key
voiceforge config set-api-key fish_audio YOUR_KEY

# List providers
voiceforge config list-providers

# Show current configuration
voiceforge config show
```

### Voice and Speech Type Management
```bash
# List available voices
voiceforge list-voices

# List voices for specific provider
voiceforge list-voices --provider fish_audio

# List all speech type presets
voiceforge list-speech-types

# Set default voice
voiceforge config set-default-voice fish_audio VOICE_ID
```

## Speech Type Presets

VoiceForge includes 12 professionally optimized speech type presets for different use cases:

### Narration
- **`female-narrator`** - Professional female audiobook narration
- **`male-narrator`** - Professional male audiobook narration  
- **`audiobook`** - Long-form audiobook optimization
- **`storytelling`** - Expressive creative storytelling

### Professional
- **`presentation`** - Clear business presentations
- **`educational`** - Engaging educational content
- **`news`** - Authoritative news delivery
- **`technical`** - Precise technical documentation

### Casual
- **`podcast`** - Conversational podcast content
- **`conversational`** - Natural everyday speech

### Specialized
- **`meditation`** - Calm, soothing relaxation guides
- **`dramatic`** - Expressive theatrical content

Each preset includes optimized parameters for:
- **Speech Speed** - Appropriate pacing for content type
- **Temperature** - Natural variation vs. consistency
- **Top-p** - Speech diversity control
- **Paragraph Pauses** - Proper content structure
- **Voice Selection** - Best voice for the use case

### Usage Examples
```bash
# Professional audiobook narration
voiceforge convert --input novel.txt --speech-type female-narrator

# Business presentation
voiceforge convert --input slides.txt --speech-type presentation

# Meditation guide
voiceforge convert --input meditation.txt --speech-type meditation

# See all available presets
voiceforge list-speech-types
```

## Natural Speech Mode

VoiceForge includes advanced natural speech processing enabled by default:

### Features
- **Smart Punctuation Pauses** - Proper timing at commas, periods, questions
- **Paragraph Breaks** - Configurable pauses between sections
- **Text Preprocessing** - Abbreviation expansion, number normalization
- **Breathing Pauses** - Natural breaks in long content
- **Sentence Optimization** - Breaking up overly long sentences

### Punctuation Pause Hierarchy
- **Commas, Semicolons, Colons** → Medium pauses (`, ..`)
- **Periods, Questions, Exclamations** → Long pauses (`. ...`)
- **Paragraph Breaks** → Extra long pauses (`... ... ...`)

### Configuration Options
```bash
# Default natural speech (recommended)
voiceforge convert --input text.txt

# Customize speech parameters
voiceforge convert --input text.txt --speech-speed 0.8 --temperature 0.6

# Adjust paragraph pause length
voiceforge convert --input text.txt --paragraph-pause long

# Disable for basic TTS
voiceforge convert --input text.txt --no-natural
```

### Paragraph Pause Options
- **`short`** - Quick transitions for conversational content
- **`medium`** - Balanced pacing (default)
- **`long`** - Clear separation for audiobooks and presentations

## Configuration

VoiceForge stores configuration in platform-specific directories:

- **Windows**: `%LOCALAPPDATA%\VoiceForge\`
- **macOS**: `~/Library/Application Support/VoiceForge/`
- **Linux**: `~/.config/voiceforge/`

### Configuration File Structure
```json
{
  "default_provider": "fish_audio",
  "providers": {
    "fish_audio": {
      "api_key_encrypted": "...",
      "default_voice": "b545c585f631496c914815291da4e893"
    }
  },
  "output": {
    "default_directory": "./voiceforge_output",
    "naming_pattern": "{filename}.mp3"
  }
}
```

## Building Standalone Executables

VoiceForge can be packaged into standalone executables that work without Python installation on Windows, macOS, and Linux.

### Quick Build

```bash
# Install build dependencies
pip install -r requirements-build.txt

# Build for current platform
python build_config.py

# Find executable in dist/ directory
```

### Platform-Specific Builds

```bash
# Windows (on Windows system)
python build_config.py --platform windows
# Or: build_windows.bat

# macOS (on macOS system) 
python build_config.py --platform macos
# Or: ./build_macos.sh

# Linux (on Linux system)
python build_config.py --platform linux  
# Or: ./build_linux.sh
```

### Build Options

```bash
# Clean build (remove previous artifacts)
python build_config.py --clean

# Debug build (larger, with debug symbols)
python build_config.py --debug

# Create platform build scripts
python build_config.py --create-scripts
```

### Distribution

After building, you'll find standalone executables in:
- **Windows**: `dist/windows/VoiceForge.exe` (~50-80 MB)
- **macOS**: `dist/macos/VoiceForge` (~13-15 MB)
- **Linux**: `dist/linux/VoiceForge` (~50-80 MB)

### End User Installation

**No Python Required!** Users can simply:

1. **Download** the appropriate executable for their platform
2. **Make executable** (macOS/Linux only): `chmod +x VoiceForge`
3. **Run directly**: `./VoiceForge --help`

### Usage Examples for Standalone Executables

```bash
# Set up API key
./VoiceForge config set-api-key fish_audio YOUR_API_KEY

# Convert text files
./VoiceForge convert --input story.txt
./VoiceForge convert --input novel.txt --speech-type female-narrator

# Explore features
./VoiceForge list-speech-types
./VoiceForge list-voices
```

### Build Requirements

- **Python 3.8+** (for building only)
- **PyInstaller 5.0+** (automatically installed)
- **Platform-specific tools**:
  - Windows: Visual Studio Build Tools
  - macOS: Xcode Command Line Tools
  - Linux: build-essential package

For detailed packaging instructions, see [`PACKAGING_GUIDE.md`](PACKAGING_GUIDE.md).

## Development

### Project Structure
```
VoiceForge/
├── src/voiceforge/
│   ├── interfaces/          # Abstract interfaces
│   ├── services/            # TTS service implementations
│   ├── core/               # Core functionality
│   ├── cli/                # Command-line interface
│   ├── gui/                # Graphical interface (coming soon)
│   └── utils/              # Utilities and helpers
├── tests/                  # Test suite
├── docs/                   # Documentation
└── requirements.txt        # Dependencies
```

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/voiceforge/voiceforge.git
cd voiceforge

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .[dev]

# Run tests
pytest

# Format code
black src/

# Type checking
mypy src/
```

### Adding New TTS Providers

1. Create a new client class implementing `TTSServiceInterface`
2. Register the provider in `service_factory.py`
3. Add configuration options and documentation

Example:
```python
from voiceforge.interfaces.tts_service_interface import TTSServiceInterface

class MyTTSClient(TTSServiceInterface):
    def get_name(self) -> str:
        return "My TTS Service"
    
    # Implement other required methods...
```

## Error Handling

VoiceForge provides detailed error messages and logging:

```bash
# Enable verbose logging
voiceforge --verbose convert --input file.txt

# Check logs (location varies by platform)
tail -f ~/.config/voiceforge/logs/voiceforge.log
```

Common issues:
- **Invalid API Key**: Check your API key configuration
- **Network Errors**: Verify internet connection and API service status
- **File Permissions**: Ensure read/write access to input/output directories
- **Character Limits**: Some providers have limits on text length

## Roadmap

### Phase 1: Core CLI (✅ Complete)
- ✅ Fish Audio integration
- ✅ Basic CLI interface
- ✅ Configuration management
- ✅ Cost estimation
- ✅ Speech type presets (12 optimized presets)
- ✅ Natural speech mode with text preprocessing
- ✅ Real-time progress tracking
- ✅ Professional voice quality

### Phase 2: Enhanced Features
- 🔄 Additional TTS providers (OpenAI, Google, Azure)
- 🔄 Batch processing
- 🔄 Voice preview functionality
- 🔄 Advanced audio settings

### Phase 3: GUI Application
- 📋 Cross-platform desktop application
- 📋 Drag-and-drop interface
- 📋 Real-time cost estimation
- 📋 Audio playback and preview

### Phase 4: Advanced Features
- 📋 Voice cloning support
- 📋 SSML markup support
- 📋 Audio post-processing
- 📋 Cloud storage integration

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 🔧 Submit pull requests
- 📖 Improve documentation
- 🧪 Add test coverage

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 **Documentation**: [GitHub Wiki](https://github.com/voiceforge/voiceforge/wiki)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/voiceforge/voiceforge/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/voiceforge/voiceforge/discussions)
- 📧 **Email**: contact@voiceforge.dev

## Acknowledgments

- [Fish Audio](https://fish.audio/) for providing excellent TTS services
- [Click](https://click.palletsprojects.com/) for the CLI framework
- [httpx](https://www.python-httpx.org/) for HTTP client functionality
- [Pydantic](https://pydantic.dev/) for data validation

---

**VoiceForge** - Transforming text into voice, one file at a time. 🎵 