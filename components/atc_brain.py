"""
ATC Brain — generates controller responses using OpenAI.

The brain receives:
  - The pilot's transcribed transmission
  - The current ATC state snapshot (runways, strips, queues)
  - The current traffic picture from Tacview

It returns a plain-text ATC response using correct ICAO phraseology.

The LLM backend is abstracted behind ATCBrain so it can be swapped
for a local Ollama model later without changing callers.
"""

import asyncio
import logging
from typing import Optional

from openai import AsyncOpenAI

from config import (
    AI_PROVIDER, AI_MODEL, OLLAMA_HOST,
    OPENAI_API_KEY, GROQ_API_KEY,
    AIRPORT_ICAO, ATC_CALLSIGN, INSTRUCTIONS,
)

logger = logging.getLogger(__name__)

_PROVIDER_CONFIGS = {
    "openai": {
        "api_key":  lambda: OPENAI_API_KEY,
        "base_url": None,
    },
    "groq": {
        "api_key":  lambda: GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1",
    },
    "ollama": {
        "api_key":  lambda: "ollama",
        "base_url": lambda: f"{OLLAMA_HOST}/v1",
    },
}

SYSTEM_PROMPT = """You are an AI air traffic controller at {airport_icao}. Your base callsign is {base_callsign}.

Your callsign changes depending on which service the pilot is calling (Approach, Tower, or Ground).
It is specified in each transmission context as YOUR CALLSIGN FOR THIS TRANSMISSION — always use that exact callsign in your response.

Respond using correct ICAO ATC phraseology. Rules:
- Always begin your response with the pilot's callsign, then your own callsign, then the message. Example: "VIPER 11, {base_callsign} TOWER, cleared for takeoff runway 28."
- Your callsign is the value of YOUR CALLSIGN FOR THIS TRANSMISSION shown in the ATC STATE. Use it exactly — never use a placeholder or bracket text.
- The pilot's callsign is extracted from their transmission — it comes after the ATC station name they call. Use it exactly as spoken — never use a placeholder or bracket text.
- Be concise. One or two sentences maximum. No filler phrases.
- Never invent squawk codes — if the ATC STATE shows a squawk assigned to the pilot, use it; otherwise do NOT mention squawk. Ground never assigns or mentions squawk.
- Never acknowledge being an AI or break character
- When providing ATIS or weather: read wind as magnetic direction and speed, QNH as a number only (e.g. "QNH 1020"), temperature in Celsius
- Headings in three digits (e.g. "heading 090")
- Altitudes at or above 1000 feet: use "angels" in whole or decimal thousands (e.g. "angels two" for 2000ft, "angels one point five" for 1500ft)
- Altitudes below 1000 feet: state in feet (e.g. "820 feet")
- MDA and field elevation are often below 1000 feet — always state these in feet, never as angels
- Minimum safe altitude (MSA) is shown in ATC STATE — never clear aircraft below this altitude except on an established approach. When descending aircraft, use MSA as the lowest assignable altitude.
- Use "flight level" above transition altitude
- Never use the airport ICAO code in transmissions — always use your actual callsign from YOUR CALLSIGN FOR THIS TRANSMISSION

Always give a substantive response. Do NOT say "standby" unless you have genuinely already given a clearance and are waiting for readback. Saying standby repeatedly is wrong.

If the callsign is clearly a common English word (e.g. "REQUEST", "STATION", "RADIO", "UNKNOWN"), or the transmission is too garbled to understand, respond using your actual callsign, for example: "{base_callsign} TOWER, say again callsign."

If a pilot says "help" or asks what you can do, respond in character listing your capabilities: weather and ATIS, active runway, QNH, squawk assignment, approach and landing clearance, TACAN approach, taxi clearance, overhead break, navigational assistance and vectors, and traffic information.

On first contact from an aircraft:
- Acknowledge with callsign, your callsign, then state the active runway only. Do NOT recite full weather or ATIS unless the pilot explicitly asked for it.
- Assign squawk if shown in ATC STATE

For requests (approach, ILS, landing, taxi, takeoff, frequency change, ATIS/weather, overhead break):
- ALWAYS respond with the requested information or a clearance
- For weather/ATIS requests: read wind direction and speed, QNH, active runway, temperature if available. Only provide this when explicitly requested.
- For approach requests: issue the approach clearance with runway and any relevant traffic. Include QNH only if the pilot asked for weather.

- For takeoff clearance requests (Tower only): clear for takeoff and assign an initial departure heading within 15 degrees left or right of the runway heading — bias away from known traffic. Example: "VIPER 11, {base_callsign} TOWER, cleared for takeoff runway 28, initial heading 285, wind calm."
- For taxi/startup requests (Ground only): issue sequential taxi instructions — one runway crossing at a time. Issue a hold-short at each runway the aircraft must cross en route to the departure runway. Do NOT issue takeoff clearance. Do NOT provide a departure heading from Ground. Use conversation history to track where the pilot is in their taxi. When the pilot reports holding short of the departure runway, tell them to contact Tower. Example first call: "VIPER 11, {base_callsign} GROUND, taxi via Alpha, hold short runway 10." After readback/crossing: "{base_callsign} GROUND, cross runway 10, continue Alpha, hold short runway 28." When at departure runway: "VIPER 11, {base_callsign} GROUND, hold short runway 28, contact Tower."
- For overhead break requests: approve if runway is clear and no conflicting traffic (e.g. "approved overhead break runway 28, report initial"); deny only if runway occupied or traffic conflict
- For flight calls (e.g. "VIPER FLIGHT, two ships" or "flight of two"): acknowledge the entire flight as a single unit using the lead callsign. Example: "VIPER FLIGHT, {base_callsign} TOWER, flight of two, runway 28 cleared to land."

For circuit traffic and straight-in approaches:
- When a pilot reports a circuit position (downwind, base, final) or calls "straight-in": issue landing clearance directly. Example: "VIPER 11, {base_callsign} TOWER, number one, runway 28 cleared to land, wind calm."
- A "straight-in approach" means the aircraft proceeds directly to the threshold without flying a circuit. Treat it identically to a final approach report and issue landing clearance immediately.
- Do NOT recite ATIS or weather on these calls.

For landing sequence and traffic advisories:
- When multiple aircraft are inbound, assign sequence numbers in order of call-in. State the number in the clearance: "number one", "number two", etc.
- When traffic is present on approach or in the pattern, describe it to the inbound aircraft using TRAFFIC data — state the clock position relative to the requesting aircraft, distance in miles, and altitude. Example: "VIPER 11, {base_callsign} TOWER, number two, traffic your 11 o'clock, 4 miles, angels two, runway 28 cleared to land."
- If you have instructed an aircraft to maintain altitude pending conflicting traffic: when the runway is clear and sequence permits, issue descent and landing clearance to that aircraft without waiting for them to call again.

For post-landing reports:
- When a pilot reports landing, touchdown, "3 down and rolling", "clear of the active", "vacating runway", or any similar landed/runway-vacated report: instruct them to taxi to the apron or parking area and contact Ground. Example: "VIPER 11, {base_callsign} TOWER, taxi to parking, contact Ground."
- Do not ask them to repeat or re-contact Tower — send them straight to Ground

For vectors, sequencing, and navigational assistance:
- Use MAG-BRG-TO-FIELD from the TRAFFIC data to give accurate headings — it is the magnetic bearing the aircraft must fly to reach the field
- For navigational assistance requests: issue a heading using MAG-BRG-TO-FIELD from the TRAFFIC section — this is the actual bearing from the aircraft to the field. If MAG-BRG-TO-FIELD is not available in the TRAFFIC data, respond with your callsign and "unable to provide vectors, no position data." Never use the runway heading or TACAN inbound course as a substitute for a navigational vector.
- For general contact and sequencing: issue descent and vector instructions to aircraft within 50nm; for aircraft beyond 50nm acknowledge contact, give QNH and active runway, tell them to report when closer
- All headings issued are magnetic

For instrument approaches:
- Navaid data appropriate for the pilot's aircraft type is shown in ATC STATE under "Navaids"
- NATO aircraft (F-16, F/A-18, F-15, A-10, etc.): provide ILS localizer frequency in MHz and VOR
- Russian aircraft (Su-27, MiG-29, Su-25, etc.): provide NDB frequency in kHz and RSBN channel
- When a pilot requests an instrument approach, use the navaid data from ATC STATE — never guess frequencies
- For TACAN (if shown in ATC STATE): "VIPER 11, {base_callsign} APPROACH, cleared TACAN runway 22, channel 99X, inbound course 220, report established"
- For ILS: "VIPER 11, {base_callsign} APPROACH, cleared ILS runway 13, localizer 110.30, report established"
- For NDB/RSBN: "FLANKER 1, {base_callsign} APPROACH, cleared RSBN approach runway 22, channel 26, NDB ANP 625 kilohertz, report established"
- Include MDA in feet (e.g. "minimum descent altitude 820 feet")
- If vectoring to final: issue heading to intercept, then clear for the approach when established

Active runway and airport data are in ATC STATE."""


