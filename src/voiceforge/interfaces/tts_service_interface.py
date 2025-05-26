"""
TTS Service Interface

Abstract base class defining the contract for all TTS service providers.
This interface ensures consistent behavior across different TTS services.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pathlib import Path


class TTSServiceInterface(ABC):
    """
    Abstract base class for TTS service providers.
    
    All TTS service implementations must inherit from this class and implement
    all abstract methods to ensure consistent behavior across providers.
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the TTS service provider.
        
        Returns:
            str: The name of the TTS service (e.g., "Fish Audio", "OpenAI TTS")
        """
        pass

    @abstractmethod
    def get_available_voices(self, api_key: str) -> Dict[str, Any]:
        """
        Retrieve available voices/models from the TTS service.
        
        Args:
            api_key (str): The API key for authentication
            
        Returns:
            Dict[str, Any]: Dictionary containing available voices/models
            
        Raises:
            AuthenticationError: If API key is invalid
            NetworkError: If unable to connect to the service
        """
        pass

    @abstractmethod
    def estimate_cost(
        self, 
        text: str, 
        voice_or_model: str, 
        settings: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Estimate the cost for converting the given text to speech.
        
        Args:
            text (str): The text to be converted
            voice_or_model (str): The voice or model to use
            settings (Optional[Dict[str, Any]]): Additional settings
            
        Returns:
            Optional[str]: Formatted cost estimate string, or None if not available
        """
        pass

    @abstractmethod
    def text_to_speech(
        self,
        api_key: str,
        text: str,
        output_file_path: Path,
        voice_or_model: str,
        mp3_bitrate: int = 128,
        extra_settings: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Convert text to speech and save as MP3 file.
        
        Args:
            api_key (str): The API key for authentication
            text (str): The text to convert to speech
            output_file_path (Path): Path where the MP3 file should be saved
            voice_or_model (str): The voice or model to use
            mp3_bitrate (int): MP3 bitrate (default: 128)
            extra_settings (Optional[Dict[str, Any]]): Additional provider-specific settings
            
        Returns:
            bool: True if conversion was successful, False otherwise
            
        Raises:
            AuthenticationError: If API key is invalid
            NetworkError: If unable to connect to the service
            FileError: If unable to write output file
        """
        pass

    @abstractmethod
    def get_required_config_fields(self) -> List[str]:
        """
        Get the list of required configuration fields for this provider.
        
        Returns:
            List[str]: List of required configuration field names
        """
        pass

    @abstractmethod
    def validate_api_key(self, api_key: str) -> bool:
        """
        Validate the provided API key.
        
        Args:
            api_key (str): The API key to validate
            
        Returns:
            bool: True if API key is valid, False otherwise
        """
        pass

    def get_default_settings(self) -> Dict[str, Any]:
        """
        Get default settings for this TTS provider.
        
        Returns:
            Dict[str, Any]: Default settings dictionary
        """
        return {
            "mp3_bitrate": 128,
            "voice": self.get_default_voice(),
        }

    @abstractmethod
    def get_default_voice(self) -> str:
        """
        Get the default voice/model for this provider.
        
        Returns:
            str: Default voice/model identifier
        """
        pass

    def get_supported_formats(self) -> List[str]:
        """
        Get list of supported output formats.
        
        Returns:
            List[str]: List of supported formats (default: ["mp3"])
        """
        return ["mp3"]

    def get_character_limit(self) -> Optional[int]:
        """
        Get the character limit for a single request.
        
        Returns:
            Optional[int]: Character limit, or None if no limit
        """
        return None 