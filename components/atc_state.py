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
    FREQ_TOWER, MSA_FT, MAGNETIC_VAR,
    BOT_LAT, BOT_LON,
)
from airfield_db import _on_runway, navaid_summary, runway_to_heading

# Runway heading and its reciprocal — used for approach detection on either end
_RWY_HEADING = runway_to_heading(ACTIVE_RUNWAY)
_RWY_RECIP   = (_RWY_HEADING + 180) % 360

# Seconds without a Tacview position update before a strip is considered stale
# (aircraft crashed, disconnected, or left the Tacview range)
STRIP_STALE_TIMEOUT = 30



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
    last_tacview_update: float = 0.0  # monotonic timestamp of last Tacview position sync

    def update_from_tacview(self, ac):
        """Sync positional data from a TacviewClient AircraftState object."""
        self.altitude_actual = ac.alt_ft
        self.speed_kts = ac.speed_kts
        self.heading = ac.heading
        self.lat = ac.lat
        self.lon = ac.lon
        self.last_tacview_update = time.monotonic()
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

        # Aircraft detected on approach via geometry (not via radio contact)
        # Each entry: {callsign, dist_nm, alt_ft, heading, runway}
        self.detected_approaches: List[dict] = []

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
        approaches: list[dict] = []

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

            # Detect aircraft on approach from geometry
            approach_info = self._detect_approach(ac)
            if approach_info:
                approaches.append(approach_info)

        # Update runway state: first occupant is landing, second is lined up
        self.active_runway.landing_callsign  = on_rwy[0] if len(on_rwy) > 0 else ""
        self.active_runway.line_up_callsign  = on_rwy[1] if len(on_rwy) > 1 else ""

        # Update detected approaches
        self.detected_approaches = approaches

        # Build arrival sequence from all aircraft on approach (known + detected),
        # ordered by distance to field (closest first).
        self._update_arrival_sequence(approaches)

        # Purge stale strips — aircraft that crashed, disconnected, or left the area.
        # A strip is stale if it had a Tacview position at some point but hasn't been
        # updated for STRIP_STALE_TIMEOUT seconds.
        self._purge_stale_strips()

    def _purge_stale_strips(self):
        """Remove strips whose Tacview object has disappeared (crash/disconnect)."""
        now = time.monotonic()
        stale = [
            cs for cs, strip in self.strips.items()
            if strip.last_tacview_update > 0
            and (now - strip.last_tacview_update) > STRIP_STALE_TIMEOUT
        ]
        for cs in stale:
            logger.info(f"Purging stale strip: {cs} (no Tacview update for >{STRIP_STALE_TIMEOUT}s)")
            del self.strips[cs]
            # Also clean up queues
            if cs in self.departure_queue:
                self.departure_queue.remove(cs)
            if cs in self.arrival_sequence:
                self.arrival_sequence.remove(cs)

    def sync_aerodromes(self, tacview_aerodromes: list):
        """Update the list of known friendly aerodromes from Tacview."""
        self.friendly_aerodromes = [
            {"name": a.name or a.object_id, "lat": a.lat, "lon": a.lon}
            for a in tacview_aerodromes
            if a.lat != 0.0 or a.lon != 0.0
        ]

    def _update_arrival_sequence(self, detected_approaches: list):
        """
        Build and maintain the arrival sequence from all aircraft on approach.

        Combines:
          - Known strips that are geometrically on approach
          - Unannounced detected approaches

        Ordered by distance to field (closest = #1).
        Aircraft that are no longer on approach are removed.
        """
        # Gather known strips on approach with their distance
        candidates: list[tuple[float, str, bool]] = []  # (dist, callsign, has_radio_contact)

        for strip in self.strips.values():
            if strip.lat == 0.0 and strip.lon == 0.0:
                continue
            if strip.speed_kts < 100 or strip.speed_kts > 400:
                continue
            dist = self._dist_nm(strip.lat, strip.lon, BOT_LAT, BOT_LON)
            if dist > 15 or dist < 0.3:
                continue
            alt_agl = strip.altitude_actual - AIRPORT_ELEVATION_FT
            if alt_agl > 5000 or alt_agl < 50:
                continue
            hdg_mag = (strip.heading - MAGNETIC_VAR + 360) % 360
            brg_to_ac = self._bearing_true(BOT_LAT, BOT_LON, strip.lat, strip.lon)
            for rwy_hdg in (_RWY_HEADING, _RWY_RECIP):
                if self._angle_diff(hdg_mag, rwy_hdg) > 20:
                    continue
                approach_bearing = (rwy_hdg + 180) % 360
                if self._angle_diff(brg_to_ac, approach_bearing) > 30:
                    continue
                candidates.append((dist, strip.callsign, True))
                break

        # Add detected (unannounced) approaches
        for ap in detected_approaches:
            # Avoid duplicates — skip if callsign matches a known strip
            is_known = any(
                cs in ap["callsign"] or ap["callsign"] in cs
                for cs in self.strips
            )
            if not is_known:
                candidates.append((ap["dist_nm"], ap["callsign"], False))

        # Sort by distance (closest first)
        candidates.sort(key=lambda x: x[0])
        self.arrival_sequence = [c[1] for c in candidates]

    def number_one_landed(self) -> Optional[str]:
        """
        Check if the current #1 in the arrival sequence has landed and vacated.
        Returns the callsign of the NEW #1 (previously #2) if the old #1 is gone,
        or None if #1 is still on approach or no sequence exists.

        An aircraft is considered landed+vacated when it was in the arrival
        sequence but is no longer geometrically on approach AND is no longer
        on the runway.
        """
        if len(self.arrival_sequence) < 2:
            return None

        old_n1 = self.arrival_sequence[0]

        # Is old #1 still on approach?
        still_on_approach = False
        for strip in self.strips.values():
            if strip.callsign != old_n1 and old_n1 not in strip.callsign:
                continue
            dist = self._dist_nm(strip.lat, strip.lon, BOT_LAT, BOT_LON)
            alt_agl = strip.altitude_actual - AIRPORT_ELEVATION_FT
            if 0.3 < dist < 15 and 50 < alt_agl < 5000 and strip.speed_kts >= 100:
                still_on_approach = True
            break

        # Also check detected approaches
        if not still_on_approach:
            for ap in self.detected_approaches:
                if old_n1 in ap["callsign"] or ap["callsign"] in old_n1:
                    still_on_approach = True
                    break

        # Is old #1 still on the runway?
        on_runway = (
            old_n1 in self.active_runway.landing_callsign
            or old_n1 in self.active_runway.line_up_callsign
        )

        if not still_on_approach and not on_runway:
            # #1 has landed and vacated — return the new #1
            return self.arrival_sequence[1] if len(self.arrival_sequence) > 1 else None

        return None

    # ------------------------------------------------------------------
    # Approach detection from geometry
    # ------------------------------------------------------------------

    @staticmethod
    def _angle_diff(a: float, b: float) -> float:
        """Smallest signed difference between two headings in degrees."""
        d = (a - b + 180) % 360 - 180
        return abs(d)

    def _detect_approach(self, ac) -> Optional[dict]:
        """
        Detect if an aircraft appears to be on a landing approach based on geometry.
        Checks both the active runway heading and its reciprocal.

        Criteria:
          - Aircraft is airborne ("Air" type, alt > 100ft)
          - Within 15nm of the field
          - Aircraft heading aligned with runway heading (±20°) on either end
          - Aircraft is approaching FROM the correct side (bearing from field ≈ reciprocal
            of the runway heading the aircraft is aligned with)
          - Altitude below 5000ft AGL
          - Speed below 400kts (not a high-speed flyby)

        Returns a dict with approach info, or None.
        """
        if "Air" not in ac.type_str or not ac.is_airborne:
            return None
        if ac.lat == 0.0 and ac.lon == 0.0:
            return None

        dist = self._dist_nm(ac.lat, ac.lon, BOT_LAT, BOT_LON)
        if dist > 15 or dist < 0.5:
            return None

        alt_agl = ac.alt_ft - AIRPORT_ELEVATION_FT
        if alt_agl > 5000 or alt_agl < 50:
            return None

        # Approach speeds: C-130 ~120kts, naval fighters ~130kts, fast jets ~170kts
        # Use 100kts floor to catch all types; below that is likely taxiing or hovering
        if ac.speed_kts > 400 or ac.speed_kts < 100:
            return None

        # Magnetic heading of the aircraft
        ac_hdg_mag = (ac.heading - MAGNETIC_VAR + 360) % 360

        # True bearing from field to aircraft
        brg_to_ac = self._bearing_true(BOT_LAT, BOT_LON, ac.lat, ac.lon)

        # --- Overhead break detection ---
        # Aircraft flies the landing direction over/near the field at 800-1200ft AGL, 300-400kts
        if (dist < 3
                and 800 <= alt_agl <= 1200
                and 300 <= ac.speed_kts <= 400
                and self._angle_diff(ac_hdg_mag, _RWY_HEADING) <= 20):
            label = (ac.pilot or ac.group or ac.name or ac.object_id).upper()
            return {
                "callsign": label,
                "dist_nm":  round(dist, 1),
                "alt_ft":   round(ac.alt_ft),
                "heading":  round(ac_hdg_mag),
                "speed_kts": round(ac.speed_kts),
                "runway":   ACTIVE_RUNWAY,
                "type":     ac.name or "",
                "pattern":  "overhead_break",
            }

        # Check alignment with either runway direction
        for rwy_hdg, rwy_label in [(_RWY_HEADING, ACTIVE_RUNWAY),
                                    (_RWY_RECIP, self._reciprocal_designator(ACTIVE_RUNWAY))]:
            # Aircraft heading should match the runway heading (flying toward the field)
            if self._angle_diff(ac_hdg_mag, rwy_hdg) > 20:
                continue

            # Aircraft should be behind the approach end:
            # bearing from field to aircraft ≈ reciprocal of runway heading (±30°)
            approach_bearing = (rwy_hdg + 180) % 360
            if self._angle_diff(brg_to_ac, approach_bearing) > 30:
                continue

            # Glide slope check: nominal 3° with ±4° tolerance (valid: ~0° to 7°)
            dist_ft = dist * 6076.12  # nm to feet
            glide_angle = math.degrees(math.atan2(alt_agl, dist_ft))
            if glide_angle > 7.0:
                continue  # too steep — not on a realistic approach

            label = (ac.pilot or ac.group or ac.name or ac.object_id).upper()
            return {
                "callsign": label,
                "dist_nm":  round(dist, 1),
                "alt_ft":   round(ac.alt_ft),
                "heading":  round(ac_hdg_mag),
                "speed_kts": round(ac.speed_kts),
                "runway":   rwy_label,
                "type":     ac.name or "",
                "pattern":  "approach",
            }

        return None

    @staticmethod
    def _bearing_true(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """True bearing in degrees from point 1 to point 2."""
        lat1r, lat2r = math.radians(lat1), math.radians(lat2)
        dlon = math.radians(lon2 - lon1)
        x = math.sin(dlon) * math.cos(lat2r)
        y = math.cos(lat1r) * math.sin(lat2r) - math.sin(lat1r) * math.cos(lat2r) * math.cos(dlon)
        return (math.degrees(math.atan2(x, y)) + 360) % 360

    @staticmethod
    def _reciprocal_designator(runway: str) -> str:
        """Convert runway designator to its reciprocal (e.g. '28' → '10', '10L' → '28R')."""
        num_str = ""
        suffix = ""
        for ch in runway:
            if ch.isdigit():
                num_str += ch
            else:
                suffix = ch
                break
        if not num_str:
            return runway
        recip = (int(num_str) + 18) % 36
        if recip == 0:
            recip = 36
        suffix_map = {"L": "R", "R": "L", "C": "C"}
        recip_suffix = suffix_map.get(suffix.upper(), "")
        return f"{recip:02d}{recip_suffix}"

    # ------------------------------------------------------------------
    # Approach conflict detection
    # ------------------------------------------------------------------

    @staticmethod
    def _time_to_touchdown(dist_nm: float, speed_kts: float) -> float:
        """Estimate seconds until touchdown given distance and ground speed."""
        if speed_kts < 10:
            return float("inf")
        return (dist_nm / speed_kts) * 3600

    def find_number_one(self) -> Optional[FlightStrip]:
        """
        Find the #1 aircraft in the landing pattern — the closest known strip
        that is geometrically on approach to either runway end.
        Returns None if no known aircraft is on approach.
        """
        candidates = []
        for strip in self.strips.values():
            if strip.lat == 0.0 and strip.lon == 0.0:
                continue
            # Approach speeds: C-130 ~120kts, naval fighters ~130kts, fast jets ~170kts
            # Use 100kts floor to catch all types on approach
            if strip.speed_kts < 100 or strip.speed_kts > 400:
                continue

            dist = self._dist_nm(strip.lat, strip.lon, BOT_LAT, BOT_LON)
            if dist > 15 or dist < 0.3:
                continue

            alt_agl = strip.altitude_actual - AIRPORT_ELEVATION_FT
            if alt_agl > 5000 or alt_agl < 50:
                continue

            # Magnetic heading
            hdg_mag = (strip.heading - MAGNETIC_VAR + 360) % 360

            # Check alignment with either runway direction
            brg_to_ac = self._bearing_true(BOT_LAT, BOT_LON, strip.lat, strip.lon)
            for rwy_hdg in (_RWY_HEADING, _RWY_RECIP):
                if self._angle_diff(hdg_mag, rwy_hdg) > 20:
                    continue
                approach_bearing = (rwy_hdg + 180) % 360
                if self._angle_diff(brg_to_ac, approach_bearing) > 30:
                    continue
                candidates.append((dist, strip))
                break

        if not candidates:
            return None
        # Closest to the field is #1
        candidates.sort(key=lambda x: x[0])
        return candidates[0][1]

    def check_approach_conflicts(self) -> List[dict]:
        """
        Check for conflicts between the #1 in pattern and unannounced traffic.

        Returns a list of conflict dicts:
          {type, number1_callsign, threat_callsign, threat_dist_nm, threat_alt_ft,
           threat_speed_kts, threat_runway, time_to_touchdown_threat, time_to_touchdown_n1}

        Conflict types:
          - "runway_incursion": unannounced aircraft is on/entering the runway
          - "approach_conflict": unannounced aircraft TTD within 30s of #1's TTD
        """
        number1 = self.find_number_one()
        if not number1:
            return []

        n1_dist = self._dist_nm(number1.lat, number1.lon, BOT_LAT, BOT_LON)
        n1_ttd = self._time_to_touchdown(n1_dist, number1.speed_kts)

        conflicts = []

        # Check runway incursion by unannounced aircraft
        if self.active_runway.landing_callsign:
            rwy_occupant = self.active_runway.landing_callsign
            # Is the occupant a known strip? If not, it's unannounced
            is_known = any(
                cs in rwy_occupant or rwy_occupant in cs
                for cs in self.strips
            )
            if not is_known and n1_dist < 5:
                conflicts.append({
                    "type":                "runway_incursion",
                    "number1_callsign":    number1.callsign,
                    "threat_callsign":     rwy_occupant,
                    "threat_dist_nm":      0,
                    "threat_alt_ft":       AIRPORT_ELEVATION_FT,
                    "threat_speed_kts":    0,
                    "threat_runway":       self.active_runway.designator,
                    "time_to_touchdown_threat": 0,
                    "time_to_touchdown_n1": round(n1_ttd),
                })

        # Check detected approach conflicts
        for ap in self.detected_approaches:
            # Skip if this is actually the #1 aircraft
            if number1.callsign in ap["callsign"] or ap["callsign"] in number1.callsign:
                continue

            ap_ttd = self._time_to_touchdown(ap["dist_nm"], ap["speed_kts"])

            # Conflict if both aircraft's TTD are within 30 seconds of each other
            if abs(ap_ttd - n1_ttd) < 30:
                conflicts.append({
                    "type":                "approach_conflict",
                    "number1_callsign":    number1.callsign,
                    "threat_callsign":     ap["callsign"],
                    "threat_dist_nm":      ap["dist_nm"],
                    "threat_alt_ft":       ap["alt_ft"],
                    "threat_speed_kts":    ap["speed_kts"],
                    "threat_runway":       ap["runway"],
                    "time_to_touchdown_threat": round(ap_ttd),
                    "time_to_touchdown_n1": round(n1_ttd),
                })

        return conflicts

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

        if self.detected_approaches:
            lines.append(f"\nDETECTED APPROACHES (no radio contact — from radar):")
            for ap in sorted(self.detected_approaches, key=lambda a: a["dist_nm"]):
                pattern_tag = "OVERHEAD BREAK" if ap.get("pattern") == "overhead_break" else "APPROACH"
                lines.append(
                    f"  {ap['callsign']} | {ap['type']} | "
                    f"RWY {ap['runway']} | {ap['dist_nm']}nm | "
                    f"ALT {ap['alt_ft']}ft | HDG {ap['heading']} | "
                    f"SPD {ap['speed_kts']}kts | {pattern_tag} | NO RADIO CONTACT"
                )

        return "\n".join(lines)
