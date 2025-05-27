"""
VoiceForge CLI Main Module

Command-line interface for VoiceForge text-to-speech conversion.
"""

import sys
from pathlib import Path
from typing import Optional
import threading
import time

import click

from .. import __version__, __app_name__
from ..core.config_manager import ConfigManager
from ..core.input_handler import InputHandler
from ..core.output_handler import OutputHandler
from ..core.speech_presets import SpeechPresets
from ..services.service_factory import TTSServiceFactory
from ..utils.logger import setup_application_logging
from ..utils.exceptions import (
    VoiceForgeError,
    AuthenticationError,
    NetworkError,
    FileError,
    ConfigurationError
)


# Global context for CLI
class CLIContext:
    """Context object for CLI commands."""
    
    def __init__(self):
        self.config_manager = None
        self.logger = None
        self.verbose = False


pass_context = click.make_pass_decorator(CLIContext, ensure=True)


@click.group()
@click.version_option(version=__version__, prog_name=__app_name__)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--config-dir', type=click.Path(), help='Custom configuration directory')
@pass_context
def cli(ctx: CLIContext, verbose: bool, config_dir: Optional[str]):
    """
    VoiceForge - Convert text files to MP3 audio using advanced TTS services.
    
    A powerful command-line tool for converting text files to high-quality
    MP3 audio using various Text-to-Speech service providers.
    """
    ctx.verbose = verbose
    
    # Setup logging
    log_dir = Path(config_dir) / "logs" if config_dir else None
    ctx.logger = setup_application_logging(verbose=verbose, log_dir=log_dir)
    
    # Initialize configuration manager
    config_dir_path = Path(config_dir) if config_dir else None
    ctx.config_manager = ConfigManager(config_dir=config_dir_path)
    
    ctx.logger.debug(f"VoiceForge CLI started (version {__version__})")


@cli.command()
@click.option('--input', '-i', 'input_file', required=True, 
              type=click.Path(exists=True, path_type=Path),
              help='Input text file to convert')
@click.option('--output', '-f', 'output_filename',
              help='Custom output filename (without extension, .mp3 will be added)')
@click.option('--output-dir', '-o', type=click.Path(path_type=Path),
              help='Output directory (default: configured directory)')
@click.option('--provider', '-p', help='TTS provider to use (default: configured provider)')
@click.option('--voice', '-v', help='Voice/model to use (default: provider default)')
@click.option('--bitrate', '-b', type=click.Choice(['64', '128', '192']), default='128', 
              help='MP3 bitrate in kbps (default: 128)')
@click.option('--natural', is_flag=True, default=True,
              help='Enable natural speech mode (default: enabled, use --no-natural to disable)')
@click.option('--no-natural', 'disable_natural', is_flag=True,
              help='Disable natural speech mode (use basic TTS without preprocessing)')
@click.option('--speech-speed', type=float, default=0.9,
              help='Speech speed (0.5-2.0, default: 0.9 for natural mode)')
@click.option('--temperature', type=float, default=0.7,
              help='Speech variation/randomness (0.1-1.0, default: 0.7)')
@click.option('--top-p', type=float, default=0.7,
              help='Speech diversity control (0.1-1.0, default: 0.7)')
@click.option('--paragraph-pause', type=click.Choice(['short', 'medium', 'long']), default='medium',
              help='Length of pauses between paragraphs (default: medium)')
@click.option('--speech-type', type=click.Choice(SpeechPresets.get_preset_choices()), 
              help='Predefined speech type with optimized parameters (overrides individual parameter settings)')
