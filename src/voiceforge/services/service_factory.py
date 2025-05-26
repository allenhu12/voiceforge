"""
TTS Service Factory

Factory class for creating TTS service instances based on provider names.
"""

from typing import Dict, Type, List, Optional
from ..interfaces.tts_service_interface import TTSServiceInterface
from ..utils.exceptions import ConfigurationError
from ..utils.logger import get_logger


class TTSServiceFactory:
    """Factory for creating TTS service instances."""
    
    _providers: Dict[str, Type[TTSServiceInterface]] = {}
    _logger = get_logger(__name__)
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[TTSServiceInterface]) -> None:
        """Register a TTS service provider."""
        cls._providers[name] = provider_class
        cls._logger.debug(f"Registered TTS provider: {name}")
    
    @classmethod
    def create_service(cls, provider_name: str) -> TTSServiceInterface:
        """Create a TTS service instance."""
        if provider_name not in cls._providers:
            available = ", ".join(cls._providers.keys())
            raise ConfigurationError(
                provider_name,
                f"Unknown TTS provider '{provider_name}'. Available: {available}"
            )
        
        provider_class = cls._providers[provider_name]
        
        try:
            instance = provider_class()
            cls._logger.debug(f"Created TTS service instance: {provider_name}")
            return instance
        except Exception as e:
            raise ConfigurationError(
                provider_name,
                f"Failed to create TTS service '{provider_name}': {str(e)}"
            )
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get list of available provider names."""
        return list(cls._providers.keys())
    
    @classmethod
    def is_provider_available(cls, provider_name: str) -> bool:
        """Check if a provider is available."""
        return provider_name in cls._providers


# Auto-register Fish Audio provider
def _register_default_providers():
    """Register default TTS providers."""
    try:
        from .fish_tts_client import FishTTSClient
        TTSServiceFactory.register_provider("fish_audio", FishTTSClient)
    except ImportError as e:
        TTSServiceFactory._logger.warning(f"Failed to register Fish Audio provider: {e}")


# Register providers on module import
_register_default_providers() 