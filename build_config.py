#!/usr/bin/env python3
"""
VoiceForge Build Configuration

This script packages VoiceForge into standalone executables for Windows, macOS, and Linux
using PyInstaller. The resulting executables include all dependencies and don't require
Python to be installed on the target system.

Usage:
    python build_config.py [--platform PLATFORM] [--debug] [--clean]

Platforms:
    - windows: Build Windows .exe
    - macos: Build macOS .app bundle
    - linux: Build Linux executable
    - all: Build for all platforms (requires cross-compilation setup)
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path
import argparse


class VoiceForgeBuildConfig:
    """Configuration for building VoiceForge executables."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.src_dir = self.project_root / "src"
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.spec_dir = self.project_root / "specs"
        
        # Application metadata
        self.app_name = "VoiceForge"
        self.app_version = "1.0.0"
        self.app_description = "Convert text files to MP3 audio using advanced TTS services"
        self.app_author = "VoiceForge Team"
        self.app_icon = self.project_root / "assets" / "icon.ico"  # Will create if needed
        
        # Entry point
        self.main_script = self.project_root / "voiceforge_main.py"
        
    def get_pyinstaller_options(self, platform_name: str, debug: bool = False) -> dict:
        """Get PyInstaller options for the specified platform."""
        
        # Common options for all platforms
        options = {
            'name': self.app_name,
            'console': True,  # CLI application
            'onefile': True,  # Single executable file
            'clean': True,
            'noconfirm': True,
            'strip': not debug,
            'optimize': 0,  # Disable optimization to preserve docstrings
            'distpath': str(self.dist_dir / platform_name),
            'workpath': str(self.build_dir / platform_name),
            'specpath': str(self.spec_dir),
        }
        
        # Platform-specific options
        if platform_name == "windows":
            options.update({
                'icon': str(self.app_icon) if self.app_icon.exists() else None,
                'version_file': str(self.spec_dir / "version_info.txt"),
                'uac_admin': False,
                'uac_uiaccess': False,
            })
        elif platform_name == "macos":
            options.update({
                'icon': str(self.app_icon) if self.app_icon.exists() else None,
                'osx_bundle_identifier': 'com.voiceforge.app',
                'codesign_identity': None,  # Set if you have a signing certificate
            })
        elif platform_name == "linux":
            options.update({
                'strip': True,
            })
        
        # Hidden imports - modules that PyInstaller might miss
        options['hiddenimports'] = [
            'voiceforge',
            'voiceforge.__init__',
            'voiceforge.cli',
            'voiceforge.cli.__init__',
            'voiceforge.cli.main',
            'voiceforge.core',
            'voiceforge.core.__init__',
            'voiceforge.core.config_manager',
            'voiceforge.core.input_handler',
            'voiceforge.core.output_handler',
            'voiceforge.core.speech_presets',
            'voiceforge.services',
            'voiceforge.services.__init__',
            'voiceforge.services.fish_tts_client',
            'voiceforge.services.service_factory',
            'voiceforge.interfaces',
            'voiceforge.interfaces.__init__',
            'voiceforge.interfaces.tts_service_interface',
            'voiceforge.utils',
            'voiceforge.utils.__init__',
            'voiceforge.utils.exceptions',
            'voiceforge.utils.logger',
            'click',
            'click.core',
            'click.decorators',
            'click.exceptions',
            'httpx',
            'httpx._transports',
            'httpx._transports.default',
            'ormsgpack',
            'pydantic',
            'pydantic.dataclasses',
            'pydantic.main',
            'cryptography',
            'cryptography.fernet',
            'chardet',
            'chardet.universaldetector',
            'python_dotenv',
        ]
        
        # Data files to include
        options['datas'] = [
            # Include the entire source directory
            (str(self.src_dir), "src"),
        ]
        
        # Binary files to include (if any)
        options['binaries'] = []
        
        # Exclude unnecessary modules to reduce size
        options['excludes'] = [
            'tkinter',
            'matplotlib',
            'numpy',
            'scipy',
            'pandas',
            'PIL',
            'PyQt5',
            'PyQt6',
            'PySide2',
            'PySide6',
            'jupyter',
            'IPython',
            'notebook',
            'sphinx',
            'pytest',
            'setuptools',
            'distutils',
        ]
        
        return options
    
    def create_version_info_file(self):
        """Create Windows version info file."""
        version_info_content = f'''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({self.app_version.replace('.', ', ')}, 0),
    prodvers=({self.app_version.replace('.', ', ')}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [StringStruct(u'CompanyName', u'{self.app_author}'),
           StringStruct(u'FileDescription', u'{self.app_description}'),
           StringStruct(u'FileVersion', u'{self.app_version}'),
           StringStruct(u'InternalName', u'{self.app_name}'),
           StringStruct(u'LegalCopyright', u'Copyright © 2025 {self.app_author}'),
           StringStruct(u'OriginalFilename', u'{self.app_name}.exe'),
           StringStruct(u'ProductName', u'{self.app_name}'),
           StringStruct(u'ProductVersion', u'{self.app_version}')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
        
        version_file = self.spec_dir / "version_info.txt"
        version_file.parent.mkdir(exist_ok=True)
        version_file.write_text(version_info_content)
        return version_file
    
    def create_icon_file(self):
        """Create a simple icon file if it doesn't exist."""
        if not self.app_icon.exists():
            # Create assets directory
            self.app_icon.parent.mkdir(exist_ok=True)
            
            # For now, we'll skip icon creation
            # In a real scenario, you'd want to include proper icon files
            print(f"[WARNING] Icon file not found at {self.app_icon}")
            print("   Consider adding icon files for better branding:")
            print("   - assets/icon.ico (Windows)")
            print("   - assets/icon.icns (macOS)")
            print("   - assets/icon.png (Linux)")
    
    def install_pyinstaller(self):
        """Install PyInstaller if not already installed."""
        try:
            import PyInstaller
            print(f"[SUCCESS] PyInstaller already installed: {PyInstaller.__version__}")
        except ImportError:
            print("[INSTALL] Installing PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("[SUCCESS] PyInstaller installed successfully")
    
    def clean_build_dirs(self):
        """Clean build and dist directories."""
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                print(f"[CLEAN] Cleaning {dir_path}")
                shutil.rmtree(dir_path)
        
        # Clean spec files
        for spec_file in self.project_root.glob("*.spec"):
            spec_file.unlink()
            print(f"[CLEAN] Removed {spec_file}")
    
    def build_for_platform(self, platform_name: str, debug: bool = False):
        """Build executable for the specified platform."""
        print(f"\n[BUILD] Building {self.app_name} for {platform_name}...")
        
        # Ensure directories exist
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        self.spec_dir.mkdir(exist_ok=True)
        
        # Create version info file for Windows
        if platform_name == "windows":
            self.create_version_info_file()
        
        # Create icon file if needed
        self.create_icon_file()
        
        # Get PyInstaller options
        options = self.get_pyinstaller_options(platform_name, debug)
        
        # Build PyInstaller command
        cmd = [
            sys.executable, "-m", "PyInstaller",
            str(self.main_script),
        ]
        
        # Add options to command
        for key, value in options.items():
            if value is None:
                continue
            elif isinstance(value, bool):
                if value:
                    cmd.append(f"--{key.replace('_', '-')}")
            elif isinstance(value, list):
                for item in value:
                    if key == 'hiddenimports':
                        cmd.extend(["--hidden-import", str(item)])
                    elif key == 'excludes':
                        cmd.extend(["--exclude-module", str(item)])
                    elif key == 'datas':
                        # Handle data files as tuples (source, dest)
                        if isinstance(item, tuple) and len(item) == 2:
                            cmd.extend(["--add-data", f"{item[0]}{os.pathsep}{item[1]}"])
                        else:
                            cmd.extend(["--add-data", str(item)])
                    else:
                        cmd.extend([f"--{key.replace('_', '-')}", str(item)])
            else:
                cmd.extend([f"--{key.replace('_', '-')}", str(value)])
        
        # Add Python path for imports
        cmd.extend(["--paths", str(self.src_dir)])
        
        print(f"[RUN] Running PyInstaller command:")
        print(f"   {' '.join(cmd)}")
        
        # Run PyInstaller
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("[SUCCESS] Build completed successfully!")
            
            # Show output file info
            output_dir = self.dist_dir / platform_name
            if output_dir.exists():
                executable_files = list(output_dir.glob("*"))
                if executable_files:
                    for exe_file in executable_files:
                        if exe_file.is_file():
                            size_mb = exe_file.stat().st_size / (1024 * 1024)
                            print(f"[OUTPUT] Output: {exe_file} ({size_mb:.1f} MB)")
                            
                            # Make executable on Unix systems
                            if platform_name in ["linux", "macos"]:
                                exe_file.chmod(0o755)
                                print(f"[EXEC] Made executable: {exe_file}")
        
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Build failed with error code {e.returncode}")
            print(f"Error output: {e.stderr}")
            return False
        
        return True
    
    def create_build_script(self, platform_name: str):
        """Create a platform-specific build script."""
        if platform_name == "windows":
            script_content = f'''@echo off
