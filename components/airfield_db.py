"""
DCS airfield database — all maps.
Provides (lat, lon, elevation_ft) keyed by ICAO code.
Used by config.py when BOT_LAT/BOT_LON are not set in config.lua.
Coordinates are approximate DCS positions.
"""

# ICAO: (lat, lon, elevation_ft)
AIRFIELDS: dict[str, tuple[float, float, int]] = {

    # -------------------------------------------------------------------------
    # CAUCASUS
    # -------------------------------------------------------------------------

    # Georgia
    "UGSB": (41.610,  41.600,    32),  # Batumi
    "UGKS": (41.921,  41.726,    59),  # Kobuleti
    "UGSN": (42.240,  42.056,    43),  # Senaki-Kolkhi
    "UGKO": (42.176,  42.475,  1529),  # Kutaisi
    "UGSS": (42.858,  41.130,    43),  # Sukhumi (Babushara)
    "UGKG": (43.103,  40.582,    68),  # Gudauta
    "UGTB": (41.669,  44.955,  1624),  # Tbilisi-Lochini

    # Russia — Caucasus region
    "URKA": (45.002,  37.347,   174),  # Anapa
    "URSS": (43.449,  39.956,    98),  # Sochi-Adler
    "URKH": (44.682,  40.036,   591),  # Maykop-Khanskaya
    "URKG": (44.963,  38.002,    65),  # Krymsk
    "URRR": (45.022,  38.968,    98),  # Krasnodar-Center
    "URKK": (45.035,  39.171,   111),  # Krasnodar-Pashkovsky
    "URMM": (44.225,  43.082,  1053),  # Mineralnye Vody
    "URMO": (43.206,  44.606,  1673),  # Beslan (Vladikavkaz)
    "URKN": (43.513,  43.636,  1410),  # Nalchik
    "URMZ": (43.789,  44.608,   507),  # Mozdok
    "URMG": (44.582,  38.015,    72),  # Gelendzhik

    # -------------------------------------------------------------------------
    # PERSIAN GULF
    # -------------------------------------------------------------------------

    # UAE
    "OMAD": (24.248,  54.547,    77),  # Al Dhafra AB
    "OMAA": (24.433,  54.651,    88),  # Abu Dhabi International
    "OMDM": (25.027,  55.366,   202),  # Al Minhad AB
    "OMDB": (25.252,  55.364,    62),  # Dubai International
    "OMSJ": (25.329,  55.517,   111),  # Sharjah
    "OMFJ": (25.112,  56.324,   152),  # Fujairah
    "OMRK": (25.613,  55.939,   102),  # Ras Al Khaimah

    # Oman
    "OOKB": (26.171,  56.244,   100),  # Khasab
    "OOMS": (23.594,  58.285,    48),  # Muscat-Seeb

    # Iran
    "OIKB": (27.218,  56.378,    22),  # Bandar Abbas
    "OIBL": (26.532,  54.825,    22),  # Bandar Lengeh
    "OIBS": (25.909,  54.539,    43),  # Sirri Island
    "OIBA": (25.876,  55.033,    20),  # Abu Musa Island
    "OIBP": (26.810,  53.356,    76),  # Lavan Island
    "OIKQ": (26.754,  55.902,    45),  # Qeshm Island

    # -------------------------------------------------------------------------
    # SYRIA
    # -------------------------------------------------------------------------

    # Syria
    "OSAP": (36.178,  37.224,  1267),  # Aleppo
    "OSLK": (35.401,  35.949,   157),  # Latakia (Basil Al Assad)
    "OSDI": (33.411,  36.516,  2020),  # Damascus
    "OSJI": (36.096,  37.939,  1198),  # Jirah
    "OSPR": (34.557,  38.317,  1322),  # Palmyra (Tadmur)
    "OSTI": (34.522,  37.914,   869),  # Tiyas (T4)
    "OSSH": (34.491,  36.909,  1801),  # Shayrat
    "OSKH": (33.064,  36.557,  2198),  # Khalkhalah
    "OSABD": (35.718, 37.099,   971),  # Abu al-Duhur
    "OSQY": (35.787,  36.818,  1168),  # Rasin al-Aboud (Rene Mouawad? Taftanaz?)

    # Lebanon
    "OLBA": (33.821,  35.488,    87),  # Beirut

    # Cyprus
    "LCLK": (34.875,  33.625,     8),  # Larnaca
    "LCPH": (34.718,  32.486,    41),  # Paphos
    "LCRA": (34.590,  32.987,    76),  # RAF Akrotiri

    # Israel
    "LLBG": (32.009,  34.887,   135),  # Tel Aviv Ben Gurion
    "LLHB": (31.233,  34.663,   902),  # Hatzerim AB
    "LLOV": (29.940,  34.936,  1492),  # Ovda
    "LLNV": (31.208,  35.012,  1330),  # Nevatim
    "LLRD": (32.665,  35.179,   185),  # Ramat David

    # Turkey
    "LTAG": (37.002,  35.426,   238),  # Incirlik AB
    "LTAF": (36.982,  35.280,    65),  # Adana Sakirpasa
    "LTAJ": (36.947,  37.479,  2315),  # Gaziantep

    # Jordan
    "OJMF": (32.356,  36.259,  2231),  # Muwaffaq Salti (Azraq)

    # -------------------------------------------------------------------------
    # NEVADA (NTTR)
    # -------------------------------------------------------------------------
    "KLSV": (36.237, -115.034,  1869),  # Nellis AFB
    "KLAS": (36.080, -115.152,  2141),  # Las Vegas McCarran
    "KTNX": (37.798, -116.781,  5549),  # Tonopah Test Range
    "KINS": (36.587, -115.673,  3133),  # Creech AFB (Indian Springs)
    "KVGT": (36.211, -115.194,  2205),  # North Las Vegas
    "KBTY": (36.861, -116.787,  3163),  # Beatty
    "KIFP": (35.158, -114.559,   700),  # Laughlin/Bullhead

    # -------------------------------------------------------------------------
    # MARIANA ISLANDS
    # -------------------------------------------------------------------------
    "PGUM": (13.484,  144.796,   298),  # Guam (Antonio B. Won Pat)
    "PGUA": (13.584,  144.930,   604),  # Andersen AFB
    "PGRO": (14.174,  145.243,   607),  # Rota
    "PGSN": (15.119,  145.729,   215),  # Saipan
    "PGFT": (14.999,  145.619,   161),  # Tinian North

    # -------------------------------------------------------------------------
    # NORMANDY
    # -------------------------------------------------------------------------
    "LFRC": (49.651,  -1.470,    459),  # Cherbourg-Maupertus
    "LFRK": (49.173,  -0.447,    256),  # Caen-Carpiquet
    "LFOH": (49.534,   0.088,    312),  # Le Havre-Octeville
    "LFQA": (49.859,   2.388,    295),  # Laon-Couvron
    "LFQB": (48.322,   3.997,    381),  # Troyes-Barberey
    "LFOE": (48.718,   1.176,    456),  # Evreux-Fauville
    "LFPG": (49.013,   2.550,    392),  # Paris Charles de Gaulle
    "LFPB": (48.970,   2.441,    217),  # Paris Le Bourget

    # -------------------------------------------------------------------------
    # THE CHANNEL
    # -------------------------------------------------------------------------
    "EGMH": (51.342,   1.341,    178),  # Manston
    "EGKB": (51.331,   0.033,    598),  # Biggin Hill
    "EGLF": (51.278,  -0.776,    238),  # Farnborough
    "EGMC": (51.572,   0.696,     49),  # Southend
    "LFQQ": (50.562,   3.089,    160),  # Lille-Lesquin
    "LFAY": (49.874,   2.716,    361),  # Amiens-Glisy
    "LFAK": (50.174,   3.154,    252),  # Denain-Prouvy

    # -------------------------------------------------------------------------
    # SOUTH ATLANTIC (Falklands)
    # -------------------------------------------------------------------------
    "EGYP": (-51.823, -58.447,   244),  # Mount Pleasant (Port Stanley)
    "SAWG": (-51.609, -69.313,    61),  # Rio Gallegos
    "SAWE": (-53.778, -67.750,    65),  # Rio Grande
    "SAVT": (-54.843, -68.295,    86),  # Ushuaia Malvinas

    # -------------------------------------------------------------------------
    # SINAI
    # -------------------------------------------------------------------------
    "HEAR": (31.073,  33.836,   121),  # El Arish
    "HECW": (30.117,  30.917,   561),  # Cairo West
    "HECA": (30.122,  31.406,   382),  # Cairo International
    "HEGN": (27.178,  33.799,    52),  # Hurghada
    "HESH": (27.977,  34.395,   178),  # Sharm el-Sheikh
    "HESC": (28.686,  34.063,  4849),  # St. Catherine
    "LLRM": (30.776,  34.668,  2976),  # Ramon
    "HETB": (30.919,  34.401,  2440),  # Bir Hasana

    # -------------------------------------------------------------------------
    # AFGHANISTAN (Koh-i-Laan)
    # -------------------------------------------------------------------------
    "OAKS": (31.516,  65.868,  3337),  # Kandahar
    "OAKB": (34.565,  69.212,  5873),  # Kabul
    "OAIX": (34.947,  69.265,  4895),  # Bagram
    "OAHN": (34.346,  62.207,  2841),  # Herat
    "OAMN": (29.934,  61.827,  1725),  # Zaranj

    # -------------------------------------------------------------------------
    # KOLA
    # -------------------------------------------------------------------------
    "ENBO": (67.269,  14.365,   489),  # Bodø
    "ENEV": (68.491,  16.678,    84),  # Evenes (Harstad/Narvik)
    "ENLK": (68.152,  13.609,    96),  # Leknes
    "ENRS": (69.055,  15.002,    16),  # Røst
    "ENBV": (70.542,  29.034,   490),  # Berlevåg
    "ENBS": (70.600,  29.692,   164),  # Båtsfjord
    "ENKR": (70.068,  29.893,   282),  # Kirkenes (Høybuktmoen)
    "ENMH": (71.029,  25.833,   276),  # Mehamn
    "ENBN": (70.204,  28.665,    72),  # Berlevåg alt
    "ULKK": (67.461,  33.576,   627),  # Murmansk
    "ULMK": (68.782,  32.750,   331),  # Monchegorsk
    "ULAS": (69.271,  33.450,    64),  # Severomorsk-1
    "ULAM": (69.017,  33.075,   147),  # Severomorsk-3
    "ULWC": (67.965,  32.430,   640),  # Olenya
}


