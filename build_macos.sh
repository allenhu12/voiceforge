#!/bin/bash
echo "Building VoiceForge for macOS..."
python3 build_config.py --platform macos
if [ $? -eq 0 ]; then
    echo ""
    echo "[SUCCESS] Build completed successfully!"
    echo "[OUTPUT] Executable location: dist/macos/VoiceForge"
    echo ""
    echo "To test the executable:"
    echo "  cd dist/macos"
    echo "  ./VoiceForge --help"
else
    echo "[ERROR] Build failed!"
fi
