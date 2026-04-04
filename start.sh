#!/usr/bin/env bash
# DCS ATC Bot — Linux launcher
# Activates the virtual environment and runs the bot.

cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Run install.sh first."
    exit 1
fi

source .venv/bin/activate
exec python3 main.py
