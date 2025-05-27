# VoiceForge Speech Type Presets Guide

Transform your text-to-speech with optimized parameter sets designed for specific use cases.

## 🎯 Quick Start

### Using Speech Type Presets
```bash
# Female narrator for audiobooks
voiceforge convert --input story.txt --speech-type female-narrator

# Professional presentation
voiceforge convert --input slides.txt --speech-type presentation

# Meditation guide
voiceforge convert --input meditation.txt --speech-type meditation
```

### List Available Presets
```bash
# Show all speech type presets
voiceforge list-speech-types
```

## 🎭 Available Speech Types

### **Narration Category**

#### **female-narrator**
- **Description**: Professional female narrator for audiobooks and storytelling
- **Voice**: Taylor Swift (`cfc33da8775c47afacccf4eebabe44dc`)
- **Parameters**: Speed=0.85, Temperature=0.6, Top-p=0.7, Pause=long
- **Best for**: Audiobooks, storytelling, professional narration

#### **male-narrator**
- **Description**: Professional male narrator for audiobooks and documentaries
- **Voice**: ElevenLabs Adam (`728f6ff2240d49308e8137ffe66008e2`)
- **Parameters**: Speed=0.85, Temperature=0.6, Top-p=0.7, Pause=long
- **Best for**: Audiobooks, documentaries, professional narration

#### **audiobook**
- **Description**: Optimized for long-form audiobook narration with clear pacing
- **Voice**: Taylor Swift (`cfc33da8775c47afacccf4eebabe44dc`)
- **Parameters**: Speed=0.8, Temperature=0.5, Top-p=0.6, Pause=long
- **Best for**: Long-form audiobooks, novels, literature

#### **storytelling**
- **Description**: Expressive, engaging speech for stories and creative content
- **Voice**: Taylor Swift (`cfc33da8775c47afacccf4eebabe44dc`)
- **Parameters**: Speed=0.85, Temperature=0.7, Top-p=0.8, Pause=medium
- **Best for**: Stories, creative writing, children's content

### **Professional Category**

#### **presentation**
- **Description**: Clear, professional speech for business presentations
- **Voice**: Energetic Male (`802e3bc2b27e49c2995d23ef70e6ac89`)
- **Parameters**: Speed=0.9, Temperature=0.4, Top-p=0.6, Pause=medium
- **Best for**: Business presentations, corporate content, training

#### **educational**
- **Description**: Clear, engaging speech for educational content and tutorials
- **Voice**: Taylor Swift (`cfc33da8775c47afacccf4eebabe44dc`)
- **Parameters**: Speed=0.85, Temperature=0.6, Top-p=0.7, Pause=medium
- **Best for**: Educational content, tutorials, e-learning

#### **news**
- **Description**: Professional, authoritative speech for news and announcements
- **Voice**: Energetic Male (`802e3bc2b27e49c2995d23ef70e6ac89`)
- **Parameters**: Speed=0.95, Temperature=0.4, Top-p=0.6, Pause=short
- **Best for**: News broadcasts, announcements, formal content

#### **technical**
- **Description**: Clear, precise speech for technical documentation and manuals
- **Voice**: Speech 1.6 AI (`speech-1.6`)
- **Parameters**: Speed=0.85, Temperature=0.4, Top-p=0.6, Pause=medium
- **Best for**: Technical documentation, manuals, specifications

### **Casual Category**

#### **podcast**
- **Description**: Conversational, natural speech for podcast content
- **Voice**: Taylor Swift (`cfc33da8775c47afacccf4eebabe44dc`)
- **Parameters**: Speed=0.9, Temperature=0.6, Top-p=0.8, Pause=short
- **Best for**: Podcasts, conversational content, interviews

#### **conversational**
- **Description**: Natural, casual speech for everyday content
- **Voice**: Taylor Swift (`cfc33da8775c47afacccf4eebabe44dc`)
- **Parameters**: Speed=0.9, Temperature=0.7, Top-p=0.7, Pause=short
- **Best for**: Casual content, blogs, personal messages

### **Specialized Category**

#### **meditation**
- **Description**: Calm, soothing speech for meditation and relaxation content
- **Voice**: Taylor Swift (`cfc33da8775c47afacccf4eebabe44dc`)
- **Parameters**: Speed=0.75, Temperature=0.5, Top-p=0.6, Pause=long
- **Best for**: Meditation guides, relaxation, mindfulness content

#### **dramatic**
- **Description**: Expressive, theatrical speech for dramatic content
- **Voice**: Taylor Swift (`cfc33da8775c47afacccf4eebabe44dc`)
- **Parameters**: Speed=0.8, Temperature=0.8, Top-p=0.8, Pause=medium
- **Best for**: Dramatic readings, theater, emotional content

## 📖 Usage Examples

### **Basic Usage**
```bash
# Use female narrator preset
voiceforge convert --input novel.txt --speech-type female-narrator

# Use presentation preset
voiceforge convert --input business_report.txt --speech-type presentation
```

### **Advanced Usage**
```bash
# Use preset but override voice
voiceforge convert --input story.txt --speech-type audiobook --voice custom_voice_id

# Use preset with custom output
voiceforge convert --input meditation.txt --speech-type meditation --output relaxation_guide

# Use preset with different bitrate
voiceforge convert --input podcast.txt --speech-type podcast --bitrate 192
```

### **Batch Processing**
```bash
# Convert multiple files with different presets
voiceforge convert --input chapter1.txt --speech-type audiobook --output book_ch1
voiceforge convert --input chapter2.txt --speech-type audiobook --output book_ch2
voiceforge convert --input intro.txt --speech-type presentation --output presentation_intro
```

## 🔧 Parameter Details