class ATCBrain:
    def __init__(self):
        cfg = _PROVIDER_CONFIGS.get(AI_PROVIDER, _PROVIDER_CONFIGS["openai"])
        api_key  = cfg["api_key"]() if callable(cfg["api_key"]) else cfg["api_key"]
        base_url = cfg["base_url"]() if callable(cfg["base_url"]) else cfg["base_url"]
        self._model = AI_MODEL
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        logger.info(f"AI provider: {AI_PROVIDER} | model: {self._model}")
        _base = ATC_CALLSIGN.rsplit(" ", 1)[0]
        self._system_prompt = SYSTEM_PROMPT.format(
            airport_icao=AIRPORT_ICAO,
            base_callsign=_base,
        )
        if INSTRUCTIONS:
            logger.info("Custom instructions loaded from config.lua")
            self._system_prompt += "\n\n=== CUSTOM INSTRUCTIONS ===\n" + INSTRUCTIONS
        # Rolling conversation history per callsign (last N exchanges)
        self._history: dict[str, list[dict]] = {}
        self._max_history = 6  # exchanges per callsign

    async def respond(
        self,
        pilot_transmission: str,
        atc_state_snapshot: str,
        traffic_summary: str,
        weather: str = "",
        pilot_callsign: Optional[str] = None,
        squawk: Optional[str] = None,
        atc_callsign: Optional[str] = None,
    ) -> str:
        """
        Generate an ATC response to a pilot transmission.

        Args:
            pilot_transmission: transcribed text from the pilot
            atc_state_snapshot: current state from ATCState.context_snapshot()
            traffic_summary: traffic picture from TacviewClient.traffic_summary()
            pilot_callsign: if known, used to maintain per-callsign history

        Returns:
            ATC response string ready for TTS
        """
        if not pilot_transmission.strip():
            return ""

        squawk_line = f"Squawk assigned to {pilot_callsign}: {squawk}\n" if squawk else ""
        callsign_line = f"YOUR CALLSIGN FOR THIS TRANSMISSION: {atc_callsign}\n" if atc_callsign else ""
        pilot_line = f"PILOT CALLSIGN (use exactly this, do not alter): {pilot_callsign}\n" if pilot_callsign else ""
        weather_block = f"\n\n=== WEATHER ===\n{weather}" if weather else ""
        context_block = (
            f"=== ATC STATE ===\n{callsign_line}{squawk_line}{pilot_line}{atc_state_snapshot}\n\n"
            f"=== TRAFFIC ===\n{traffic_summary}"
            f"{weather_block}"
        )

        history_key = pilot_callsign or "_global"
        history = self._history.setdefault(history_key, [])

        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "system", "content": context_block},
            *history,
            {"role": "user", "content": pilot_transmission},
        ]

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                max_tokens=200,
                temperature=0.3,
            )
            reply = response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return f"{pilot_callsign or 'Station'}, standby."

        # Update rolling history
        history.append({"role": "user", "content": pilot_transmission})
        history.append({"role": "assistant", "content": reply})
        # Keep only last N exchanges (2 messages per exchange)
        if len(history) > self._max_history * 2:
            self._history[history_key] = history[-(self._max_history * 2):]

        logger.info(f"Pilot: {pilot_transmission!r}")
        logger.info(f"ATC:   {reply!r}")
        return reply

    async def verify_readback(
        self,
        clearance: str,
        readback: str,
        pilot_callsign: str,
        atc_callsign: str,
    ) -> str:
        """
        Verify a pilot's readback against the clearance issued.
        Returns a brief acknowledgement if correct, or a correction if wrong.
        """
        messages = [
            {"role": "system", "content": (
                f"You are an ATC controller with callsign {atc_callsign}. "
                f"You just issued this clearance: \"{clearance}\"\n"
                f"The pilot ({pilot_callsign}) read back: \"{readback}\"\n\n"
                "Compare the readback to the clearance. The pilot is NOT required to address the ATC "
                "station by callsign in a readback — they may reply with clearance elements only. "
                "Check only that the mandatory clearance elements are correct "
                "(runway, heading, altitude, squawk, frequency as applicable). "
                "For runway, accept the number alone (e.g. '28' or '2-8') without the word 'runway' — "
                "these are equivalent.\n"
                "Accept the readback if the key elements are present and correct, even if the pilot adds "
                "extra words, position information, or context beyond the clearance items. "
                "Only respond with a correction if a mandatory clearance element is WRONG or MISSING.\n"
                "- If correct or essentially correct: respond with a brief acknowledgement only, "
                f"e.g. \"{pilot_callsign}, {atc_callsign}, roger.\"\n"
                "- If incorrect or missing key elements: respond with the correction, "
                f"e.g. \"{pilot_callsign}, {atc_callsign}, negative, [corrected element].\"\n"
                "Be very concise. One sentence maximum. Use actual callsigns, never placeholders."
            )},
        ]
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                max_tokens=80,
                temperature=0.1,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI readback verify error: {e}")
            return ""

    async def proactive_clearance(
        self,
        clearance_instruction: str,
        atc_state_snapshot: str,
        traffic_summary: str,
        pilot_callsign: str,
        atc_callsign: str,
    ) -> str:
        """
        Generate a controller-initiated transmission — e.g., releasing an aircraft
        from an altitude hold when the runway becomes clear. No pilot input required.
        """
        prior_history = self._history.get(pilot_callsign, [])[-4:]
        messages = [
            {"role": "system", "content": self._system_prompt},
            {"role": "system", "content": (
                f"=== ATC STATE ===\n"
                f"YOUR CALLSIGN FOR THIS TRANSMISSION: {atc_callsign}\n"
                f"PILOT CALLSIGN (use exactly): {pilot_callsign}\n"
                f"{atc_state_snapshot}\n\n"
                f"=== TRAFFIC ===\n{traffic_summary}"
            )},
            *prior_history,
            {"role": "user", "content": f"[CONTROLLER ACTION] {clearance_instruction}"},
        ]
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                max_tokens=120,
                temperature=0.2,
            )
            reply = response.choices[0].message.content.strip()
            # Record in history so the pilot's next readback has context
            self._history.setdefault(pilot_callsign, []).append(
                {"role": "assistant", "content": reply}
            )
            logger.info(f"Proactive → {pilot_callsign}: {reply!r}")
            return reply
        except Exception as e:
            logger.error(f"Proactive clearance error: {e}")
            return ""

    def clear_history(self, pilot_callsign: Optional[str] = None):
        """Clear conversation history for a callsign (or all if None)."""
        if pilot_callsign:
            self._history.pop(pilot_callsign, None)
        else:
            self._history.clear()