@click.option('--overwrite', is_flag=True, help='Overwrite existing output files')
@click.option('--estimate-only', is_flag=True, help='Only show cost estimate, do not convert')
@pass_context
def convert(
    ctx: CLIContext,
    input_file: Path,
    output_filename: Optional[str],
    output_dir: Optional[Path],
    provider: Optional[str],
    voice: Optional[str],
    bitrate: str,
    natural: bool,
    disable_natural: bool,
    speech_speed: float,
    temperature: float,
    top_p: float,
    paragraph_pause: str,
    speech_type: Optional[str],
    overwrite: bool,
    estimate_only: bool
):
    """Convert a text file to MP3 audio."""
    try:
        # Handle speech type preset (overrides individual parameters)
        if speech_type:
            try:
                preset = SpeechPresets.get_preset(speech_type)
                # Override parameters with preset values
                speech_speed = preset.speech_speed
                temperature = preset.temperature
                top_p = preset.top_p
                paragraph_pause = preset.paragraph_pause
                natural = preset.natural_speech
                
                # Use preset's preferred voice if no voice specified
                if not voice:
                    voice = preset.voice_preference
                
                click.echo(f"🎭 Using speech type preset: {preset.name}")
                click.echo(f"   Description: {preset.description}")
                click.echo(f"   Use case: {preset.use_case}")
                click.echo(f"   Parameters: speed={speech_speed}, temp={temperature}, top_p={top_p}, pause={paragraph_pause}")
                
            except ValueError as e:
                click.echo(f"❌ Error: {e}")
                sys.exit(1)
        
        # Handle natural speech mode (default is enabled)
        if disable_natural:
            natural = False
        
        # Determine provider
        if not provider:
            provider = ctx.config_manager.get_default_provider()
        
        # Check if provider is available
        if not TTSServiceFactory.is_provider_available(provider):
            available = TTSServiceFactory.get_available_providers()
            raise ConfigurationError(
                provider,
                f"Provider '{provider}' not available. Available: {', '.join(available)}"
            )
        
        # Check API key (not required for estimate-only)
        api_key = ctx.config_manager.get_api_key(provider)
        if not api_key and not estimate_only:
            click.echo(f"❌ No API key found for {provider}. Use 'voiceforge config set-api-key' to set it.")
            sys.exit(1)
        
        # Initialize components
        input_handler = InputHandler()
        output_handler = OutputHandler(ctx.config_manager.get_output_directory())
        tts_service = TTSServiceFactory.create_service(provider)
        
        # Read input file
        click.echo(f"📖 Reading input file: {input_file}")
        text = input_handler.read_text_file(input_file)
        char_count = input_handler.count_characters(text)
        
        click.echo(f"📊 Text statistics:")
        click.echo(f"   Characters: {char_count['total_characters']:,}")
        click.echo(f"   Words: {char_count['words']:,}")
        click.echo(f"   Lines: {char_count['lines']:,}")
        
        # Warn about large files
        if char_count['total_characters'] > 5000:
            click.echo(f"\n⚠️  Large file detected! Processing {char_count['total_characters']:,} characters may take several minutes.")
            if char_count['total_characters'] > 10000:
                click.echo(f"⚠️  Files over 10,000 characters may take 5-10 minutes or more to process.")
        
        # Estimate processing time
        estimated_time = char_count['total_characters'] / 100  # Rough estimate: 100 chars/second
        if estimated_time > 10:
            click.echo(f"⏱️  Estimated processing time: {estimated_time:.0f}-{estimated_time*1.5:.0f} seconds")
        
        # Determine voice
        if not voice:
            # First check if there's a configured default voice for this provider
            configured_voice = ctx.config_manager.get_default_voice(provider)
            if configured_voice:
                voice = configured_voice
                # Map known voice IDs to names
                voice_names = {
                    "b545c585f631496c914815291da4e893": "Default Female Voice",
                    "cfc33da8775c47afacccf4eebabe44dc": "Taylor Swift",
                    "54e3a85ac9594ffa83264b8a494b901b": "SpongeBob SquarePants",
                    "e58b0d7efca34eb38d5c4985e378abcb": "POTUS 47 - Trump",
                    "802e3bc2b27e49c2995d23ef70e6ac89": "Energetic Male",
                    "speech-1.6": "Speech 1.6 (AI)",
                    "speech-1.5": "Speech 1.5 (AI)"
                }
                voice_name = voice_names.get(voice, voice[:8] + "...")
                click.echo(f"📢 Using configured default voice: {voice_name}")
            else:
                # Fall back to provider's default
                voice = tts_service.get_default_voice()
        
        # Cost estimation
        estimated_cost = tts_service.estimate_cost(text, voice)
        if estimated_cost:
            click.echo(f"💰 Estimated cost: {estimated_cost}")
        
        # Output size estimation
        size_estimate = tts_service.estimate_output_size(text, int(bitrate), voice)
        if size_estimate and "error" not in size_estimate:
            click.echo(f"📏 Estimated output:")
            click.echo(f"   Duration: {size_estimate['estimated_duration_str']}")
            click.echo(f"   File size: {size_estimate['estimated_size_str']} (at {bitrate} kbps)")
            click.echo(f"   Words: {size_estimate['word_count']:,} (~{size_estimate['words_per_minute']} WPM)")
        
        if estimate_only:
            click.echo("✅ Cost estimation complete.")
            return
        
        # Confirm conversion
        if not click.confirm(f"Convert using {provider} with voice '{voice}'?"):
            click.echo("❌ Conversion cancelled.")
            return
        
        # Determine output path
        output_path = output_handler.get_output_path(
            input_file=input_file,
            output_dir=output_dir,
            custom_filename=output_filename,
            provider=provider,
            voice=voice
        )
        
        click.echo(f"🔄 Converting text to speech...")
        click.echo(f"   Provider: {provider}")
        click.echo(f"   Voice: {voice}")
        click.echo(f"   Output: {output_path}")
        
        # Show natural speech mode info
        if natural:
            if speech_type:
                click.echo(f"🎭 Natural speech mode enabled via preset:")
            else:
                click.echo(f"🎭 Natural speech mode enabled (default):")
            click.echo(f"   Speech speed: {speech_speed}x")
            click.echo(f"   Temperature: {temperature}")
            click.echo(f"   Top-p: {top_p}")
            click.echo(f"   Paragraph pauses: {paragraph_pause}")
            click.echo(f"   Text preprocessing: enabled")
            if not speech_type:
                click.echo(f"   💡 Use --speech-type to apply optimized presets")
        else:
            click.echo(f"⚡ Basic TTS mode (natural speech disabled)")
        
        # Prepare extra settings for natural speech
        extra_settings = {}
        if natural:
            extra_settings = {
                "natural_speech": True,
                "speech_speed": speech_speed,
                "temperature": temperature,
                "top_p": top_p,
                "paragraph_pause": paragraph_pause,
                "enable_preprocessing": True,
                "prosody": {
                    "speed": speech_speed,
                    "volume": 0
                }
            }
        
        # Show progress spinner during conversion
        progress_bar = None
        
        def progress_callback(percentage: int, status: str):
            if progress_bar:
                # Update progress bar position
                if percentage > progress_bar.pos:
                    progress_bar.update(percentage - progress_bar.pos)
                # Update label
                progress_bar.label = f"Converting: {status}"
        
        # Show real progress bar during conversion
        with click.progressbar(length=100, label='Converting: Starting...') as bar:
            progress_bar = bar
            
            # Perform the conversion with progress callback
            success = tts_service.text_to_speech(
                api_key=api_key,
                text=text,
                output_file_path=output_path,
                voice_or_model=voice,
                mp3_bitrate=int(bitrate),
                extra_settings=extra_settings,
                progress_callback=progress_callback
            )
        
        if success:
            file_size = output_path.stat().st_size
            file_size_mb = file_size / 1024 / 1024
            click.echo(f"✅ Conversion successful!")
            click.echo(f"   Output file: {output_path}")
            click.echo(f"   File size: {file_size_mb:.2f} MB")
            
            # Show comparison with estimate if available
            if size_estimate and "error" not in size_estimate:
                estimated_mb = size_estimate['estimated_size_mb']
                difference_mb = file_size_mb - estimated_mb
                accuracy_percent = (1 - abs(difference_mb) / estimated_mb) * 100 if estimated_mb > 0 else 0
                
                if abs(difference_mb) < 0.1:
                    click.echo(f"   Estimate accuracy: Very close! (±{abs(difference_mb):.2f} MB)")
                elif accuracy_percent > 80:
                    click.echo(f"   Estimate accuracy: Good ({accuracy_percent:.0f}% accurate)")
                else:
                    click.echo(f"   Estimate vs actual: {estimated_mb:.1f} MB → {file_size_mb:.1f} MB")
            
            # Offer to open output directory
            if click.confirm("Open output directory?"):
                output_handler.open_output_directory(output_path.parent)
        else:
            click.echo("❌ Conversion failed.")
            sys.exit(1)
            
    except VoiceForgeError as e:
        click.echo(f"❌ Error: {e}")
        if ctx.verbose:
            ctx.logger.exception("Conversion failed")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Unexpected error: {e}")
        if ctx.verbose:
            ctx.logger.exception("Unexpected error during conversion")
        sys.exit(1)