def lookup(icao: str) -> tuple[float, float, int] | None:
    """Return (lat, lon, elevation_ft) for an ICAO code, or None if not found."""
    return AIRFIELDS.get(icao.upper())


# ---------------------------------------------------------------------------
# Runway database
# Each entry: (threshold1_lat, threshold1_lon, threshold2_lat, threshold2_lon, width_m)
# Thresholds are the two ends of the runway centerline.
# width_m is the half-width corridor on each side of the centerline.
# ---------------------------------------------------------------------------

# ICAO: list of (lat1, lon1, lat2, lon2, width_m)
RUNWAYS: dict[str, list[tuple[float, float, float, float, int]]] = {

    # CAUCASUS
    "UGSB": [(41.6025, 41.5887, 41.6175, 41.6107, 30)],   # Batumi 13/31
    "UGKS": [(41.9121, 41.7107, 41.9305, 41.7388, 30)],   # Kobuleti 07/25
    "UGSN": [(42.2301, 42.0357, 42.2488, 42.0798, 30)],   # Senaki 09/27
    "UGKO": [(42.1614, 42.4551, 42.1908, 42.4945, 30)],   # Kutaisi 08/26
    "UGSS": [(42.8479, 41.1079, 42.8660, 41.1501, 30)],   # Sukhumi 12/30
    "UGKG": [(43.0939, 40.5618, 43.1115, 40.6008, 30)],   # Gudauta 12/30
    "UGTB": [(41.6591, 44.9204, 41.6776, 44.9892, 30)],   # Tbilisi 13R/31L
    "URKA": [(45.0115, 37.3328, 44.9945, 37.3620, 30)],   # Anapa 22/04
    "URSS": [(43.4401, 39.9329, 43.4588, 39.9799, 30)],   # Sochi 06/24
    "URKH": [(44.6726, 39.9982, 44.6908, 40.0714, 30)],   # Maykop 09/27
    "URKG": [(44.9510, 37.9751, 44.9693, 38.0283, 30)],   # Krymsk 09/27
    "URRR": [(45.0087, 38.9368, 45.0348, 38.9997, 30)],   # Krasnodar-Center 09/27
    "URKK": [(45.0192, 39.1337, 45.0500, 39.2064, 30)],   # Krasnodar-Pashkovsky 09/27
    "URMM": [(44.2107, 43.0517, 44.2370, 43.1108, 30)],   # Mineralnye Vody 12/30
    "URMO": [(43.1952, 44.5762, 43.2183, 44.6376, 30)],   # Beslan 11/29
    "URKN": [(43.5014, 43.6082, 43.5233, 43.6627, 30)],   # Nalchik 12/30
    "URMZ": [(43.7812, 44.5949, 43.7960, 44.6218, 30)],   # Mozdok 10/28

    # PERSIAN GULF
    "OMAD": [(24.2296, 54.5164, 24.2659, 54.5777, 30)],   # Al Dhafra 13L/31R
    "OMDM": [(25.0106, 55.3418, 25.0434, 55.3949, 30)],   # Al Minhad 09/27
    "OMDB": [(25.2396, 55.3522, 25.2636, 55.3956, 30)],   # Dubai 12L/30R
    "OIKB": [(27.2015, 56.3558, 27.2339, 56.4009, 30)],   # Bandar Abbas 21/03
    "OOKB": [(26.1618, 56.2263, 26.1806, 56.2612, 30)],   # Khasab 17/35

    # CYPRUS
    "LCLK": [(34.8694, 33.6063, 34.8810, 33.6437, 30)],   # Larnaca 04/22
    "LCPH": [(34.7129, 32.4751, 34.7232, 32.5063, 30)],   # Paphos 11/29
    "LCRA": [(34.5910, 32.9620, 34.5920, 33.0101, 30)],   # Akrotiri 10/28

    # SYRIA
    "OSLK": [(35.3892, 35.9290, 35.4123, 35.9687, 30)],   # Latakia 17/35
    "OSAP": [(36.1693, 37.2173, 36.1864, 37.2311, 30)],   # Aleppo 09/27
    "OSDI": [(33.4028, 36.5020, 33.4208, 36.5291, 30)],   # Damascus 23/05
    "LTAG": [(36.9901, 35.4097, 37.0098, 35.4435, 30)],   # Incirlik 05/23

    # NEVADA
    "KLSV": [(36.2196, -115.0512, 36.2563, -115.0332, 30)],  # Nellis 03R/21L
    "KLAS": [(36.0712, -115.1735, 36.0951, -115.1411, 30)],  # Las Vegas 01L/19R
    "KINS": [(36.5731, -115.6902, 36.5961, -115.6612, 30)],  # Creech 03/21
}


