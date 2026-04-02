"""
ATC state manager.

Maintains the operational picture:
  - Active strips (aircraft that have made contact)
  - Runway state (active runway, aircraft on approach/departure)
  - Squawk assignments
  - Clearances issued

This is the source of truth the ATC brain uses to stay consistent
across multiple transmissions.
"""

import math
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from config import (
    AIRPORT_ICAO, ACTIVE_RUNWAY,
    TACAN_CHANNEL, TACAN_INBOUND_COURSE, TACAN_MDA_FT, AIRPORT_ELEVATION_FT,
    FREQ_TOWER, MSA_FT,
)
from airfield_db import _on_runway, navaid_summary



class FlightPhase(Enum):
    UNKNOWN = "unknown"
    STARTUP = "startup"
    TAXI_OUT = "taxi_out"
    HOLDING_SHORT = "holding_short"
    DEPARTURE = "departure"
    AIRBORNE = "airborne"
    INBOUND = "inbound"
    APPROACH = "approach"
    FINAL = "final"
    LANDING = "landing"
    VACATING = "vacating"
    TAXI_IN = "taxi_in"
    PARKED = "parked"


@dataclass
class FlightStrip:
    callsign: str
    aircraft_type: str = "UNKN"
    phase: FlightPhase = FlightPhase.UNKNOWN
    departure: str = ""
    destination: str = ""
    altitude_cleared: int = 0       # feet
    altitude_actual: float = 0.0    # feet (from Tacview)
    speed_kts: float = 0.0
    heading: float = 0.0
    lat: float = 0.0
    lon: float = 0.0
    runway_assigned: str = ""
    taxi_route: str = ""
    clearance_notes: List[str] = field(default_factory=list)
    first_contact: float = field(default_factory=time.time)
    last_contact: float = field(default_factory=time.time)

    def update_from_tacview(self, ac):
        """Sync positional data from a TacviewClient AircraftState object."""
        self.altitude_actual = ac.alt_ft
        self.speed_kts = ac.speed_kts
        self.heading = ac.heading
        self.lat = ac.lat
        self.lon = ac.lon
        if not self.aircraft_type or self.aircraft_type == "UNKN":
            self.aircraft_type = ac.name or "UNKN"

    def add_note(self, note: str):
        self.clearance_notes.append(f"[{time.strftime('%H:%M:%S')}] {note}")
        if len(self.clearance_notes) > 20:
            self.clearance_notes.pop(0)

    def recent_notes(self, n: int = 5) -> str:
        return "\n".join(self.clearance_notes[-n:]) if self.clearance_notes else "None"


@dataclass
class RunwayState:
    designator: str       # e.g. "13" or "31L"
    in_use_departure: bool = True
    in_use_arrival: bool = True
    line_up_callsign: str = ""    # aircraft currently lined up
    landing_callsign: str = ""    # aircraft on short final / landing


