"""
ATC Bot launcher — starts main.py silently with output redirected to bot.log.
Compile to exe with:  pyinstaller --onefile --noconsole --name "ATC Bot" launcher.py
"""

import os
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


def main():
    here = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
    script   = os.path.join(here, "main.py")
    log_path = os.path.join(here, "bot.log")

    python = _find_python()

    with open(log_path, "a", encoding="utf-8") as log:
        log.write(f"\n{'='*60}\n")
        log.write(f"ATC Bot started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"{'='*60}\n")

        if not python:
            log.write("ERROR: Python interpreter not found in PATH.\n")
            return

        log.write(f"Python: {python}\n")
        log.write(f"Script: {script}\n\n")
        log.flush()

        kwargs = {"stdout": log, "stderr": subprocess.STDOUT, "cwd": here}
        if sys.platform == "win32":
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        proc = subprocess.Popen([python, script], **kwargs)
        proc.wait()
        log.write(f"\nBot exited with code {proc.returncode} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


if __name__ == "__main__":
    main()