import math as _math


def _on_runway(
    ac_lat: float, ac_lon: float, ac_alt_ft: float,
    field_elev_ft: float,
    icao: str,
    agl_limit_ft: float = 200.0,
) -> bool:
    """
    Return True if the aircraft is within any runway corridor at the given airfield.
    Uses a centerline + half-width corridor check in local Cartesian space.
    """
    if ac_alt_ft > field_elev_ft + agl_limit_ft:
        return False

    runways = RUNWAYS.get(icao.upper(), [])
    for r in runways:
        lat1, lon1, lat2, lon2 = r[0], r[1], r[2], r[3]
        width_m = r[4]

        # Midpoint for local projection
        clat = (lat1 + lat2) / 2.0
        m_per_deg_lat = 111320.0
        m_per_deg_lon = 111320.0 * _math.cos(_math.radians(clat))

        # Runway vector in metres
        rx = (lon2 - lon1) * m_per_deg_lon
        ry = (lat2 - lat1) * m_per_deg_lat
        length = _math.sqrt(rx * rx + ry * ry)
        if length < 1:
            continue

        # Aircraft position relative to threshold 1
        ax = (ac_lon - lon1) * m_per_deg_lon
        ay = (ac_lat - lat1) * m_per_deg_lat

        # Project onto runway centerline
        along  = (ax * rx + ay * ry) / length
        across = abs(ax * ry - ay * rx) / length

        if 0 <= along <= length and across <= width_m:
            return True

    return False


