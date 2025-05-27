"""
Speech Type Presets for VoiceForge

This module defines predefined speech types with optimized parameter sets
for different use cases like audiobooks, presentations, podcasts, etc.
"""

from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class SpeechPreset:
    """Represents a speech preset with optimized parameters."""
    name: str
    description: str
    voice_preference: str  # Preferred voice type or specific voice ID
    speech_speed: float
    temperature: float
    top_p: float
    paragraph_pause: str
    use_case: str
    natural_speech: bool = True
    
    def to_settings_dict(self) -> Dict[str, Any]:
        """Convert preset to settings dictionary for TTS client."""
        return {
            "natural_speech": self.natural_speech,
            "speech_speed": self.speech_speed,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "paragraph_pause": self.paragraph_pause,
            "enable_preprocessing": self.natural_speech,
            "prosody": {
                "speed": self.speech_speed,
                "volume": 0
            }
        }


class SpeechPresets:
    """Collection of predefined speech type presets."""
    
    # Define all available presets
    PRESETS = {
        "female-narrator": SpeechPreset(
            name="Female Narrator",
            description="Professional female narrator for audiobooks and storytelling",
            voice_preference="b545c585f631496c914815291da4e893",  # New default female voice
            speech_speed=0.85,
            temperature=0.6,
            top_p=0.7,
            paragraph_pause="long",
            use_case="Audiobooks, storytelling, professional narration"
        ),
        
        "male-narrator": SpeechPreset(
            name="Male Narrator",
            description="Professional male narrator for audiobooks and documentaries",
            voice_preference="728f6ff2240d49308e8137ffe66008e2",  # ElevenLabs Adam
            speech_speed=0.85,
            temperature=0.6,
            top_p=0.7,
            paragraph_pause="long",
            use_case="Audiobooks, documentaries, professional narration"
        ),
        
        "audiobook": SpeechPreset(
            name="Audiobook",
            description="Optimized for long-form audiobook narration with clear pacing",
            voice_preference="b545c585f631496c914815291da4e893",  # New default female voice
            speech_speed=0.8,
            temperature=0.5,
            top_p=0.6,
            paragraph_pause="long",
            use_case="Long-form audiobooks, novels, literature"
        ),
        
        "presentation": SpeechPreset(
            name="Presentation",
            description="Clear, professional speech for business presentations",
            voice_preference="802e3bc2b27e49c2995d23ef70e6ac89",  # Energetic Male
            speech_speed=0.9,
            temperature=0.4,
            top_p=0.6,
            paragraph_pause="medium",
            use_case="Business presentations, corporate content, training"
        ),
        
        "educational": SpeechPreset(
            name="Educational",
            description="Clear, engaging speech for educational content and tutorials",
            voice_preference="b545c585f631496c914815291da4e893",  # New default female voice
            speech_speed=0.85,
            temperature=0.6,
            top_p=0.7,
            paragraph_pause="medium",
            use_case="Educational content, tutorials, e-learning"
        ),
        
        "podcast": SpeechPreset(
            name="Podcast",
            description="Conversational, natural speech for podcast content",
            voice_preference="b545c585f631496c914815291da4e893",  # New default female voice
            speech_speed=0.9,
            temperature=0.6,
            top_p=0.8,
            paragraph_pause="short",
            use_case="Podcasts, conversational content, interviews"
        ),
        
        "news": SpeechPreset(
            name="News",
            description="Professional, authoritative speech for news and announcements",
            voice_preference="802e3bc2b27e49c2995d23ef70e6ac89",  # Energetic Male
            speech_speed=0.95,
            temperature=0.4,
            top_p=0.6,
            paragraph_pause="short",
            use_case="News broadcasts, announcements, formal content"
        ),
        
        "storytelling": SpeechPreset(
            name="Storytelling",
            description="Expressive, engaging speech for stories and creative content",
            voice_preference="b545c585f631496c914815291da4e893",  # New default female voice
            speech_speed=0.85,
            temperature=0.7,
            top_p=0.8,
            paragraph_pause="medium",
            use_case="Stories, creative writing, children's content"
        ),
        
        "meditation": SpeechPreset(
            name="Meditation",
            description="Calm, soothing speech for meditation and relaxation content",
            voice_preference="b545c585f631496c914815291da4e893",  # New default female voice
            speech_speed=0.75,
            temperature=0.5,
            top_p=0.6,
            paragraph_pause="long",
            use_case="Meditation guides, relaxation, mindfulness content"
        ),
        
        "technical": SpeechPreset(
            name="Technical",
            description="Clear, precise speech for technical documentation and manuals",
            voice_preference="speech-1.6",  # AI model for consistency
            speech_speed=0.85,
            temperature=0.4,
            top_p=0.6,
            paragraph_pause="medium",
            use_case="Technical documentation, manuals, specifications"
        ),
        
        "conversational": SpeechPreset(
            name="Conversational",
            description="Natural, casual speech for everyday content",
            voice_preference="b545c585f631496c914815291da4e893",  # New default female voice
            speech_speed=0.9,
            temperature=0.7,
            top_p=0.7,
            paragraph_pause="short",
            use_case="Casual content, blogs, personal messages"
        ),
        
        "dramatic": SpeechPreset(
            name="Dramatic",
            description="Expressive, theatrical speech for dramatic content",
            voice_preference="b545c585f631496c914815291da4e893",  # New default female voice
            speech_speed=0.8,
            temperature=0.8,
            top_p=0.8,
            paragraph_pause="medium",
            use_case="Dramatic readings, theater, emotional content"
        )
    }
    
    @classmethod
    def get_preset(cls, preset_name: str) -> SpeechPreset:
        """Get a speech preset by name."""
        if preset_name not in cls.PRESETS:
            available = list(cls.PRESETS.keys())
            raise ValueError(f"Unknown speech preset '{preset_name}'. Available: {', '.join(available)}")
        return cls.PRESETS[preset_name]
    
    @classmethod
    def get_all_presets(cls) -> Dict[str, SpeechPreset]:
        """Get all available speech presets."""
        return cls.PRESETS.copy()
    
    @classmethod
    def get_preset_names(cls) -> List[str]:
        """Get list of all preset names."""
        return list(cls.PRESETS.keys())
    
    @classmethod
    def get_preset_choices(cls) -> List[str]:
        """Get list of preset names for CLI choices."""
        return sorted(cls.PRESETS.keys())
    
    @classmethod
    def describe_preset(cls, preset_name: str) -> str:
        """Get a detailed description of a preset."""
        preset = cls.get_preset(preset_name)
        return f"{preset.name}: {preset.description} (Use case: {preset.use_case})"
    
    @classmethod
    def list_all_presets(cls) -> str:
        """Get a formatted list of all presets with descriptions."""
        lines = ["Available Speech Types:"]
        for name, preset in sorted(cls.PRESETS.items()):
            lines.append(f"  • {name}: {preset.description}")
            lines.append(f"    Use case: {preset.use_case}")
            lines.append(f"    Parameters: speed={preset.speech_speed}, temp={preset.temperature}, top_p={preset.top_p}")
            lines.append("")
        return "\n".join(lines) 