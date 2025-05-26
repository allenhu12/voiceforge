"""
VoiceForge Input Handler

Handles reading and validating text files for TTS conversion.
Provides character counting and input validation functionality.
"""

import os
from pathlib import Path
from typing import List, Tuple, Optional
import chardet

from ..utils.exceptions import FileError
from ..utils.logger import get_logger


class InputHandler:
    """
    Handles input file operations for VoiceForge.
    
    Provides functionality for reading text files, validating content,
    and preparing text for TTS conversion.
    """
    
    SUPPORTED_EXTENSIONS = {'.txt'}
    MAX_FILE_SIZE_MB = 10  # Maximum file size in MB
    
    def __init__(self):
        """Initialize the input handler."""
        self.logger = get_logger(__name__)
    
    def read_text_file(self, file_path: Path) -> str:
        """
        Read text content from a file.
        
        Args:
            file_path (Path): Path to the text file
            
        Returns:
            str: Text content of the file
            
        Raises:
            FileError: If file cannot be read or is invalid
        """
        file_path = Path(file_path)
        
        # Validate file exists
        if not file_path.exists():
            raise FileError(str(file_path), "read", "File does not exist")
        
        # Validate file extension
        if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise FileError(
                str(file_path), 
                "read", 
                f"Unsupported file type. Supported: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )
        
        # Check file size
        file_size_mb = file_path.stat().st_size / (1024 * 1024)
        if file_size_mb > self.MAX_FILE_SIZE_MB:
            raise FileError(
                str(file_path),
                "read",
                f"File too large ({file_size_mb:.1f}MB). Maximum size: {self.MAX_FILE_SIZE_MB}MB"
            )
        
        try:
            # Try to read with UTF-8 first
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # If UTF-8 fails, detect encoding
                self.logger.debug(f"UTF-8 failed for {file_path}, detecting encoding...")
                encoding = self._detect_encoding(file_path)
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
            
            # Validate content
            if not content.strip():
                raise FileError(str(file_path), "read", "File is empty or contains only whitespace")
            
            self.logger.info(f"Successfully read file: {file_path} ({len(content)} characters)")
            return content
            
        except Exception as e:
            if isinstance(e, FileError):
                raise
            raise FileError(str(file_path), "read", f"Failed to read file: {str(e)}")
    
    def _detect_encoding(self, file_path: Path) -> str:
        """
        Detect file encoding using chardet.
        
        Args:
            file_path (Path): Path to the file
            
        Returns:
            str: Detected encoding
        """
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            
            result = chardet.detect(raw_data)
            encoding = result.get('encoding', 'utf-8')
            confidence = result.get('confidence', 0)
            
            self.logger.debug(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")
            
            # Fallback to utf-8 if confidence is too low
            if confidence < 0.7:
                self.logger.warning(f"Low confidence in encoding detection, using UTF-8")
                encoding = 'utf-8'
            
            return encoding
            
        except Exception as e:
            self.logger.warning(f"Encoding detection failed: {e}, using UTF-8")
            return 'utf-8'
    
    def validate_file(self, file_path: Path) -> Tuple[bool, str]:
        """
        Validate a file without reading its content.
        
        Args:
            file_path (Path): Path to the file
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        try:
            file_path = Path(file_path)
            
            # Check if file exists
            if not file_path.exists():
                return False, "File does not exist"
            
            # Check if it's a file (not directory)
            if not file_path.is_file():
                return False, "Path is not a file"
            
            # Check file extension
            if file_path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                return False, f"Unsupported file type. Supported: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            
            # Check file size
            file_size_mb = file_path.stat().st_size / (1024 * 1024)
            if file_size_mb > self.MAX_FILE_SIZE_MB:
                return False, f"File too large ({file_size_mb:.1f}MB). Maximum: {self.MAX_FILE_SIZE_MB}MB"
            
            # Check if file is readable
            if not os.access(file_path, os.R_OK):
                return False, "File is not readable"
            
            return True, ""
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def count_characters(self, text: str) -> dict:
        """
        Count various character metrics for the text.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Character count metrics
        """
        return {
            'total_characters': len(text),
            'characters_no_spaces': len(text.replace(' ', '')),
            'words': len(text.split()),
            'lines': len(text.splitlines()),
            'paragraphs': len([p for p in text.split('\n\n') if p.strip()])
        }
    
    def prepare_text_for_tts(self, text: str, max_length: Optional[int] = None) -> List[str]:
        """
        Prepare text for TTS conversion by splitting into chunks if needed.
        
        Args:
            text (str): Input text
            max_length (Optional[int]): Maximum length per chunk
            
        Returns:
            List[str]: List of text chunks ready for TTS
        """
        # Clean up the text
        cleaned_text = self._clean_text(text)
        
        # If no max length specified or text is short enough, return as single chunk
        if not max_length or len(cleaned_text) <= max_length:
            return [cleaned_text]
        
        # Split into chunks
        chunks = self._split_text_intelligently(cleaned_text, max_length)
        
        self.logger.info(f"Split text into {len(chunks)} chunks for TTS processing")
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """
        Clean text for TTS processing.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Cleaned text
        """
        # Remove excessive whitespace
        cleaned = ' '.join(text.split())
        
        # Remove or replace problematic characters
        # (This can be expanded based on TTS provider requirements)
        replacements = {
            '"': '"',  # Smart quotes
            '"': '"',
            ''': "'",
            ''': "'",
            '…': '...',
            '–': '-',
            '—': '-',
        }
        
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        
        return cleaned
    
    def _split_text_intelligently(self, text: str, max_length: int) -> List[str]:
        """
        Split text into chunks at natural boundaries.
        
        Args:
            text (str): Text to split
            max_length (int): Maximum length per chunk
            
        Returns:
            List[str]: List of text chunks
        """
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by sentences first
        sentences = self._split_into_sentences(text)
        
        for sentence in sentences:
            # If adding this sentence would exceed max_length
            if len(current_chunk) + len(sentence) > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                
                # If single sentence is too long, split it further
                if len(sentence) > max_length:
                    sentence_chunks = self._split_long_sentence(sentence, max_length)
                    chunks.extend(sentence_chunks[:-1])
                    current_chunk = sentence_chunks[-1]
                else:
                    current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text (str): Input text
            
        Returns:
            List[str]: List of sentences
        """
        # Simple sentence splitting (can be improved with NLTK if needed)
        import re
        
        # Split on sentence endings, but be careful with abbreviations
        sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')
        sentences = sentence_endings.split(text)
        
        return [s.strip() for s in sentences if s.strip()]
    
    def _split_long_sentence(self, sentence: str, max_length: int) -> List[str]:
        """
        Split a long sentence into smaller chunks.
        
        Args:
            sentence (str): Long sentence to split
            max_length (int): Maximum length per chunk
            
        Returns:
            List[str]: List of sentence chunks
        """
        if len(sentence) <= max_length:
            return [sentence]
        
        chunks = []
        words = sentence.split()
        current_chunk = ""
        
        for word in words:
            if len(current_chunk) + len(word) + 1 > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = word
                else:
                    # Single word is too long, split it
                    chunks.append(word[:max_length])
                    current_chunk = word[max_length:]
            else:
                current_chunk += " " + word if current_chunk else word
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def get_file_info(self, file_path: Path) -> dict:
        """
        Get comprehensive information about a file.
        
        Args:
            file_path (Path): Path to the file
            
        Returns:
            dict: File information
        """
        try:
            file_path = Path(file_path)
            stat = file_path.stat()
            
            info = {
                'path': str(file_path),
                'name': file_path.name,
                'size_bytes': stat.st_size,
                'size_mb': stat.st_size / (1024 * 1024),
                'modified': stat.st_mtime,
                'extension': file_path.suffix.lower(),
                'is_valid': False,
                'error': None
            }
            
            # Add validation info
            is_valid, error = self.validate_file(file_path)
            info['is_valid'] = is_valid
            info['error'] = error
            
            # If valid, add character count
            if is_valid:
                try:
                    content = self.read_text_file(file_path)
                    info['character_count'] = self.count_characters(content)
                except Exception as e:
                    info['error'] = f"Failed to read content: {str(e)}"
                    info['is_valid'] = False
            
            return info
            
        except Exception as e:
            return {
                'path': str(file_path),
                'error': f"Failed to get file info: {str(e)}",
                'is_valid': False
            } 