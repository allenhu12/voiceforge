"""
VoiceForge Custom Exceptions

Custom exception classes for better error handling and user feedback.
"""


class VoiceForgeError(Exception):
    """Base exception class for VoiceForge application."""
    
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class AuthenticationError(VoiceForgeError):
    """Raised when API authentication fails."""
    
    def __init__(self, provider: str, message: str = None):
        self.provider = provider
        if not message:
            message = f"Authentication failed for {provider}"
        super().__init__(message)


class NetworkError(VoiceForgeError):
    """Raised when network operations fail."""
    
    def __init__(self, message: str = "Network operation failed", status_code: int = None):
        self.status_code = status_code
        if status_code:
            message = f"{message} (HTTP {status_code})"
        super().__init__(message)


class FileError(VoiceForgeError):
    """Raised when file operations fail."""
    
    def __init__(self, file_path: str, operation: str, message: str = None):
        self.file_path = file_path
        self.operation = operation
        if not message:
            message = f"Failed to {operation} file: {file_path}"
        super().__init__(message)


class ConfigurationError(VoiceForgeError):
    """Raised when configuration is invalid or missing."""
    
    def __init__(self, config_key: str = None, message: str = None):
        self.config_key = config_key
        if not message:
            if config_key:
                message = f"Invalid or missing configuration: {config_key}"
            else:
                message = "Configuration error"
        super().__init__(message)


class TTSServiceError(VoiceForgeError):
    """Raised when TTS service operations fail."""
    
    def __init__(self, provider: str, message: str, error_code: str = None):
        self.provider = provider
        self.error_code = error_code
        super().__init__(f"{provider}: {message}")


class CostEstimationError(VoiceForgeError):
    """Raised when cost estimation fails."""
    
    def __init__(self, message: str = "Failed to estimate cost"):
        super().__init__(message) 