echo Building VoiceForge for Windows...
python build_config.py --platform windows
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Build completed successfully!
    echo 📦 Executable location: dist\\windows\\{self.app_name}.exe
    echo.
    echo To test the executable:
    echo   cd dist\\windows
    echo   {self.app_name}.exe --help
) else (
    echo ❌ Build failed!
)
pause
'''
            script_file = self.project_root / "build_windows.bat"
            
        elif platform_name == "macos":
            script_content = f'''#!/bin/bash
echo "Building VoiceForge for macOS..."
python3 build_config.py --platform macos
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build completed successfully!"
    echo "📦 Executable location: dist/macos/{self.app_name}"
    echo ""
    echo "To test the executable:"
    echo "  cd dist/macos"
    echo "  ./{self.app_name} --help"
else
    echo "❌ Build failed!"
fi
'''
            script_file = self.project_root / "build_macos.sh"
            
        elif platform_name == "linux":
            script_content = f'''#!/bin/bash
echo "Building VoiceForge for Linux..."
python3 build_config.py --platform linux
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build completed successfully!"
    echo "📦 Executable location: dist/linux/{self.app_name}"
    echo ""
    echo "To test the executable:"
    echo "  cd dist/linux"
    echo "  ./{self.app_name} --help"
else
    echo "❌ Build failed!"
