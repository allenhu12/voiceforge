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
  -f, --output TEXT      Custom output filename (without extension)
  -o, --output-dir PATH  Output directory
  -p, --provider TEXT    TTS provider (default: fish_audio)
  -v, --voice TEXT       Voice/model to use (default: Taylor Swift)
  -b, --bitrate INTEGER  MP3 bitrate (default: 128)
  --natural             Enable natural speech mode (default: enabled)
  --no-natural          Disable natural speech mode (use basic TTS)
  --speech-speed FLOAT  Speech speed (0.5-2.0, default: 0.9)
  --temperature FLOAT   Speech variation (0.1-1.0, default: 0.7)
  --top-p FLOAT         Speech diversity (0.1-1.0, default: 0.7)
  --paragraph-pause     Paragraph pause length: short/medium/long (default: medium)
  --speech-type         Predefined speech type with optimized parameters
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

### List Speech Types Command
```bash
voiceforge list-speech-types

Show all available speech type presets with optimized parameters
```

---

## 💡 Common Usage Patterns

### Basic Conversion
```bash
# Simple conversion (uses Taylor Swift voice + natural speech by default)
voiceforge convert --input story.txt

# With custom output filename (natural speech enabled by default)
voiceforge convert --input story.txt --output my_audio_book

# With custom output directory (natural speech enabled by default)
voiceforge convert --input story.txt --output-dir ./audio

# With custom filename and directory (natural speech enabled by default)
voiceforge convert --input story.txt --output my_story --output-dir ./audiobooks

# With specific voice (natural speech still enabled by default)
voiceforge convert --input story.txt --voice speech-1.6

# Disable natural speech for basic TTS
voiceforge convert --input story.txt --no-natural

# Fine-tune natural speech parameters (already enabled by default)
voiceforge convert --input story.txt --speech-speed 0.8 --temperature 0.6

# Use different human voice (natural speech enabled by default)
voiceforge convert --input story.txt --voice 802e3bc2b27e49c2995d23ef70e6ac89
```

### Speech Type Presets (NEW!)
```bash
# Female narrator for audiobooks (optimized parameters)
voiceforge convert --input novel.txt --speech-type female-narrator

# Male narrator for documentaries
voiceforge convert --input documentary.txt --speech-type male-narrator

# Professional business presentation
voiceforge convert --input slides.txt --speech-type presentation

# Educational content
voiceforge convert --input lesson.txt --speech-type educational

# Meditation and relaxation guide
voiceforge convert --input meditation.txt --speech-type meditation

# Podcast episode
voiceforge convert --input episode.txt --speech-type podcast

# Technical documentation
voiceforge convert --input manual.txt --speech-type technical

# News and announcements
voiceforge convert --input news.txt --speech-type news

# Storytelling and creative content
voiceforge convert --input story.txt --speech-type storytelling

# Dramatic readings
voiceforge convert --input play.txt --speech-type dramatic

# Use preset but override voice
voiceforge convert --input text.txt --speech-type audiobook --voice custom_voice_id

# List all available speech types
voiceforge list-speech-types
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

### Natural Speech Mode Features
```bash
# Natural speech is enabled by default - no flags needed!
voiceforge convert --input text.txt

# Features included automatically:
# • Enhanced punctuation pauses (medium at commas, long at periods)
# • Smart paragraph breaks with configurable pause lengths
# • Text preprocessing (abbreviations, numbers, etc.)
# • Optimized speech parameters for natural flow

# Customize speech speed (natural speech already enabled)
voiceforge convert --input text.txt --speech-speed 0.8

# Adjust speech variation (natural speech already enabled)
voiceforge convert --input text.txt --temperature 0.6

# Control speech diversity (natural speech already enabled)
voiceforge convert --input text.txt --top-p 0.8

# Customize paragraph pauses for better structure (natural speech already enabled)
voiceforge convert --input text.txt --paragraph-pause long

# Short pauses for fast-paced content (natural speech already enabled)
voiceforge convert --input text.txt --paragraph-pause short

# Perfect for audiobooks (longer pauses between sections)
voiceforge convert --input audiobook.txt --paragraph-pause long --speech-speed 0.85

# Disable natural speech if you want basic TTS
voiceforge convert --input text.txt --no-natural
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