#!/usr/bin/env python3
"""
VoiceForge Standalone Entry Point

This is the main entry point for the standalone VoiceForge executable.
It avoids relative import issues that can occur with PyInstaller.
"""

import sys
import os
from pathlib import Path

# Add the source directory to Python path
if getattr(sys, 'frozen', False):
    # Running as compiled executable - PyInstaller extracts to _MEIPASS
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller temporary directory
        application_path = Path(sys._MEIPASS)
    else:
        application_path = Path(sys.executable).parent
else:
    # Running as script
    application_path = Path(__file__).parent

# Add src directory to path for imports
src_path = application_path / "src"
if src_path.exists():
    sys.path.insert(0, str(src_path))
else:
    # Fallback: try to find voiceforge module in current directory structure
    current_dir = Path(__file__).parent
    possible_paths = [
        current_dir / "src",
        current_dir,
        current_dir.parent / "src"
    ]
    
    for path in possible_paths:
        if (path / "voiceforge").exists():
            sys.path.insert(0, str(path))
            break

# Now import and run the main CLI
try:
    # Import all necessary components
    from voiceforge.cli.main import cli, CLIContext, pass_context
    from voiceforge import __version__, __app_name__
    import click
    
    if __name__ == '__main__':
        # Ensure the CLI is called with proper context
        # This helps preserve the docstrings and help text
        try:
            cli(standalone_mode=False)
        except SystemExit:
            # Handle normal CLI exits
            pass
        except Exception as e:
            print(f"[ERROR] CLI error: {e}")
            sys.exit(1)
        
except ImportError as e:
    print(f"[ERROR] Import error: {e}")
    print("Please ensure VoiceForge is properly installed.")
    print(f"Python path: {sys.path}")
    print(f"Application path: {application_path}")
    print(f"Source path: {src_path}")
    sys.exit(1)
except Exception as e:
    print(f"[ERROR] Fatal error: {e}")
    sys.exit(1) 