fi
'''
            script_file = self.project_root / "build_linux.sh"
        
        script_file.write_text(script_content)
        
        # Make script executable on Unix systems
        if platform_name in ["macos", "linux"]:
            script_file.chmod(0o755)
        
        print(f"[SCRIPT] Created build script: {script_file}")
        return script_file


def main():
    """Main build function."""
    parser = argparse.ArgumentParser(description="Build VoiceForge standalone executables")
    parser.add_argument("--platform", choices=["windows", "macos", "linux", "all"], 
                       default="auto", help="Target platform (default: auto-detect)")
    parser.add_argument("--debug", action="store_true", help="Build debug version")
    parser.add_argument("--clean", action="store_true", help="Clean build directories first")
    parser.add_argument("--create-scripts", action="store_true", 
                       help="Create platform-specific build scripts")
    
    args = parser.parse_args()
    
    # Initialize build config
    config = VoiceForgeBuildConfig()
    
    # Auto-detect platform if needed
    if args.platform == "auto":
        system = platform.system().lower()
        if system == "windows":
            args.platform = "windows"
        elif system == "darwin":
            args.platform = "macos"
        elif system == "linux":
            args.platform = "linux"
        else:
            print(f"[ERROR] Unsupported platform: {system}")
            sys.exit(1)
    
    print(f"[CONFIG] VoiceForge Build Configuration")
    print(f"   Version: {config.app_version}")
    print(f"   Platform: {args.platform}")
    print(f"   Debug: {args.debug}")
    print(f"   Project root: {config.project_root}")
    
    # Create build scripts if requested
    if args.create_scripts:
        print("\n[SCRIPT] Creating build scripts...")
        for platform_name in ["windows", "macos", "linux"]:
            config.create_build_script(platform_name)
        print("[SUCCESS] Build scripts created successfully!")
        return
    
    # Clean build directories if requested
    if args.clean:
        config.clean_build_dirs()
    
    # Install PyInstaller
    config.install_pyinstaller()
    
    # Build for specified platform(s)
    if args.platform == "all":
        platforms = ["windows", "macos", "linux"]
        print("[WARNING] Building for all platforms requires cross-compilation setup")
        print("   Consider building on each target platform separately")
    else:
        platforms = [args.platform]
    
    success_count = 0
    for platform_name in platforms:
        if config.build_for_platform(platform_name, args.debug):
            success_count += 1
        else:
            print(f"[ERROR] Failed to build for {platform_name}")
    
    # Summary
    print(f"\n[SUMMARY] Build Summary:")
    print(f"   Successful builds: {success_count}/{len(platforms)}")
    
    if success_count == len(platforms):
        print("[SUCCESS] All builds completed successfully!")
        print("\n[DIST] Distribution files:")
        for platform_name in platforms:
            dist_dir = config.dist_dir / platform_name
            if dist_dir.exists():
                for file in dist_dir.iterdir():
                    if file.is_file():
                        size_mb = file.stat().st_size / (1024 * 1024)
                        print(f"   {file} ({size_mb:.1f} MB)")
        
        print("\n[USAGE] Usage Instructions:")
        print("   1. Copy the executable to the target system")
        print("   2. Run the executable from command line:")
        for platform_name in platforms:
            if platform_name == "windows":
                print(f"      Windows: VoiceForge.exe --help")
            else:
                print(f"      {platform_name.title()}: ./VoiceForge --help")
        print("   3. Set up API key: VoiceForge config set-api-key fish_audio YOUR_KEY")
        print("   4. Convert text: VoiceForge convert --input file.txt")
    else:
        print("[ERROR] Some builds failed. Check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main() 