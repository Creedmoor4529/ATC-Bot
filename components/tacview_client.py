"""
Tacview real-time telemetry client.

Connects to Tacview's ACMI real-time export (TCP, default port 42674) and
maintains a live picture of all objects in the mission.

ACMI stream format:
  - Line-based text (UTF-8)
  - Handshake: server sends "XtraLib.Stream.0" header
  - Each frame begins with "#<timestamp>" and contains object updates
  - Object line format:  <id>,<property>=<value>,<property>=<value>,...
    - id=0 is the global/reference object (sets reference lat/lon/alt)
  - Removal line format: -<id>

Key properties tracked per object:
  T          - transform: lon|lat|alt or lon|lat|alt|roll|pitch|yaw|...
  Name       - type name (e.g. "F-16C_50")
  Pilot      - pilot/callsign
  Group      - group name
  Coalition  - Allies / Enemies / Neutral
  Type       - ACMI type string (e.g. "Air+FixedWing")
"""

import asyncio
import logging
import math
from dataclasses import dataclass, field
from typing import Dict, Optional

from config import TACVIEW_HOST, TACVIEW_PORT, TACVIEW_PASSWORD, MAGNETIC_VAR

logger = logging.getLogger(__name__)

HANDSHAKE_MAGIC = b"XtraLib.Stream.0"


