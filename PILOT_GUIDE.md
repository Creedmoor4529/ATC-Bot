# DCS ATC Bot — Pilot Communication Guide

This guide covers how to communicate with the ATC bot over SRS radio. The bot uses standard ICAO phraseology and expects pilots to follow real-world radio conventions.

> **Tip:** The bot listens on three frequencies — Approach, Tower, and Ground. Tune the correct frequency for the service you need. Frequencies are set in `config.lua`.

---

## General Radio Etiquette

1. **Address the station first, then identify yourself.**
   Example: *"Kutaisi Tower, VIPER 11"*

2. **Keep transmissions short and clear.** The bot uses speech-to-text — speak clearly and avoid long pauses mid-sentence.

3. **Use your callsign consistently.** The bot tracks you by callsign across frequency changes.

4. **Read back all clearances.** The bot verifies your readback and will correct you if you miss a key element (runway, heading, altitude).

---

## First Contact / Check-In

Tune the appropriate frequency and call in with your callsign.

| You say | Bot responds with |
|---------|-------------------|
| *"Kutaisi Tower, VIPER 11"* | Active runway and acknowledgement |
| *"Kutaisi Approach, VIPER 11, inbound"* | Radar contact, your distance and bearing from the field, request for fuel state, and handoff to Tower |

---

## Requesting Weather / ATIS

Ask explicitly for weather or ATIS on any frequency.

| You say | Bot responds with |
|---------|-------------------|
| *"VIPER 11, request weather"* | Wind direction and speed, QNH, temperature, active runway |
| *"VIPER 11, request ATIS"* | Same as above |

> The bot does **not** automatically read weather on first contact — you must ask for it.

---

## Approach & Landing

### Inbound Call (Approach Frequency)

| You say | Bot responds with |
|---------|-------------------|
| *"Kutaisi Approach, VIPER 11, inbound runway 28"* | Radar contact, distance/bearing, request fuel state, switch to Tower |

### Fuel State

When asked to "update state" or "say state," report your fuel in **thousands of pounds**.

| You say | Meaning |
|---------|---------|
| *"VIPER 11, state 5"* | 5,000 lbs of fuel |
| *"VIPER 11, state 3 point 2"* | 3,200 lbs of fuel |
| *"VIPER 11, state 1 point 5"* | 1,500 lbs — **low fuel**, you will receive priority handling |

> **"State" always means fuel**, not altitude. Below 2,000 lbs is considered low fuel.

### Straight-In / Visual Approach (Tower Frequency)

| You say | Bot responds with |
|---------|-------------------|
| *"Kutaisi Tower, VIPER 11, straight-in runway 28"* | Sequence number and landing clearance |
| *"Kutaisi Tower, VIPER 11, 10 mile final runway 28"* | Landing clearance with traffic advisory if applicable |

### Circuit / Pattern Calls (Tower Frequency)

Report your position in the pattern. The bot will issue landing clearance.

| You say | Bot responds with |
|---------|-------------------|
| *"VIPER 11, downwind runway 28"* | Sequence and clearance |
| *"VIPER 11, turning base"* | Landing clearance |
| *"VIPER 11, final runway 28"* | Landing clearance |

---

## Overhead Break

Request an overhead break on Tower frequency.

| You say | Bot responds with |
|---------|-------------------|
| *"Kutaisi Tower, VIPER 11, request overhead break runway 28"* | Approved/denied with instructions |
| *"VIPER 11, on initial"* | Descend to MDA, report final |
| *"VIPER 11, final runway 28"* | Landing clearance |

---

## Instrument Approaches

Only request these when you need them — the bot defaults to visual approaches in VMC.

### TACAN Approach
| You say | Bot responds with |
|---------|-------------------|
| *"VIPER 11, request TACAN approach runway 28"* | TACAN channel, inbound course, MDA, report established |
| *"VIPER 11, request TACAN channel"* | TACAN channel only |

### ILS Approach (NATO aircraft — not available for F/A-18)
| You say | Bot responds with |
|---------|-------------------|
| *"VIPER 11, request ILS runway 28"* | Localizer frequency, report established |

> **F/A-18 Hornet pilots:** The F/A-18 cannot use ground-based ILS in DCS. Request TACAN approach instead.

---

## Taxi & Ground Operations (Ground Frequency)

| You say | Bot responds with |
|---------|-------------------|
| *"Kutaisi Ground, VIPER 11, request taxi"* | Taxi instructions to active runway, contact Tower for departure |
| *"Kutaisi Ground, VIPER 11, request startup"* | Startup clearance |

> If you request taxi or startup on Tower or Approach, you will be told to contact Ground.

---

## Takeoff (Tower Frequency)

| You say | Bot responds with |
|---------|-------------------|
| *"Kutaisi Tower, VIPER 11, ready for departure"* | Takeoff clearance with departure heading and wind |

> If you request takeoff on Ground frequency, you will be told to contact Tower.

---

## Post-Departure (Tower/Departure Frequency)

| You say | Bot responds with |
|---------|-------------------|
| *"VIPER 11, airborne, climbing angels 5"* | Radar contact, continue climb |
| *"VIPER 11, airborne"* | Radar contact |

---

## After Landing

| You say | Bot responds with |
|---------|-------------------|
| *"VIPER 11, clear of the active"* | Taxi to parking, contact Ground |
| *"VIPER 11, touchdown"* | Taxi to parking, contact Ground |

---

## Navigational Assistance / Vectors

If you're lost or need help finding the field, ask for vectors on any frequency.

| You say | Bot responds with |
|---------|-------------------|
| *"Kutaisi Approach, VIPER 11, request vectors to the field"* | Heading to fly based on your current position (requires Tacview connection) |

> The bot uses your real-time position from Tacview to calculate headings. If Tacview is not connected, vectors are unavailable.

---

## Flight Operations

If you're flying as a formation, call in as a flight.

| You say | Bot responds with |
|---------|-------------------|
| *"Kutaisi Tower, VIPER FLIGHT, two ships, request overhead break"* | Clearance for the entire flight |

---

## Emergencies

### Mayday (Life-threatening emergency)
| You say | Bot responds with |
|---------|-------------------|
| *"Mayday Mayday Mayday, VIPER 11, engine failure"* | Immediate acknowledgement, runway cleared, vectors to field, landing clearance |

### Pan-Pan (Urgent but not immediately life-threatening)
| You say | Bot responds with |
|---------|-------------------|
| *"Pan Pan Pan Pan, VIPER 11, hydraulic failure"* | Priority handling, vectors and landing clearance |

---

## Asking for Help

If you're not sure what the bot can do:

| You say | Bot responds with |
|---------|-------------------|
| *"VIPER 11, help"* | List of available services |

---

## Quick Reference — Frequency Assignments

| Service | Handles | Does NOT handle |
|---------|---------|-----------------|
| **Ground** | Taxi, startup | Takeoff, approach |
| **Tower** | Takeoff, landing, pattern work, overhead break | Taxi, vectors |
| **Approach** | Inbound sequencing, vectors, instrument approaches | Taxi, takeoff |

If you request a service on the wrong frequency, the bot will redirect you to the correct one.

---

## Tips for Best Results

- **Speak naturally but clearly.** The speech-to-text handles conversational radio calls well.
- **Include your callsign.** The bot needs it to track and respond to you.
- **Don't rush.** Give a brief pause before speaking after keying the radio.
- **One request per transmission.** Keep calls focused on a single action.
- **Read back clearances.** The bot checks your readback and will correct errors.