class ATCState:
    """Central state object shared between all ATC components."""

    def __init__(self):
        self.airport_icao: str = AIRPORT_ICAO
        self.active_runway: RunwayState = RunwayState(designator=ACTIVE_RUNWAY)
        self.strips: Dict[str, FlightStrip] = {}
        # Queues
        self.departure_queue: List[str] = []     # callsigns waiting for takeoff
        self.arrival_sequence: List[str] = []    # callsigns on approach sequence

        # Known friendly aerodromes (populated from Tacview)
        self.friendly_aerodromes: List[dict] = []  # [{name, lat, lon}]

    # ------------------------------------------------------------------
    # Strip management
    # ------------------------------------------------------------------

    def get_or_create_strip(self, callsign: str) -> FlightStrip:
        callsign = callsign.upper()
        if callsign not in self.strips:
            self.strips[callsign] = FlightStrip(callsign=callsign)
        return self.strips[callsign]

    def update_strip_contact(self, callsign: str):
        strip = self.get_or_create_strip(callsign)
        strip.last_contact = time.time()

    # ------------------------------------------------------------------
    # Runway management
    # ------------------------------------------------------------------

    def set_active_runway(self, designator: str):
        self.active_runway = RunwayState(designator=designator)

    def runway_clear(self) -> bool:
        return (
            not self.active_runway.line_up_callsign
            and not self.active_runway.landing_callsign
        )

    # ------------------------------------------------------------------
    # Queue management
    # ------------------------------------------------------------------

    def add_to_departure_queue(self, callsign: str):
        if callsign not in self.departure_queue:
            self.departure_queue.append(callsign)

    def next_for_departure(self) -> Optional[str]:
        return self.departure_queue[0] if self.departure_queue else None

    def cleared_for_departure(self, callsign: str):
        if callsign in self.departure_queue:
            self.departure_queue.remove(callsign)
        self.active_runway.line_up_callsign = callsign

    def add_to_arrival_sequence(self, callsign: str):
        if callsign not in self.arrival_sequence:
            self.arrival_sequence.append(callsign)

    # ------------------------------------------------------------------
    # Sync with Tacview
    # ------------------------------------------------------------------

    def sync_tacview(self, tacview_aircraft: list):
        """Update strip positional data from Tacview objects and runway occupancy."""
        on_rwy: list[str] = []

        for ac in tacview_aircraft:
            label = (ac.pilot or ac.group or "").upper()
            if not label:
                continue
            # Match to existing strip by callsign substring
            for callsign, strip in self.strips.items():
                if callsign in label or label in callsign:
                    strip.update_from_tacview(ac)
                    break

            # Check runway occupancy — ignore stationary aircraft not in our strips
            if _on_runway(ac.lat, ac.lon, ac.alt_ft, AIRPORT_ELEVATION_FT, self.airport_icao):
                is_known = any(cs in label or label in cs for cs in self.strips)
                if is_known or ac.speed_kts > 5:
                    on_rwy.append(label)

        # Update runway state: first occupant is landing, second is lined up
        self.active_runway.landing_callsign  = on_rwy[0] if len(on_rwy) > 0 else ""
        self.active_runway.line_up_callsign  = on_rwy[1] if len(on_rwy) > 1 else ""

    def sync_aerodromes(self, tacview_aerodromes: list):
        """Update the list of known friendly aerodromes from Tacview."""
        self.friendly_aerodromes = [
            {"name": a.name or a.object_id, "lat": a.lat, "lon": a.lon}
            for a in tacview_aerodromes
            if a.lat != 0.0 or a.lon != 0.0
        ]

    # ------------------------------------------------------------------
    # Context snapshot for LLM
    # ------------------------------------------------------------------

    @staticmethod
    def _dist_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        return math.degrees(2 * math.asin(math.sqrt(a))) * 60

    def context_snapshot(self, airport_lat: float = 0.0, airport_lon: float = 0.0, requesting_aircraft_type: str = "") -> str:
        tower_mhz = f"{FREQ_TOWER / 1e6:.3f}"
        lines = [
            f"Airport: {self.airport_icao}",
            f"Elevation: {AIRPORT_ELEVATION_FT}ft",
            f"Minimum safe altitude: {MSA_FT}ft",
            f"Active runway: {self.active_runway.designator}",
            f"Runway clear: {self.runway_clear()}"
            + (f" | On runway: {self.active_runway.landing_callsign}" if self.active_runway.landing_callsign else "")
            + (f", {self.active_runway.line_up_callsign}" if self.active_runway.line_up_callsign else ""),
            f"Tower frequency: {tower_mhz} MHz",
        ]
        nav_str = navaid_summary(self.airport_icao, requesting_aircraft_type)
        if nav_str:
            lines.append(f"Navaids: {nav_str}")
        if TACAN_CHANNEL:
            # Enforce minimum safe MDA of 1200 ft regardless of database value
            tacan_mda = max(TACAN_MDA_FT, 1200)
            lines.append(
                f"TACAN approach: channel {TACAN_CHANNEL} | "
                f"inbound course {TACAN_INBOUND_COURSE:03d}° | "
                f"MDA {tacan_mda}ft"
            )

        if self.friendly_aerodromes:
            names = ", ".join(a["name"] for a in self.friendly_aerodromes)
            lines.append(f"Friendly aerodromes: {names}")

        if self.departure_queue:
            lines.append(f"Departure queue: {', '.join(self.departure_queue)}")
        if self.arrival_sequence:
            lines.append(f"Arrival sequence: {', '.join(self.arrival_sequence)}")

        active_strips = [s for s in self.strips.values()
                         if s.phase != FlightPhase.PARKED]
        if active_strips:
            lines.append(f"\nKnown aircraft ({len(active_strips)}):")
            for s in active_strips:
                dist_str = ""
                if airport_lat and airport_lon and (s.lat != 0.0 or s.lon != 0.0):
                    dist = self._dist_nm(s.lat, s.lon, airport_lat, airport_lon)
                    dist_str = f" | DIST {dist:.0f}nm"
                lines.append(
                    f"  {s.callsign} | {s.aircraft_type} | {s.phase.value} | "
                    f"ALT {s.altitude_actual:.0f}ft | HDG {s.heading:.0f}{dist_str}"
                )

        return "\n".join(lines)