@cli.group()
@pass_context
def config(ctx: CLIContext):
    """Manage VoiceForge configuration."""
    pass


@config.command('set-api-key')
@click.argument('provider')
@click.argument('api_key')
@pass_context
def set_api_key(ctx: CLIContext, provider: str, api_key: str):
    """Set API key for a TTS provider."""
    try:
        if ctx.config_manager.set_api_key(provider, api_key):
            ctx.config_manager.save_config()
            click.echo(f"✅ API key set for {provider}")
            
            # Validate the key
            if TTSServiceFactory.is_provider_available(provider):
                tts_service = TTSServiceFactory.create_service(provider)
                if tts_service.validate_api_key(api_key):
                    click.echo(f"✅ API key validated successfully")
                else:
                    click.echo(f"⚠️  Warning: API key validation failed")
        else:
            click.echo(f"❌ Failed to set API key for {provider}")
            sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error setting API key: {e}")
        sys.exit(1)


@config.command('list-providers')
@pass_context
def list_providers(ctx: CLIContext):
    """List available TTS providers."""
    providers = TTSServiceFactory.get_available_providers()
    
    if not providers:
        click.echo("No TTS providers available.")
        return
    
    click.echo("Available TTS providers:")
    for provider in providers:
        has_key = "✅" if ctx.config_manager.has_api_key(provider) else "❌"
        is_default = "⭐" if provider == ctx.config_manager.get_default_provider() else "  "
        click.echo(f"  {is_default} {provider} {has_key}")