def _bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Magnetic bearing in degrees from point 1 to point 2 (true − magnetic variation)."""
    lat1r, lat2r = math.radians(lat1), math.radians(lat2)
    dlon = math.radians(lon2 - lon1)
    x = math.sin(dlon) * math.cos(lat2r)
    y = math.cos(lat1r) * math.sin(lat2r) - math.sin(lat1r) * math.cos(lat2r) * math.cos(dlon)
    true_brg = (math.degrees(math.atan2(x, y)) + 360) % 360
    return (true_brg - MAGNETIC_VAR + 360) % 360


@dataclass
class AircraftState:
    object_id: str
    name: str = ""
    pilot: str = ""
    group: str = ""
    coalition: str = ""
    type_str: str = ""
    lat: float = 0.0
    lon: float = 0.0
    alt_m: float = 0.0     # metres MSL
    roll: float = 0.0
    pitch: float = 0.0
    heading: float = 0.0   # degrees true
    speed_ms: float = 0.0  # m/s
    timestamp: float = 0.0

    @property
    def alt_ft(self) -> float:
        return self.alt_m * 3.28084

    @property
    def speed_kts(self) -> float:
        return self.speed_ms * 1.94384

    @property
    def is_airborne(self) -> bool:
        return self.alt_ft > 100

    def summary(self, airport_lat: float = 0.0, airport_lon: float = 0.0) -> str:
        label = self.pilot or self.group or self.name or self.object_id
        base = (
            f"{label} | {self.type_str} | "
            f"HDG {self.heading:.0f} | "
            f"ALT {self.alt_ft:.0f}ft | "
            f"SPD {self.speed_kts:.0f}kts | "
            f"LAT {self.lat:.4f} LON {self.lon:.4f}"
        )
        if airport_lat and airport_lon:
            brg = _bearing(self.lat, self.lon, airport_lat, airport_lon)
            base += f" | MAG-BRG-TO-FIELD {brg:.0f}"
        return base


class TacviewClient:
    """
    Async Tacview ACMI real-time feed reader.
    Maintains self.objects: Dict[str, AircraftState] keyed by ACMI object id.
    """

    def __init__(self):
        self.objects: Dict[str, AircraftState] = {}
        self._ref_lat: float = 0.0
        self._ref_lon: float = 0.0
        self._ref_alt: float = 0.0
        self._current_timestamp: float = 0.0
        self._running = False
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None

    @property
    def ref_lat(self) -> float:
        return self._ref_lat

    @property
    def ref_lon(self) -> float:
        return self._ref_lon

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def connect(self):
        logger.info(f"Connecting to Tacview at {TACVIEW_HOST}:{TACVIEW_PORT}")
        self._reader, self._writer = await asyncio.open_connection(
            TACVIEW_HOST, TACVIEW_PORT
        )
        self._running = True
        await self._handshake()
        asyncio.create_task(self._read_loop())
        logger.info("Tacview connected.")

    async def disconnect(self):
        self._running = False
        if self._writer:
            self._writer.close()
            await self._writer.wait_closed()

    def get_airborne(self) -> list[AircraftState]:
        """Return all objects that appear to be airborne aircraft."""
        return [
            o for o in self.objects.values()
            if "Air" in o.type_str and o.is_airborne
        ]

    def get_all_aircraft(self) -> list[AircraftState]:
        """Return all objects typed as aircraft (airborne or not)."""
        return [o for o in self.objects.values() if "Air" in o.type_str]

    def get_blue_aerodromes(self) -> list[AircraftState]:
        """Return all blue-coalition aerodrome objects from the ACMI stream."""
        return [
            o for o in self.objects.values()
            if "Aerodrome" in o.type_str and o.coalition == "Allies"
        ]

    def traffic_summary(self, airport_lat: float = 0.0, airport_lon: float = 0.0, radius_nm: float = 150.0) -> str:
        """Human-readable traffic picture for injection into LLM context.
        Filters to aircraft within radius_nm of the airport position."""
        aircraft = self.get_all_aircraft()
        if airport_lat and airport_lon:
            aircraft = [a for a in aircraft if self._distance_nm(a.lat, a.lon, airport_lat, airport_lon) <= radius_nm]
        if not aircraft:
            return "No traffic within range."
        lines = [f"Traffic within {radius_nm:.0f}nm ({len(aircraft)} aircraft):"]
        for ac in sorted(aircraft, key=lambda a: self._distance_nm(a.lat, a.lon, airport_lat, airport_lon)):
            dist = self._distance_nm(ac.lat, ac.lon, airport_lat, airport_lon) if airport_lat else 0
            lines.append(f"  - {ac.summary(airport_lat, airport_lon)} | DIST {dist:.0f}nm")
        return "\n".join(lines)

    @staticmethod
    def _distance_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Approximate great-circle distance in nautical miles."""
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        return math.degrees(2 * math.asin(math.sqrt(a))) * 60

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    async def _handshake(self):
        # Read the full server greeting (terminated by \x00)
        server_hello = await self._reader.readuntil(b"\x00")
        logger.debug(f"Tacview server hello: {server_hello!r}")
        # Build client handshake — only include password line if set
        parts = ["XtraLib.Stream.0", "Tacview.RealTimeTelemetry.0", "DCS-ATC-Bot"]
        if TACVIEW_PASSWORD:
            parts.append(TACVIEW_PASSWORD)
        client_hello = "\n".join(parts) + "\n\x00"
        logger.debug(f"Tacview client hello: {client_hello!r}")
        self._writer.write(client_hello.encode("utf-8"))
        await self._writer.drain()

    async def _read_loop(self):
        lines_read = 0
        while self._running:
            try:
                line = await self._reader.readline()
                if not line:
                    logger.warning(f"Tacview stream ended after {lines_read} lines.")
                    break
                lines_read += 1
                if lines_read <= 5:
                    logger.debug(f"Tacview line {lines_read}: {line[:120]!r}")
                self._process_line(line.decode("utf-8", errors="replace").rstrip("\n\r"))
            except (asyncio.IncompleteReadError, ConnectionResetError):
                logger.warning("Tacview connection closed.")
                break
            except Exception as e:
                logger.error(f"Tacview read error: {e}")
        self._running = False

    def _process_line(self, line: str):
        if not line or line.startswith("//"):
            return

        # Timestamp marker
        if line.startswith("#"):
            try:
                self._current_timestamp = float(line[1:])
            except ValueError:
                pass
            return

        # Object removal
        if line.startswith("-"):
            obj_id = line[1:]
            self.objects.pop(obj_id, None)
            return

        # Object update: id,prop=val,...
        comma = line.find(",")
        if comma == -1:
            return
        obj_id = line[:comma]
        props_str = line[comma + 1:]

        if obj_id == "0":
            self._update_reference(props_str)
            return

        obj = self.objects.setdefault(obj_id, AircraftState(object_id=obj_id))
        self._apply_props(obj, props_str)
        obj.timestamp = self._current_timestamp

    def _update_reference(self, props_str: str):
        for prop in props_str.split(","):
            if "=" not in prop:
                continue
            key, val = prop.split("=", 1)
            key = key.strip()
            if key == "ReferenceLongitude":
                try:
                    self._ref_lon = float(val)
                except ValueError:
                    pass
            elif key == "ReferenceLatitude":
                try:
                    self._ref_lat = float(val)
                except ValueError:
                    pass
            elif key == "ReferenceAltitude":
                try:
                    self._ref_alt = float(val)
                except ValueError:
                    pass
            elif key == "T":
                parts = val.split("|")
                if len(parts) >= 1 and parts[0]:
                    self._ref_lon = float(parts[0])
                if len(parts) >= 2 and parts[1]:
                    self._ref_lat = float(parts[1])
                if len(parts) >= 3 and parts[2]:
                    self._ref_alt = float(parts[2])

    def _apply_props(self, obj: AircraftState, props_str: str):
        for prop in props_str.split(","):
            if "=" not in prop:
                continue
            key, val = prop.split("=", 1)
            key = key.strip()
            val = val.strip()

            if key == "T":
                self._parse_transform(obj, val)
            elif key == "Name":
                obj.name = val
            elif key == "Pilot":
                obj.pilot = val
            elif key == "Group":
                obj.group = val
            elif key == "Coalition":
                obj.coalition = val
            elif key == "Type":
                obj.type_str = val

    def _parse_transform(self, obj: AircraftState, val: str):
        """
        T value format: lon|lat|alt[|roll|pitch|yaw[|...]]
        Empty fields inherit from previous state.
        Coordinates are offsets from the reference point.
        Speed and heading are derived from consecutive position updates.
        """
        parts = val.split("|")

        def _get(idx: int, current: float) -> float:
            if idx < len(parts) and parts[idx] != "":
                return float(parts[idx])
            return current

        prev_lat = obj.lat
        prev_lon = obj.lon
        prev_ts  = obj.timestamp

        obj.lon = self._ref_lon + _get(0, obj.lon - self._ref_lon)
        obj.lat = self._ref_lat + _get(1, obj.lat - self._ref_lat)
        obj.alt_m = self._ref_alt + _get(2, obj.alt_m - self._ref_alt)

        if len(parts) >= 6:
            obj.roll    = _get(3, obj.roll)
            obj.pitch   = _get(4, obj.pitch)
            obj.heading = _get(5, obj.heading)

        # Derive speed and heading from position delta when we have a time reference
        dt = self._current_timestamp - prev_ts
        if dt > 0 and prev_lat != 0.0 and prev_lon != 0.0:
            dlat = (obj.lat - prev_lat) * 111_320          # degrees → metres
            dlon = (obj.lon - prev_lon) * 111_320 * math.cos(math.radians(obj.lat))
            dist = math.sqrt(dlat ** 2 + dlon ** 2)
            obj.speed_ms = dist / dt
            if dist > 0.1:                                  # only update heading if moving
                obj.heading = (math.degrees(math.atan2(dlon, dlat)) + 360) % 360
