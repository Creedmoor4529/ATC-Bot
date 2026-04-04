@echo off
echo Building ATC Bot launcher...
pip install pyinstaller >nul 2>&1
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist "ATC Bot.spec" del /f "ATC Bot.spec"
pyinstaller --onefile --console --name "ATC Bot" launcher.py --noconfirm --clean
echo.
if exist "dist\ATC Bot.exe" (
    copy /y "dist\ATC Bot.exe" "ATC Bot.exe" >nul
    echo Done. ATC Bot.exe updated.
) else (
    echo ERROR: Build failed — exe not found in dist\
)
pause
