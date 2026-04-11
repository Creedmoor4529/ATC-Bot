@echo off
setlocal enabledelayedexpansion

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo ============================================================
echo  ATC Bot Updater
echo ============================================================
echo.

:: ── Check git ────────────────────────────────────────────────
where git >nul 2>&1
if errorlevel 1 (
    echo [ERROR] git not found in PATH. Install Git for Windows.
    goto :fail
)

:: ── Check Python ─────────────────────────────────────────────
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH.
    goto :fail
)

:: ── Git pull ─────────────────────────────────────────────────
echo [1/4] Pulling latest changes from git...
echo.
git pull
if errorlevel 1 (
    echo.
    echo [ERROR] git pull failed. Check your connection or resolve conflicts.
    goto :fail
)
echo.

:: ── Install / update dependencies ────────────────────────────
echo [2/4] Updating dependencies...
echo.
python -m pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] pip install failed.
    goto :fail
)
echo Dependencies up to date.
echo.

:: ── Rebuild exe ──────────────────────────────────────────────
echo [3/4] Rebuilding ATC Bot.exe...
echo.
python -m pip install pyinstaller --quiet
pyinstaller --onefile --console --name "ATC Bot" --icon=atcicon.ico launcher.py --distpath dist --workpath build --noconfirm
if errorlevel 1 (
    echo [ERROR] PyInstaller build failed.
    goto :fail
)
echo.

:: ── Copy exe to project root ──────────────────────────────────
echo [4/4] Installing updated exe...
if exist "dist\ATC Bot.exe" (
    copy /y "dist\ATC Bot.exe" "ATC Bot.exe" >nul
    echo ATC Bot.exe updated successfully.
) else (
    echo [ERROR] Built exe not found in dist\.
    goto :fail
)

echo.
echo ============================================================
echo  Update complete.
echo ============================================================
echo.
pause
exit /b 0

:fail
echo.
echo ============================================================
echo  Update FAILED. See errors above.
echo ============================================================
echo.
pause
exit /b 1
