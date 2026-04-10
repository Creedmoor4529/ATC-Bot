import os
import re
import sys
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "components"))
from airfield_db import (
    MAP_AIRFIELDS as _MAP_AIRFIELDS,
    airfields_on_map as _airfields_on_map,
    lookup as _airfield_lookup,
    mag_var_lookup as _mag_var_lookup,
    maps_for_airfield as _maps_for_airfield,
    preferred_runway as _preferred_runway,
    runway_designators as _runway_designators,
    runway_to_heading as _runway_to_heading,
    tacan_lookup as _tacan_lookup,
    validate_airfield as _validate_airfield,
)

load_dotenv()

# ---------------------------------------------------------------------------
# Lua config loader
# Reads config.lua and returns a dict of key → value (str, int, or float).
# Priority: config.lua overrides .env defaults; .env still wins for secrets.
# ---------------------------------------------------------------------------

def _load_lua_config(path: str) -> dict:
    result = {}
    if not os.path.exists(path):
        return result
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("--"):
                continue
            # Strip inline comments
            line = re.sub(r"\s*--.*$", "", line).strip()
            m = re.match(r'^(\w+)\s*=\s*(.+)$', line)
            if not m:
                continue
            key, raw = m.group(1), m.group(2).strip().rstrip(",")
            if raw.startswith('"') or raw.startswith("'"):
                result[key] = raw.strip('"\'')
            elif raw == "true":
                result[key] = True
            elif raw == "false":
                result[key] = False
            else:
                try:
                    result[key] = int(raw) if "." not in raw else float(raw)
                except ValueError:
                    result[key] = raw
    return result

_cfg_dir = os.path.dirname(__file__)
_LUA = _load_lua_config(os.path.join(_cfg_dir, "config.lua"))
# config.local.lua overrides config.lua — user-specific settings go here
# so that config.lua can be updated freely via git pull.
_LUA.update(_load_lua_config(os.path.join(_cfg_dir, "config.local.lua")))

def _get(key: str, env_key: str, default, cast=str):
    """Resolve value: config.lua > .env > default."""
    if key in _LUA:
        return cast(_LUA[key]) if not isinstance(_LUA[key], cast) else _LUA[key]
    env_val = os.getenv(env_key)
    if env_val is not None:
        return cast(env_val)
    return default

# ---------------------------------------------------------------------------
# AI provider — driven by config.lua, secrets from .env
# ---------------------------------------------------------------------------
AI_PROVIDER  = _get("AI_PROVIDER",  "AI_PROVIDER",  "openai", str).lower()
OLLAMA_HOST  = _get("OLLAMA_HOST",  "OLLAMA_HOST",  "http://localhost:11434", str)

_DEFAULT_MODELS = {"openai": "gpt-4o-mini", "groq": "llama-3.3-70b-versatile", "ollama": "llama3.1"}
AI_MODEL = _get("AI_MODEL", "AI_MODEL", _DEFAULT_MODELS.get(AI_PROVIDER, "gpt-4o-mini"), str)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GROQ_API_KEY   = os.getenv("GROQ_API_KEY", "")

# Legacy alias
OPENAI_MODEL = AI_MODEL

# SRS
SRS_HOST         = os.getenv("SRS_HOST", "127.0.0.1")
SRS_PORT         = int(os.getenv("SRS_PORT", "5002"))
SRS_COALITION    = int(os.getenv("SRS_COALITION", "2"))
SRS_EAM_PASSWORD = os.getenv("SRS_EAM_PASSWORD", "")

# Tacview
TACVIEW_HOST     = os.getenv("TACVIEW_HOST", "127.0.0.1")
TACVIEW_PORT     = int(os.getenv("TACVIEW_PORT", "42674"))
TACVIEW_PASSWORD = os.getenv("TACVIEW_PASSWORD", "")

# Piper TTS
PIPER_EXE   = os.getenv("PIPER_EXE",   "piper/piper.exe")
_voice_name = _get("PIPER_VOICE", "PIPER_VOICE", "en_US-amy-medium", str)
# Accept bare voice name or full path
if os.sep in _voice_name or "/" in _voice_name:
    PIPER_VOICE = _voice_name
else:
    PIPER_VOICE = f"piper/voices/{_voice_name}.onnx"

# Whisper
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "distil-large-v3")

# Logging — set LOG_LEVEL in .env to DEBUG, INFO, WARNING, or ERROR (default: DEBUG)
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG").upper()

# Audio
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS    = 1

DCS_EXPORT_PORT = int(os.getenv("DCS_EXPORT_PORT", "15099"))
DCS_CHAT_ENABLED = _get("DCS_CHAT_ENABLED", "DCS_CHAT_ENABLED", True, bool)
DCS_CHAT_PORT    = _get("DCS_CHAT_PORT",    "DCS_CHAT_PORT",    15100, int)
DCS_CHAT_HOST    = os.getenv("DCS_CHAT_HOST", os.getenv("TACVIEW_HOST", "127.0.0.1"))

# ---------------------------------------------------------------------------
# Operational config — driven by config.lua, overridable via .env
# ---------------------------------------------------------------------------

ATC_CALLSIGN  = _get("ATC_CALLSIGN", "ATC_CALLSIGN", "ANAPA APPROACH", str)
AIRPORT_ICAO  = _get("AIRPORT_ICAO",  "AIRPORT_ICAO",  "URKA",          str)