def runway_lookup(icao: str) -> list[tuple[float, float, float, float, int]]:
    """Return runway threshold data for an ICAO code."""
    return RUNWAYS.get(icao.upper(), [])


# ---------------------------------------------------------------------------
# Navigation aids database
#
# Keys per entry:
#   "vor"   — NATO/civilian VOR:  (ident, freq_mhz)
#   "ils"   — NATO ILS (MHz):     [(runway, loc_mhz, gs_mhz_or_None), ...]
#   "ndb"   — Russian NDB (kHz):  [(ident, freq_khz), ...]
#   "rsbn"  — Russian RSBN:       [(runway, channel), ...]
#   "tacan" — TACAN channel:      "NNX" string (e.g. "107X")
#
# Russian airfields use NDB/RSBN for instrument approaches.
# Georgian/NATO airfields use VOR/ILS (MHz).
# Military airfields may additionally have a TACAN channel.
# ---------------------------------------------------------------------------

NAVAIDS: dict[str, dict] = {

    # -------------------------------------------------------------------------
    # CAUCASUS — Georgian (NATO ILS)
    # -------------------------------------------------------------------------
    "UGSB": {
        "vor": ("BTM", 114.80),
        "ils": [("13", 110.30, 329.60)],
        "tacan": "16X",
        "freq": (131.0, 260.0),
    },
    "UGKS": {
        "vor": ("KOB", 112.50),
        "ils": [("07", 109.75, None)],
        "tacan": "67X",
        "freq": (133.0, 262.0),
    },
    "UGSN": {
        "vor": ("SNK", 113.60),
        "ils": [("09", 108.90, None)],
        "tacan": "31X",
        "freq": (132.0, 261.0),
    },
    "UGKO": {
        "vor": ("KTS", 112.50),
        "ils": [("08", 110.50, None)],
        "tacan": "44X",
        "freq": (134.0, 263.0),
    },
    "UGSS": {
        "vor": ("SUK", 114.10),
        "ils": [("12", 108.90, None)],
        "freq": (129.0, 258.0),
    },
    "UGKG": {
        "vor": ("GUD", 113.20),
        "ils": [("12", 109.10, None)],
        "freq": (130.0, 259.0),
    },
    "UGTB": {
        "vor": ("TBS", 113.80),
        "ils": [
            ("13R", 110.30, None),
            ("31L", 109.90, None),
        ],
        "tacan": "25X",
        "freq": (138.0, 267.0),
    },

    # -------------------------------------------------------------------------
    # CAUCASUS — Russian (NDB/RSBN)
    # -------------------------------------------------------------------------
    "URKA": {
        "vor": ("ANP", 114.30),
        "ndb": [("ANP", 625)],
        "rsbn": [("22", 26), ("04", 26)],
        "freq": (121.0, 250.0),
    },
    "URSS": {
        "vor": ("SCH", 115.80),
        "ndb": [("SCH", 540)],
        "rsbn": [("06", 28)],
        "freq": (127.0, 256.0),
    },
    "URKH": {
        "ndb": [("MKP", 440)],
        "rsbn": [("09", 30)],
        "freq": (125.0, 254.0),
    },
    "URKG": {
        "ndb": [("KRM", 490)],
        "rsbn": [("09", 32)],
        "freq": (124.0, 253.0),
    },
    "URRR": {
        "vor": ("KRR", 115.40),
        "ndb": [("KRR", 408)],
        "rsbn": [("09", 34)],
        "freq": (122.0, 251.0),
    },
    "URKK": {
        "vor": ("KRP", 116.00),
        "ndb": [("KRP", 527)],
        "rsbn": [("09", 36), ("27", 36)],
        "freq": (128.0, 257.0),
    },
    "URMM": {
        "vor": ("MRV", 115.20),
        "ndb": [("MRV", 591)],
        "rsbn": [("12", 38)],
        "freq": (135.0, 264.0),
    },
    "URMO": {
        "vor": ("BES", 114.00),
        "ndb": [("BES", 462)],
        "rsbn": [("11", 40)],
        "freq": (141.0, 270.0),
    },
    "URKN": {
        "vor": ("NAL", 112.10),
        "ndb": [("NAL", 370)],
        "rsbn": [("12", 42)],
        "freq": (136.0, 265.0),
    },
    "URMZ": {
        "vor": ("MOZ", 115.00),
        "ndb": [("MOZ", 625)],
        "rsbn": [("10", 44), ("28", 44)],
        "freq": (137.0, 266.0),
    },
    "URMG": {
        "ndb": [("GLN", 510)],
        "rsbn": [("24", 46)],
        "freq": (126.0, 255.0),
    },

    # -------------------------------------------------------------------------
    # PERSIAN GULF
    # -------------------------------------------------------------------------
    "OMAD": {
        "vor": ("ADV", 114.35),
        "ils": [
            ("13L", 110.10, None),
            ("31R", 109.90, None),
        ],
        "tacan": "96X",
        "freq": (119.9,  None),
    },
    "OMAA": {
        "vor": ("AUH", 114.25),
        "ils": [
            ("13L", 111.10, None),
            ("31R", 110.30, None),
        ],
        "freq": (119.2,  None),
    },
    "OMDM": {
        "vor": ("MHD", 112.60),
        "ils": [("09",  110.50, None)],
        "freq": (118.55, None),
    },
    "OMDB": {
        "vor": ("DXB", 116.70),
        "ils": [
            ("12L", 110.90, None),
            ("30R", 111.30, None),
        ],
        "freq": (118.75, None),
    },
    "OMSJ": {
        "vor": ("SHJ", 113.25),
        "ils": [("12", 110.10, None)],
        "freq": (118.6,  None),
    },
    "OMFJ": {
        "ils": [("29", 110.30, None)],
        "freq": (124.6,  None),
    },
    "OMRK": {
        "ils": [("17", 109.90, None)],
        "freq": (121.6,  None),
    },
    "OOKB": {
        "vor": ("KHB", 112.60),
        "ils": [("17", 110.90, None)],
        "freq": (124.35, None),
    },
    "OOMS": {
        "vor": ("MCT", 116.50),
        "ils": [
            ("08L", 110.10, None),
            ("26R", 109.90, None),
        ],
    },
    "OIKB": {
        "vor": ("BND", 117.10),
        "ils": [("21", 110.50, None)],
        "tacan": "78X",
        "freq": (118.1,  None),
    },
    "OIBL": {
        "vor": ("BLH", 117.30),
        "freq": (121.7,  None),
    },
    "OIBS": {
        "ndb": [("SIR", 350)],
        "freq": (135.05, None),
    },
    "OIBA": {
        "ndb": [("ABM", 275)],
        "freq": (122.9,  None),
    },
    "OIBP": {
        "ndb": [("LAV", 320)],
    },
    "OIKQ": {
        "vor": ("QSM", 115.20),
        "freq": (118.05, None),
    },

    # -------------------------------------------------------------------------
    # SYRIA
    # -------------------------------------------------------------------------
    "OSAP": {
        "vor": ("ALP", 116.20),
        "ils": [("09", 110.10, None)],
        "freq": (119.1,  251.1),
    },
    "OSLK": {
        "vor": ("LTK", 114.80),
        "ils": [
            ("17", 110.30, None),
            ("35", 109.90, None),
        ],
        "freq": (118.1,  250.6),
    },
    "OSDI": {
        "vor": ("DAM", 116.00),
        "ils": [
            ("23L", 111.10, None),
            ("05R", 110.50, None),
        ],
        "freq": (118.5,  253.25),
    },
    "OSJI": {
        "ils": [("27", 109.10, None)],
        "freq": (118.1,  250.9),
    },
    "OSPR": {
        "vor": ("PAL", 114.00),
        "freq": (121.9,  251.15),
    },
    "OSTI": {
        "vor": ("TYS", 113.60),
        "ils": [("26", 110.10, None)],
        "freq": (120.5,  None),
    },
    "OSSH": {
        "ils": [("24", 109.70, None)],
        "freq": (120.2,  None),
    },
    "OLBA": {
        "vor": ("BEI", 114.80),
        "ils": [
            ("03",  110.90, None),
            ("21",  110.50, None),
        ],
        "freq": (118.9,  253.2),
    },
    "LCLK": {
        "vor": ("LCA", 116.40),
        "ils": [("04", 110.30, None)],
        "freq": (121.2,  None),
    },
    "LCPH": {
        "vor": ("PFO", 115.60),
        "ils": [("29", 110.10, None)],
        "tacan": "79X",
        "freq": (119.9,  252.1),
    },
    "LCRA": {
        "vor": ("AKT", 112.70),
        "ils": [("28", 110.30, None)],
        "tacan": "107X",
        "freq": (128.0,  252.0),
    },
    "LLBG": {
        "vor": ("BGN", 116.60),
        "ils": [
            ("08",  110.90, None),
            ("26",  110.50, None),
        ],
        "tacan": "82X",
        "freq": (134.6,  250.7),
    },
    "LLHB": {
        "ils": [("23", 109.90, None)],
        "freq": (119.75, 252.15),
    },
    "LLOV": {
        "vor": ("OVD", 112.20),
        "ils": [("21", 110.30, None)],
        "freq": (129.9,  250.05),
    },
    "LTAG": {
        "vor": ("INJ", 112.30),
        "ils": [
            ("05",  110.10, None),
            ("23",  109.90, None),
        ],
        "tacan": "21X",
        "freq": (122.1,  360.1),
    },
    "LTAF": {
        "vor": ("ADA", 112.70),
        "ils": [("05", 110.50, None)],
        "freq": (121.1,  251.25),
    },
    "OJMF": {
        "vor": ("MZR", 113.60),
        "ils": [("27", 110.30, None)],
        "tacan": "106X",
        "freq": (120.5,  253.15),
    },
    "OSKH": {
        "vor": ("KHL", 114.40),
        "ils": [("24", 110.10, None)],
        "freq": (122.5,  None),
    },
    "LLNV": {
        "vor": ("NTV", 112.80),
        "ils": [
            ("05", 110.50, None),
            ("23", 109.90, None),
        ],
        "freq": (132.4,  252.2),
    },
    "LLRD": {
        "vor": ("RDD", 113.40),
        "ils": [
            ("09", 110.30, None),
            ("27", 109.90, None),
        ],
        "tacan": "84X",
        "freq": (118.6,  251.3),
    },
    "LTAJ": {
        "vor": ("GZP", 116.00),
        "ils": [("10", 110.10, None)],
        "freq": (120.1,  250.1),
    },

    # -------------------------------------------------------------------------
    # NEVADA (NTTR)
    # -------------------------------------------------------------------------
    "KLSV": {
        "vor": ("LSV", 116.90),
        "ils": [
            ("03R", 111.30, None),
            ("21L", 110.90, None),
        ],
        "tacan": "12X",
        "freq": (132.55, 327.0),
    },
    "KLAS": {
        "vor": ("LAS", 116.90),
        "ils": [
            ("01L", 111.10, None),
            ("19R", 110.30, None),
            ("07L", 111.70, None),
            ("25R", 110.55, None),
        ],
        "freq": (119.9,  257.8),
    },
    "KTNX": {
        "vor": ("TNX", 116.00),
        "ils": [("14", 110.10, None)],
        "freq": (124.75, 257.95),
    },
    "KINS": {
        "vor": ("INS", 112.10),
        "ils": [("03", 109.90, None)],
        "tacan": "87X",
        "freq": (118.3,  360.6),
    },
    "KVGT": {
        "vor": ("VGT", 111.40),
        "ils": [("12L", 110.30, None)],
        "freq": (125.7,  360.75),
    },
    "KBTY": {
        "vor": ("BTY", 112.70),
    },
    "KIFP": {
        "vor": ("IFP", 115.60),
        "ils": [("16", 109.90, None)],
        "freq": (123.9,  None),
    },

    # -------------------------------------------------------------------------
    # MARIANA ISLANDS
    # -------------------------------------------------------------------------
    "PGUA": {
        "vor": ("UAM", 116.30),
        "ils": [
            ("06L", 110.30, None),
            ("24R", 109.90, None),
        ],
        "tacan": "54X",
        "freq": (126.2,  250.1),
    },
    "PGUM": {
        "vor": ("GUM", 116.80),
        "ils": [
            ("06L", 111.10, None),
            ("24R", 110.50, None),
        ],
        "freq": (118.1,  340.2),
    },
    "PGRO": {
        "vor": ("ROA", 116.00),
        "ils": [("09", 110.30, None)],
        "freq": (123.6,  250.0),
    },
    "PGSN": {
        "vor": ("SPN", 116.40),
        "ils": [("07", 110.10, None)],
        "freq": (125.7,  256.9),
    },
    "PGFT": {
        "vor": ("TIQ", 112.30),
        "freq": (123.65, 250.05),
    },

    # -------------------------------------------------------------------------
    # NORMANDY
    # -------------------------------------------------------------------------
    "LFRC": {
        "vor": ("CPB", 114.15),
        "ils": [("28", 110.30, None)],
    },
    "LFRK": {
        "vor": ("CGN", 114.90),
        "ils": [("31", 110.90, None)],
    },
    "LFOE": {
        "vor": ("EVX", 113.00),
        "ils": [("23", 110.10, None)],
    },
    "LFPG": {
        "vor": ("CGN", 115.35),
        "ils": [
            ("09L", 110.30, None),
            ("27R", 109.90, None),
        ],
    },
    "LFOH": {
        "vor": ("LHO", 113.60),
        "ils": [("05", 110.10, None)],
    },
    "LFQA": {
        "vor": ("LAO", 114.20),
        "ils": [("26", 109.90, None)],
    },
    "LFQB": {
        "vor": ("TRO", 114.70),
        "ils": [("27", 110.30, None)],
    },
    "LFPB": {
        "vor": ("LBG", 115.00),
        "ils": [
            ("09", 110.70, None),
            ("27", 110.10, None),
        ],
    },

    # -------------------------------------------------------------------------
    # THE CHANNEL
    # -------------------------------------------------------------------------
    "EGMH": {
        "vor": ("MID", 114.00),
        "ils": [("28", 110.10, None)],
    },
    "EGKB": {
        "vor": ("BIG", 115.10),
        "ils": [("21", 109.50, None)],
    },
    "EGLF": {
        "vor": ("FAR", 113.75),
        "ils": [("24", 110.90, None)],
    },
    "LFQQ": {
        "vor": ("LIL", 114.50),
        "ils": [("26", 110.30, None)],
    },
    "EGMC": {
        "vor": ("SND", 113.40),
        "ils": [("06", 110.90, None)],
    },
    "LFAY": {
        "vor": ("AMI", 113.80),
        "ils": [("27", 110.10, None)],
    },
    "LFAK": {
        "vor": ("DPN", 114.50),
        "ils": [("27", 109.90, None)],
    },

    # -------------------------------------------------------------------------
    # SOUTH ATLANTIC
    # -------------------------------------------------------------------------
    "EGYP": {
        "vor": ("MPA", 115.10),
        "ils": [
            ("10", 110.30, None),
            ("28", 109.90, None),
        ],
    },
    "SAWG": {
        "vor": ("RGL", 116.70),
        "ils": [("07", 110.10, None)],
    },
    "SAWE": {
        "vor": ("RGA", 113.60),
        "ils": [("07", 110.30, None)],
    },
    "SAVT": {
        "vor": ("USH", 115.40),
        "ils": [("25", 110.10, None)],
    },

    # -------------------------------------------------------------------------
    # SINAI
    # -------------------------------------------------------------------------
    "HEAR": {
        "vor": ("EAR", 114.20),
        "ils": [("10", 110.10, None)],
        "freq": (121.0,  251.05),
    },
    "HECW": {
        "vor": ("CWE", 113.60),
        "ils": [("09", 109.90, None)],
        "tacan": "114X",
        "freq": (131.2,  250.45),
    },
    "HECA": {
        "vor": ("CAI", 116.00),
        "ils": [
            ("05R", 111.10, None),
            ("23L", 110.50, None),
        ],
        "freq": (118.1,  250.4),
    },
    "HEGN": {
        "vor": ("HRG", 115.40),
        "ils": [("16", 110.30, None)],
        "freq": (119.6,  251.55),
    },
    "LLRM": {
        "vor": ("RAM", 113.10),
        "ils": [
            ("01",  110.90, None),
            ("19",  110.10, None),
        ],
        "freq": (119.8,  252.25),
    },
    "HESH": {
        "vor": ("SSH", 113.20),
        "ils": [("04", 110.50, None)],
        "freq": (118.9,  251.8),
    },
    "HESC": {
        "vor": ("SCT", 114.80),
        "freq": (124.5,  250.85),
    },
    "HETB": {
        "ndb": [("TBH", 290)],
        "freq": (118.8,  251.0),
    },

    # -------------------------------------------------------------------------
    # AFGHANISTAN
    # -------------------------------------------------------------------------
    "OAKS": {
        "vor": ("KDH", 112.70),
        "ils": [("05", 110.10, None)],
        "tacan": "75X",
        "freq": (125.5,  360.2),
    },
    "OAKB": {
        "vor": ("KBL", 116.50),
        "ils": [
            ("11", 110.30, None),
            ("29", 109.90, None),
        ],
        "tacan": "65X",
        "freq": (120.6,  284.25),
    },
    "OAIX": {
        "vor": ("BAG", 115.80),
        "ils": [("03", 110.10, None)],
        "tacan": "74X",
        "freq": (120.1,  325.75),
    },
    "OAHN": {
        "vor": ("HEA", 113.40),
        "ils": [("06", 110.30, None)],
        "tacan": "54X",
        "freq": (123.35, 240.3),
    },
    "OAMN": {
        "ndb": [("ZRJ", 275)],
    },

    # -------------------------------------------------------------------------
    # KOLA
    # -------------------------------------------------------------------------
    "ENBO": {
        "vor": ("BOD", 114.50),
        "ils": [
            ("07",  110.30, None),
            ("25",  109.90, None),
        ],
        "tacan": "45X",
        "freq": (118.45, 251.15),
    },
    "ENEV": {
        "vor": ("EVE", 113.80),
        "ils": [("16", 110.10, None)],
        "freq": (118.0,  250.8),
    },
    "ENKR": {
        "vor": ("KKN", 112.40),
        "ils": [("09", 109.70, None)],
        "freq": (120.35, 250.25),
    },
    "ULKK": {
        "vor": ("MMK", 115.00),
        "ils": [
            ("13",  110.90, None),
            ("31",  110.10, None),
        ],
        "freq": (127.3,  250.2),
    },
    "ULMK": {
        "vor": ("MCG", 114.20),
        "ils": [("26", 109.90, None)],
        "freq": (118.25, 250.1),
    },
    "ULAS": {
        "ils": [("24", 110.30, None)],
        "freq": (127.8,  251.2),
    },
    "ULAM": {
        "ils": [("26", 109.50, None)],
        "freq": (124.3,  251.1),
    },
    "ULWC": {
        "vor": ("OLE", 113.40),
        "ils": [("08", 110.10, None)],
        "freq": (131.4,  251.25),
    },
    "ENLK": {
        "vor": ("LKN", 113.90),
        "ils": [("07", 110.30, None)],
    },
    "ENMH": {
        "vor": ("MEH", 112.30),
        "ils": [("17", 109.90, None)],
    },
}