### **Speech Speed**
- **0.75**: Very slow, meditative pace
- **0.8-0.85**: Slow, clear narration pace
- **0.9**: Natural, comfortable pace
- **0.95**: Slightly faster, news-style pace

### **Temperature**
- **0.4**: Very consistent, robotic-like
- **0.5-0.6**: Consistent with slight variation
- **0.7**: Natural variation (recommended)
- **0.8**: High variation, expressive

### **Top-p**
- **0.6**: Focused, consistent speech
- **0.7**: Balanced diversity (recommended)
- **0.8**: More diverse, conversational

### **Paragraph Pause**
- **short**: Quick transitions, conversational
- **medium**: Balanced pacing
- **long**: Clear separation, audiobook style

## 🎯 Choosing the Right Preset

### **For Audiobooks**
- **audiobook**: Long-form content, consistent pacing
- **female-narrator**: Professional female voice
- **male-narrator**: Professional male voice

### **For Business**
- **presentation**: Professional, authoritative
- **educational**: Clear, engaging
- **technical**: Precise, consistent

### **For Content Creation**
- **podcast**: Conversational, engaging
- **storytelling**: Expressive, creative
- **conversational**: Natural, casual

### **For Wellness**
- **meditation**: Calm, soothing
- **dramatic**: Expressive, theatrical

## 🔍 Discovery Commands

```bash
# List all speech type presets
voiceforge list-speech-types

# Show available voices
voiceforge list-voices

# Show current configuration
voiceforge config show
```

## ⚙️ How Presets Work

### **Parameter Override**
When you use `--speech-type`, it overrides individual parameter settings:
```bash
# These parameters are ignored when using --speech-type
voiceforge convert --input text.txt \
  --speech-type female-narrator \
  --speech-speed 1.0 \          # Ignored (preset uses 0.85)
  --temperature 0.9 \           # Ignored (preset uses 0.6)
  --top-p 0.5                   # Ignored (preset uses 0.7)
```

### **Voice Selection Priority**
1. Explicit `--voice` parameter (highest priority)
2. Speech type preset voice preference
3. Configured default voice
4. Provider default voice (lowest priority)

### **Natural Speech Mode**
All presets automatically enable natural speech mode with optimized text preprocessing.

## 🎨 Customization

### **Creating Custom Workflows**
```bash
# Female narrator for fiction
voiceforge convert --input fiction.txt --speech-type female-narrator

# Male narrator for non-fiction
voiceforge convert --input nonfiction.txt --speech-type male-narrator

# Technical documentation
voiceforge convert --input manual.txt --speech-type technical

# Meditation series
voiceforge convert --input session1.txt --speech-type meditation --output meditation_01
voiceforge convert --input session2.txt --speech-type meditation --output meditation_02
```

### **Content-Specific Optimization**
- **Novels**: Use `audiobook` or `storytelling`
- **Business Reports**: Use `presentation` or `educational`
- **Podcasts**: Use `podcast` or `conversational`
- **Tutorials**: Use `educational` or `technical`
- **Relaxation**: Use `meditation`
- **Drama**: Use `dramatic` or `storytelling`

## 🚀 Best Practices

### **1. Match Content to Preset**
Choose presets that align with your content's purpose and audience.

### **2. Test Different Presets**
Try multiple presets with sample text to find the best fit.

### **3. Consider Voice Preference**
Some presets work better with specific voice types (male vs. female).

### **4. Use Consistent Presets**
For series or multi-part content, use the same preset for consistency.

### **5. Override When Needed**
Use `--voice` to override preset voice while keeping optimized parameters.

## 📊 Preset Comparison Table

| Preset | Speed | Temp | Top-p | Pause | Voice Type | Best For |
|--------|-------|------|-------|-------|------------|----------|
| female-narrator | 0.85 | 0.6 | 0.7 | long | Female | Audiobooks |
| male-narrator | 0.85 | 0.6 | 0.7 | long | Male | Documentaries |
| audiobook | 0.8 | 0.5 | 0.6 | long | Female | Long-form |
| presentation | 0.9 | 0.4 | 0.6 | medium | Male | Business |
| educational | 0.85 | 0.6 | 0.7 | medium | Female | Learning |
| podcast | 0.9 | 0.6 | 0.8 | short | Female | Conversational |
| news | 0.95 | 0.4 | 0.6 | short | Male | Formal |
| meditation | 0.75 | 0.5 | 0.6 | long | Female | Relaxation |
| technical | 0.85 | 0.4 | 0.6 | medium | AI | Documentation |
| conversational | 0.9 | 0.7 | 0.7 | short | Female | Casual |
| storytelling | 0.85 | 0.7 | 0.8 | medium | Female | Creative |
| dramatic | 0.8 | 0.8 | 0.8 | medium | Female | Theater |

## 💡 Tips & Tricks

### **Quick Commands**
```bash
# Female audiobook narrator
voiceforge convert --input book.txt --speech-type female-narrator

# Business presentation
voiceforge convert --input slides.txt --speech-type presentation

# Relaxing meditation
voiceforge convert --input guide.txt --speech-type meditation
```

### **Batch Scripts**
Create shell scripts for common workflows:
```bash
#!/bin/bash
# Convert all chapters with audiobook preset
for file in chapter*.txt; do
    voiceforge convert --input "$file" --speech-type audiobook
done
```

### **Quality Optimization**
- Use `audiobook` for highest quality long-form content
- Use `technical` for consistent, clear documentation
- Use `meditation` for the most soothing, calm delivery

---

**Ready to create professional-quality speech with optimized presets!** 🎵

Use `voiceforge list-speech-types` to explore all available options and find the perfect preset for your content. 