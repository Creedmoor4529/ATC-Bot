@echo off
echo Building ATC Bot launcher...
pip install pyinstaller >nul 2>&1
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
pyinstaller --onefile --console --name "ATC Bot" launcher.py --noconfirm
echo.
if exist "dist\ATC Bot.exe" (
    copy /y "dist\ATC Bot.exe" "ATC Bot.exe" >nul
    echo Done. ATC Bot.exe updated.
) else (
    echo ERROR: Build failed — exe not found in dist\
)
pause
