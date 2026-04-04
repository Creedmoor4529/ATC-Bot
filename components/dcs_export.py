"""
DCS Lua weather export receiver.

Listens for UDP packets sent by dcs_atc_export.lua (installed in
DCS Saved Games/Scripts/Hooks/) and maintains a live weather picture
for the active airport.

Data received (JSON):
  wind_dir       — wind direction FROM, degrees true
  wind_speed_ms  — wind speed in m/s
  pressure_hpa   — QNH in hPa (static pressure at field elevation)
  temp_c         — temperature in °C
"""

import asyncio
import json
import logging
import socket
import time

from config import MAGNETIC_VAR, DCS_EXPORT_PORT, DCS_CHAT_ENABLED, DCS_CHAT_PORT, DCS_CHAT_HOST

logger = logging.getLogger(__name__)

# Seconds without a DCS packet before the connection is considered lost.
# The Lua hook sends every 30 s, so 90 s = 3 missed intervals.
DCS_HEARTBEAT_TIMEOUT = 90


class DCSWeather:
    """Holds the latest weather and airbase data received from DCS."""

    def __init__(self):
        self.wind_dir_true: float = 0.0     # degrees true, wind FROM
        self.wind_speed_ms: float = 0.0     # m/s
        self.pressure_hpa: float = 1013.25  # hPa
        self.temp_c: float = 15.0           # °C
        self._has_data: bool = False
        self.last_seen: float = 0.0         # monotonic time of last received packet

    @property
    def is_alive(self) -> bool:
        """True if a packet has been received within the heartbeat timeout."""
        return self.last_seen > 0 and (time.monotonic() - self.last_seen) < DCS_HEARTBEAT_TIMEOUT

    @property
    def wind_speed_kts(self) -> float:
        return self.wind_speed_ms * 1.94384

    @property
    def wind_dir_mag(self) -> float:
        """Wind direction FROM, magnetic."""
        return (self.wind_dir_true - MAGNETIC_VAR + 360) % 360

    @property
    def qnh_inhg(self) -> float:
        return self.pressure_hpa * 0.02953

    def update(self, data: dict):
        self.last_seen = time.monotonic()
        if "status" in data:
            logger.info(f"DCS hook status: {data['status']}")
            return
        self.wind_dir_true = float(data.get("wind_dir", 0.0))
        self.wind_speed_ms = float(data.get("wind_speed_ms", 0.0))
        self.pressure_hpa = float(data.get("pressure_hpa", 1013.25))
        self.temp_c = float(data.get("temp_c", 15.0))
        self._has_data = True
        logger.debug(
            f"Weather update: wind {self.wind_dir_mag:.0f}°M "
            f"{self.wind_speed_kts:.0f}kts, QNH {self.pressure_hpa:.0f}hPa, "
            f"temp {self.temp_c:.0f}°C"
        )

    def snapshot(self) -> str:
        """Human-readable weather string for injection into LLM context."""
        if not self._has_data:
            return "Weather: not available from DCS"
        spd = self.wind_speed_kts
        wind_str = "calm" if spd < 1 else f"{self.wind_dir_mag:03.0f} at {spd:.0f} knots"
        return (
            f"Wind: {wind_str} | "
            f"QNH: {self.pressure_hpa:.0f} hPa / {self.qnh_inhg:.2f} inHg | "
            f"Temperature: {self.temp_c:.0f}°C"
        )


class DCSExportListener:
    """Async UDP listener that feeds weather packets into a DCSWeather instance."""

    def __init__(self, weather: DCSWeather, port: int = DCS_EXPORT_PORT):
        self.weather = weather
        self.port = port
        self._transport = None

    async def start(self):
        loop = asyncio.get_event_loop()
        try:
            self._transport, _ = await loop.create_datagram_endpoint(
                lambda: _WeatherProtocol(self.weather),
                local_addr=("0.0.0.0", self.port),
            )
            logger.info(f"DCS weather export listener on UDP 0.0.0.0:{self.port}")
        except Exception as e:
            logger.warning(f"DCS export listener failed (port {self.port}): {e} — weather unavailable")

    def stop(self):
        if self._transport:
            self._transport.close()


class _WeatherProtocol(asyncio.DatagramProtocol):
    def __init__(self, weather: DCSWeather):
        self.weather = weather

    def datagram_received(self, data: bytes, addr):
        try:
            msg = json.loads(data.decode("utf-8"))
            if "error" in msg:
                logger.debug(f"DCS export error: {msg['error']}")
                return
            self.weather.update(msg)
        except Exception as e:
            # DCS internal errors arrive as raw Lua error strings, not JSON
            logger.debug(f"DCS export: ignoring non-JSON packet ({len(data)} bytes)")

    def error_received(self, exc):
        logger.debug(f"DCS export socket error: {exc}")


class DCSChatSender:
    """Sends text messages to the DCS Lua hook for in-game chat display."""

    def __init__(self, dcs_host: str = DCS_CHAT_HOST, port: int = DCS_CHAT_PORT):
        self.enabled = DCS_CHAT_ENABLED
        self._host = dcs_host
        self._port = port
        self._sock: socket.socket | None = None
        if self.enabled:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            logger.info(f"DCS chat sender ready → {self._host}:{self._port}")

    def send(self, message: str):
        """Send a chat message to the DCS hook. Silently drops if disabled or errored."""
        if not self.enabled or not self._sock:
            return
        try:
            self._sock.sendto(message.encode("utf-8"), (self._host, self._port))
        except Exception as e:
            logger.debug(f"DCS chat send error: {e}")
