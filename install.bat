@echo off
setlocal enabledelayedexpansion
title DCS ATC Bot — Installer

echo ============================================================
echo  DCS ATC Bot — Windows Installer
echo ============================================================
echo.

:: --- Check Python ----------------------------------------------------------
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.11+ from https://python.org
    pause & exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PYVER=%%v
echo [OK] Python %PYVER% found.

:: --- Install Python deps ---------------------------------------------------
echo.
echo [1/4] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 ( echo [ERROR] pip install failed. & pause & exit /b 1 )
echo [OK] Python dependencies installed.

:: --- Download Piper --------------------------------------------------------
echo.
echo [2/4] Setting up Piper TTS...
if exist "piper\piper.exe" (
    echo [OK] Piper already installed, skipping.
) else (
    set PIPER_URL=https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_windows_amd64.zip
    set PIPER_ZIP=%TEMP%\piper_windows_amd64.zip
    echo Downloading Piper...
    powershell -Command "Invoke-WebRequest -Uri '!PIPER_URL!' -OutFile '!PIPER_ZIP!' -UseBasicParsing"
    if errorlevel 1 ( echo [ERROR] Failed to download Piper. & pause & exit /b 1 )
    echo Extracting Piper...
    powershell -Command "Expand-Archive -Path '!PIPER_ZIP!' -DestinationPath '.' -Force"
    del "!PIPER_ZIP!"
    if exist "piper\piper.exe" (
        echo [OK] Piper installed.
    ) else (
        echo [ERROR] Piper extraction failed.
        pause & exit /b 1
    )
)

:: --- Download voice model --------------------------------------------------
echo.
echo [3/4] Setting up voice model (en_US-amy-medium)...
if exist "piper\voices\en_US-amy-medium.onnx" (
    echo [OK] Voice model already present, skipping.
) else (
    mkdir piper\voices 2>nul
    set BASE_URL=https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/amy/medium
    echo Downloading voice model ^(this may take a moment^)...
    powershell -Command "Invoke-WebRequest -Uri '!BASE_URL!/en_US-amy-medium.onnx' -OutFile 'piper\voices\en_US-amy-medium.onnx' -UseBasicParsing"
    powershell -Command "Invoke-WebRequest -Uri '!BASE_URL!/en_US-amy-medium.onnx.json' -OutFile 'piper\voices\en_US-amy-medium.onnx.json' -UseBasicParsing"
    if exist "piper\voices\en_US-amy-medium.onnx" (
        echo [OK] Voice model downloaded.
    ) else (
        echo [ERROR] Voice model download failed.
        pause & exit /b 1
    )
)

:: --- Create .env -----------------------------------------------------------
echo.
echo [4/4] Setting up .env...
if exist ".env" (
    echo [OK] .env already exists, skipping.
) else (
    copy ".env.example" ".env" >nul
    echo [OK] .env created from .env.example — add your API key before starting.
)

:: --- Done ------------------------------------------------------------------
echo.
echo ============================================================
echo  Installation complete.
echo.
echo  Next steps:
echo    1. Edit .env and add your API key (OPENAI_API_KEY or GROQ_API_KEY)
echo    2. Edit config.lua to set your airfield and frequencies
echo    3. Install dcs_atc_export.lua into DCS Saved Games\Scripts\Hooks\
echo    4. Run:  python main.py
echo       OR:   build_launcher.bat  to create ATC Bot.exe
echo ============================================================
echo.
pause