def navaid_lookup(icao: str) -> dict:
    """Return nav aid data for an ICAO code, or empty dict if not found."""
    return NAVAIDS.get(icao.upper(), {})


def tacan_lookup(icao: str) -> str:
    """Return the TACAN channel string for an airfield (e.g. '107X'), or '' if none."""
    return NAVAIDS.get(icao.upper(), {}).get("tacan", "")


def freq_lookup(icao: str) -> tuple[float, float | None] | None:
    """Return (vhf_mhz, uhf_mhz) for an airfield's DCS ATC frequency, or None if unknown.
    uhf_mhz is None when no UHF frequency is defined for that map.
    """
    return NAVAIDS.get(icao.upper(), {}).get("freq", None)


# ---------------------------------------------------------------------------
# Aircraft type classifier
# ---------------------------------------------------------------------------

# Aircraft whose DCS type name contains any of these substrings are Russian-origin
_RUSSIAN_PATTERNS = {
    "su-", "su_", "mig-", "mig_", "yak-", "yak_", "il-", "il_",
    "tu-", "tu_", "an-", "an_", "be-", "be_", "ka-", "ka_",
    "mi-", "mi_", "l-39", "l39",
    "su27", "su33", "su25", "su24", "su34", "su30", "su57",
    "mig21", "mig23", "mig25", "mig29", "mig31",
}

