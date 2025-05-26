"""
VoiceForge - Convert text files to MP3 audio using advanced TTS services.

A cross-platform CLI/GUI application that converts text files to high-quality 
MP3 audio using pluggable Text-to-Speech service providers.
"""

__version__ = "1.0.0"
__app_name__ = "VoiceForge"
__description__ = "Convert text files to MP3 audio using advanced TTS services"
__author__ = "VoiceForge Team"
__license__ = "MIT"
__url__ = "https://github.com/voiceforge/voiceforge"

# Version info tuple for programmatic access
VERSION_INFO = tuple(map(int, __version__.split('.')))

# Export main components will be imported when needed to avoid circular imports

__all__ = [
    "__version__",
    "__app_name__", 
    "__description__",
    "__author__",
    "__license__",
    "__url__",
    "VERSION_INFO",
] 