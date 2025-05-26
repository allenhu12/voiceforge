"""
VoiceForge Output Handler

Handles saving MP3 files and managing output directories.
Provides file naming, versioning, and output validation functionality.
"""

import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from ..utils.exceptions import FileError
from ..utils.logger import get_logger, log_file_operation


class OutputHandler:
    """
    Handles output file operations for VoiceForge.
    
    Provides functionality for saving MP3 files, managing output directories,
    and handling file naming conventions.
    """
    
    def __init__(self, default_output_dir: Optional[Path] = None):
        """
        Initialize the output handler.
        
        Args:
            default_output_dir (Optional[Path]): Default output directory
        """
        self.logger = get_logger(__name__)
        self.default_output_dir = default_output_dir or Path("./voiceforge_output")
    
    def save_audio_file(
        self,
        audio_data: bytes,
        output_path: Path,
        overwrite: bool = False
    ) -> Path:
        """
        Save audio data to an MP3 file.
        
        Args:
            audio_data (bytes): Audio data to save
            output_path (Path): Desired output file path
            overwrite (bool): Whether to overwrite existing files
            
        Returns:
            Path: Actual path where file was saved
            
        Raises:
            FileError: If file cannot be saved
        """
        output_path = Path(output_path)
        
        # Ensure output directory exists
        self.ensure_directory_exists(output_path.parent)
        
        # Handle file naming if file already exists
        final_path = self._resolve_output_path(output_path, overwrite)
        
        try:
            # Write audio data to file
            with open(final_path, 'wb') as f:
                f.write(audio_data)
            
            # Verify file was written correctly
            if not final_path.exists() or final_path.stat().st_size == 0:
                raise FileError(str(final_path), "write", "File was not written correctly")
            
            log_file_operation(self.logger, "write", final_path, True)
            self.logger.info(f"Audio saved successfully: {final_path} ({len(audio_data)} bytes)")
            
            return final_path
            
        except Exception as e:
            log_file_operation(self.logger, "write", final_path, False)
            if isinstance(e, FileError):
                raise
            raise FileError(str(final_path), "write", f"Failed to save audio file: {str(e)}")
    
    def _resolve_output_path(self, desired_path: Path, overwrite: bool) -> Path:
        """
        Resolve the actual output path, handling existing files.
        
        Args:
            desired_path (Path): Desired output path
            overwrite (bool): Whether to overwrite existing files
            
        Returns:
            Path: Resolved output path
        """
        if not desired_path.exists() or overwrite:
            return desired_path
        
        # Generate a unique filename
        base_path = desired_path.parent
        stem = desired_path.stem
        suffix = desired_path.suffix
        
        counter = 1
        while True:
            new_path = base_path / f"{stem}_{counter}{suffix}"
            if not new_path.exists():
                self.logger.info(f"File exists, using: {new_path}")
                return new_path
            counter += 1
            
            # Prevent infinite loop
            if counter > 1000:
                raise FileError(
                    str(desired_path),
                    "write",
                    "Too many existing files with similar names"
                )
    
    def ensure_directory_exists(self, directory: Path) -> None:
        """
        Ensure a directory exists, creating it if necessary.
        
        Args:
            directory (Path): Directory path to ensure exists
            
        Raises:
            FileError: If directory cannot be created
        """
        try:
            directory = Path(directory)
            directory.mkdir(parents=True, exist_ok=True)
            
            # Verify directory is writable
            if not os.access(directory, os.W_OK):
                raise FileError(
                    str(directory),
                    "create",
                    "Directory is not writable"
                )
                
        except Exception as e:
            if isinstance(e, FileError):
                raise
            raise FileError(
                str(directory),
                "create",
                f"Failed to create directory: {str(e)}"
            )
    
    def generate_output_filename(
        self,
        input_filename: str,
        provider: str = None,
        voice: str = None,
        timestamp: bool = False
    ) -> str:
        """
        Generate an output filename based on input and options.
        
        Args:
            input_filename (str): Original input filename
            provider (str): TTS provider name (optional)
            voice (str): Voice/model name (optional)
            timestamp (bool): Whether to include timestamp
            
        Returns:
            str: Generated output filename
        """
        # Remove extension from input filename
        base_name = Path(input_filename).stem
        
        # Build filename components
        components = [base_name]
        
        if provider:
            components.append(provider)
        
        if voice:
            # Clean voice name for filename
            clean_voice = self._clean_filename_component(voice)
            components.append(clean_voice)
        
        if timestamp:
            timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
            components.append(timestamp_str)
        
        # Join components and add .mp3 extension
        filename = "_".join(components) + ".mp3"
        
        # Ensure filename is valid for the filesystem
        return self._sanitize_filename(filename)
    
    def _clean_filename_component(self, component: str) -> str:
        """
        Clean a component for use in filenames.
        
        Args:
            component (str): Component to clean
            
        Returns:
            str: Cleaned component
        """
        # Remove or replace problematic characters
        cleaned = component.replace(" ", "_")
        cleaned = "".join(c for c in cleaned if c.isalnum() or c in "._-")
        return cleaned[:50]  # Limit length
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        Sanitize filename for cross-platform compatibility.
        
        Args:
            filename (str): Filename to sanitize
            
        Returns:
            str: Sanitized filename
        """
        # Characters not allowed in filenames on various systems
        invalid_chars = '<>:"/\\|?*'
        
        for char in invalid_chars:
            filename = filename.replace(char, "_")
        
        # Remove leading/trailing dots and spaces
        filename = filename.strip(". ")
        
        # Ensure filename is not empty
        if not filename:
            filename = "output.mp3"
        
        # Limit total filename length
        if len(filename) > 255:
            name_part = filename[:-4]  # Remove .mp3
            filename = name_part[:251] + ".mp3"  # Keep .mp3 extension
        
        return filename
    
    def get_output_path(
        self,
        input_file: Path,
        output_dir: Optional[Path] = None,
        custom_filename: Optional[str] = None,
        provider: str = None,
        voice: str = None
    ) -> Path:
        """
        Get the full output path for a conversion.
        
        Args:
            input_file (Path): Input file path
            output_dir (Optional[Path]): Output directory (uses default if None)
            custom_filename (Optional[str]): Custom filename (generates if None)
            provider (str): TTS provider name
            voice (str): Voice/model name
            
        Returns:
            Path: Full output path
        """
        # Use provided output directory or default
        if output_dir:
            output_directory = Path(output_dir)
        else:
            output_directory = self.default_output_dir
        
        # Generate filename if not provided
        if custom_filename:
            filename = custom_filename
            if not filename.endswith('.mp3'):
                filename += '.mp3'
            filename = self._sanitize_filename(filename)
        else:
            filename = self.generate_output_filename(
                input_file.name,
                provider=provider,
                voice=voice
            )
        
        return output_directory / filename
    
    def create_output_summary(
        self,
        output_files: list,
        total_duration: float = None,
        total_cost: str = None
    ) -> Dict[str, Any]:
        """
        Create a summary of output operations.
        
        Args:
            output_files (list): List of output file paths
            total_duration (float): Total processing duration in seconds
            total_cost (str): Total estimated cost
            
        Returns:
            Dict[str, Any]: Output summary
        """
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_files': len(output_files),
            'output_files': [],
            'total_size_bytes': 0,
            'total_duration_seconds': total_duration,
            'total_cost': total_cost
        }
        
        for file_path in output_files:
            file_path = Path(file_path)
            if file_path.exists():
                file_info = {
                    'path': str(file_path),
                    'name': file_path.name,
                    'size_bytes': file_path.stat().st_size,
                    'size_mb': file_path.stat().st_size / (1024 * 1024)
                }
                summary['output_files'].append(file_info)
                summary['total_size_bytes'] += file_info['size_bytes']
        
        summary['total_size_mb'] = summary['total_size_bytes'] / (1024 * 1024)
        
        return summary
    
    def open_output_directory(self, directory: Path) -> bool:
        """
        Open the output directory in the system file manager.
        
        Args:
            directory (Path): Directory to open
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            directory = Path(directory)
            if not directory.exists():
                self.logger.warning(f"Directory does not exist: {directory}")
                return False
            
            import subprocess
            import sys
            
            if sys.platform == "win32":
                os.startfile(directory)
            elif sys.platform == "darwin":
                subprocess.run(["open", directory])
            else:  # Linux and other Unix-like systems
                subprocess.run(["xdg-open", directory])
            
            self.logger.info(f"Opened directory: {directory}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to open directory {directory}: {e}")
            return False
    
    def cleanup_temp_files(self, temp_dir: Path) -> None:
        """
        Clean up temporary files and directories.
        
        Args:
            temp_dir (Path): Temporary directory to clean up
        """
        try:
            if temp_dir.exists() and temp_dir.is_dir():
                shutil.rmtree(temp_dir)
                self.logger.debug(f"Cleaned up temporary directory: {temp_dir}")
        except Exception as e:
            self.logger.warning(f"Failed to clean up temporary directory {temp_dir}: {e}")
    
    def validate_output_directory(self, directory: Path) -> tuple[bool, str]:
        """
        Validate that an output directory is suitable for use.
        
        Args:
            directory (Path): Directory to validate
            
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        try:
            directory = Path(directory)
            
            # Check if directory exists or can be created
            if not directory.exists():
                try:
                    directory.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    return False, f"Cannot create directory: {str(e)}"
            
            # Check if it's actually a directory
            if not directory.is_dir():
                return False, "Path is not a directory"
            
            # Check if directory is writable
            if not os.access(directory, os.W_OK):
                return False, "Directory is not writable"
            
            # Check available space (basic check)
            try:
                stat = shutil.disk_usage(directory)
                free_space_mb = stat.free / (1024 * 1024)
                if free_space_mb < 10:  # Less than 10MB free
                    return False, f"Insufficient disk space ({free_space_mb:.1f}MB available)"
            except Exception:
                # If we can't check disk space, continue anyway
                pass
            
            return True, ""
            
        except Exception as e:
            return False, f"Validation error: {str(e)}" 