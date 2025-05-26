"""
VoiceForge Configuration Manager

Handles application configuration, API keys, and settings management.
Provides secure storage and retrieval of sensitive information.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ..utils.exceptions import ConfigurationError
from ..utils.logger import get_logger


class ConfigManager:
    """
    Manages application configuration and secure API key storage.
    
    Handles loading, saving, and encrypting configuration data including
    API keys for different TTS providers.
    """
    
    DEFAULT_CONFIG = {
        "app_name": "VoiceForge",
        "version": "1.0.0",
        "default_provider": "fish_audio",
        "providers": {},
        "output": {
            "default_directory": "./voiceforge_output",
            "naming_pattern": "{filename}.mp3"
        },
        "ui": {
            "theme": "dark",
            "remember_settings": True
        },
        "logging": {
            "level": "INFO",
            "file_logging": False
        }
    }
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_dir (Optional[Path]): Custom configuration directory
        """
        self.logger = get_logger(__name__)
        
        # Set configuration directory
        if config_dir:
            self.config_dir = Path(config_dir)
        else:
            self.config_dir = self._get_default_config_dir()
        
        self.config_file = self.config_dir / "config.json"
        self.key_file = self.config_dir / ".key"
        
        # Ensure config directory exists
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize encryption
        self._encryption_key = self._get_or_create_encryption_key()
        self._cipher = Fernet(self._encryption_key)
        
        # Load configuration
        self._config = self._load_config()
    
    def _get_default_config_dir(self) -> Path:
        """Get the default configuration directory based on OS."""
        if os.name == 'nt':  # Windows
            config_dir = Path.home() / "AppData" / "Local" / "VoiceForge"
        elif os.name == 'posix':  # macOS/Linux
            if os.uname().sysname == 'Darwin':  # macOS
                config_dir = Path.home() / "Library" / "Application Support" / "VoiceForge"
            else:  # Linux
                config_dir = Path.home() / ".config" / "voiceforge"
        else:
            config_dir = Path.home() / ".voiceforge"
        
        return config_dir
    
    def _get_or_create_encryption_key(self) -> bytes:
        """Get or create encryption key for API key storage."""
        if self.key_file.exists():
            try:
                return self.key_file.read_bytes()
            except Exception as e:
                self.logger.warning(f"Failed to read encryption key: {e}")
        
        # Generate new key
        key = Fernet.generate_key()
        try:
            self.key_file.write_bytes(key)
            # Set restrictive permissions (owner only)
            if os.name != 'nt':  # Not Windows
                os.chmod(self.key_file, 0o600)
        except Exception as e:
            self.logger.warning(f"Failed to save encryption key: {e}")
        
        return key
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if not self.config_file.exists():
            self.logger.info("Creating default configuration")
            return self.DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            merged_config = self.DEFAULT_CONFIG.copy()
            merged_config.update(config)
            
            return merged_config
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def save_config(self) -> bool:
        """
        Save current configuration to file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
            
            self.logger.debug(f"Configuration saved to {self.config_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key (str): Configuration key (supports dot notation, e.g., "output.default_directory")
            default (Any): Default value if key not found
            
        Returns:
            Any: Configuration value
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by key.
        
        Args:
            key (str): Configuration key (supports dot notation)
            value (Any): Value to set
        """
        keys = key.split('.')
        config = self._config
        
        # Navigate to the parent of the target key
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Set the value
        config[keys[-1]] = value
    
    def get_provider_config(self, provider: str) -> Dict[str, Any]:
        """
        Get configuration for a specific TTS provider.
        
        Args:
            provider (str): Provider name
            
        Returns:
            Dict[str, Any]: Provider configuration
        """
        return self._config.get("providers", {}).get(provider, {})
    
    def set_provider_config(self, provider: str, config: Dict[str, Any]) -> None:
        """
        Set configuration for a specific TTS provider.
        
        Args:
            provider (str): Provider name
            config (Dict[str, Any]): Provider configuration
        """
        if "providers" not in self._config:
            self._config["providers"] = {}
        
        self._config["providers"][provider] = config
    
    def get_api_key(self, provider: str) -> Optional[str]:
        """
        Get decrypted API key for a provider.
        
        Args:
            provider (str): Provider name
            
        Returns:
            Optional[str]: Decrypted API key or None if not found
        """
        provider_config = self.get_provider_config(provider)
        encrypted_key = provider_config.get("api_key_encrypted")
        
        if not encrypted_key:
            return None
        
        try:
            # Decrypt the API key
            decrypted_bytes = self._cipher.decrypt(encrypted_key.encode())
            return decrypted_bytes.decode()
        except Exception as e:
            self.logger.error(f"Failed to decrypt API key for {provider}: {e}")
            return None
    
    def set_api_key(self, provider: str, api_key: str) -> bool:
        """
        Set encrypted API key for a provider.
        
        Args:
            provider (str): Provider name
            api_key (str): API key to encrypt and store
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Encrypt the API key
            encrypted_bytes = self._cipher.encrypt(api_key.encode())
            encrypted_key = encrypted_bytes.decode()
            
            # Get or create provider config
            provider_config = self.get_provider_config(provider)
            provider_config["api_key_encrypted"] = encrypted_key
            
            # Update provider config
            self.set_provider_config(provider, provider_config)
            
            self.logger.info(f"API key set for provider: {provider}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to encrypt API key for {provider}: {e}")
            return False
    
    def remove_api_key(self, provider: str) -> bool:
        """
        Remove API key for a provider.
        
        Args:
            provider (str): Provider name
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            provider_config = self.get_provider_config(provider)
            if "api_key_encrypted" in provider_config:
                del provider_config["api_key_encrypted"]
                self.set_provider_config(provider, provider_config)
                self.logger.info(f"API key removed for provider: {provider}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to remove API key for {provider}: {e}")
            return False
    
    def list_providers(self) -> List[str]:
        """
        Get list of configured providers.
        
        Returns:
            List[str]: List of provider names
        """
        return list(self._config.get("providers", {}).keys())
    
    def has_api_key(self, provider: str) -> bool:
        """
        Check if API key exists for a provider.
        
        Args:
            provider (str): Provider name
            
        Returns:
            bool: True if API key exists, False otherwise
        """
        provider_config = self.get_provider_config(provider)
        return "api_key_encrypted" in provider_config
    
    def get_default_provider(self) -> str:
        """
        Get the default TTS provider.
        
        Returns:
            str: Default provider name
        """
        return self._config.get("default_provider", "fish_audio")
    
    def set_default_provider(self, provider: str) -> None:
        """
        Set the default TTS provider.
        
        Args:
            provider (str): Provider name
        """
        self._config["default_provider"] = provider
    
    def get_output_directory(self) -> Path:
        """
        Get the default output directory.
        
        Returns:
            Path: Output directory path
        """
        output_dir = self.get("output.default_directory", "./voiceforge_output")
        return Path(output_dir).expanduser().resolve()
    
    def set_output_directory(self, directory: Path) -> None:
        """
        Set the default output directory.
        
        Args:
            directory (Path): Output directory path
        """
        self.set("output.default_directory", str(directory))
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to defaults (preserving API keys)."""
        # Preserve API keys
        providers = self._config.get("providers", {})
        
        # Reset to defaults
        self._config = self.DEFAULT_CONFIG.copy()
        
        # Restore API keys
        self._config["providers"] = providers 