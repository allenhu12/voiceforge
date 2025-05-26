"""
VoiceForge CLI Main Module

Command-line interface for VoiceForge text-to-speech conversion.
"""

import sys
from pathlib import Path
from typing import Optional

import click

from .. import __version__, __app_name__
from ..core.config_manager import ConfigManager
from ..core.input_handler import InputHandler
from ..core.output_handler import OutputHandler
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
@click.option('--output-dir', '-o', type=click.Path(path_type=Path),
              help='Output directory (default: configured directory)')
@click.option('--provider', '-p', help='TTS provider to use (default: configured provider)')
@click.option('--voice', '-v', help='Voice/model to use (default: provider default)')
@click.option('--bitrate', '-b', type=int, default=128, 
              help='MP3 bitrate (default: 128)')
@click.option('--overwrite', is_flag=True, help='Overwrite existing output files')
@click.option('--estimate-only', is_flag=True, help='Only show cost estimate, do not convert')
@pass_context
def convert(
    ctx: CLIContext,
    input_file: Path,
    output_dir: Optional[Path],
    provider: Optional[str],
    voice: Optional[str],
    bitrate: int,
    overwrite: bool,
    estimate_only: bool
):
    """Convert a text file to MP3 audio."""
    try:
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
        
        # Determine voice
        if not voice:
            voice = tts_service.get_default_voice()
        
        # Cost estimation
        estimated_cost = tts_service.estimate_cost(text, voice)
        if estimated_cost:
            click.echo(f"💰 Estimated cost: {estimated_cost}")
        
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
            provider=provider,
            voice=voice
        )
        
        click.echo(f"🔄 Converting text to speech...")
        click.echo(f"   Provider: {provider}")
        click.echo(f"   Voice: {voice}")
        click.echo(f"   Output: {output_path}")
        
        # Perform conversion
        success = tts_service.text_to_speech(
            api_key=api_key,
            text=text,
            output_file_path=output_path,
            voice_or_model=voice,
            mp3_bitrate=bitrate
        )
        
        if success:
            file_size = output_path.stat().st_size
            click.echo(f"✅ Conversion successful!")
            click.echo(f"   Output file: {output_path}")
            click.echo(f"   File size: {file_size / 1024 / 1024:.2f} MB")
            
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


@cli.command('list-voices')
@click.option('--provider', '-p', help='TTS provider (default: configured provider)')
@pass_context
def list_voices(ctx: CLIContext, provider: Optional[str]):
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
        voices_data = tts_service.get_available_voices(api_key)
        
        click.echo(f"\nAvailable voices for {voices_data.get('provider', provider)}:")
        
        models = voices_data.get('models', [])
        if not models:
            click.echo("  No voices available.")
            return
        
        for model in models:
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