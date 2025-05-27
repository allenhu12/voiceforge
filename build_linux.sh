#!/bin/bash
echo "Building VoiceForge for Linux..."
python3 build_config.py --platform linux
if [ $? -eq 0 ]; then
    echo ""
    echo "[SUCCESS] Build completed successfully!"
    echo "[OUTPUT] Executable location: dist/linux/VoiceForge"
    echo ""
    echo "To test the executable:"
    echo "  cd dist/linux"
    echo "  ./VoiceForge --help"
else
    echo "[ERROR] Build failed!"
fi