# Force NATO classification regardless
_NATO_PATTERNS = {
    "f-", "f_", "a-", "a_", "b-", "b_", "c-", "c_", "e-", "e_",
    "av-8", "av8", "hawk", "tornado", "typhoon", "eurofighter",
    "harrier", "jaguar", "mirage", "rafale", "m-2000",
    "f16", "f15", "f18", "f14", "f5", "f86", "f4",
    "a10", "a4", "av8b", "b52", "b1", "b2", "c130",
}


def classify_aircraft(aircraft_type: str) -> str:
    """
    Return 'russian' or 'nato' based on aircraft type name.
    Used to determine which nav aids to provide (NDB/RSBN vs ILS/VOR).
    """
    if not aircraft_type:
        return "nato"
    t = aircraft_type.lower()
    for pat in _NATO_PATTERNS:
        if pat in t:
            return "nato"
    for pat in _RUSSIAN_PATTERNS:
        if pat in t:
            return "russian"
    return "nato"


def navaid_summary(icao: str, aircraft_type: str) -> str:
    """
    Return a human-readable navaid string appropriate for the aircraft type.
    Russian aircraft get NDB/RSBN info; NATO aircraft get VOR/ILS info.
    """
    navaids = navaid_lookup(icao)
    if not navaids:
        return "No navaid data available."

    origin = classify_aircraft(aircraft_type)
    lines = []

    if origin == "russian":
        if navaids.get("ndb"):
            for ident, freq in navaids["ndb"]:
                lines.append(f"NDB: {ident} {freq} kHz")
        if navaids.get("rsbn"):
            for rwy, ch in navaids["rsbn"]:
                lines.append(f"RSBN runway {rwy}: channel {ch}")
        if navaids.get("vor"):
            ident, freq = navaids["vor"]
            lines.append(f"VOR: {ident} {freq:.2f} MHz")
    else:
        if navaids.get("vor"):
            ident, freq = navaids["vor"]
            lines.append(f"VOR: {ident} {freq:.2f} MHz")
        if navaids.get("ils"):
            for rwy, loc, gs in navaids["ils"]:
                gs_str = f" / GS {gs:.2f} MHz" if gs else ""
                lines.append(f"ILS runway {rwy}: LOC {loc:.2f} MHz{gs_str}")
        if not navaids.get("vor") and not navaids.get("ils"):
            if navaids.get("ndb"):
                for ident, freq in navaids["ndb"]:
                    lines.append(f"NDB: {ident} {freq} kHz")

    return " | ".join(lines) if lines else "No compatible navaids available."


