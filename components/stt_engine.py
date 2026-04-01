"""
Speech-to-text engine using faster-whisper (CTranslate2).

Accepts raw PCM audio bytes (16-bit, 16kHz, mono) and returns a transcript.
Runs transcription in a thread pool so it doesn't block the async event loop.
"""

import asyncio
import logging
import numpy as np
from faster_whisper import WhisperModel

from config import WHISPER_MODEL

logger = logging.getLogger(__name__)

_model = None


def _load_model():
    global _model
    if _model is None:
        logger.info(f"Loading faster-whisper model: {WHISPER_MODEL}")
        _model = WhisperModel(WHISPER_MODEL, device="auto", compute_type="auto")
        logger.info("faster-whisper model loaded.")
    return _model


def _transcribe_sync(pcm_bytes: bytes) -> str:
    """Synchronous transcription — runs in a thread pool."""
    model = _load_model()

    # Convert 16-bit PCM bytes to float32 numpy array normalised to [-1, 1]
    audio_np = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0

    segments, _info = model.transcribe(
        audio_np,
        language="en",
        beam_size=1,
        condition_on_previous_text=False,
    )
    text = " ".join(seg.text.strip() for seg in segments).strip()
    logger.debug(f"Transcript: {text!r}")
    return text


async def transcribe(pcm_bytes: bytes) -> str:
    """
    Transcribe PCM audio asynchronously.
    Returns the recognised text, or empty string on failure.
    """
    if not pcm_bytes:
        return ""
    loop = asyncio.get_running_loop()
    try:
        text = await loop.run_in_executor(None, _transcribe_sync, pcm_bytes)
        return text
    except Exception as e:
        logger.error(f"Whisper transcription error: {e}")
        return ""


def preload():
    """Call once at startup to warm up the model before first transmission."""
    _load_model()
