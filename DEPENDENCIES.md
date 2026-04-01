# Dependencies

A full list of everything the bot depends on and where to get it.

---

## Software Requirements

| Software | Version | Purpose | Download |
|----------|---------|---------|----------|
| **Windows** | 10 or 11 | Host OS | — |
| **Python** | 3.11+ | Runtime | [python.org](https://www.python.org/downloads/) |
| **DCS World** | Any | Simulation | [digitalcombatsimulator.com](https://www.digitalcombatsimulator.com/) |
| **SRS** | Latest | Radio comms | [dcssimpleradio.com](http://dcssimpleradio.com/) |
| **Tacview** | Any with real-time telemetry | Live traffic feed | [tacview.net](https://www.tacview.net/) |

> The bot itself can run on Linux — only DCS World requires Windows. See the README for Linux setup.

---

## AI Provider (choose one)

| Provider | Cost | Sign-up |
|----------|------|---------|
| **Groq** | Free tier | [console.groq.com](https://console.groq.com/) |
| **Ollama** | Free, local | [ollama.com](https://ollama.com/) |
| **OpenAI** | Paid | [platform.openai.com](https://platform.openai.com/) |

Set `AI_PROVIDER` in `config.lua`. Add your API key to `.env`.

---

## Python Packages

Installed automatically by `install.bat` / `install.sh` via `pip install -r requirements.txt`.

| Package | Purpose |
|---------|---------|
| `openai>=1.30.0` | OpenAI and Groq API client |
| `faster-whisper>=1.1.0` | Speech-to-text (STT) via CTranslate2 |
| `python-dotenv>=1.0.0` | `.env` file loading |
| `opuslib>=3.0.1` | Opus audio codec (SRS audio) |
| `numpy>=1.24.0` | Audio array processing |
| `scipy>=1.10.0` | Audio resampling (22050→16000 Hz for Whisper) |

---

## Automatically Downloaded by Installer

These are fetched by `install.bat` / `install.sh` and do not need to be installed manually.

| Component | What it is | Source |
|-----------|-----------|--------|
| **Piper TTS** | Text-to-speech binary (`piper/piper.exe`) | [github.com/rhasspy/piper](https://github.com/rhasspy/piper/releases) |
| **en_US-amy-medium voice** | Piper voice model (`.onnx` + `.onnx.json`) | HuggingFace rhasspy/piper-voices |
| **Whisper model** | `distil-large-v3` weights — downloaded on first run | HuggingFace via `faster-whisper` package |

---

## Optional — Building the Launcher EXE

Only needed if you want to compile `ATC Bot.exe` instead of running `python main.py`.

```
pip install pyinstaller
build_launcher.bat
```

---

## Native Library — Opus

The Opus audio codec requires a native shared library alongside the Python `opuslib` package.

| Platform | Library file | Notes |
|----------|-------------|-------|
| Windows | `opus.dll` | Included in this repo |
| Linux | `libopus.so` | Install via `sudo apt install libopus0` or equivalent |