# DCS theatre name (matches the JSON filenames produced by the runway extractor
# hook). Required — used to disambiguate airfields that exist on multiple maps
# (Beirut, Ramat David, Damascus, etc.) and to validate the AIRPORT_ICAO choice.
# Valid values: Afghanistan, Caucasus, GermanyCW, Iraq, Kola, MarianaIslands,
# MarianaIslandsWWII, Nevada, Normandy, PersianGulf, SinaiMap, SouthAtlantic,
# Syria, TheChannel
DCS_MAP = _get("DCS_MAP", "DCS_MAP", "", str)
if not DCS_MAP:
    raise SystemExit(
        "config error: DCS_MAP is not set. Add `DCS_MAP = \"<map>\"` to "
        "config.local.lua. Valid maps: " + ", ".join(sorted(_MAP_AIRFIELDS))
    )
if DCS_MAP not in _MAP_AIRFIELDS:
    raise SystemExit(
        f"config error: DCS_MAP=\"{DCS_MAP}\" is not recognised. Valid maps: "
        + ", ".join(sorted(_MAP_AIRFIELDS))
    )
if not _validate_airfield(DCS_MAP, AIRPORT_ICAO):
    other_maps = _maps_for_airfield(AIRPORT_ICAO)
    hint = (
        f" — {AIRPORT_ICAO} is on map(s): {', '.join(other_maps)}"
        if other_maps else ""
    )
    raise SystemExit(
        f"config error: AIRPORT_ICAO=\"{AIRPORT_ICAO}\" is not present on "
        f"DCS_MAP=\"{DCS_MAP}\"{hint}. "
        f"Airfields on {DCS_MAP}: {', '.join(_airfields_on_map(DCS_MAP))}"
    )

ACTIVE_RUNWAY = _get("ACTIVE_RUNWAY", "ACTIVE_RUNWAY",
                     _preferred_runway(AIRPORT_ICAO) or "", str)

# Validate runway against the database — catch stale/wrong defaults early.
if ACTIVE_RUNWAY:
    _rwy_desigs = _runway_designators(AIRPORT_ICAO, DCS_MAP)
    if _rwy_desigs:
        # Build the full set of valid designators (each stored entry + its reciprocal)
        _valid = set()
        for _d in _rwy_desigs:
            _valid.add(_d)
            # Compute reciprocal
            _num = ""
            _suf = ""
            for _ch in _d:
                if _ch.isdigit():
                    _num += _ch
                else:
                    _suf = _ch
                    break
            if _num:
                _rn = (int(_num) + 18) % 36
                if _rn == 0:
                    _rn = 36
                _rs = {"L": "R", "R": "L", "C": "C"}.get(_suf.upper(), "")
                _valid.add(f"{_rn:02d}{_rs}")
        if ACTIVE_RUNWAY not in _valid:
            import logging as _logging
            _logging.warning(
                f"ACTIVE_RUNWAY=\"{ACTIVE_RUNWAY}\" does not match any runway "
                f"at {AIRPORT_ICAO} on {DCS_MAP}. "
                f"Valid runways: {', '.join(sorted(_valid))}. "
                f"Falling back to {_rwy_desigs[0]}."
            )
            ACTIVE_RUNWAY = _rwy_desigs[0]

MAGNETIC_VAR  = _get("MAGNETIC_VAR",  "MAGNETIC_VAR",
                     _mag_var_lookup(AIRPORT_ICAO), float)

# Resolve position: config.lua/env override → airfield DB → fallback zeros
_db = _airfield_lookup(AIRPORT_ICAO)
_db_lat, _db_lon, _db_elev = (_db if _db else (0.0, 0.0, 0))

BOT_LAT              = _get("BOT_LAT",             "BOT_LAT",             _db_lat,  float)
BOT_LON              = _get("BOT_LON",             "BOT_LON",             _db_lon,  float)
BOT_ALT              = _get("BOT_ALT",             "BOT_ALT",             10000,    float)
AIRPORT_ELEVATION_FT = _get("AIRPORT_ELEVATION_FT","AIRPORT_ELEVATION_FT",_db_elev, int)

TACAN_CHANNEL        = _get("TACAN_CHANNEL",        "TACAN_CHANNEL",
                             _tacan_lookup(AIRPORT_ICAO), str)
TACAN_INBOUND_COURSE = _get("TACAN_INBOUND_COURSE", "TACAN_INBOUND_COURSE",
                             _runway_to_heading(ACTIVE_RUNWAY), int)
TACAN_MDA_FT         = _get("TACAN_MDA_FT",         "TACAN_MDA_FT",
                             AIRPORT_ELEVATION_FT + 400, int)
MSA_FT               = _get("MSA_FT",               "MSA_FT",
                             max(2000, AIRPORT_ELEVATION_FT + 1000), int)

FREQ_APPROACH   = _get("FREQ_APPROACH",   "FREQ_APPROACH",   123600000, float)
FREQ_APPROACH_2 = _get("FREQ_APPROACH_2", "FREQ_APPROACH_2", 236000000, float)
FREQ_TOWER      = _get("FREQ_TOWER",      "FREQ_TOWER",      122100000, float)
FREQ_TOWER_2    = _get("FREQ_TOWER_2",    "FREQ_TOWER_2",    257800000, float)
FREQ_GROUND     = _get("FREQ_GROUND",     "FREQ_GROUND",     121900000, float)
FREQ_GROUND_2   = _get("FREQ_GROUND_2",   "FREQ_GROUND_2",   275800000, float)

INSTRUCTIONS = _get("INSTRUCTIONS", "INSTRUCTIONS", "", str)

# Automatic runway selection based on wind (favours the runway with the
# strongest headwind component). Configured runway is used when wind is calm.
AUTO_RUNWAY_SELECTION = _get("AUTO_RUNWAY_SELECTION", "AUTO_RUNWAY_SELECTION", True, bool)
