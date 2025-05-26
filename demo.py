#!/usr/bin/env python3
"""
VoiceForge Demo Script

This script demonstrates VoiceForge functionality without requiring an API key.
It shows the CLI interface, configuration management, and cost estimation features.

Usage: python demo.py
"""

import subprocess
import sys
from pathlib import Path
import time

def run_command(cmd, description=""):
    """Run a command and display the output."""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"Command: {cmd}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def create_demo_files():
    """Create demo text files for testing."""
    print("\n📝 Creating demo text files...")
    
    # Create demo texts
    demo_texts = {
        "short_demo.txt": "Hello! This is a short demo of VoiceForge. It converts text to speech using AI.",
        "medium_demo.txt": """Welcome to VoiceForge, an advanced text-to-speech conversion tool.

VoiceForge supports multiple TTS providers and offers high-quality audio generation. 
You can convert text files to MP3 format with just a few simple commands.

The application features secure API key management, cost estimation, and cross-platform compatibility.""",
        "long_demo.txt": """VoiceForge: Advanced Text-to-Speech Conversion

Chapter 1: Introduction

VoiceForge is a powerful, modular text-to-speech application designed for both developers and end-users. 
Built with Python, it provides a clean CLI interface and will soon feature a modern GUI.

Key Features:
- Multiple TTS provider support (Fish Audio, with OpenAI and Google coming soon)
- Secure API key management with encryption
- Cost estimation before conversion
- High-quality MP3 output with configurable bitrates
- Cross-platform compatibility (Windows, macOS, Linux)
- Extensible architecture for adding new providers

Chapter 2: Architecture

The application follows a modular design with clear separation of concerns:
- Interfaces define contracts for TTS providers
- Services implement specific TTS provider clients
- Core modules handle configuration, input/output, and business logic
- CLI provides user-friendly command-line interface
- Utils contain shared utilities and error handling

This architecture makes VoiceForge easy to extend and maintain while ensuring consistent behavior across different TTS providers.

Thank you for trying VoiceForge!"""
    }
    
    for filename, content in demo_texts.items():
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Created {filename} ({len(content)} characters)")

def main():
    """Run the VoiceForge demo."""
    print("🎵 VoiceForge Demo Script")
    print("=" * 50)
    print("This demo showcases VoiceForge functionality without requiring an API key.")
    print("We'll demonstrate the CLI interface, configuration, and cost estimation.")
    
    # Check if VoiceForge is installed
    print("\n🔍 Checking VoiceForge installation...")
    if not run_command("voiceforge --version", "Check VoiceForge version"):
        print("❌ VoiceForge is not installed. Please run 'pip install -e .' first.")
        sys.exit(1)
    
    # Create demo files
    create_demo_files()
    
    # Demo 1: Show help
    run_command("voiceforge --help", "Display VoiceForge help")
    
    # Demo 2: Show configuration
    run_command("voiceforge config show", "Show current configuration")
    
    # Demo 3: List providers
    run_command("voiceforge config list-providers", "List available TTS providers")
    
    # Demo 4: Cost estimation for different file sizes
    for filename in ["short_demo.txt", "medium_demo.txt", "long_demo.txt"]:
        run_command(f"voiceforge convert --input {filename} --estimate-only", 
                   f"Cost estimation for {filename}")
    
    # Demo 5: Show convert command help
    run_command("voiceforge convert --help", "Show convert command options")
    
    # Demo 6: Show list-voices command (will fail without API key, but shows the interface)
    run_command("voiceforge list-voices", "Attempt to list voices (will show API key requirement)")
    
    # Demo 7: Show verbose mode
    run_command("voiceforge --verbose config show", "Verbose mode demonstration")
    
    print("\n" + "="*60)
    print("🎉 Demo Complete!")
    print("="*60)
    print("\n📋 What you've seen:")
    print("✅ VoiceForge CLI interface and help system")
    print("✅ Configuration management")
    print("✅ Provider listing (Fish Audio)")
    print("✅ Cost estimation for different text sizes")
    print("✅ File reading and character counting")
    print("✅ Error handling (API key requirement)")
    print("✅ Verbose logging mode")
    
    print("\n🚀 Next Steps:")
    print("1. Get a Fish Audio API key from https://fish.audio/")
    print("2. Set your API key: voiceforge config set-api-key fish_audio YOUR_KEY")
    print("3. Convert text to speech: voiceforge convert --input short_demo.txt")
    print("4. Explore voice options: voiceforge list-voices")
    
    print("\n📚 Documentation:")
    print("- docs/getting-started-guide.md - Complete tutorial")
    print("- docs/quick-reference.md - Command reference")
    print("- README.md - Project overview")
    print("- progress.md - Development progress")
    
    # Cleanup demo files
    print("\n🧹 Cleaning up demo files...")
    for filename in ["short_demo.txt", "medium_demo.txt", "long_demo.txt"]:
        try:
            Path(filename).unlink()
            print(f"✅ Removed {filename}")
        except FileNotFoundError:
            pass
    
    print("\n🎵 Thank you for trying VoiceForge!")

if __name__ == "__main__":
    main() 