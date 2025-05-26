"""
Fish Audio TTS Client

Implementation of TTSServiceInterface for Fish Audio TTS service.
Handles Fish Audio API communication, authentication, and audio generation.
"""

import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import httpx
import ormsgpack
from pydantic import BaseModel

from ..interfaces.tts_service_interface import TTSServiceInterface
from ..utils.exceptions import AuthenticationError, NetworkError, TTSServiceError
from ..utils.logger import get_logger, log_api_request


class ServeTTSRequest(BaseModel):
    """Fish Audio TTS request model."""
    text: str
    format: str = "mp3"
    mp3_bitrate: int = 128
    model: str = "speech-1.6"


class FishTTSClient(TTSServiceInterface):
    """
    Fish Audio TTS service client.
    
    Implements the TTSServiceInterface for Fish Audio's TTS API.
    Uses msgpack for request serialization and supports various voices/models.
    """
    
    BASE_URL = "https://api.fish.audio"
    TTS_ENDPOINT = "/v1/tts"
    MODELS_ENDPOINT = "/model"
    
    # Estimated pricing (characters per dollar) - update based on actual Fish Audio pricing
    ESTIMATED_COST_PER_1K_CHARS = 0.015  # $0.015 per 1000 characters
    
    DEFAULT_MODELS = [
        "speech-1.6",
        "speech-1.4", 
        "speech-1.2"
    ]
    
    def __init__(self):
        """Initialize the Fish Audio TTS client."""
        self.logger = get_logger(__name__)
        self._client = None
        self._models_cache = None
        self._cache_timestamp = None
        self._cache_duration = 3600  # Cache for 1 hour
    
    def get_name(self) -> str:
        """Get the name of the TTS service provider."""
        return "Fish Audio"
    
    def get_available_voices(self, api_key: str, limit: int = 20) -> Dict[str, Any]:
        """
        Retrieve available voices/models from Fish Audio.
        
        Args:
            api_key (str): The API key for authentication
            
        Returns:
            Dict[str, Any]: Dictionary containing available voices/models
        """
        try:
            # Check cache first
            if self._is_cache_valid():
                self.logger.debug("Using cached models")
                return self._models_cache
            
            client = self._get_client(api_key)
            
            log_api_request(self.logger, "Fish Audio", self.MODELS_ENDPOINT, "GET")
            
            # Add pagination parameters to get more voices
            params = {
                "page_size": min(limit, 100),  # Fish Audio max is 100 per page
                "page_number": 1
            }
            
            response = client.get(
                f"{self.BASE_URL}{self.MODELS_ENDPOINT}",
                params=params,
                timeout=30.0
            )
            
            if response.status_code == 401:
                raise AuthenticationError("Fish Audio", "Invalid API key")
            elif response.status_code != 200:
                raise NetworkError(f"Fish Audio API error", response.status_code)
            
            models_data = response.json()
            
            # Process and cache the models
            processed_models = self._process_models_response(models_data, limit)
            self._models_cache = processed_models
            self._cache_timestamp = time.time()
            
            self.logger.info(f"Retrieved {len(processed_models.get('models', []))} models from Fish Audio")
            return processed_models
            
        except (AuthenticationError, NetworkError):
            raise
        except Exception as e:
            self.logger.error(f"Failed to get Fish Audio models: {e}")
            # Return default models as fallback
            return self._get_default_models()
    
    def _is_cache_valid(self) -> bool:
        """Check if the models cache is still valid."""
        if not self._models_cache or not self._cache_timestamp:
            return False
        return (time.time() - self._cache_timestamp) < self._cache_duration
    
    def _process_models_response(self, models_data: Dict, limit: int = 20) -> Dict[str, Any]:
        """Process the models response from Fish Audio API."""
        processed = {
            "provider": "Fish Audio",
            "models": [],
            "default_model": "speech-1.6",
            "total_available": 0
        }
        
        # Handle Fish Audio API response format
        if isinstance(models_data, dict):
            # Get total count
            processed["total_available"] = models_data.get("total", 0)
            
            # Process items (voice models)
            items = models_data.get("items", [])
            
            # Add default AI models first
            processed["models"].extend([
                {
                    "id": "speech-1.6",
                    "name": "Speech 1.6 (AI)",
                    "description": "Latest Fish Audio AI speech model",
                    "languages": ["en", "zh", "ja", "ko", "fr", "de", "es", "ar"],
                    "type": "ai",
                    "author": "Fish Audio"
                },
                {
                    "id": "speech-1.5", 
                    "name": "Speech 1.5 (AI)",
                    "description": "Previous generation AI speech model",
                    "languages": ["en", "zh", "ja"],
                    "type": "ai",
                    "author": "Fish Audio"
                }
            ])
            
            # Add human voice models
            for item in items[:limit]:  # Limit based on parameter
                if isinstance(item, dict) and item.get("type") == "tts":
                    # Get sample audio info if available
                    samples = item.get("samples", [])
                    sample_text = ""
                    if samples and len(samples) > 0:
                        sample_text = samples[0].get("text", "")[:100] + "..." if len(samples[0].get("text", "")) > 100 else samples[0].get("text", "")
                    
                    processed["models"].append({
                        "id": item.get("_id", "unknown"),
                        "name": item.get("title", "Unknown Voice"),
                        "description": item.get("description", sample_text),
                        "languages": item.get("languages", ["en"]),
                        "type": "human",
                        "author": item.get("author", {}).get("nickname", "Unknown"),
                        "like_count": item.get("like_count", 0),
                        "task_count": item.get("task_count", 0),
                        "tags": item.get("tags", [])
                    })
        
        # Fallback if no items found
        if not processed["models"]:
            processed = self._get_default_models()
        
        return processed
    
    def _get_default_models(self) -> Dict[str, Any]:
        """Get default models when API is unavailable."""
        return {
            "provider": "Fish Audio",
            "models": [
                {
                    "id": "speech-1.6",
                    "name": "Speech 1.6",
                    "description": "Latest Fish Audio speech model",
                    "languages": ["en", "zh", "ja", "ko", "fr", "de", "es", "ar"]
                },
                {
                    "id": "speech-1.4", 
                    "name": "Speech 1.4",
                    "description": "Previous generation speech model",
                    "languages": ["en", "zh", "ja"]
                }
            ],
            "default_model": "speech-1.6"
        }
    
    def estimate_cost(
        self, 
        text: str, 
        voice_or_model: str, 
        settings: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Estimate the cost for converting text to speech.
        
        Args:
            text (str): The text to be converted
            voice_or_model (str): The voice or model to use
            settings (Optional[Dict[str, Any]]): Additional settings
            
        Returns:
            Optional[str]: Formatted cost estimate string
        """
        try:
            char_count = len(text)
            
            # Calculate cost based on character count
            cost_per_char = self.ESTIMATED_COST_PER_1K_CHARS / 1000
            estimated_cost = char_count * cost_per_char
            
            # Format the cost estimate
            if estimated_cost < 0.01:
                return f"~$0.01 ({char_count:,} chars)"
            else:
                return f"~${estimated_cost:.3f} ({char_count:,} chars)"
                
        except Exception as e:
            self.logger.warning(f"Failed to estimate cost: {e}")
            return None
    
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
        Convert text to speech using Fish Audio API.
        
        Args:
            api_key (str): The API key for authentication
            text (str): The text to convert to speech
            output_file_path (Path): Path where the MP3 file should be saved
            voice_or_model (str): The voice or model to use
            mp3_bitrate (int): MP3 bitrate (default: 128)
            extra_settings (Optional[Dict[str, Any]]): Additional settings
            
        Returns:
            bool: True if conversion was successful, False otherwise
        """
        try:
            start_time = time.time()
            
            # Use simple JSON request for better performance
            request_data = {
                "text": text,
                "format": "mp3"
            }
            
            # Prepare headers
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Add model/voice handling
            if voice_or_model and voice_or_model not in ["speech-1.6", "speech-1.5"]:
                # Human voice model
                request_data["reference_id"] = voice_or_model
            else:
                # AI model - use header
                headers["model"] = voice_or_model
            
            log_api_request(self.logger, "Fish Audio", self.TTS_ENDPOINT)
            self.logger.debug(f"TTS request: {len(text)} chars, voice: {voice_or_model}")
            
            # Make the API request with a fresh client for better performance
            with httpx.Client() as client:
                response = client.post(
                    f"{self.BASE_URL}{self.TTS_ENDPOINT}",
                    json=request_data,
                    headers=headers,
                    timeout=30.0  # Reduced timeout for faster failure detection
                )
            
            api_time = time.time() - start_time
            self.logger.debug(f"API response time: {api_time:.2f}s")
            
            # Handle response
            if response.status_code == 401:
                raise AuthenticationError("Fish Audio", "Invalid API key")
            elif response.status_code == 400:
                raise TTSServiceError("Fish Audio", "Bad request - check text and model parameters")
            elif response.status_code == 429:
                raise TTSServiceError("Fish Audio", "Rate limit exceeded - please wait and try again")
            elif response.status_code != 200:
                raise NetworkError(f"Fish Audio API error", response.status_code)
            
            # Save the audio data
            audio_data = response.content
            if not audio_data:
                raise TTSServiceError("Fish Audio", "Received empty audio data")
            
            self.logger.debug(f"Received {len(audio_data)} bytes of audio data")
            
            # Write to file
            write_start = time.time()
            output_file_path = Path(output_file_path)
            output_file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file_path, 'wb') as f:
                f.write(audio_data)
            
            write_time = time.time() - write_start
            total_time = time.time() - start_time
            
            # Verify file was written
            if not output_file_path.exists() or output_file_path.stat().st_size == 0:
                raise TTSServiceError("Fish Audio", "Failed to save audio file")
            
            self.logger.info(
                f"TTS conversion successful: {len(text)} chars → {len(audio_data)} bytes → {output_file_path}"
            )
            self.logger.debug(f"Total time: {total_time:.2f}s (API: {api_time:.2f}s, Write: {write_time:.3f}s)")
            return True
            
        except (AuthenticationError, NetworkError, TTSServiceError):
            raise
        except Exception as e:
            self.logger.error(f"Fish Audio TTS conversion failed: {e}")
            raise TTSServiceError("Fish Audio", f"Conversion failed: {str(e)}")
    
    def get_required_config_fields(self) -> List[str]:
        """Get the list of required configuration fields."""
        return ["api_key"]
    
    def validate_api_key(self, api_key: str) -> bool:
        """
        Validate the Fish Audio API key.
        
        Args:
            api_key (str): The API key to validate
            
        Returns:
            bool: True if API key is valid, False otherwise
        """
        try:
            if not api_key or not api_key.strip():
                return False
            
            client = self._get_client(api_key)
            
            # Try to get models as a validation check
            response = client.get(
                f"{self.BASE_URL}{self.MODELS_ENDPOINT}",
                timeout=10.0
            )
            
            return response.status_code == 200
            
        except Exception as e:
            self.logger.debug(f"API key validation failed: {e}")
            return False
    
    def get_default_voice(self) -> str:
        """Get the default voice/model for Fish Audio."""
        return "speech-1.6"
    
    def get_character_limit(self) -> Optional[int]:
        """Get the character limit for Fish Audio (if any)."""
        # Fish Audio doesn't specify a hard limit, but we'll set a reasonable one
        return 10000  # 10k characters per request
    
    def _get_client(self, api_key: str) -> httpx.Client:
        """
        Get or create an HTTP client with proper configuration.
        
        Args:
            api_key (str): API key for authentication
            
        Returns:
            httpx.Client: Configured HTTP client
        """
        if not self._client:
            self._client = httpx.Client(
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "User-Agent": "VoiceForge/1.0.0"
                },
                timeout=30.0
            )
        else:
            # Update authorization header
            self._client.headers["Authorization"] = f"Bearer {api_key}"
        
        return self._client
    
    def __del__(self):
        """Clean up HTTP client on destruction."""
        if self._client:
            try:
                self._client.close()
            except Exception:
                pass 