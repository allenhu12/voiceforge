# VoiceForge Quick Reference

**Version:** 1.0.0  
**Last Updated:** January 26, 2025

---

## 🚀 Quick Start

```bash
# 1. Install VoiceForge
pip install -e .

# 2. Set up API key
voiceforge config set-api-key fish_audio YOUR_API_KEY

# 3. Convert text to speech
voiceforge convert --input text.txt
```

---

## 📋 Command Reference

### Global Options
```bash
voiceforge [OPTIONS] COMMAND [ARGS]...

Options:
  --version          Show version and exit
  -v, --verbose      Enable verbose logging
  --config-dir PATH  Custom configuration directory
  --help             Show help message
```

### Convert Command
```bash
voiceforge convert [OPTIONS]

Options:
  -i, --input PATH       Input text file (required)
  -o, --output-dir PATH  Output directory
  -p, --provider TEXT    TTS provider (default: fish_audio)
  -v, --voice TEXT       Voice/model to use
  -b, --bitrate INTEGER  MP3 bitrate (default: 128)
  --overwrite           Overwrite existing files
  --estimate-only       Show cost estimate only
  --help                Show help message
```

### Config Commands
```bash
voiceforge config COMMAND [ARGS]...

Commands:
  set-api-key PROVIDER KEY  Set API key for provider
  list-providers           List available providers
  show                     Show current configuration
```

### List Voices Command
```bash
voiceforge list-voices [OPTIONS]

Options:
  -p, --provider TEXT  TTS provider (default: configured)
  --help              Show help message
```

---

## 💡 Common Usage Patterns

### Basic Conversion
```bash
# Simple conversion
voiceforge convert --input story.txt

# With custom output directory
voiceforge convert --input story.txt --output-dir ./audio

# With specific voice
voiceforge convert --input story.txt --voice speech-1.4
```

### Cost Estimation
```bash
# Check cost before converting
voiceforge convert --input story.txt --estimate-only

# Expected output:
# 💰 Estimated cost: ~$0.05 (3,245 chars)
```

### Configuration Management
```bash
# Set up Fish Audio
voiceforge config set-api-key fish_audio fa-your-key-here

# Check configuration
voiceforge config show

# List all providers
voiceforge config list-providers
```

### Voice Management
```bash
# List available voices
voiceforge list-voices

# List voices for specific provider
voiceforge list-voices --provider fish_audio
```

### Advanced Options
```bash
# High quality audio
voiceforge convert --input text.txt --bitrate 320

# Overwrite existing files
voiceforge convert --input text.txt --overwrite

# Verbose logging for debugging
voiceforge --verbose convert --input text.txt
```

---

## 🔧 Configuration Locations

### Default Config Directories
- **Windows:** `%LOCALAPPDATA%\VoiceForge\`
- **macOS:** `~/Library/Application Support/VoiceForge/`
- **Linux:** `~/.config/voiceforge/`

### Config Files
- `config.json` - Main configuration
- `.key` - Encryption key for API keys
- `logs/voiceforge.log` - Application logs (if enabled)

---

## 🎯 File Naming Patterns

### Default Output Names
```
{input_filename}_{provider}_{voice}.mp3

Examples:
- story_fish_audio_speech-1.6.mp3
- document_fish_audio_speech-1.4.mp3
```

### Custom Output Directory
```bash
# Default: ./voiceforge_output/
# Custom: --output-dir ./my-audio/
```

---

## 🐛 Quick Troubleshooting

### Common Errors

**"No API key found"**
```bash
voiceforge config set-api-key fish_audio YOUR_KEY
```

**"File does not exist"**
```bash
ls -la your-file.txt  # Check if file exists
pwd                   # Check current directory
```

**"Authentication failed"**
```bash
# Check your API key in Fish Audio dashboard
voiceforge config set-api-key fish_audio NEW_KEY
```

**"Network operation failed"**
```bash
# Check internet connection
curl -I https://api.fish.audio/v1/models
```

### Debug Mode
```bash
# Enable verbose logging
voiceforge --verbose convert --input text.txt

# Check configuration
voiceforge config show
```

---

## 📊 Supported Features

### File Formats
- **Input:** `.txt` files
- **Output:** `.mp3` files

### TTS Providers
- **Fish Audio** ✅ (speech-1.6, speech-1.4)
- **OpenAI TTS** 🔄 (Coming in Phase 2)
- **Google Cloud TTS** 🔄 (Coming in Phase 2)

### Audio Quality
- **Bitrates:** 64, 128, 192, 320 kbps
- **Format:** MP3
- **Quality:** High-quality AI-generated speech

### Languages (Fish Audio)
- English, Chinese, Japanese, Korean
- French, German, Spanish, Arabic

---

## 🚀 Phase 2 Preview

### Coming Soon
```bash
# Batch processing (multiple files)
voiceforge batch --input-dir ./texts/ --output-dir ./audio/

# Multiple providers
voiceforge convert --input text.txt --provider openai --voice alloy

# Voice preview
voiceforge preview --provider fish_audio --voice speech-1.6 --text "Hello world"
```

---

## 📞 Getting Help

### Built-in Help
```bash
voiceforge --help                    # General help
voiceforge convert --help            # Convert command help
voiceforge config --help             # Config commands help
```

### Documentation
- `docs/getting-started-guide.md` - Complete tutorial
- `README.md` - Project overview
- `progress.md` - Development progress

### Support
- GitHub Issues: Report bugs and request features
- GitHub Discussions: Community support
- Email: contact@voiceforge.dev

---

**💡 Pro Tip:** Use `--estimate-only` to check costs before converting large files! 