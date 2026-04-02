# DCS ATC Bot

An AI-powered air traffic controller for DCS World. The bot listens on SRS radio frequencies, transcribes pilot transmissions using faster-whisper STT, generates realistic ATC responses using an LLM, and broadcasts them back over SRS using Piper TTS.

---

## Requirements

- Windows 10/11
- [DCS World](https://www.digitalcombatsimulator.com/)
- [SRS (SimpleRadio Standalone)](http://dcssimpleradio.com/) — server must be running
- [Tacview](https://www.tacview.net/) — with real-time telemetry enabled
- Python 3.11+
- An AI provider account (OpenAI, Groq, or local Ollama)

---

## Installation

### 1. Run the install script

**Windows:**
```
install.bat
```

**Linux:**
```
chmod +x install.sh && ./install.sh
```

The install script will:
- Create a Python virtual environment (`.venv/`)
- Install Python dependencies
- Download and extract Piper TTS
- Download the `en_US-amy-medium` voice model
- Create `.env` from `.env.example`

#### NVIDIA GPU support (optional but recommended)

If you have an NVIDIA GPU, install CUDA dependencies for GPU-accelerated speech recognition. Without these, faster-whisper falls back to CPU which is significantly slower.

**Option A — Python packages (quickest, works on any distro):**
```
source .venv/bin/activate
pip install nvidia-cublas-cu12 nvidia-cudnn-cu12
```

**Option B — System CUDA toolkit:**

Ubuntu / Debian:
```
sudo apt install nvidia-cuda-toolkit
```

Fedora / RHEL:
```
sudo dnf install cuda-toolkit
```

Arch Linux:
```
sudo pacman -S cuda
```

#### Running the bot on Linux
```
source .venv/bin/activate
python3 main.py
```

> **Linux note:** DCS World is Windows-only. The bot can run on Linux and connect to an SRS server running on a Windows machine over the network. Set `BOT_HOST` in `dcs_atc_export.lua` to the Linux machine's IP address.

### 2. Install the DCS weather export hook

1. Copy `dcs_atc_export.lua` to:
   ```
   %USERPROFILE%\Saved Games\DCS_Server Instance\Scripts\Hooks\
   ```
2. Open the file and set `BOT_HOST`:
   - Same machine as DCS: `"127.0.0.1"`
   - Bot on a different machine: set to that machine's local IP (e.g. `"192.168.1.50"`)

### 4. Configure the bot

Copy `.env.example` to `.env` and fill in your API key:

```
OPENAI_API_KEY=sk-...       # if using OpenAI
GROQ_API_KEY=gsk_...        # if using Groq (free)
```

Then edit `config.lua` to match your airfield and preferences (see Configuration below).

### 5. Enable Tacview real-time telemetry

On a dedicated server, Tacview is configured via `options.lua` rather than the GUI. Open:

```
%USERPROFILE%\Saved Games\DCS_DEDICATED_SERVER\Config\Options.lua
```

Find the `["Tacview"]` block inside `["plugins"]` and set the following values:

```lua
["tacviewRealTimeTelemetryEnabled"] = true,
["tacviewRealTimeTelemetryPort"] = "42674",
["tacviewRemoteControlEnabled"] = true,
["tacviewRemoteControlPort"] = "42675",
["tacviewPlaybackDelay"] = 0,
```

> **Important:** `tacviewPlaybackDelay` must be `0`. Any non-zero value introduces a delay in the telemetry stream and the bot will not receive live position data.

If the `["Tacview"]` block does not exist, add it inside the `["plugins"]` table. Leave `["tacviewRealTimeTelemetryPassword"]` and `["tacviewRemoteControlPassword"]` as empty strings unless you want password protection.

---

## Configuration

All operational settings are in `config.lua`. The file is self-documented with a full airfield reference at the top.

### Key settings

| Setting | Description |
|---------|-------------|
| `AIRPORT_ICAO` | ICAO code of your airfield (see reference list in config.lua) |
| `ATC_CALLSIGN` | Base callsign e.g. `"ANAPA"` — bot appends APPROACH / TOWER / GROUND automatically |
| `ACTIVE_RUNWAY` | Active runway designator e.g. `"22"` |
| `MAGNETIC_VAR` | Magnetic variation in degrees east for your map |
| `TACAN_CHANNEL` | TACAN channel e.g. `"99X"` — set to `""` to disable |
| `TACAN_INBOUND_COURSE` | TACAN inbound course in magnetic degrees |
| `TACAN_MDA_FT` | Minimum descent altitude in feet |
| `AI_PROVIDER` | `"openai"`, `"groq"`, or `"ollama"` |
| `AI_MODEL` | Override the default model (optional) |
| `FREQ_APPROACH` | Approach frequency in Hz e.g. `131000000` |
| `FREQ_TOWER` | Tower frequency in Hz |
| `FREQ_GROUND` | Ground frequency in Hz |
| `INSTRUCTIONS` | Optional custom ATC instructions appended to the system prompt |

### AI Providers

| Provider | Cost | Setup |
|----------|------|-------|
| **Groq** | Free tier | Sign up at console.groq.com, add `GROQ_API_KEY` to `.env` |
| **Ollama** | Free, local | Install from ollama.com, run `ollama pull llama3.1` |
| **OpenAI** | Paid | Add `OPENAI_API_KEY` to `.env` |

Set `AI_PROVIDER` in `config.lua` to switch between them.

### Speech-to-Text (Whisper) Models

The bot uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) for speech recognition. Set `WHISPER_MODEL` in your `.env` to choose a model (default: `distil-large-v3`).

| Model | Size | Speed | Accuracy | VRAM |
|-------|------|-------|----------|------|
| `tiny` | 75 MB | Fastest | Low | ~1 GB |
| `base` | 142 MB | Very fast | Fair | ~1 GB |
| `small` | 466 MB | Fast | Good | ~2 GB |
| `medium` | 1.5 GB | Moderate | Very good | ~5 GB |
| `large-v3` | 3.1 GB | Slow | Best | ~10 GB |
| `distil-large-v3` | 1.5 GB | Fast | Near-best | ~4 GB |

Example `.env` setting:
```
WHISPER_MODEL=small
```

Models are downloaded automatically from HuggingFace on first run. Smaller models are faster but less accurate — `distil-large-v3` offers the best speed/accuracy tradeoff for ATC use.

### Custom Instructions

Add site-specific ATC rules to the `INSTRUCTIONS` field in `config.lua`:

```lua
INSTRUCTIONS = "Expect fast jet traffic. All aircraft report 10 nautical miles. Preferred approach is straight-in runway 22."
```

---

## Running the Bot

**Option A — Executable (recommended)**

Run `build_launcher.bat` once to compile the launcher, then double-click `ATC Bot.exe`.
The bot runs silently in the background. All output is written to `bot.log`.

**Option B — Command line**

```
python main.py
```

---

## How It Works

1. Bot connects to SRS and listens on all configured frequencies simultaneously
2. Pilot transmits on any ATC frequency
3. Audio is decoded and transcribed by faster-whisper STT (distil-large-v3)
4. Pilot callsign is extracted from the transmission
5. LLM generates an ATC response using live traffic data (Tacview) and weather (DCS export)
6. Piper TTS synthesises the response to audio
7. Bot transmits the audio back on the same frequency the pilot used
8. Bot callsign automatically matches the service: APPROACH, TOWER, or GROUND

---

## Frequencies

Set frequencies in `config.lua` to match your SRS server. Each service has a primary and secondary frequency:

```lua
FREQ_APPROACH   = 131000000   -- 131.000 MHz
FREQ_APPROACH_2 = 260000000   -- 260.000 MHz (UHF)
FREQ_TOWER      = 131000000
FREQ_TOWER_2    = 260000000
FREQ_GROUND     = 131000000
FREQ_GROUND_2   = 260000000
```

---

## Remote / Off-Site Hosting

The bot can run on a machine that is not on the same LAN as the DCS server. Each connection requires a different approach:

### SRS
No changes needed — SRS already connects to a hostname/IP and works over the internet.

### Tacview (TCP — bot connects outbound to DCS server)

1. On the DCS server's router, **forward TCP port 42674** to the DCS machine's LAN IP
2. In the bot's `.env`, set `TACVIEW_HOST` to the DCS server's public IP or DDNS hostname:
   ```
   TACVIEW_HOST=your-server.ddns.net
   ```

### DCS weather export (UDP — DCS server sends outbound to bot)

1. On the **bot machine's** router, **forward UDP port 15099** to the bot machine's LAN IP
2. In `dcs_atc_export.lua`, set `BOT_HOST` to the bot machine's **public IP or DDNS hostname**:
   ```lua
   local BOT_HOST = "your-bot-machine.ddns.net"
   ```
3. The default port `15099` can be changed by editing both `BOT_PORT` in `dcs_atc_export.lua` and `DCS_EXPORT_PORT` in `.env`

### Summary

| Connection | Direction | Port to forward | Where to forward |
|---|---|---|---|
| Tacview | Bot → DCS server | TCP 42674 on DCS router | DCS machine LAN IP |
| DCS weather export | DCS server → Bot | UDP 15099 on bot router | Bot machine LAN IP |
| SRS | Bot → SRS server | None (outbound only) | — |

---

## System Requirements

The bot runs alongside DCS World. The heaviest local component is **faster-whisper** (speech-to-text) — everything else is lightweight.

### Minimum (CPU-only, no dedicated GPU)

| Component | Requirement |
|-----------|-------------|
| **CPU** | 4-core, Intel 8th gen+ / Ryzen 2000+ |
| **RAM** | 8 GB |
| **GPU** | None required (Whisper runs on CPU, but slower) |
| **Storage** | ~2 GB for models + Python environment |

> On CPU-only systems, transcription with `distil-large-v3` will be slow (~3-5x real-time). Set `WHISPER_MODEL=small` or `base` in `.env` for faster results at the cost of accuracy.

### Recommended (with NVIDIA GPU)

| Component | Requirement |
|-----------|-------------|
| **CPU** | 4+ cores |
| **RAM** | 16 GB |
| **GPU** | NVIDIA with 4+ GB VRAM and CUDA support (e.g. GTX 1650 / RTX 3050) |
| **Storage** | ~2 GB for models + Python environment |

The bot auto-detects GPU availability (`device="auto"` in faster-whisper). With a CUDA-capable GPU, transcription is near real-time.

**Bottom line:** If your machine can run DCS, it can run the bot — especially with a smaller Whisper model like `small` or `base`.

---

## Troubleshooting

**Bot shows wrong callsign / old airfield name**
Your `.env` file may be overriding `config.lua`. Remove any `ATC_CALLSIGN`, `AIRPORT_ICAO`, or frequency entries from `.env` — these should only be in `config.lua`.

**No weather data**
Check `%USERPROFILE%\Saved Games\DCS_Server Instance\Logs\atc_export.log`. If it shows `socket=false`, the DCS Lua socket library is not available. Ensure DCS is not in a restricted export mode.

**STT not transcribing**
faster-whisper downloads the `distil-large-v3` model from HuggingFace on first run — this may take a few minutes. Check `bot.log` for errors.

**Piper not found**
Verify `piper/piper.exe` exists in the project root and the voice model is in `piper/voices/`.

**Bot not responding on radio**
- Confirm SRS server is running and the bot has connected (check `bot.log`)
- Confirm Tacview real-time telemetry is enabled
- Confirm frequencies in `config.lua` match the SRS frequencies you are transmitting on

---

## File Overview

| File | Purpose |
|------|---------|
| `config.lua` | Main user configuration — airfield, callsign, frequencies, AI provider |
| `.env` | Secret keys (API keys, server addresses) — never committed to git |
| `dcs_atc_export.lua` | DCS Lua hook — install to Saved Games/DCS_Server Instance/Scripts/Hooks/ |
| `main.py` | Bot entry point and audio pipeline |
| `components/atc_brain.py` | LLM interface — generates ATC responses |
| `components/atc_state.py` | Tracks aircraft strips, squawks, runway state |
| `components/tacview_client.py` | Reads live traffic from Tacview |
| `components/srs_client.py` | SRS radio audio send/receive |
| `components/stt_engine.py` | faster-whisper speech-to-text |
| `components/tts_engine.py` | Piper text-to-speech |
| `components/dcs_export.py` | Receives weather data from DCS |
| `components/airfield_db.py` | ICAO coordinate lookup table |
| `bot.log` | Runtime log — written when using the launcher exe |

---

## Development

This project was developed with [Claude.ai](https://claude.ai) (Anthropic).
