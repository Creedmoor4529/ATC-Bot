"""
DCS ATC Bot — main orchestrator.

Startup sequence:
  1. Connect to Tacview (real-time aircraft feed)
  2. Connect to SRS (radio audio bot)
  3. Preload Whisper STT model
  4. Enter main event loop:
     - Receive SRS audio → Whisper STT → ATC Brain → Piper TTS → SRS transmit
     - Continuously sync Tacview data into ATC state

Usage:
  1. Copy .env.example to .env and fill in your values
  2. Install dependencies:  pip install -r requirements.txt
  3. Download Piper + voice model (see components/tts_engine.py)
  4. Start DCS + Tacview + SRS server
  5. python main.py
"""

import os
import sys

# On Windows, add project root to PATH so ctypes can find opus.dll
if sys.platform == "win32":
    _project_root = os.path.dirname(os.path.abspath(__file__))
    os.environ["PATH"] = _project_root + os.pathsep + os.environ.get("PATH", "")

import asyncio
import logging
import signal
from collections import deque

import numpy as np
import opuslib

from components.atc_brain import ATCBrain
from components.atc_state import ATCState
from components.srs_client import SRSAudioBot, SRSClient, SRSRadio, MODULATION_AM
from components.stt_engine import transcribe, preload as preload_whisper
from components.tacview_client import TacviewClient
from components.dcs_export import DCSWeather, DCSExportListener
from components.tts_engine import synthesize, check_piper_available
from config import (
    ATC_CALLSIGN, AUDIO_SAMPLE_RATE, SRS_COALITION,
    FREQ_GROUND, FREQ_GROUND_2, FREQ_TOWER, FREQ_TOWER_2,
    FREQ_APPROACH, FREQ_APPROACH_2,
    BOT_LAT, BOT_LON, BOT_ALT,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
# Suppress noisy third-party loggers
for _noisy in ("httpcore", "httpx", "openai._base_client"):
    logging.getLogger(_noisy).setLevel(logging.WARNING)
logger = logging.getLogger("atc_main")

# How many seconds of silence before we process a transmission
SILENCE_TIMEOUT = 1.2
# Minimum audio duration to attempt STT (seconds)
MIN_AUDIO_DURATION = 0.5
# Opus frame duration
OPUS_FRAME_MS = 40

_BASE = ATC_CALLSIGN.rsplit(" ", 1)[0]  # e.g. "BATUMI" from "BATUMI APPROACH"
ATC_FREQUENCIES = [
    SRSRadio(frequency=FREQ_APPROACH,   modulation=MODULATION_AM, name="Approach",   callsign=f"{_BASE} APPROACH"),
    SRSRadio(frequency=FREQ_APPROACH_2, modulation=MODULATION_AM, name="Approach 2", callsign=f"{_BASE} APPROACH"),
    SRSRadio(frequency=FREQ_TOWER,      modulation=MODULATION_AM, name="Tower",      callsign=f"{_BASE} TOWER"),
    SRSRadio(frequency=FREQ_TOWER_2,    modulation=MODULATION_AM, name="Tower 2",    callsign=f"{_BASE} TOWER"),
    SRSRadio(frequency=FREQ_GROUND,     modulation=MODULATION_AM, name="Ground",     callsign=f"{_BASE} GROUND"),
    SRSRadio(frequency=FREQ_GROUND_2,   modulation=MODULATION_AM, name="Ground 2",   callsign=f"{_BASE} GROUND"),
]


class AudioAccumulator:
    """
    Accumulates incoming Opus audio frames from SRS and fires a callback
    when a complete transmission is detected (silence timeout).
    """

    def __init__(self, on_transmission, sample_rate=AUDIO_SAMPLE_RATE):
        self._on_transmission = on_transmission
        self._sample_rate = sample_rate
        self._buffer: list[bytes] = []
        self._decoder = opuslib.Decoder(sample_rate, 1)
        self._silence_task: asyncio.Task | None = None
        self._frequency: float = 0.0
        self._guid: str = ""

    def feed(self, opus_bytes: bytes, frequency: float, guid: str = ""):
        """Called for each incoming Opus packet."""
        try:
            pcm = self._decoder.decode(opus_bytes, AUDIO_SAMPLE_RATE * OPUS_FRAME_MS // 1000)
            self._buffer.append(pcm)
            self._frequency = frequency
            if not self._guid:
                self._guid = guid  # capture GUID from first packet of transmission
        except Exception as e:
            logger.debug(f"Opus decode error: {e}")

        # Reset silence timer
        if self._silence_task and not self._silence_task.done():
            self._silence_task.cancel()
        loop = asyncio.get_running_loop()
        self._silence_task = loop.create_task(self._silence_expire())

    async def _silence_expire(self):
        await asyncio.sleep(SILENCE_TIMEOUT)
        if not self._buffer:
            return
        pcm_all = b"".join(self._buffer)
        guid = self._guid
        self._buffer.clear()
        self._guid = ""
        duration = len(pcm_all) / (self._sample_rate * 2)
        if duration >= MIN_AUDIO_DURATION:
            asyncio.create_task(self._on_transmission(pcm_all, self._frequency, guid))


READBACK_WINDOW = 10.0  # seconds to wait for pilot readback

class ATCBot:
    def __init__(self):
        self.state = ATCState()
        self.brain = ATCBrain()
        self.tacview = TacviewClient()
        self.weather = DCSWeather()
        self.dcs_export = DCSExportListener(self.weather)
        self.accumulator = AudioAccumulator(self._on_transmission)
        # pending readbacks keyed by frequency: {clearance, pilot_callsign, atc_callsign, radio_index, expires}
        self._pending_readbacks: dict[float, dict] = {}
        # altitude-hold queue: aircraft told to maintain altitude awaiting runway clearance
        # each entry: {callsign, radio_index, sequence}
        self._altitude_hold_queue: list[dict] = []

        srs_client_obj = SRSClient(
            name=_BASE,
            radios=ATC_FREQUENCIES,
            coalition=SRS_COALITION,
            lat=BOT_LAT,
            lon=BOT_LON,
            alt=BOT_ALT,
        )
        self.srs = SRSAudioBot(
            client=srs_client_obj,
            on_audio_received=self.accumulator.feed,
        )

    async def start(self):
        logger.info("=== DCS ATC Bot starting ===")

        if not check_piper_available():
            logger.error(
                "Piper TTS not found. See components/tts_engine.py for setup instructions."
            )
            sys.exit(1)

        logger.info("Preloading Whisper STT model...")
        await asyncio.get_running_loop().run_in_executor(None, preload_whisper)

        logger.info("Starting DCS weather export listener...")
        await self.dcs_export.start()

        logger.info("Connecting to Tacview...")
        try:
            await self.tacview.connect()
        except Exception as e:
            logger.warning(f"Tacview connection failed: {e} — continuing without live traffic.")

        logger.info("Connecting to SRS...")
        await self.srs.connect()

        logger.info(f"ATC Bot online. Callsign: {ATC_CALLSIGN}")
        logger.info(f"Monitoring {len(ATC_FREQUENCIES)} frequencies:")
        for r in ATC_FREQUENCIES:
            logger.info(f"  {r.name}: {r.frequency / 1e6:.3f} MHz")

        # Periodic Tacview sync + reconnect
        asyncio.create_task(self._tacview_loop())
        # SRS reconnect monitor
        asyncio.create_task(self._srs_reconnect_loop())
        # DCS server heartbeat monitor
        asyncio.create_task(self._dcs_heartbeat_monitor_loop())
        # Altitude-hold release monitor
        asyncio.create_task(self._altitude_hold_monitor_loop())

    async def stop(self):
        logger.info("Shutting down...")
        self.dcs_export.stop()
        await self.srs.disconnect()
        await self.tacview.disconnect()

    async def _tacview_loop(self):
        """Sync Tacview data while connected; reconnect with backoff when dropped."""
        delay = 5
        while True:
            if self.tacview._running:
                await asyncio.sleep(2)
                try:
                    self.state.sync_tacview(self.tacview.get_all_aircraft())
                    self.state.sync_aerodromes(self.tacview.get_blue_aerodromes())
                except Exception as e:
                    logger.debug(f"Tacview sync error: {e}")
                delay = 5
            else:
                logger.info(f"Tacview disconnected — reconnecting in {delay}s...")
                await asyncio.sleep(delay)
                delay = min(delay * 2, 60)
                try:
                    await self.tacview.connect()
                    logger.info("Tacview reconnected.")
                    delay = 5
                except Exception as e:
                    logger.warning(f"Tacview reconnect failed: {e}")

    async def _dcs_heartbeat_monitor_loop(self):
        """Log a warning when DCS stops sending export packets, and when it resumes."""
        from components.dcs_export import DCS_HEARTBEAT_TIMEOUT
        was_alive = False
        ever_seen = False
        # Wait one full timeout period before first check so startup noise settles.
        await asyncio.sleep(DCS_HEARTBEAT_TIMEOUT)
        while True:
            await asyncio.sleep(30)
            alive = self.weather.is_alive
            if alive:
                ever_seen = True
            if not ever_seen:
                logger.warning(
                    f"DCS export: no packets received yet on UDP {self.dcs_export.port}. "
                    "Check dcs_atc_export.lua is loaded and BOT_HOST points to this machine."
                )
            elif was_alive and not alive:
                logger.warning(
                    f"DCS heartbeat lost — no export packet for >{DCS_HEARTBEAT_TIMEOUT}s. "
                    "Is DCS running and dcs_atc_export.lua loaded?"
                )
            elif not was_alive and alive:
                logger.info("DCS heartbeat restored — export packets resuming.")
            was_alive = alive

    async def _srs_reconnect_loop(self):
        """Detect SRS disconnection and reconnect with backoff."""
        delay = 5
        while True:
            await asyncio.sleep(5)
            if not self.srs._running:
                logger.info(f"SRS disconnected — reconnecting in {delay}s...")
                await asyncio.sleep(delay)
                delay = min(delay * 2, 60)
                try:
                    try:
                        await self.srs.disconnect()
                    except Exception:
                        pass
                    await self.srs.connect()
                    logger.info("SRS reconnected.")
                    delay = 5
                except Exception as e:
                    logger.warning(f"SRS reconnect failed: {e}")

    async def _on_transmission(self, pcm_bytes: bytes, frequency: float, guid: str = ""):
        """
        Full pipeline: PCM audio → STT → ATC Brain → TTS → SRS transmit.
        """
        import time as _time
        logger.info(f"Processing transmission ({len(pcm_bytes)//2} samples, {frequency/1e6:.3f} MHz)")

        # 1. Speech-to-text
        text = await transcribe(pcm_bytes)
        if not text:
            logger.info("STT returned empty — skipping.")
            return
        logger.info(f"Pilot said: {text!r}")

        # 1a. Drop pure courtesy phrases — no ATC response needed.
        _COURTESY_ONLY = {
            "thank you", "thanks", "thank you very much", "thanks very much",
            "good day", "goodbye", "bye", "cheers", "seeya", "see ya",
        }
        if text.strip().rstrip(".!").lower() in _COURTESY_ONLY:
            logger.info("Courtesy phrase — no response.")
            return

        # 1b. Check for pending readback on this frequency
        pending = self._pending_readbacks.get(frequency)
        if pending and _time.monotonic() < pending["expires"]:
            del self._pending_readbacks[frequency]
            logger.info(f"Readback received: {text!r}")
            reply = await self.brain.verify_readback(
                clearance=pending["clearance"],
                readback=text,
                pilot_callsign=pending["pilot_callsign"],
                atc_callsign=pending["atc_callsign"],
            )
            if reply:
                logger.info(f"Readback reply: {reply!r}")
                pcm_reply = await synthesize(reply)
                if pcm_reply:
                    await self.srs.transmit(pcm_reply, radio_index=pending["radio_index"])
            return

        # 2. Resolve pilot callsign.
        # Primary: look up the transmitting SRS client GUID → DCS name → callsign (before |).
        # Fallback: extract from STT text if GUID not in registry (e.g. not yet synced).
        pilot_callsign = None
        srs_dcs_name = self.srs.client_name(guid) if guid else ""
        if srs_dcs_name:
            # DCS format: "callsign | pilot_name | squad | ..." — first part is the radio callsign
            pilot_callsign = srs_dcs_name.split("|")[0].strip()
            logger.debug(f"SRS GUID lookup: {guid[:8]}.. → {srs_dcs_name!r} → callsign={pilot_callsign!r}")

        if not pilot_callsign:
            # Fallback: extract from transcribed text.
            # Strategy: find last APPROACH/TOWER/GROUND service word, take the token(s) after it.
            _SERVICE_WORDS = {"APPROACH", "TOWER", "GROUND", "CONTROL", "RADAR", "DIRECTOR"}
            _MESSAGE_WORDS = {
                "REQUEST", "INBOUND", "WITH", "DESCEND", "CLIMB", "MAINTAIN",
                "SQUAWK", "ROGER", "WILCO", "NEGATIVE", "AFFIRM", "REPORT",
                "DECLARE", "EMERGENCY", "MAYDAY", "PAN", "CONFIRM", "CHECKING",
            }
            words_clean = [w.rstrip(".,") for w in text.upper().split()]
            service_idx = None
            for i, w in enumerate(words_clean):
                if w in _SERVICE_WORDS:
                    service_idx = i
            if service_idx is not None and service_idx + 1 < len(words_clean):
                parts = []
                for w in words_clean[service_idx + 1:]:
                    if w in _MESSAGE_WORDS or w in _SERVICE_WORDS:
                        break
                    parts.append(w)
                    if len(parts) == 2:
                        break
                if parts:
                    pilot_callsign = " ".join(parts)
            if not pilot_callsign:
                _STATION_WORDS = {w.upper() for radio in ATC_FREQUENCIES for w in (radio.callsign or "").split()}
                _STATION_WORDS.update(_SERVICE_WORDS)
                for w in words_clean:
                    if w not in _STATION_WORDS and w not in _MESSAGE_WORDS:
                        pilot_callsign = w
                        break

        # 3. Determine which radio/service this transmission is on
        radio_index = self._frequency_to_radio_index(frequency)
        atc_callsign = ATC_FREQUENCIES[radio_index].callsign or ATC_CALLSIGN

        # 4. Update ATC state
        if pilot_callsign:
            self.state.update_strip_contact(pilot_callsign)

        # 5. Generate ATC response

        apt_lat = BOT_LAT
        apt_lon = BOT_LON
        ac_type = ""
        if pilot_callsign and pilot_callsign in self.state.strips:
            ac_type = self.state.strips[pilot_callsign].aircraft_type
        atc_snapshot = self.state.context_snapshot(airport_lat=apt_lat, airport_lon=apt_lon, requesting_aircraft_type=ac_type)
        traffic = self.tacview.traffic_summary(airport_lat=apt_lat, airport_lon=apt_lon, radius_nm=150.0)
        logger.debug(f"Traffic summary ({len(self.tacview.objects)} Tacview objects, apt={apt_lat:.3f},{apt_lon:.3f}):\n{traffic}")

        response = await self.brain.respond(
            pilot_transmission=text,
            atc_state_snapshot=atc_snapshot,
            traffic_summary=traffic,
            weather=self.weather.snapshot(),
            pilot_callsign=pilot_callsign,
            atc_callsign=atc_callsign,
        )
        if not response:
            return
        logger.info(f"ATC response: {response!r}")

        # 5b. Altitude-hold queue management
        if pilot_callsign:
            _resp_lower = response.lower()
            # Detect "maintain [altitude]" — add to hold queue
            if ("maintain" in _resp_lower and
                    ("angel" in _resp_lower or "altitude" in _resp_lower or "feet" in _resp_lower) and
                    not any(e["callsign"] == pilot_callsign for e in self._altitude_hold_queue)):
                seq = len(self._altitude_hold_queue) + 1
                self._altitude_hold_queue.append({
                    "callsign":    pilot_callsign,
                    "radio_index": radio_index,
                    "sequence":    seq,
                })
                logger.info(f"Altitude hold: {pilot_callsign} queued (#{seq})")
            # Detect landing clearance — remove from hold queue
            if "cleared to land" in _resp_lower or "cleared for landing" in _resp_lower:
                before = len(self._altitude_hold_queue)
                self._altitude_hold_queue = [
                    e for e in self._altitude_hold_queue if e["callsign"] != pilot_callsign
                ]
                if len(self._altitude_hold_queue) < before:
                    logger.info(f"Altitude hold: {pilot_callsign} cleared to land, removed from queue")

        # 6. TTS synthesis
        pcm_response = await synthesize(response)
        if not pcm_response:
            logger.warning("TTS produced no audio.")
            return

        # 7. Transmit on the same frequency the pilot used
        await self.srs.transmit(pcm_response, radio_index=radio_index)

        # 8. Open readback window for READBACK_WINDOW seconds
        # Don't open a window for rejections — there's nothing to read back.
        _rejection_phrases = ("unable", "negative", "no position data", "say again callsign", "standby")
        _is_rejection = any(p in response.lower() for p in _rejection_phrases)
        if pilot_callsign and not _is_rejection:
            import time as _time
            self._pending_readbacks[frequency] = {
                "clearance":      response,
                "pilot_callsign": pilot_callsign,
                "atc_callsign":   atc_callsign,
                "radio_index":    radio_index,
                "expires":        _time.monotonic() + READBACK_WINDOW,
            }

    async def _altitude_hold_monitor_loop(self):
        """
        Background loop: when the runway clears, proactively issue landing clearance
        to the next aircraft in the altitude-hold queue (in sequence order).
        """
        import time as _time
        _prev_clear = True
        _last_release = 0.0
        while True:
            await asyncio.sleep(5)
            if not self._altitude_hold_queue:
                _prev_clear = self.state.runway_clear()
                continue
            runway_clear = self.state.runway_clear()
            runway_just_cleared = runway_clear and not _prev_clear
            # Also release if somehow the queue is stale and runway has been clear a while
            stale_hold = runway_clear and (_time.monotonic() - _last_release) > 60
            if runway_just_cleared or stale_hold:
                await self._release_next_altitude_hold()
                _last_release = _time.monotonic()
            _prev_clear = runway_clear

    async def _release_next_altitude_hold(self):
        """Issue a proactive landing clearance to the next queued altitude-hold aircraft."""
        if not self._altitude_hold_queue:
            return
        entry = self._altitude_hold_queue.pop(0)
        # Re-number remaining entries
        for i, e in enumerate(self._altitude_hold_queue):
            e["sequence"] = i + 1

        pilot_callsign = entry["callsign"]
        radio_index    = entry["radio_index"]
        sequence       = entry["sequence"]
        atc_callsign   = ATC_FREQUENCIES[radio_index].callsign or ATC_CALLSIGN

        apt_lat = BOT_LAT
        apt_lon = BOT_LON
        ac_type = self.state.strips[pilot_callsign].aircraft_type if pilot_callsign in self.state.strips else ""
        atc_snapshot = self.state.context_snapshot(airport_lat=apt_lat, airport_lon=apt_lon, requesting_aircraft_type=ac_type)
        traffic      = self.tacview.traffic_summary(airport_lat=apt_lat, airport_lon=apt_lon, radius_nm=150.0)

        seq_word = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}.get(sequence, str(sequence))
        instruction = (
            f"The runway is now clear. Issue landing clearance to {pilot_callsign}, "
            f"number {seq_word} in sequence. Use the active runway."
        )
        logger.info(f"Releasing altitude hold: {pilot_callsign} (#{sequence})")
        clearance = await self.brain.proactive_clearance(
            clearance_instruction=instruction,
            atc_state_snapshot=atc_snapshot,
            traffic_summary=traffic,
            pilot_callsign=pilot_callsign,
            atc_callsign=atc_callsign,
        )
        if not clearance:
            return
        pcm = await synthesize(clearance)
        if not pcm:
            return
        await self.srs.transmit(pcm, radio_index=radio_index)
        # Open a readback window on that frequency
        import time as _time
        freq = ATC_FREQUENCIES[radio_index].frequency
        self._pending_readbacks[freq] = {
            "clearance":      clearance,
            "pilot_callsign": pilot_callsign,
            "atc_callsign":   atc_callsign,
            "radio_index":    radio_index,
            "expires":        _time.monotonic() + READBACK_WINDOW,
        }

    def _frequency_to_radio_index(self, frequency: float) -> int:
        """Find the radio index closest to the given frequency."""
        best = 0
        best_diff = float("inf")
        for i, radio in enumerate(ATC_FREQUENCIES):
            diff = abs(radio.frequency - frequency)
            if diff < best_diff:
                best_diff = diff
                best = i
        return best


async def main():
    bot = ATCBot()

    loop = asyncio.get_running_loop()

    def _shutdown():
        logger.info("Shutdown signal received.")
        asyncio.create_task(bot.stop())

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _shutdown)
        except NotImplementedError:
            # Windows doesn't support add_signal_handler for all signals
            pass

    await bot.start()

    try:
        await asyncio.Event().wait()  # run forever
    except KeyboardInterrupt:
        await bot.stop()


if __name__ == "__main__":
    asyncio.run(main())