# ---------------------------------------------------------------------------
# Magnetic variation lookup (degrees east; negative = degrees west)
# Region-level estimates keyed by two-character ICAO prefix.
# ---------------------------------------------------------------------------

_MAG_VAR_BY_PREFIX: dict[str, float] = {
    # Caucasus
    "UG": 5.5,   # Georgia
    "UR": 6.5,   # Russia (Caucasus / south)
    # Persian Gulf / Middle East
    "OM": 1.5,   # UAE
    "OO": 1.5,   # Oman
    "OI": 2.0,   # Iran
    "OS": 4.5,   # Syria
    "OL": 4.5,   # Lebanon
    "LC": 4.5,   # Cyprus
    "LL": 4.0,   # Israel
    "LT": 4.0,   # Turkey
    "OJ": 3.5,   # Jordan
    # Nevada (NTTR)
    "KL": 11.5, "KT": 11.5, "KI": 11.5, "KV": 11.5, "KB": 11.5,
    # Mariana Islands
    "PG": -2.0,
    # Normandy / France
    "LF": -2.5,
    # Channel / UK  (EGYP override below)
    "EG": -1.5,
    # South Atlantic
    "SA": -13.0,
    # Sinai / Egypt
    "HE": 3.5,
    # Afghanistan
    "OA": 3.5,
    # Kola — Norway
    "EN": 12.0,
    # Kola — Russia
    "UL": 15.0, "UK": 15.0,
}

