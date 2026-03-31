@echo off
echo Building ATC Bot launcher...
pip install pyinstaller >nul 2>&1
pyinstaller --onefile --noconsole --name "ATC Bot" launcher.py
echo.
echo Done. Executable is in the dist\ folder.
pause
