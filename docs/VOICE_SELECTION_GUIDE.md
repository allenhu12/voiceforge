# VoiceForge Voice Selection Guide

This guide shows you how to get all available voice IDs from Fish Audio and use them with VoiceForge.

## 🎯 Quick Start

### 1. List Available Voices

```bash
# Show first 20 voices with details
voiceforge list-voices

# Show only voice IDs (first 10)
voiceforge list-voices --ids-only --limit 10

# Show more voices (up to 100)
voiceforge list-voices --limit 50
```

### 2. Use a Specific Voice

```bash
# Convert text using a specific voice ID
voiceforge convert --input text.txt --voice 54e3a85ac9594ffa83264b8a494b901b

# Convert with SpongeBob voice
voiceforge convert --input text.txt --voice 54e3a85ac9594ffa83264b8a494b901b
```

## 📋 Getting All Voice IDs

### Method 1: VoiceForge CLI (Recommended)

```bash
# Get just the IDs (fastest)
voiceforge list-voices --ids-only --limit 50

# Get IDs with details
voiceforge list-voices --limit 50
```

### Method 2: Standalone Script

```bash
# Get first 100 voice IDs
python get_all_voice_ids.py --api-key YOUR_API_KEY --limit 100 --ids-only

# Get all voices and save to files
python get_all_voice_ids.py --api-key YOUR_API_KEY --save-to-file

# Get unlimited voices (will take time!)
python get_all_voice_ids.py --api-key YOUR_API_KEY --ids-only
```

### Method 3: Direct API Call

```bash
# Get voice data directly from API
curl -H "Authorization: Bearer YOUR_API_KEY" \
     "https://api.fish.audio/model?page_size=100&page_number=1"
```

## 🎭 Popular Voice Models

Based on the current Fish Audio catalog, here are some popular voices:

### 🤖 AI Models
- `speech-1.6` - Latest Fish Audio AI model (multilingual)
- `speech-1.5` - Previous generation AI model

### 👤 Character Voices
- `54e3a85ac9594ffa83264b8a494b901b` - **SpongeBob SquarePants** (377 likes, 141K uses)
- `e58b0d7efca34eb38d5c4985e378abcb` - **POTUS 47 - Trump** (1,453 likes, 113K uses)
- `728f6ff2240d49308e8137ffe66008e2` - **ElevenLabs Adam** (254 likes, 50K uses)

### 🎙️ Professional Voices
- `802e3bc2b27e49c2995d23ef70e6ac89` - **Energetic Male** (485 likes, 85K uses)
- `ef9c79b62ef34530bf452c0e50e3c260` - **Horror** (633 likes, 25K uses)

### 🌍 International Voices
- `54a5170264694bfc8e9ad98df7bd89c3` - **丁真** (Chinese, 4,907 likes, 369K uses)
- `7f92f8afb8ec43bf81429cc1c9199cb1` - **AD学姐** (Chinese, 3,194 likes, 254K uses)
- `aebaa2305aa2452fbdc8f41eec852a79` - **雷军** (Chinese, 1,621 likes, 87K uses)
- `5b67899dc9a34685ae09c94c890a606f` - **عصام الشوالي** (Arabic, 1,449 likes, 106K uses)

## 🔧 Usage Examples

### Example 1: Convert with SpongeBob Voice

```bash
echo "I'm ready, I'm ready, I'm ready!" > spongebob_test.txt
voiceforge convert --input spongebob_test.txt --voice 54e3a85ac9594ffa83264b8a494b901b
```

### Example 2: Convert with Professional Voice

```bash
echo "Welcome to our professional presentation." > professional_test.txt
voiceforge convert --input professional_test.txt --voice 802e3bc2b27e49c2995d23ef70e6ac89
```

### Example 3: Convert with Chinese Voice

```bash
echo "大家好，欢迎来到VoiceForge演示。" > chinese_test.txt
voiceforge convert --input chinese_test.txt --voice 54a5170264694bfc8e9ad98df7bd89c3
```

## 📊 Voice Statistics

Fish Audio currently has **400,000+** voice models available, including:

- **Character voices** (SpongeBob, Trump, etc.)
- **Professional voices** (news anchors, presenters)
- **Celebrity voices** (various public figures)
- **International voices** (Chinese, Arabic, Japanese, etc.)
- **Specialized voices** (horror, comedy, etc.)

## 🔍 Finding the Right Voice

### By Language
```bash
# List voices and filter by language in the output
voiceforge list-voices --limit 50 | grep "Languages: en"
voiceforge list-voices --limit 50 | grep "Languages: zh"
voiceforge list-voices --limit 50 | grep "Languages: ar"
```

### By Popularity
Voices are sorted by popularity (likes and usage count). The first results are typically the most popular.

### By Type
- **AI Models**: Use `speech-1.6` for general purpose
- **Human Models**: Browse the list for specific characters or styles

## 💡 Tips

1. **Start with popular voices** - They tend to have better quality
2. **Check language support** - Make sure the voice supports your text language
3. **Test with short text first** - Before converting long documents
4. **Save favorite voice IDs** - Keep a list of voices you like
5. **Use cost estimation** - Check costs before converting large texts

## 🚀 Advanced Usage

### Batch Processing with Different Voices

```bash
# Convert multiple files with different voices
voiceforge convert --input story1.txt --voice 54e3a85ac9594ffa83264b8a494b901b
voiceforge convert --input story2.txt --voice 802e3bc2b27e49c2995d23ef70e6ac89
voiceforge convert --input story3.txt --voice e58b0d7efca34eb38d5c4985e378abcb
```

### Save Voice List for Reference

```bash
# Save all voice IDs to a file
voiceforge list-voices --ids-only --limit 100 > my_voice_ids.txt

# Save detailed voice info
python get_all_voice_ids.py --api-key YOUR_API_KEY --limit 200 --save-to-file
```

## 🔗 Resources

- **Fish Audio Playground**: https://fish.audio/ - Browse and test voices
- **VoiceForge Documentation**: See README.md for more details
- **API Documentation**: https://docs.fish.audio/ - Official Fish Audio docs

---

**Happy voice cloning!** 🎵 