@config.command('show')
@pass_context
def show_config(ctx: CLIContext):
    """Show current configuration."""
    click.echo("VoiceForge Configuration:")
    click.echo(f"  Default provider: {ctx.config_manager.get_default_provider()}")
    click.echo(f"  Output directory: {ctx.config_manager.get_output_directory()}")
    click.echo(f"  Configured providers: {len(ctx.config_manager.list_providers())}")
    
    # Show default voice for each provider
    for provider in ctx.config_manager.list_providers():
        default_voice = ctx.config_manager.get_default_voice(provider)
        if default_voice:
            # Map known voice IDs to names
            voice_names = {
                "b545c585f631496c914815291da4e893": "Default Female Voice",
                "cfc33da8775c47afacccf4eebabe44dc": "Taylor Swift",
                "54e3a85ac9594ffa83264b8a494b901b": "SpongeBob SquarePants",
                "e58b0d7efca34eb38d5c4985e378abcb": "POTUS 47 - Trump",
                "802e3bc2b27e49c2995d23ef70e6ac89": "Energetic Male",
                "7f92f8afb8ec43bf81429cc1c9199cb1": "AD学姐",
                "54a5170264694bfc8e9ad98df7bd89c3": "丁真",
                "aebaa2305aa2452fbdc8f41eec852a79": "雷军",
                "speech-1.6": "Speech 1.6 (AI)",
                "speech-1.5": "Speech 1.5 (AI)"
            }
            voice_name = voice_names.get(default_voice, default_voice[:8] + "...")
            click.echo(f"  Default voice for {provider}: {voice_name} ({default_voice})")


@config.command('set-default-voice')
@click.argument('provider')
@click.argument('voice_id')
@pass_context
def set_default_voice(ctx: CLIContext, provider: str, voice_id: str):
    """Set default voice for a TTS provider."""
    try:
        # Check if provider has API key
        if not ctx.config_manager.has_api_key(provider):
            click.echo(f"❌ No API key found for {provider}. Set API key first.")
            sys.exit(1)
        
        # Set the default voice
        if ctx.config_manager.set_default_voice(provider, voice_id):
            ctx.config_manager.save_config()
            
            # Map known voice IDs to names
            voice_names = {
                "b545c585f631496c914815291da4e893": "Default Female Voice",
                "cfc33da8775c47afacccf4eebabe44dc": "Taylor Swift",
                "54e3a85ac9594ffa83264b8a494b901b": "SpongeBob SquarePants",
                "e58b0d7efca34eb38d5c4985e378abcb": "POTUS 47 - Trump",
                "802e3bc2b27e49c2995d23ef70e6ac89": "Energetic Male",
                "728f6ff2240d49308e8137ffe66008e2": "ElevenLabs Adam",
                "0cd6cf9684dd4cc9882fbc98957c9b1d": "The Elephant",
                "7f92f8afb8ec43bf81429cc1c9199cb1": "AD学姐",
                "54a5170264694bfc8e9ad98df7bd89c3": "丁真",
                "aebaa2305aa2452fbdc8f41eec852a79": "雷军",
                "5b67899dc9a34685ae09c94c890a606f": "عصام الشوالي",
                "ef9c79b62ef34530bf452c0e50e3c260": "Horror",
                "speech-1.6": "Speech 1.6 (AI)",
                "speech-1.5": "Speech 1.5 (AI)"
            }
            
            voice_name = voice_names.get(voice_id, "Custom Voice")
            click.echo(f"✅ Default voice set for {provider}: {voice_name}")
            click.echo(f"   Voice ID: {voice_id}")
        else:
            click.echo(f"❌ Failed to set default voice for {provider}")
            sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Error setting default voice: {e}")
        sys.exit(1)


