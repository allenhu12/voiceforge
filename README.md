# VoiceForge

Convert text files to high-quality MP3 audio using advanced Text-to-Speech services.

## Features

- 🎯 **Simple CLI Interface** - Easy-to-use command-line tool
- 🔌 **Pluggable TTS Providers** - Support for Fish Audio, with more providers coming
- 💰 **Cost Estimation** - Know the cost before conversion
- 📁 **Batch Processing** - Convert multiple files efficiently
- 🌍 **Cross-Platform** - Works on Windows, macOS, and Linux
- 🔒 **Secure API Key Management** - Encrypted storage of sensitive credentials
- 📊 **Detailed Statistics** - Character counts, file sizes, and conversion metrics

## Quick Start

### Installation

```bash
# Install VoiceForge
pip install voiceforge

# Or install with GUI support (coming soon)
pip install voiceforge[gui]
```

### Basic Usage

1. **Set up your API key** (Fish Audio example):
   ```bash
   voiceforge config set-api-key fish_audio YOUR_API_KEY
   ```

2. **Convert a text file**:
   ```bash
   voiceforge convert --input story.txt
   ```

3. **List available voices**:
   ```bash
   voiceforge list-voices
   ```

## Supported TTS Providers

### Fish Audio
- **Models**: speech-1.6, speech-1.4
- **Languages**: English, Chinese, Japanese, Korean, French, German, Spanish, Arabic
- **Pricing**: ~$0.015 per 1,000 characters
- **Setup**: Get your API key from [Fish Audio](https://fish.audio/)

## CLI Commands

### Convert Text to Speech
```bash
# Basic conversion
voiceforge convert --input file.txt

# Specify provider and voice
voiceforge convert --input file.txt --provider fish_audio --voice speech-1.6

# Custom output directory
voiceforge convert --input file.txt --output-dir ./audio

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

### Voice Management
```bash
# List available voices
voiceforge list-voices

# List voices for specific provider
voiceforge list-voices --provider fish_audio
```

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
      "default_voice": "speech-1.6"
    }
  },
  "output": {
    "default_directory": "./voiceforge_output",
    "naming_pattern": "{filename}.mp3"
  }
}
```

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

### Phase 1: Core CLI (Current)
- ✅ Fish Audio integration
- ✅ Basic CLI interface
- ✅ Configuration management
- ✅ Cost estimation

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