# Per-airport overrides where the prefix gives the wrong result
_MAG_VAR_OVERRIDES: dict[str, float] = {
    "EGYP": -10.0,   # Mount Pleasant, Falklands (EG prefix, but southern hemisphere)
}


def mag_var_lookup(icao: str) -> float:
    """Return approximate magnetic variation (degrees east) for a DCS airfield."""
    icao = icao.upper()
    if icao in _MAG_VAR_OVERRIDES:
        return _MAG_VAR_OVERRIDES[icao]
    return _MAG_VAR_BY_PREFIX.get(icao[:2], 0.0)


def preferred_runway(icao: str) -> str | None:
    """
    Return the preferred runway designator for an airfield.
    Uses the first ILS entry in NAVAIDS as the primary approach runway.
    Returns None for airports with no ILS data (caller should require manual override).
    """
    navaids = NAVAIDS.get(icao.upper(), {})
    ils = navaids.get("ils", [])
    return ils[0][0] if ils else None


def runway_to_heading(runway: str) -> int:
    """
    Convert a runway designator to its approximate magnetic inbound heading.
    Examples: "28" → 280, "10L" → 100, "04" → 40.
    """
    num_str = ""
    for ch in runway:
        if ch.isdigit():
            num_str += ch
        else:
            break
    return int(num_str) * 10 if num_str else 0