@cli.command('list-speech-types')
@pass_context
def list_speech_types(ctx: CLIContext):
    """List all available speech type presets."""
    click.echo("🎭 Available Speech Type Presets:\n")
    
    presets = SpeechPresets.get_all_presets()
    
    # Group presets by category for better organization
    categories = {
        "Narration": ["female-narrator", "male-narrator", "audiobook", "storytelling"],
        "Professional": ["presentation", "educational", "news", "technical"],
        "Casual": ["podcast", "conversational"],
        "Specialized": ["meditation", "dramatic"]
    }
    
    for category, preset_names in categories.items():
        click.echo(f"📂 {category}:")
        for name in preset_names:
            if name in presets:
                preset = presets[name]
                click.echo(f"  • {name}: {preset.description}")
                click.echo(f"    Use case: {preset.use_case}")
                click.echo(f"    Parameters: speed={preset.speech_speed}, temp={preset.temperature}, top_p={preset.top_p}")
                click.echo()
        click.echo()
    
    click.echo("💡 Usage examples:")
    click.echo("   voiceforge convert --input story.txt --speech-type female-narrator")
    click.echo("   voiceforge convert --input presentation.txt --speech-type presentation")
    click.echo("   voiceforge convert --input meditation.txt --speech-type meditation")
    click.echo("\n🔧 Note: Speech type presets override individual parameter settings")


@cli.command('list-voices')
@click.option('--provider', '-p', help='TTS provider (default: configured provider)')
@click.option('--ids-only', is_flag=True, help='Show only voice IDs (one per line)')
@click.option('--limit', '-l', type=int, default=20, help='Limit number of voices shown (default: 20)')
@pass_context
def list_voices(ctx: CLIContext, provider: Optional[str], ids_only: bool, limit: int):
    """List available voices for a TTS provider."""
    try:
        if not provider:
            provider = ctx.config_manager.get_default_provider()
        
        api_key = ctx.config_manager.get_api_key(provider)
        if not api_key:
            click.echo(f"❌ No API key found for {provider}")
            sys.exit(1)
        
        tts_service = TTSServiceFactory.create_service(provider)
        
        click.echo(f"🔄 Fetching voices for {provider}...")
        voices_data = tts_service.get_available_voices(api_key, limit=limit)
        
        total_available = voices_data.get('total_available', 0)
        click.echo(f"\nAvailable voices for {voices_data.get('provider', provider)}:")
        if total_available > 0:
            click.echo(f"📊 Total voices available: {total_available:,}")
            click.echo(f"📋 Showing first {len(voices_data.get('models', []))} voices:\n")
        
        models = voices_data.get('models', [])
        if not models:
            click.echo("  No voices available.")
            return
        
        # If ids-only flag is set, just print the IDs
        if ids_only:
            for model in models:
                click.echo(model.get('id', 'unknown'))
            return
        
        # Group by type
        ai_models = [m for m in models if m.get('type') == 'ai']
        human_models = [m for m in models if m.get('type') == 'human']
        
        # Display AI models first
        if ai_models:
            click.echo("🤖 AI Models:")
            for model in ai_models:
                name = model.get('name', model.get('id', 'Unknown'))
                model_id = model.get('id', 'unknown')
                description = model.get('description', '')
                languages = ', '.join(model.get('languages', []))
                
                click.echo(f"  • {name} ({model_id})")
                if description:
                    click.echo(f"    {description}")
                if languages:
                    click.echo(f"    Languages: {languages}")
                click.echo()
        
        # Display human voice models
        if human_models:
            click.echo("👤 Human Voice Models:")
            for model in human_models:
                name = model.get('name', model.get('id', 'Unknown'))
                model_id = model.get('id', 'unknown')
                description = model.get('description', '')
                languages = ', '.join(model.get('languages', []))
                author = model.get('author', 'Unknown')
                like_count = model.get('like_count', 0)
                task_count = model.get('task_count', 0)
                tags = model.get('tags', [])
                
                click.echo(f"  • {name} ({model_id})")
                if description:
                    click.echo(f"    {description}")
                if languages:
                    click.echo(f"    Languages: {languages}")
                if author != 'Unknown':
                    click.echo(f"    Author: {author}")
                if like_count > 0:
                    click.echo(f"    👍 {like_count:,} likes | 🎯 {task_count:,} uses")
                if tags:
                    click.echo(f"    Tags: {', '.join(tags)}")
                click.echo()
        
        if total_available > len(models):
            click.echo(f"💡 Tip: There are {total_available - len(models):,} more voices available.")
            click.echo("    Visit https://fish.audio/ to browse all voices.")
            
    except VoiceForgeError as e:
        click.echo(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Main entry point for the CLI."""
    try:
        cli()
    except KeyboardInterrupt:
        click.echo("\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        click.echo(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 