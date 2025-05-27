#!/bin/bash
echo "Building VoiceForge for Linux..."
python3 build_config.py --platform linux
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build completed successfully!"
    echo "📦 Executable location: dist/linux/VoiceForge"
    echo ""
    echo "To test the executable:"
    echo "  cd dist/linux"
    echo "  ./VoiceForge --help"
else
    echo "❌ Build failed!"
fi
