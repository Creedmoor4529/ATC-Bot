#!/usr/bin/env bash
set -e

echo "============================================================"
echo " DCS ATC Bot — Linux Installer"
echo "============================================================"
echo

# --- Detect arch -----------------------------------------------------------
ARCH=$(uname -m)
case "$ARCH" in
    x86_64)  PIPER_ARCH="x86_64" ;;
    aarch64) PIPER_ARCH="aarch64" ;;
    armv7l)  PIPER_ARCH="armv7l" ;;
    *)
        echo "[ERROR] Unsupported architecture: $ARCH"
        exit 1
        ;;
esac

# --- Check Python ----------------------------------------------------------
if ! command -v python3 &>/dev/null; then
    echo "[ERROR] Python 3 not found. Install with: sudo apt install python3 python3-pip"
    exit 1
fi
PYVER=$(python3 --version)
echo "[OK] $PYVER found."

# --- System dependencies ---------------------------------------------------
echo
echo "[1/4] Installing system dependencies..."
if command -v apt-get &>/dev/null; then
    sudo apt-get install -y libopus0 curl
elif command -v dnf &>/dev/null; then
    sudo dnf install -y opus curl
elif command -v pacman &>/dev/null; then
    sudo pacman -Sy --noconfirm opus curl
else
    echo "[WARN] Could not detect package manager. Make sure libopus is installed."
fi
echo "[OK] System dependencies ready."

# --- Install Python deps (always use a venv) -------------------------------
echo
echo "[2/4] Installing Python dependencies..."
if command -v apt-get &>/dev/null; then
    sudo apt-get install -y python3-venv 2>/dev/null || true
fi
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "[OK] Python dependencies installed (virtual environment: .venv/)"

# --- Download Piper --------------------------------------------------------
echo
echo "[3/4] Setting up Piper TTS..."
PIPER_VERSION="2023.11.14-2"
PIPER_URL="https://github.com/rhasspy/piper/releases/download/${PIPER_VERSION}/piper_linux_${PIPER_ARCH}.tar.gz"

if [ -f "piper/piper" ]; then
    echo "[OK] Piper already installed, skipping."
else
    echo "Downloading Piper for $ARCH..."
    curl -L "$PIPER_URL" -o /tmp/piper_linux.tar.gz
    tar -xzf /tmp/piper_linux.tar.gz
    rm /tmp/piper_linux.tar.gz
    chmod +x piper/piper
    if [ -f "piper/piper" ]; then
        echo "[OK] Piper installed."
    else
        echo "[ERROR] Piper extraction failed."
        exit 1
    fi
fi

# --- Read voice name from config.lua ---------------------------------------
VOICE_NAME="en_US-amy-medium"
if [ -f "config.lua" ]; then
    _v=$(grep -m1 '^PIPER_VOICE' config.lua | sed 's/.*=\s*//;s/["'"'"']//g;s/\s*--.*//' | xargs)
    [ -n "$_v" ] && VOICE_NAME="$_v"
fi

# --- Download voice model --------------------------------------------------
echo
echo "[4/4] Setting up voice model ($VOICE_NAME)..."
mkdir -p piper/voices

if [ -f "piper/voices/${VOICE_NAME}.onnx" ]; then
    echo "[OK] Voice model already present, skipping."
else
    # Parse voice name: en_US-amy-medium → en/en_US/amy/medium
    V_LOCALE=$(echo "$VOICE_NAME" | cut -d'-' -f1)        # en_US
    V_LANGPRE=$(echo "$V_LOCALE" | cut -d'_' -f1)         # en
    V_SPEAKER=$(echo "$VOICE_NAME" | cut -d'-' -f2)       # amy
    V_QUALITY=$(echo "$VOICE_NAME" | cut -d'-' -f3)       # medium
    VOICE_URL="https://huggingface.co/rhasspy/piper-voices/resolve/main/${V_LANGPRE}/${V_LOCALE}/${V_SPEAKER}/${V_QUALITY}"
    echo "Downloading voice model from HuggingFace..."
    echo "URL: $VOICE_URL"
    curl -L "${VOICE_URL}/${VOICE_NAME}.onnx"      -o "piper/voices/${VOICE_NAME}.onnx"
    curl -L "${VOICE_URL}/${VOICE_NAME}.onnx.json" -o "piper/voices/${VOICE_NAME}.onnx.json"
    if [ -f "piper/voices/${VOICE_NAME}.onnx" ]; then
        echo "[OK] Voice model downloaded."
    else
        echo "[ERROR] Voice model download failed."
        exit 1
    fi
fi

# --- Create .env -----------------------------------------------------------
echo
if [ -f ".env" ]; then
    echo "[OK] .env already exists, skipping."
else
    cp .env.example .env
    echo "[OK] .env created from .env.example — add your API key before starting."
fi

# --- Update Piper path in .env if not set ----------------------------------
if ! grep -q "^PIPER_EXE" .env; then
    echo "PIPER_EXE=piper/piper" >> .env
fi

# --- Create start.sh launcher ------------------------------------------------
cat > start.sh << 'LAUNCHER'
#!/usr/bin/env bash
# DCS ATC Bot — Linux launcher
cd "$(dirname "$0")"
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Run install.sh first."
    exit 1
fi
source .venv/bin/activate
exec python3 main.py
LAUNCHER
chmod +x start.sh
echo "[OK] start.sh created."

# --- Done ------------------------------------------------------------------
echo
echo "============================================================"
echo " Installation complete."
echo
echo " Next steps:"
echo "   1. Edit .env and add your API key (OPENAI_API_KEY or GROQ_API_KEY)"
echo "   2. Edit config.lua to set your airfield and frequencies"
echo "   3. Install dcs_atc_export.lua on the Windows DCS machine:"
echo "      %USERPROFILE%\\Saved Games\\DCS\\Scripts\\Hooks\\"
echo "   4. Set BOT_HOST in dcs_atc_export.lua to this machine's IP"
echo "   5. Run: ./start.sh"
echo "============================================================"
echo
