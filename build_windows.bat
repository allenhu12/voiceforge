@echo off
echo Building VoiceForge for Windows...
python build_config.py --platform windows
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Build completed successfully!
    echo [OUTPUT] Executable location: dist\windows\VoiceForge.exe
    echo.
    echo To test the executable:
    echo   cd dist\windows
    echo   VoiceForge.exe --help
) else (
    echo [ERROR] Build failed!
)
pause
