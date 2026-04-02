"""
ATC Bot launcher — starts main.py with output to console and bot.log.
Closing the console window cleanly kills the bot process.
Compile with:  pyinstaller --onefile --console --name "ATC Bot" launcher.py
"""

import os
import signal
import shutil
import subprocess
import sys
from datetime import datetime


def _find_python() -> str | None:
    """Find the Python interpreter, excluding this exe if running compiled."""
    this = os.path.abspath(sys.executable).lower()
    for candidate in (sys.executable, "python", "python3"):
        found = shutil.which(candidate)
        if found and os.path.abspath(found).lower() != this:
            return found
    return None


proc = None


def _shutdown(signum=None, frame=None):
    """Kill the bot subprocess and exit."""
    if proc and proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    sys.exit(0)


def main():
    global proc

    # Handle Ctrl+C and console close events
    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)
    if sys.platform == "win32":
        signal.signal(signal.SIGBREAK, _shutdown)

    here = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
    script   = os.path.join(here, "main.py")
    log_path = os.path.join(here, "bot.log")

    python = _find_python()

    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"\n{'='*60}\n")
        log.write(f"ATC Bot started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"{'='*60}\n")

        if not python:
            msg = "ERROR: Python interpreter not found in PATH.\n"
            log.write(msg)
            print(msg)
            return

        log.write(f"Python: {python}\n")
        log.write(f"Script: {script}\n\n")
        log.flush()

        print(f"ATC Bot running — output in bot.log")
        print(f"Press Ctrl+C or close this window to stop.\n")

        kwargs = {"cwd": here, "stdout": log, "stderr": subprocess.STDOUT}
        proc = subprocess.Popen([python, "-u", script], **kwargs)

        try:
            proc.wait()
        except KeyboardInterrupt:
            _shutdown()

        log.write(f"\nBot exited with code {proc.returncode} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


if __name__ == "__main__":
    main()
