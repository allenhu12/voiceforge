"""
VoiceForge Logging Utility

Provides centralized logging configuration for the VoiceForge application.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def get_logger(
    name: str = "voiceforge",
    level: str = "INFO",
    log_file: Optional[Path] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Get a configured logger for VoiceForge.
    
    Args:
        name (str): Logger name (default: "voiceforge")
        level (str): Logging level (default: "INFO")
        log_file (Optional[Path]): Path to log file (optional)
        console_output (bool): Whether to output to console (default: True)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger
    
    # Set logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(numeric_level)
    
    # Create formatter
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        try:
            # Ensure log directory exists
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            # If file logging fails, log to console
            logger.warning(f"Failed to set up file logging: {e}")
    
    return logger


def setup_application_logging(
    verbose: bool = False,
    log_dir: Optional[Path] = None
) -> logging.Logger:
    """
    Set up application-wide logging configuration.
    
    Args:
        verbose (bool): Enable verbose (DEBUG) logging
        log_dir (Optional[Path]): Directory for log files
        
    Returns:
        logging.Logger: Main application logger
    """
    level = "DEBUG" if verbose else "INFO"
    
    log_file = None
    if log_dir:
        log_file = log_dir / "voiceforge.log"
    
    return get_logger(
        name="voiceforge",
        level=level,
        log_file=log_file,
        console_output=True
    )


def log_api_request(logger: logging.Logger, provider: str, endpoint: str, method: str = "POST"):
    """
    Log API request information (without sensitive data).
    
    Args:
        logger (logging.Logger): Logger instance
        provider (str): TTS provider name
        endpoint (str): API endpoint (without sensitive parameters)
        method (str): HTTP method (default: "POST")
    """
    logger.debug(f"API Request: {method} {provider} - {endpoint}")


def log_file_operation(logger: logging.Logger, operation: str, file_path: Path, success: bool = True):
    """
    Log file operation information.
    
    Args:
        logger (logging.Logger): Logger instance
        operation (str): Operation type (e.g., "read", "write")
        file_path (Path): File path
        success (bool): Whether operation was successful
    """
    status = "SUCCESS" if success else "FAILED"
    logger.debug(f"File {operation}: {file_path} - {status}")


def log_cost_estimation(logger: logging.Logger, provider: str, characters: int, estimated_cost: str):
    """
    Log cost estimation information.
    
    Args:
        logger (logging.Logger): Logger instance
        provider (str): TTS provider name
        characters (int): Number of characters
        estimated_cost (str): Estimated cost string
    """
    logger.info(f"Cost estimate ({provider}): {characters} chars → {estimated_cost}") 