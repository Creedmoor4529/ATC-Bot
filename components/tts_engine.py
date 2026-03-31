"""
Text-to-speech engine using Piper TTS (local, offline).

Piper is a fast neural TTS engine. This module shells out to the
piper executable and returns PCM audio bytes (16-bit, 16kHz, mono)
ready for transmission through SRS.

Setup:
  1. Download piper from https://github.com/rhasspy/piper/releases
  2. Extract piper.exe into the piper/ folder
  3. Download a voice model (.onnx + .onnx.json) into piper/voices/
     Recommended: en_US-amy-medium  (clear, neutral female voice)
     or en_GB-alan-medium           (British male, suits ATC style)

Config (in .env):
  PIPER_EXE=piper/piper.exe
  PIPER_VOICE=piper/voices/en_US-amy-medium.onnx
"""

import asyncio
import io
import logging
import os
import re
import struct
import subprocess
import tempfile
import wave

from config import PIPER_EXE, PIPER_VOICE, AUDIO_SAMPLE_RATE

logger = logging.getLogger(__name__)

_DIGIT_WORDS = {
    '0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
    '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine',
}

def _expand_numbers(text: str) -> str:
    """Replace digit sequences with hyphenated spoken form for TTS.
    e.g. '13' → 'one-three', '1001' → 'one-zero-zero-one'
    """
    def _spell(match: re.Match) -> str:
        digits = match.group(0)
        words = [_DIGIT_WORDS[d] for d in digits]
        return words[0] if len(words) == 1 else '-'.join(words)
    return re.sub(r'\d+', _spell, text)


def _run_piper_sync(text: str) -> bytes:
    """
    Run piper synchronously and return raw PCM bytes (16-bit, 16kHz, mono).
    Uses a temp WAV file as output, then strips the WAV header.
    """
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        cmd = [
            PIPER_EXE,
            "--model", PIPER_VOICE,
            "--output_file", tmp_path,
        ]
        result = subprocess.run(
            cmd,
            input=text.encode("utf-8"),
            capture_output=True,
            timeout=30,
        )
        if result.returncode != 0:
            logger.error(
                f"Piper failed (rc={result.returncode}): "
                f"{result.stderr.decode('utf-8', errors='replace')}"
            )
            return b""

        return _wav_to_pcm(tmp_path)
    finally:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def _wav_to_pcm(wav_path: str) -> bytes:
    """Read a WAV file and return raw 16-bit PCM bytes, resampled to 16kHz if needed."""
    with wave.open(wav_path, "rb") as wf:
        src_rate = wf.getframerate()
        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        frames = wf.readframes(wf.getnframes())

    # Convert stereo to mono if needed
    if channels == 2:
        samples = memoryview(frames).cast("h")  # 16-bit signed
        mono = bytes(
            struct.pack("<h", (samples[i] + samples[i + 1]) // 2)
            for i in range(0, len(samples), 2)
        )
        frames = mono

    # Resample if source rate differs from target
    if src_rate != AUDIO_SAMPLE_RATE:
        frames = _resample_pcm(frames, src_rate, AUDIO_SAMPLE_RATE)

    return frames


def _resample_pcm(pcm: bytes, src_rate: int, dst_rate: int) -> bytes:
    """Polyphase resampler for 16-bit mono PCM (anti-aliased)."""
    if src_rate == dst_rate:
        return pcm
    import math
    import numpy as np
    from scipy.signal import resample_poly
    g = math.gcd(src_rate, dst_rate)
    up, down = dst_rate // g, src_rate // g
    samples = np.frombuffer(pcm, dtype="<i2").astype(np.float32)
    resampled = resample_poly(samples, up, down)
    return np.clip(resampled, -32768, 32767).astype(np.int16).tobytes()




async def synthesize(text: str) -> bytes:
    """
    Synthesize text to PCM audio bytes asynchronously.
    Returns 16-bit, 16kHz, mono PCM bytes, or empty bytes on failure.
    """
    if not text.strip():
        return b""
    text = _expand_numbers(text)
    loop = asyncio.get_event_loop()
    try:
        pcm = await loop.run_in_executor(None, _run_piper_sync, text)
        return pcm
    except Exception as e:
        logger.error(f"TTS synthesis error: {e}")
        return b""


def check_piper_available() -> bool:
    """Return True if the piper executable and voice model are present."""
    if not os.path.isfile(PIPER_EXE):
        logger.error(f"Piper executable not found: {PIPER_EXE}")
        return False
    if not os.path.isfile(PIPER_VOICE):
        logger.error(f"Piper voice model not found: {PIPER_VOICE}")
        return False
    return True
