@echo off
echo Building ATC Bot launcher...
pip install pyinstaller >nul 2>&1
pyinstaller --onefile --console --name "ATC Bot" launcher.py
echo.
echo Done. Executable is in the dist\ folder.
pause
