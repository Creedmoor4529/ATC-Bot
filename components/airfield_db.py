"""
DCS airfield database — all maps.
Provides (lat, lon, elevation_ft) keyed by ICAO code.
Used by config.py when BOT_LAT/BOT_LON are not set in config.lua.
Coordinates are approximate DCS positions.
"""

# ICAO: (lat, lon, elevation_ft)
AIRFIELDS: dict[str, tuple[float, float, int]] = {

# --- Afghanistan ---
    "OABM": (34.8063, 67.8069,  8490),  # Bamyan
    "OABN": (31.8358, 64.2202,  2886),  # Camp Bastion
    "OABT": (31.5520, 64.3633,  2546),  # Bost
    "OACC": (34.5294, 65.2802,  7450),  # Chaghcharan
    "OADR": (31.0856, 64.0576,  2398),  # Dwyer
    "OAFR": (32.3549, 62.1731,  2240),  # Farah
    "OAFS": (33.3632, 69.9587,  3777),  # FOB Salerno
    "OAGZ": (33.6216, 69.2331,  7725),  # Gardez
    "OAHR": (34.2200, 62.2301,  3182),  # Herat
    "OAIX": (34.9588, 69.2754,  4895),  # Bagram
    "OAJL": (34.4061, 70.4906,  1841),  # Jalalabad
    "OAKB": (34.5702, 69.1963,  5869),  # Kabul
    "OAKN": (31.5132, 65.8607,  3336),  # Kandahar
    "OAKT": (33.3365, 69.9592,  3754),  # Khost
    "OAMN": (35.9244, 64.7662,  2758),  # Maymana Zahiraddin Faryabi
    "OAQN": (34.9921, 63.1245,  2921),  # Qala i Naw
    "OASA": (33.1211, 68.8420,  7391),  # Sharana
    "OASD": (33.3830, 62.2604,  3716),  # Shindand
    "OATN": (32.6099, 65.8565,  4374),  # Tarinkot
    "OAZJ": (30.9709, 62.0538,  1585),  # Nimroz

# --- Caucasus ---
    "UGKG": (43.1242, 40.5642,    69),  # Gudauta
    "UGKO": (42.1792, 42.4957,   148),  # Kutaisi
    "UGKS": (41.9321, 41.8765,    59),  # Kobuleti
    "UGSB": (41.6033, 41.6093,    33),  # Batumi
    "UGSN": (42.2387, 42.0610,    43),  # Senaki-Kolkhi
    "UGSS": (42.8527, 41.1424,    44),  # Sukhumi-Babushara
    "UGTB": (41.6747, 44.9469,  1574),  # Tbilisi-Lochini
    "UGTS": (41.6412, 44.9472,  1474),  # Soganlug
    "UGTV": (41.6377, 45.0191,  1524),  # Vaziani
    "URKA": (45.0132, 37.3598,   141),  # Anapa-Vityazevo
    "URKG": (44.9614, 37.9859,    66),  # Krymsk
    "URKH": (44.6714, 40.0214,   591),  # Maykop-Khanskaya
    "URKK": (45.0461, 39.2031,   112),  # Krasnodar-Pashkovsky
    "URKN": (43.5101, 43.6251,  1411),  # Nalchik
    "URKN2": (44.6733, 37.7862,   131),  # Novorossiysk
    "URMG": (44.5677, 38.0041,    72),  # Gelendzhik
    "URMM": (44.2186, 43.1007,  1050),  # Mineralnye Vody
    "URMO": (43.2085, 44.5889,  1719),  # Beslan
    "URMZ": (43.7913, 44.6203,   507),  # Mozdok
    "URRR": (45.0874, 38.9252,    98),  # Krasnodar-Center
    "URSS": (43.4394, 39.9242,    98),  # Sochi-Adler

# --- GermanyCW ---
    "EDAB": (51.3303, 12.6701,   509),  # Brandis
    "EDAC": (51.7214, 11.9791,   284),  # Kothen
    "EDAD": (51.8321, 12.1770,   195),  # Dessau
    "EDAM": (51.3616, 11.9330,   340),  # Merseburg
    "EDAS": (51.3966, 12.4175,   415),  # Leipzig Mockau
    "EDAV": (52.8249, 13.7118,   111),  # Finow
    "EDAY": (53.3562, 13.7771,   176),  # Dedelow
    "EDBA": (51.3838, 11.4632,   930),  # Allstedt
    "EDBC": (51.8538, 11.4005,   569),  # Cochstedt
    "EDBH": (54.3385, 12.7022,    21),  # Barth
    "EDBM": (53.5680, 12.6588,   261),  # Waren Vielist
    "EDBN": (53.6022, 13.2906,   177),  # Neubrandenburg
    "EDCG": (53.8759, 14.1678,    66),  # Garz
    "EDCN": (53.6212, 11.5651,   149),  # Pinnow
    "EDCP": (54.1665, 13.7615,    23),  # Peenemunde
    "EDCT": (53.9314, 13.2165,     7),  # Tutow
    "EDCW": (53.9143, 11.4979,    32),  # Wismar
    "EDDB": (52.3885, 13.5537,   146),  # Schonefeld
    "EDDE": (50.9781, 10.9760,  1012),  # Bindersleben
    "EDDF": (50.0466, 8.5942,   328),  # Frankfurt
    "EDDH": (53.6351, 9.9986,    73),  # Hamburg
    "EDDI": (52.4710, 13.3897,   154),  # Tempelhof
    "EDDK": (50.8778, 7.1338,   236),  # Cologne
    "EDDL": (51.2816, 6.7558,   121),  # Dusseldorf
    "EDDP": (51.4118, 12.2440,   421),  # Schkeuditz
    "EDDT": (52.5598, 13.3100,   116),  # Tegel
    "EDDV": (52.4538, 9.7104,   168),  # Hannover
    "EDDW": (53.0469, 8.7747,    41),  # Bremen
    "EDFB": (50.5400, 9.6471,   937),  # Fulda
    "EDFG": (50.1958, 9.1595,   417),  # Gelnhausen
    "EDFH": (49.9565, 7.2723,  1621),  # Hahn
    "EDFS": (50.0489, 10.1740,   753),  # Schweinfurt
    "EDFV": (49.8652, 7.9649,   413),  # Sprendlingen
    "EDFZ": (49.9683, 8.1414,   722),  # Mainz Finthen
    "EDGA": (49.3636, 9.4276,  1199),  # Adelsheim
    "EDGH": (51.7055, 10.8860,  1619),  # Hasselfelde
    "EDGM": (54.3894, 12.8981,    10),  # Gross Mohrdorf
    "EDGW": (52.1376, 10.5763,   278),  # Grosse Wiese
    "EDHA": (50.9890, 10.4943,  1017),  # Haina
    "EDHE": (53.6459, 9.7121,    23),  # Uetersen
    "EDHG": (53.2490, 10.4639,   148),  # Luneburg
    "EDHI": (53.5294, 9.8221,    10),  # Hamburg Finkenwerder
    "EDHK": (54.3791, 10.1360,    53),  # Kiel
    "EDHL": (53.8023, 10.7018,    75),  # Lubeck
    "EDIE": (49.3940, 8.6590,   346),  # Heidelberg
    "EDLD": (49.4028, 7.5363,  1182),  # Landstuhl
    "EDLG": (52.3245, 10.1726,   159),  # Glindbruchkippe
    "EDOA": (53.3039, 12.7356,   207),  # Larz
    "EDOG": (52.5277, 11.3575,   183),  # Gardelegen
    "EDOI": (52.6563, 12.7526,    98),  # Bienenfarm
    "EDOJ": (52.1380, 13.2881,   185),  # Sperenberg
    "EDOL": (51.9969, 12.9666,   312),  # Altes Lager
    "EDOP": (53.4233, 11.7693,   171),  # Parchim
    "EDOS": (51.2654, 10.6439,   889),  # Obermehler Schlotheim
    "EDOV": (52.6281, 11.8059,   122),  # Stendal
    "EDOW": (52.6652, 13.0048,   135),  # Perwenitz
    "EDOX": (52.9675, 9.2773,   147),  # Verden-Scharnhorst
    "EDQG": (49.6465, 9.9527,   953),  # Giebelstadt
    "EDRZ": (49.2005, 7.3924,  1083),  # Zweibrucken
    "EDTH": (51.6866, 12.2079,   282),  # Thurland
    "EDUB": (52.0357, 13.7630,   164),  # Brand
    "EDUE": (51.5485, 13.2364,   285),  # Falkenberg
    "EDUG": (52.4766, 13.1510,   136),  # Gatow
    "EDUH": (52.6136, 14.2590,    49),  # Marxwalde
    "EDUK": (53.1952, 12.1571,   287),  # Kammermark
    "EDUM": (52.6187, 10.4144,   219),  # Ummern
    "EDUO": (52.7154, 13.2227,   108),  # Oranienburg
    "EDUT": (53.0320, 13.5681,   242),  # Templin
    "EDUW": (52.6310, 13.7511,   259),  # Werneuchen
    "EDUZ": (51.9952, 12.1281,   250),  # Zerbst
    "EDVE": (52.3194, 10.5638,   273),  # Braunschweig
    "EDVM": (52.1809, 9.9542,   322),  # Hildesheim
    "EDVN": (52.9846, 11.2438,    49),  # Northeim
    "EDVR": (52.1759, 9.0491,   174),  # Rinteln
    "EDVU": (52.9836, 10.4723,   249),  # Uelzen
    "EDXJ": (53.3183, 9.5759,   125),  # Sittensen
    "EDXW": (53.0609, 9.2083,    82),  # Weser Wumme
    "EKCH": (55.6144, 12.6646,    25),  # Kastrup
    "EKRN": (55.0672, 14.7451,    49),  # Bornholm
    "EPCJ": (52.9390, 14.4383,   176),  # Chojna
    "EPSC": (53.5789, 14.9130,    98),  # Szczecin-Goleniow
    "ESMS": (55.5479, 13.3744,   217),  # Sturup
    "ESMT": (55.5949, 13.7219,   115),  # Tagra
    "ESMV": (55.7261, 13.4425,    58),  # Revinge
    "ETAB": (49.9503, 6.5774,  1208),  # Bitburg
    "ETAD": (49.9859, 6.7136,   984),  # Spangdahlem
    "ETAR": (49.4373, 7.6156,   805),  # Ramstein
    "ETHB": (52.2772, 9.0713,   193),  # Buckeburg
    "ETHC": (52.5926, 10.0394,   126),  # Celle
    "ETHF": (51.1125, 9.2911,   552),  # Fritzlar
    "ETHM": (52.3880, 11.8444,   143),  # Mahlwinkel
    "ETHM2": (50.3676, 7.3265,   601),  # Mendig
    "ETHN": (52.9428, 12.7696,   148),  # Neuruppin
    "ETHS": (52.9192, 10.1665,   254),  # Fassberg
    "ETMD": (54.2609, 12.4270,    26),  # Damgarten
    "ETMN": (53.7694, 8.6758,    39),  # Nordholz
    "ETNL": (53.9198, 12.2608,   115),  # Laage
    "ETNN": (50.8273, 6.6431,   296),  # Norvenich
    "ETNW": (52.4583, 9.4403,   166),  # Wunstorf
    "ETOB": (52.4405, 12.4710,   115),  # Briest
    "ETOU": (50.0474, 8.3113,   453),  # Wiesbaden
    "ETSB": (50.1648, 7.0553,  1509),  # Buchel
    "ETSH": (51.7668, 13.1889,   245),  # Holzdorf
    "ETSP": (49.8546, 7.5888,  1313),  # Pferdsfeld
    "ETSW": (53.2049, 12.5403,   222),  # Wittstock
    "ETUO": (51.9231, 8.2908,   213),  # Gutersloh
    "ETUS": (49.5106, 7.8782,  1022),  # Sembach

# --- Iraq ---
    "ORAA": (33.7811, 42.4073,   568),  # Al-Asad Airbase
    "ORAK": (32.4878, 45.7431,    40),  # Al-Kut Airport
    "ORAS": (33.2873, 44.4880,    76),  # Al-Salam Airbase
    "ORAT": (33.3460, 43.5848,   260),  # Al-Taquddum Airport
    "ORBD": (33.9526, 44.3595,   144),  # Balad Airbase
    "ORBI": (33.2676, 44.2179,    96),  # Baghdad International Airport
    "ORBM": (36.3150, 43.1430,   742),  # Mosul International Airport
    "ORBP": (36.5401, 44.3335,  2004),  # Bashur Airport
    "ORER": (36.2583, 43.9471,  1226),  # Erbil International Airport
    "ORH2": (33.3638, 40.5861,  2070),  # H-2 Airbase
    "ORH3": (32.9406, 39.7338,  2542),  # H-3 Main Airbase
    "ORH3NW": (33.0815, 39.5866,  2551),  # H-3 Northwest Airbase
    "ORH3SW": (32.7481, 39.5935,  2648),  # H-3 Southwest Airbase
    "ORK1": (35.5072, 44.2894,   976),  # K1 Base
    "ORKK": (35.4766, 44.3379,  1027),  # Kirkuk International Airport
    "ORQW": (35.7781, 43.1148,   721),  # Qayyarah Airfield West
    "ORSU": (35.5705, 45.3025,  2430),  # Sulaimaniyah International Airport
    "ORTI": (33.5170, 44.2592,   116),  # Al-Taji Airport
    "ORTL": (34.6763, 43.5290,   428),  # Al-Sahra Airport

# --- Kola ---
    "EFET": (68.3560, 23.4110,   998),  # Enontekio
    "EFHS": (65.8986, 25.7218,   379),  # Hosio
    "EFIV": (68.6133, 27.4240,   468),  # Ivalo
    "EFKE": (65.7921, 24.5863,    47),  # Kemi Tornio
    "EFKS": (65.9947, 29.2211,   864),  # Kuusamo
    "EFKT": (67.7106, 24.8413,   637),  # Kittila
    "EFRO": (66.5746, 25.8500,   612),  # Rovaniemi
    "EFSO": (67.4010, 26.6158,   595),  # Sodankyla
    "EFVU": (67.0759, 26.5605,   736),  # Vuojarvi
    "ENAN": (69.3067, 16.1212,    22),  # Andoya
    "ENAT": (69.9736, 23.3822,     9),  # Alta
    "ENBO": (67.2670, 14.3355,    26),  # Bodo
    "ENDU": (69.0522, 18.5664,   225),  # Bardufoss
    "ENEV": (68.5025, 16.6776,    86),  # Evenes
    "ENKR": (69.7280, 29.9120,   282),  # Kirkenes
    "ENNA": (70.0578, 24.9753,    17),  # Banak
    "ESNJ": (66.5035, 20.1349,   879),  # Jokkmokk
    "ESNQ": (67.8303, 20.3523,  1435),  # Kiruna
    "ESNX": (65.5982, 19.2582,  1240),  # Arvidsjaur
    "ESPA": (65.5546, 22.0986,    65),  # Kallax
    "ESPB": (65.8105, 21.6926,    42),  # Boden Heli Base
    "ESPE": (65.8797, 20.1295,   594),  # Vidsel
    "ESUK": (67.7699, 20.2496,  1552),  # Kalixfors
    "ESUT": (65.7997, 15.0901,  1502),  # Hemavan
    "ULAF": (67.4542, 32.8099,   495),  # Afrikanda
    "ULAM": (68.8568, 33.7159,   567),  # Severomorsk-3
    "ULAS": (69.0410, 33.4048,   262),  # Severomorsk-1
    "ULKK": (68.7908, 32.7354,   249),  # Murmansk International
    "ULKL": (65.2118, 31.1384,   400),  # Kalevala
    "ULKY": (69.2629, 31.2089,   471),  # Koshka Yavr
    "ULMA": (66.9664, 30.3659,   548),  # Alakurtti
    "ULMK": (67.9801, 33.0055,   548),  # Monchegorsk
    "ULMK2": (69.1018, 32.4203,   305),  # Kilpyavr
    "ULMP": (69.4070, 30.9993,   249),  # Luostari Pechenga
    "ULPD": (64.9167, 34.2861,   157),  # Poduzhemye
    "ULWC": (68.1656, 33.4782,   722),  # Olenya

# --- MarianaIslands ---
    "PGFT": (14.9974, 145.6083,   240),  # Tinian Intl
    "PGOR": (13.4398, 144.6468,    94),  # Olf Orote
    "PGPG": (18.1242, 145.7611,    50),  # Pagan Airstrip
    "PGRO": (14.1749, 145.2325,   569),  # Rota Intl
    "PGSN": (15.1151, 145.7188,   213),  # Saipan Intl
    "PGUA": (13.5760, 144.9175,   546),  # Andersen AFB
    "PGUM": (13.4796, 144.7848,   255),  # Antonio B. Won Pat Intl

# --- MarianaIslandsWWII ---
    "WAF3": (15.0687, 145.6313,    85),  # Airfield 3
    "WAGN": (13.4806, 144.7837,   258),  # Agana
    "WCKA": (15.1564, 145.7028,    11),  # Charon Kanoa
    "WGRG": (15.0022, 145.5943,   280),  # Gurguan Point
    "WISL": (15.1200, 145.7224,   191),  # Isley
    "WKAG": (15.1680, 145.7688,   230),  # Kagman
    "WMRP": (15.2834, 145.8092,   148),  # Marpi
    "WORO": (13.4398, 144.6336,    82),  # Orote
    "WPAG": (18.1244, 145.7620,    49),  # Pagan
    "WROT": (14.1749, 145.2373,   595),  # Rota
    "WUSH": (15.0788, 145.6321,    83),  # Ushi

# --- Nevada ---
    "K0L7": (35.7738, -115.3257,  2824),  # Jean
    "K0L9": (36.3105, -114.4693,  1549),  # Echo Bay
    "K1L1": (37.7934, -114.4192,  4815),  # Lincoln County
    "K3Q0": (38.3745, -118.0935,  4562),  # Mina
    "K67L": (36.8273, -114.0603,  1859),  # Mesquite
    "KBTY": (36.8684, -116.7861,  3173),  # Beatty
    "KBVU": (35.9437, -114.8606,  2122),  # Boulder City
    "KHND": (35.9675, -115.1335,  2492),  # Henderson Executive
    "KIFP": (35.1659, -114.5599,   656),  # Laughlin
    "KINS": (36.5844, -115.6868,  3126),  # Creech
    "KLAS": (36.0767, -115.1622,  2170),  # McCarran International
    "KLSV": (36.2257, -115.0438,  1842),  # Nellis
    "KPMS": (37.0948, -116.3154,  5057),  # Pahute Mesa
    "KTNX": (37.7840, -116.7733,  5534),  # Tonopah Test Range
    "KTPH": (38.0580, -117.0759,  5394),  # Tonopah
    "KVGT": (36.2134, -115.1867,  2229),  # North Las Vegas
    "KXTA": (37.2191, -115.7853,  4494),  # Groom Lake

# --- PersianGulf ---
    "OIBA": (25.8750, 55.0214,    16),  # Abu Musa Island
    "OIBK": (26.5297, 53.9649,   115),  # Kish Intl
    "OIBL": (26.5308, 54.8131,    81),  # Bandar Lengeh
    "OIBP": (26.8154, 53.3416,    75),  # Lavan Island
    "OIBS": (25.9033, 54.5482,    18),  # Sirri Island
    "OIBT": (26.2515, 55.3113,    43),  # Tunb Island AFB
    "OIBTK": (26.2436, 55.1494,    15),  # Tunb Kochak
    "OIKB": (27.2036, 56.3704,    18),  # Bandar Abbas Intl
    "OIKJ": (28.7316, 57.6641,  2664),  # Jiroft
    "OIKK": (30.2577, 56.9583,  5746),  # Kerman
    "OIKP": (27.1599, 56.1831,    51),  # Havadarya
    "OIKQ": (26.7663, 55.9181,    26),  # Qeshm Island
    "OISL": (27.6748, 54.3683,  2636),  # Lar
    "OISS": (29.5331, 52.6099,  4879),  # Shiraz Intl
    "OIZJ": (25.6505, 57.7921,    26),  # Bandar-e-Jask
    "OMAA": (24.4647, 54.6392,    92),  # Abu Dhabi Intl
    "OMAB": (24.4341, 54.4507,    12),  # Al-Bateen
    "OMAD": (24.2579, 54.5342,    52),  # Al Dhafra AFB
    "OMAL": (24.2768, 55.6117,   814),  # Al Ain Intl
    "OMAW": (23.6607, 53.8125,   400),  # Liwa AFB
    "OMDB": (25.2483, 55.3793,    16),  # Dubai Intl
    "OMDM": (25.0268, 55.3837,   191),  # Al Minhad AFB
    "OMDW": (24.8886, 55.1749,   123),  # Al Maktoum Intl
    "OMFJ": (25.1057, 56.3404,    61),  # Fujairah Intl
    "OMQS": (22.7760, 55.0771,   330),  # Quasoura_airport
    "OMRK": (25.6023, 55.9419,    71),  # Ras Al Khaimah Intl
    "OMSA": (25.2162, 54.2369,    25),  # Sir Abu Nuayr
    "OMSJ": (25.3228, 55.5314,    98),  # Sharjah Intl
    "OMSN": (24.4482, 54.5147,    10),  # Sas Al Nakheel
    "OOKB": (26.1798, 56.2432,    48),  # Khasab

# --- SinaiMap ---
    "HEAR": (31.0259, 33.8246,   311),  # El Arish
    "HEAS": (30.5704, 32.1098,    19),  # Abu Suwayr
    "HEAU": (28.9053, 33.1954,     3),  # Abu Rudeis
    "HEBA": (30.9287, 29.6839,    85),  # Borg El Arab International Airport
    "HEBH": (26.5455, 33.1286,  1165),  # Al Bahr al Ahmar
    "HEBL": (30.3863, 31.6097,    92),  # Bilbeis Air Base
    "HEBN": (29.1829, 31.0161,    98),  # Beni Suef
    "HEBR": (30.8268, 30.9443,    20),  # Birma Air Base
    "HEBZ": (31.0015, 32.5613,   120),  # Baluza
    "HECA": (30.0981, 31.4199,   394),  # Cairo International Airport
    "HECW": (30.0932, 30.8998,   440),  # Cairo West
    "HEDS": (30.4238, 32.3350,     7),  # Difarsuwar Airfield
    "HEFD": (30.3287, 32.2821,    28),  # Fayed
    "HEGB": (30.5500, 30.5460,    79),  # Gebel El Basur Air Base
    "HEGN": (27.1934, 33.7870,    43),  # Hurghada International Airport
    "HEGR": (31.0709, 34.1377,   423),  # El Gora
    "HEIN": (30.3270, 31.4372,   155),  # Inshas Airbase
    "HEIS": (30.5901, 32.2467,    11),  # Al Ismailiyah
    "HEJK": (30.8295, 30.1805,    26),  # Jiyanklis Air Base
    "HEKB": (30.2352, 32.5001,    13),  # Kibrit Air Base
    "HEKH": (30.3133, 30.8731,    46),  # Al Khatatbah
    "HEKW": (29.5446, 30.8986,     7),  # Kom Awshim
    "HEMN": (28.0893, 30.7350,   125),  # El Minya
    "HEMS": (30.9556, 31.4409,     7),  # Al Mansurah
    "HEMZ": (30.4010, 33.1562,  1004),  # Melez
    "HEQS": (30.5907, 31.1261,    33),  # Quwaysina
    "HERM": (31.0326, 30.6688,    10),  # Al Rahmaniyah Air Base
    "HESC": (28.6766, 34.0638,  4256),  # St Catherine
    "HESH": (27.9692, 34.3829,    98),  # Sharm El Sheikh International Airport
    "HESL": (30.7830, 32.0378,     8),  # As Salihiyah
    "HETB": (30.1880, 33.4256,  1225),  # Bir Hasanah
    "HETB2": (29.6008, 34.7917,  2326),  # Taba International Airport
    "HEWJ": (30.0576, 31.8283,   749),  # Wadi al Jandali
    "HEWR": (28.9878, 31.7037,   984),  # Wadi Abu Rish
    "HEZQ": (30.5823, 31.6637,     7),  # AzZaqaziq
    "LLBG": (31.9970, 34.8863,    99),  # Ben-Gurion
    "LLER": (29.7421, 35.0186,   226),  # Ramon International Airport
    "LLES": (32.4399, 35.0136,    48),  # Ein Shamer
    "LLHB": (31.2357, 34.6697,   686),  # Hatzerim
    "LLHS": (31.7549, 34.7157,   100),  # Hatzor
    "LLKM": (31.2585, 34.6484,   634),  # Kedem
    "LLMG": (32.5976, 35.2200,   133),  # Megiddo
    "LLNV": (31.2054, 34.9959,  1303),  # Nevatim
    "LLOV": (29.9306, 34.9291,  1434),  # Ovda
    "LLPM": (31.8931, 34.6878,    33),  # Palmachim
    "LLRD": (32.6749, 35.1774,   100),  # Ramat David
    "LLRM": (30.7733, 34.6538,  2031),  # Ramon Airbase
    "LLSD": (32.1198, 34.7858,    20),  # Sde Dov
    "LLTN": (31.8261, 34.8170,   142),  # Tel Nof
    "OEKF": (30.3370, 36.1632,  2859),  # King Feisal Air Base
    "OETB": (28.3798, 36.5957,  2543),  # Tabuk
    "OLBA": (33.8384, 35.4797,    20),  # Rafic Hariri Intl
    "OSDI": (33.3856, 36.4964,  2006),  # Damascus Intl
    "OSKH": (33.0894, 36.5339,  2346),  # Khalkhalah Air Base
    "OSMZ": (33.4720, 36.2115,  2392),  # Mezzeh Air Base

# --- Syria ---
    "LCEN": (35.1593, 33.4901,   312),  # Ercan
    "LCGK": (35.2364, 33.7073,   148),  # Gecitkale
    "LCLK": (34.8656, 33.6136,    16),  # Larnaca
    "LCLT": (35.1063, 33.3217,   758),  # Lakatamia
    "LCNC": (35.1438, 33.2821,   689),  # Nicosia
    "LCPH": (34.7224, 32.4718,    86),  # Paphos
    "LCPN": (35.2783, 33.2670,   771),  # Pinarbashi
    "LCRA": (34.5941, 32.9748,    69),  # Akrotiri
    "LCRA2": (35.0166, 33.7217,   276),  # Kingsfield
    "LLBG": (32.0124, 34.8709,   134),  # Ben Gurion
    "LLES": (32.4398, 35.0147,   109),  # Eyn Shemer
    "LLHA": (32.8065, 35.0450,    20),  # Haifa
    "LLHS": (31.7662, 34.7353,   110),  # Hatzor
    "LLHZ": (32.1773, 34.8441,   118),  # Herzliya
    "LLIB": (32.9793, 35.5727,   866),  # Rosh Pina
    "LLKS": (33.2124, 35.5924,   341),  # Kiryat Shmona
    "LLMG": (32.5976, 35.2202,   180),  # Megiddo
    "LLPM": (31.8949, 34.6888,    45),  # Palmachim
    "LLRD": (32.6751, 35.1773,   133),  # Ramat David
    "LLTN": (31.8297, 34.8379,   209),  # Tel Nof
    "LTAF": (36.9883, 35.2914,    56),  # Adana Sakirpasa
    "LTAG": (36.9943, 35.4127,   157),  # Incirlik
    "LTAJ": (36.9518, 37.4627,  2294),  # Gaziantep
    "LTCH": (37.4605, 38.9129,  2703),  # Sanliurfa
    "LTDA": (36.3713, 36.2981,   228),  # Hatay
    "LTFG": (36.2978, 32.2861,    36),  # Gazipasa
    "OJAM": (31.9990, 36.2322,  2297),  # King Abdullah II
    "OJAM2": (31.9787, 36.0070,  2455),  # Marka
    "OJH3": (32.9410, 39.7326,  2541),  # H3
    "OJH3NW": (33.0704, 39.6066,  2578),  # H3 Northwest
    "OJH3SW": (32.7380, 39.6122,  2671),  # H3 Southwest
    "OJH4": (32.5369, 38.2064,  2257),  # H4
    "OJMA": (32.3488, 36.2702,  2205),  # King Hussein Air College
    "OJMF": (31.8192, 36.7908,  1636),  # Muwaffaq Salti
    "OJPH": (32.1522, 37.1606,  2148),  # Prince Hassan
    "OJRW": (32.4037, 39.1422,  2979),  # Ruwayshid
    "OJTH": (32.6981, 36.4027,  2381),  # Tha'lah
    "OLBA": (33.8365, 35.4874,    39),  # Beirut-Rafic Hariri
    "OLKA": (34.5840, 35.9987,    14),  # Rene Mouawad
    "OLRA": (33.8429, 35.9769,  2976),  # Rayak
    "OLWH": (34.2870, 35.6840,   619),  # Wujah Al Hajar
    "OSABD": (35.7315, 37.1188,   820),  # Abu al-Duhur
    "OSAN": (33.9266, 36.8753,  2737),  # An Nasiriyah
    "OSAP": (36.1790, 37.2383,  1254),  # Aleppo
    "OSDI": (33.4153, 36.5043,  2008),  # Damascus
    "OSDR": (33.6147, 36.7625,  2067),  # Al-Dumayr
    "OSDZ": (35.2900, 40.1614,   713),  # Deir ez-Zor
    "OSHM": (35.1161, 36.7255,   984),  # Hama
    "OSJI": (36.0994, 37.9209,  1138),  # Jirah
    "OSKH": (33.0883, 36.5346,  2323),  # Khalkhalah
    "OSKW": (36.1894, 37.5704,  1186),  # Kuweires
    "OSLK": (35.4116, 35.9500,    93),  # Bassel Al-Assad
    "OSMN": (36.5228, 37.0336,  1614),  # Minakh
    "OSMR": (33.2842, 36.4443,  2161),  # Marj Ruhayyil
    "OSMS1": (33.5004, 36.4663,  2008),  # Marj as Sultan North
    "OSMS2": (33.4875, 36.4745,  2006),  # Marj as Sultan South
    "OSMZ": (33.4827, 36.2351,  2356),  # Mezzeh
    "OSPR": (34.5582, 38.3311,  1267),  # Palmyra
    "OSQS": (34.5669, 36.5854,  1729),  # Al Qusayr
    "OSQS2": (33.4586, 36.3569,  2134),  # Qabr as Sitt
    "OSSH": (34.4946, 36.8945,  2638),  # Shayrat
    "OSSQ": (33.6801, 37.2041,  2274),  # Sayqal
    "OSTB": (35.7556, 38.5513,  1099),  # Tabqa
    "OSTF": (35.9732, 36.7859,  1020),  # Taftanaz
    "OSTI": (34.5225, 37.6458,  1798),  # Tiyas
    "OSTS": (36.2635, 38.9241,   981),  # Tal Siman

    # ---- NORMANDY (preserved — map not owned) ----
    "LFRC": (49.651,  -1.470,    459),  # Cherbourg-Maupertus
    "LFRK": (49.173,  -0.447,    256),  # Caen-Carpiquet
    "LFOH": (49.534,   0.088,    312),  # Le Havre-Octeville
    "LFQA": (49.859,   2.388,    295),  # Laon-Couvron
    "LFQB": (48.322,   3.997,    381),  # Troyes-Barberey
    "LFOE": (48.718,   1.176,    456),  # Evreux-Fauville
    "LFPG": (49.013,   2.550,    392),  # Paris Charles de Gaulle
    "LFPB": (48.970,   2.441,    217),  # Paris Le Bourget

    # ---- THE CHANNEL (preserved — map not owned) ----
    "EGMH": (51.342,   1.341,    178),  # Manston
    "EGKB": (51.331,   0.033,    598),  # Biggin Hill
    "EGLF": (51.278,  -0.776,    238),  # Farnborough
    "EGMC": (51.572,   0.696,     49),  # Southend
    "LFQQ": (50.562,   3.089,    160),  # Lille-Lesquin
    "LFAY": (49.874,   2.716,    361),  # Amiens-Glisy
    "LFAK": (50.174,   3.154,    252),  # Denain-Prouvy

    # ---- SOUTH ATLANTIC (preserved — map not owned) ----
    "EGYP": (-51.823, -58.447,   244),  # Mount Pleasant (Port Stanley)
    "SAWG": (-51.609, -69.313,    61),  # Rio Gallegos
    "SAWE": (-53.778, -67.750,    65),  # Rio Grande
    "SAVT": (-54.843, -68.295,    86),  # Ushuaia Malvinas
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
MAP_AIRFIELDS: dict[str, set[str]] = {
    "Afghanistan": {
        "OABM", "OABN", "OABT", "OACC", "OADR", "OAFR", "OAFS", "OAGZ", "OAHR",
        "OAIX", "OAJL", "OAKB", "OAKN", "OAKT", "OAMN", "OAQN", "OASA", "OASD",
        "OATN", "OAZJ",
    },
    "Caucasus": {
        "UGKG", "UGKO", "UGKS", "UGSB", "UGSN", "UGSS", "UGTB", "UGTS", "UGTV",
        "URKA", "URKG", "URKH", "URKK", "URKN", "URKN2", "URMG", "URMM", "URMO",
        "URMZ", "URRR", "URSS",
    },
    "GermanyCW": {
        "EDAB", "EDAC", "EDAD", "EDAM", "EDAS", "EDAV", "EDAY", "EDBA", "EDBC",
        "EDBH", "EDBM", "EDBN", "EDCG", "EDCN", "EDCP", "EDCT", "EDCW", "EDDB",
        "EDDE", "EDDF", "EDDH", "EDDI", "EDDK", "EDDL", "EDDP", "EDDT", "EDDV",
        "EDDW", "EDFB", "EDFG", "EDFH", "EDFS", "EDFV", "EDFZ", "EDGA", "EDGH",
        "EDGM", "EDGW", "EDHA", "EDHE", "EDHG", "EDHI", "EDHK", "EDHL", "EDIE",
        "EDLD", "EDLG", "EDOA", "EDOG", "EDOI", "EDOJ", "EDOL", "EDOP", "EDOS",
        "EDOV", "EDOW", "EDOX", "EDQG", "EDRZ", "EDTH", "EDUB", "EDUE", "EDUG",
        "EDUH", "EDUK", "EDUM", "EDUO", "EDUT", "EDUW", "EDUZ", "EDVE", "EDVM",
        "EDVN", "EDVR", "EDVU", "EDXJ", "EDXW", "EKCH", "EKRN", "EPCJ", "EPSC",
        "ESMS", "ESMT", "ESMV", "ETAB", "ETAD", "ETAR", "ETHB", "ETHC", "ETHF",
        "ETHM", "ETHM2", "ETHN", "ETHS", "ETMD", "ETMN", "ETNL", "ETNN", "ETNW",
        "ETOB", "ETOU", "ETSB", "ETSH", "ETSP", "ETSW", "ETUO", "ETUS",
    },
    "Iraq": {
        "ORAA", "ORAK", "ORAS", "ORAT", "ORBD", "ORBI", "ORBM", "ORBP", "ORER",
        "ORH2", "ORH3", "ORH3NW", "ORH3SW", "ORK1", "ORKK", "ORQW", "ORSU", "ORTI",
        "ORTL",
    },
    "Kola": {
        "EFET", "EFHS", "EFIV", "EFKE", "EFKS", "EFKT", "EFRO", "EFSO", "EFVU",
        "ENAN", "ENAT", "ENBO", "ENDU", "ENEV", "ENKR", "ENNA", "ESNJ", "ESNQ",
        "ESNX", "ESPA", "ESPB", "ESPE", "ESUK", "ESUT", "ULAF", "ULAM", "ULAS",
        "ULKK", "ULKL", "ULKY", "ULMA", "ULMK", "ULMK2", "ULMP", "ULPD", "ULWC",
    },
    "MarianaIslands": {
        "PGFT", "PGOR", "PGPG", "PGRO", "PGSN", "PGUA", "PGUM",
    },
    "MarianaIslandsWWII": {
        "WAF3", "WAGN", "WCKA", "WGRG", "WISL", "WKAG", "WMRP", "WORO", "WPAG",
        "WROT", "WUSH",
    },
    "Nevada": {
        "K0L7", "K0L9", "K1L1", "K3Q0", "K67L", "KBTY", "KBVU", "KHND", "KIFP",
        "KINS", "KLAS", "KLSV", "KPMS", "KTNX", "KTPH", "KVGT", "KXTA",
    },
    "Normandy": {
        "LFOE", "LFOH", "LFPB", "LFPG", "LFQA", "LFQB", "LFRC", "LFRK",
    },
    "PersianGulf": {
        "OIBA", "OIBK", "OIBL", "OIBP", "OIBS", "OIBT", "OIBTK", "OIKB", "OIKJ",
        "OIKK", "OIKP", "OIKQ", "OISL", "OISS", "OIZJ", "OMAA", "OMAB", "OMAD",
        "OMAL", "OMAW", "OMDB", "OMDM", "OMDW", "OMFJ", "OMQS", "OMRK", "OMSA",
        "OMSJ", "OMSN", "OOKB",
    },
    "SinaiMap": {
        "HEAR", "HEAS", "HEAU", "HEBA", "HEBH", "HEBL", "HEBN", "HEBR", "HEBZ",
        "HECA", "HECW", "HEDS", "HEFD", "HEGB", "HEGN", "HEGR", "HEIN", "HEIS",
        "HEJK", "HEKB", "HEKH", "HEKW", "HEMN", "HEMS", "HEMZ", "HEQS", "HERM",
        "HESC", "HESH", "HESL", "HETB", "HETB2", "HEWJ", "HEWR", "HEZQ", "LLBG",
        "LLER", "LLES", "LLHB", "LLHS", "LLKM", "LLMG", "LLNV", "LLOV", "LLPM",
        "LLRD", "LLRM", "LLSD", "LLTN", "OEKF", "OETB", "OLBA", "OSDI", "OSKH",
        "OSMZ",
    },
    "SouthAtlantic": {
        "EGYP", "SAVT", "SAWE", "SAWG",
    },
    "Syria": {
        "LCEN", "LCGK", "LCLK", "LCLT", "LCNC", "LCPH", "LCPN", "LCRA", "LCRA2",
        "LLBG", "LLES", "LLHA", "LLHS", "LLHZ", "LLIB", "LLKS", "LLMG", "LLPM",
        "LLRD", "LLTN", "LTAF", "LTAG", "LTAJ", "LTCH", "LTDA", "LTFG", "OJAM",
        "OJAM2", "OJH3", "OJH3NW", "OJH3SW", "OJH4", "OJMA", "OJMF", "OJPH",
        "OJRW", "OJTH", "OLBA", "OLKA", "OLRA", "OLWH", "OSABD", "OSAN", "OSAP",
        "OSDI", "OSDR", "OSDZ", "OSHM", "OSJI", "OSKH", "OSKW", "OSLK", "OSMN",
        "OSMR", "OSMS1", "OSMS2", "OSMZ", "OSPR", "OSQS", "OSQS2", "OSSH", "OSSQ",
        "OSTB", "OSTF", "OSTI", "OSTS",
    },
    "TheChannel": {
        "EGKB", "EGLF", "EGMC", "EGMH", "LFAK", "LFAY", "LFQQ",
    },
}


RUNWAYS: dict[str, dict[str, list[tuple[float, float, float, float, int]]]] = {
    "Afghanistan": {
        "OABM": [(34.8126, 67.8074, 34.8053, 67.8261, 28)],  # 7
        "OABN": [
            (31.8646, 64.2209, 31.8357, 64.2264, 38),  # 1
            (31.8572, 64.2129, 31.8537, 64.2135, 28),  # 1
        ],
        "OABT": [(31.5677, 64.3638, 31.5520, 64.3658, 28)],  # 1
        "OACC": [(34.5231, 65.2798, 34.5300, 65.2628, 18)],  # 25
        "OADR": [(31.0986, 64.0579, 31.0853, 64.0760, 35)],  # 5
        "OAFR": [(32.3717, 62.1733, 32.3549, 62.1622, 28)],  # 33
        "OAFS": [(33.3629, 69.9587, 33.3639, 69.9518, 28)],  # 26
        "OAGZ": [(33.6350, 69.2344, 33.6211, 69.2407, 28)],  # 3
        "OAHR": [(34.1958, 62.2300, 34.2200, 62.2259, 35)],  # 18
        "OAIX": [
            (34.9317, 69.2730, 34.9598, 69.2588, 35),  # 21
            (34.9321, 69.2721, 34.9602, 69.2578, 35),  # 3
        ],
        "OAJL": [(34.3956, 70.4895, 34.4049, 70.5067, 20)],  # 13
        "OAKB": [(34.5632, 69.1957, 34.5683, 69.2296, 38)],  # 11
        "OAKN": [
            (31.4975, 65.8601, 31.5140, 65.8353, 35),  # 23
            (31.5201, 65.8467, 31.5213, 65.8449, 28),  # 23
        ],
        "OAKT": [(33.3285, 69.9584, 33.3376, 69.9436, 28)],  # 23
        "OAMN": [(35.9366, 64.7667, 35.9247, 64.7551, 18)],  # 32
        "OAQN": [(34.9793, 63.1243, 34.9923, 63.1112, 18)],  # 22
        "OASA": [(33.1299, 68.8429, 33.1216, 68.8341, 28)],  # 32
        "OASD": [
            (33.4023, 62.2605, 33.3830, 62.2616, 30),  # 36
            (33.4088, 62.2683, 33.4069, 62.2684, 28),  # 36
        ],
        "OATN": [(32.6009, 65.8560, 32.6093, 65.8724, 35)],  # 12
        "OAZJ": [(30.9561, 62.0537, 30.9708, 62.0678, 28)],  # 14
    },
    "Caucasus": {
        "UGKG": [(43.1055, 40.5615, 43.1232, 40.5780, 35)],  # 15
        "UGKO": [(42.1735, 42.4947, 42.1817, 42.4679, 35)],  # 25
        "UGKS": [(41.9255, 41.8754, 41.9343, 41.8511, 35)],  # 25
        "UGSB": [(41.6142, 41.6109, 41.6050, 41.5895, 35)],  # 31
        "UGSN": [(42.2406, 42.0613, 42.2411, 42.0347, 35)],  # 27
        "UGSS": [(42.8666, 41.1444, 42.8556, 41.1056, 35)],  # 30
        "UGTB": [(41.6618, 44.9442, 41.6722, 44.9683, 35)],  # 13
        "UGTS": [(41.6556, 44.9501, 41.6435, 44.9266, 35)],  # 14
        "UGTV": [(41.6226, 45.0160, 41.6355, 45.0385, 35)],  # 13
        "URKA": [(44.9957, 37.3582, 45.0142, 37.3375, 35)],  # 22
        "URKG": [(44.9754, 37.9874, 44.9605, 38.0027, 35)],  # 4
        "URKH": [(44.6928, 40.0243, 44.6697, 40.0462, 35)],  # 4
        "URKK": [(45.0282, 39.2009, 45.0478, 39.1754, 35)],  # 23
        "URKN": [(43.5201, 43.6271, 43.5079, 43.6458, 35)],  # 6
        "URKN2": [(44.6621, 37.7850, 44.6741, 37.7715, 35)],  # 22
        "URMG": [(44.5789, 38.0054, 44.5669, 38.0178, 35)],  # 1
        "URMM": [(44.2331, 43.1033, 44.2226, 43.0590, 35)],  # 30
        "URMO": [(43.2067, 44.5886, 43.2047, 44.6231, 35)],  # 10
        "URMZ": [(43.7889, 44.6198, 43.7945, 44.5919, 35)],  # 26
        "URRR": [(45.0883, 38.9253, 45.0856, 38.9547, 35)],  # 9
        "URSS": [(43.4515, 39.9258, 43.4372, 39.9564, 35)],  # 6
    },
    "GermanyCW": {
        "EDAB": [(51.3280, 12.6704, 51.3286, 12.6423, 35)],  # 26
        "EDAC": [(51.7238, 11.9787, 51.7190, 11.9444, 28)],  # 28
        "EDAD": [(51.8292, 12.1775, 51.8343, 12.2087, 38)],  # 9
        "EDAM": [(51.3640, 11.9325, 51.3640, 11.9675, 30)],  # 8
        "EDAS": [(51.3922, 12.4182, 51.3954, 12.3979, 35)],  # 25
        "EDAV": [(52.8312, 13.7109, 52.8231, 13.6772, 28)],  # 28
        "EDAY": [(53.3541, 13.7774, 53.3569, 13.7928, 28)],  # 10
        "EDBA": [(51.3799, 11.4639, 51.3813, 11.4291, 28)],  # 25
        "EDBC": [(51.8554, 11.4002, 51.8564, 11.4357, 38)],  # 8
        "EDBH": [(54.3371, 12.7024, 54.3393, 12.7170, 18)],  # 27
        "EDBM": [(53.5643, 12.6593, 53.5675, 12.6484, 18)],  # 24
        "EDBN": [(53.6005, 13.2909, 53.6039, 13.3213, 38)],  # 9
        "EDCG": [(53.8824, 14.1669, 53.8746, 14.1402, 28)],  # 28
        "EDCN": [(53.6122, 11.5667, 53.6209, 11.5595, 28)],  # 20
        "EDCP": [(54.1498, 13.7641, 54.1676, 13.7832, 38)],  # 13
        "EDCT": [(53.9121, 13.2197, 53.9315, 13.2184, 35)],  # 17
        "EDCW": [(53.9142, 11.4980, 53.9147, 11.5069, 18)],  # 9
        "EDDB": [
            (52.3822, 13.5547, 52.3863, 13.5140, 38),  # 25
            (52.3706, 13.5263, 52.3747, 13.4856, 38),  # 7
        ],
        "EDDE": [(50.9829, 10.9751, 50.9761, 10.9496, 28)],  # 28
        "EDDF": [
            (50.0400, 8.5959, 50.0408, 8.5388, 38),  # 25
            (50.0335, 8.5896, 50.0343, 8.5326, 38),  # 7
        ],
        "EDDH": [
            (53.6219, 10.0018, 53.6318, 9.9608, 38),  # 23
            (53.6542, 9.9903, 53.6282, 9.9830, 38),  # 5
        ],
        "EDDI": [
            (52.4695, 13.3899, 52.4726, 13.4187, 38),  # 9
            (52.4738, 13.3892, 52.4762, 13.4181, 38),  # 27
        ],
        "EDDK": [
            (50.8556, 7.1402, 50.8802, 7.1549, 38),  # 14
            (50.8659, 7.1191, 50.8641, 7.1605, 38),  # 32
            (50.8555, 7.1242, 50.8742, 7.1354, 38),  # 7
        ],
        "EDDL": [(51.2893, 6.7536, 51.2846, 6.7818, 38)],  # 5
        "EDDP": [(51.4204, 12.2425, 51.4096, 12.2118, 38)],  # 29
        "EDDT": [
            (52.5590, 13.3101, 52.5579, 13.2757, 35),  # 26
            (52.5604, 13.3052, 52.5593, 13.2708, 35),  # 8
        ],
        "EDDV": [
            (52.4581, 9.7094, 52.4509, 9.6781, 38),  # 27
            (52.4710, 9.6953, 52.4639, 9.6640, 38),  # 9
        ],
        "EDDW": [(53.0445, 8.7754, 53.0494, 8.8012, 35)],  # 9
        "EDFB": [(50.5404, 9.6470, 50.5394, 9.6391, 28)],  # 27
        "EDFG": [(50.1956, 9.1596, 50.1971, 9.1744, 28)],  # 9
        "EDFH": [(49.9427, 7.2760, 49.9542, 7.2518, 38)],  # 21
        "EDFS": [(50.0493, 10.1739, 50.0484, 10.1654, 28)],  # 27
        "EDFV": [(49.8774, 7.9619, 49.8645, 7.9580, 28)],  # 33
        "EDFZ": [
            (49.9688, 8.1413, 49.9695, 8.1544, 28),  # 8
            (50.0086, 8.0928, 50.0078, 8.1046, 18),  # 7
        ],
        "EDGA": [(49.3723, 9.4258, 49.3661, 9.4545, 28)],  # 5
        "EDGH": [(51.7063, 10.8858, 51.7045, 10.8716, 28)],  # 27
        "EDGM": [(54.3755, 12.9005, 54.3909, 12.9241, 35)],  # 13
        "EDGW": [(52.1369, 10.5764, 52.1369, 10.5652, 18)],  # 26
        "EDHA": [(50.9966, 10.4927, 50.9867, 10.4665, 28)],  # 28
        "EDHE": [(53.6483, 9.7116, 53.6447, 9.6965, 28)],  # 27
        "EDHG": [(53.2486, 10.4640, 53.2485, 10.4551, 18)],  # 26
        "EDHI": [(53.5369, 9.8204, 53.5314, 9.8454, 28)],  # 5
        "EDHK": [(54.3786, 10.1361, 54.3804, 10.1533, 28)],  # 8
        "EDHL": [(53.8051, 10.7012, 53.8047, 10.7326, 30)],  # 7
        "EDIE": [(49.3942, 8.6589, 49.3928, 8.6454, 28)],  # 26
        "EDLD": [(49.4031, 7.5364, 49.4031, 7.5363, 28)],  # 31
        "EDLG": [(52.3220, 10.1732, 52.3257, 10.1878, 28)],  # 10
        "EDOA": [(53.3067, 12.7351, 53.3060, 12.7700, 28)],  # 8
        "EDOG": [(52.5322, 11.3567, 52.5268, 11.3436, 28)],  # 29
        "EDOI": [(52.6614, 12.7519, 52.6558, 12.7424, 18)],  # 30
        "EDOJ": [(52.1338, 13.2887, 52.1400, 13.3232, 35)],  # 9
        "EDOL": [(51.9920, 12.9674, 51.9989, 13.0002, 35)],  # 10
        "EDOP": [(53.4299, 11.7680, 53.4258, 11.8052, 35)],  # 7
        "EDOS": [(51.2714, 10.6428, 51.2641, 10.6268, 28)],  # 29
        "EDOV": [(52.6282, 11.8059, 52.6300, 11.8338, 38)],  # 8
        "EDOW": [(52.6856, 13.0015, 52.6656, 13.0124, 28)],  # 1
        "EDOX": [(52.9636, 9.2781, 52.9679, 9.2832, 18)],  # 13
        "EDQG": [(49.6472, 9.9525, 49.6486, 9.9769, 38)],  # 8
        "EDRZ": [(49.2163, 7.3883, 49.2028, 7.4134, 38)],  # 3
        "EDTH": [(51.7057, 12.2046, 51.6871, 12.2159, 28)],  # 36
        "EDUB": [(52.0397, 13.7624, 52.0340, 13.7305, 28)],  # 27
        "EDUE": [(51.5469, 13.2367, 51.5460, 13.1955, 38)],  # 26
        "EDUG": [(52.4756, 13.1511, 52.4751, 13.1251, 38)],  # 26
        "EDUH": [(52.6139, 14.2590, 52.6120, 14.2265, 28)],  # 26
        "EDUK": [(53.1957, 12.1570, 53.1962, 12.1731, 28)],  # 8
        "EDUM": [(52.6226, 10.4137, 52.6184, 10.4083, 18)],  # 31
        "EDUO": [(52.7349, 13.2196, 52.7149, 13.2141, 28)],  # 34
        "EDUT": [
            (53.0349, 13.5677, 53.0291, 13.5175, 38),  # 27
            (53.0290, 13.5000, 53.0014, 13.5227, 38),  # 9
        ],
        "EDUW": [(52.6307, 13.7512, 52.6329, 13.7864, 35)],  # 8
        "EDUZ": [(52.0018, 12.1269, 51.9975, 12.1616, 28)],  # 7
        "EDVE": [(52.3203, 10.5636, 52.3179, 10.5443, 35)],  # 26
        "EDVM": [(52.1800, 9.9544, 52.1796, 9.9372, 28)],  # 25
        "EDVN": [(52.9849, 11.2437, 52.9838, 11.2305, 18)],  # 27
        "EDVR": [(52.1729, 9.0496, 52.1764, 9.0562, 18)],  # 12
        "EDVU": [(52.9847, 10.4721, 52.9825, 10.4569, 18)],  # 27
        "EDXJ": [(53.3224, 9.5750, 53.3195, 9.5909, 28)],  # 6
        "EDXW": [(53.0514, 9.2105, 53.0608, 9.2061, 28)],  # 19
        "EKCH": [
            (55.6254, 12.6626, 55.6131, 12.6422, 38),  # 30
            (55.6192, 12.6382, 55.6095, 12.6627, 38),  # 12
            (55.6106, 12.5993, 55.5946, 12.6399, 38),  # 4
        ],
        "EKRN": [(55.0585, 14.7463, 55.0683, 14.7718, 38)],  # 11
        "EPCJ": [(52.9417, 14.4379, 52.9374, 14.4061, 28)],  # 27
        "EPSC": [(53.5915, 14.9115, 53.5780, 14.8930, 38)],  # 31
        "ESMS": [(55.5234, 13.3787, 55.5479, 13.3741, 38)],  # 17
        "ESMT": [(55.6075, 13.7200, 55.5942, 13.7083, 28)],  # 33
        "ESMV": [(55.7331, 13.4413, 55.7245, 13.4133, 18)],  # 29
        "ETAB": [(49.9424, 6.5797, 49.9469, 6.5487, 38)],  # 24
        "ETAD": [(49.9713, 6.7178, 49.9819, 6.6798, 28)],  # 23
        "ETAR": [(49.4398, 7.6150, 49.4340, 7.5852, 38)],  # 27
        "ETHB": [(52.2777, 9.0712, 52.2794, 9.0953, 28)],  # 8
        "ETHC": [(52.5927, 10.0394, 52.5901, 10.0093, 28)],  # 26
        "ETHF": [(51.1175, 9.2901, 51.1117, 9.2816, 28)],  # 30
        "ETHM": [(52.3911, 11.8438, 52.3854, 11.8090, 35)],  # 27
        "ETHM2": [(50.3668, 7.3267, 50.3652, 7.3045, 28)],  # 26
        "ETHN": [(52.9372, 12.7706, 52.9449, 12.8033, 38)],  # 10
        "ETHS": [(52.9166, 10.1671, 52.9223, 10.2025, 38)],  # 9
        "ETMD": [(54.2648, 12.4262, 54.2632, 12.4622, 28)],  # 7
        "ETMN": [(53.7691, 8.6758, 53.7660, 8.6412, 38)],  # 26
        "ETNL": [(53.9139, 12.2620, 53.9222, 12.2968, 38)],  # 10
        "ETNN": [(50.8314, 6.6419, 50.8311, 6.6754, 28)],  # 7
        "ETNW": [
            (52.4587, 9.4402, 52.4559, 9.4140, 28),  # 26
            (52.4458, 9.4419, 52.4573, 9.4231, 28),  # 8
        ],
        "ETOB": [(52.4370, 12.4716, 52.4383, 12.4363, 35)],  # 25
        "ETOU": [(50.0493, 8.3108, 50.0503, 8.3403, 28)],  # 8
        "ETSB": [(50.1809, 7.0508, 50.1673, 7.0769, 28)],  # 3
        "ETSH": [(51.7710, 13.1882, 51.7646, 13.1512, 28)],  # 27
        "ETSP": [(49.8522, 7.5894, 49.8580, 7.6200, 35)],  # 9
        "ETSW": [(53.2021, 12.5408, 53.2027, 12.5052, 35)],  # 26
        "ETUO": [(51.9199, 8.2917, 51.9257, 8.3165, 35)],  # 9
        "ETUS": [(49.5050, 7.8796, 49.5073, 7.8472, 35)],  # 25
    },
    "Iraq": {
        "ORAA": [
            (33.7808, 42.4073, 33.7816, 42.4480, 35),  # 9
            (33.7895, 42.4345, 33.7904, 42.4751, 35),  # 27
        ],
        "ORAK": [
            (32.4804, 45.7429, 32.4873, 45.7683, 28),  # 11
            (32.4775, 45.7435, 32.4844, 45.7689, 28),  # 29
        ],
        "ORAS": [(33.2706, 44.4879, 33.2872, 44.5008, 35)],  # 15
        "ORAT": [
            (33.3324, 43.5849, 33.3461, 43.6122, 35),  # 12
            (33.3301, 43.5819, 33.3438, 43.6092, 35),  # 30
        ],
        "ORBD": [
            (33.9331, 44.3594, 33.9525, 44.3749, 38),  # 14
            (33.9286, 44.3472, 33.9424, 44.3697, 38),  # 32
        ],
        "ORBI": [
            (33.2440, 44.2178, 33.2676, 44.2334, 35),  # 15
            (33.2565, 44.2341, 33.2800, 44.2497, 35),  # 33
        ],
        "ORBM": [(36.2978, 43.1431, 36.3150, 43.1510, 28)],  # 15
        "ORBP": [(36.5290, 44.3334, 36.5400, 44.3451, 28)],  # 13
        "ORER": [
            (36.2183, 43.9474, 36.2583, 43.9460, 35),  # 18
            (36.2198, 43.9518, 36.2555, 43.9742, 35),  # 36
        ],
        "ORH2": [
            (33.3488, 40.5865, 33.3639, 40.5905, 28),  # 16
            (33.3566, 40.5968, 33.3637, 40.6131, 28),  # 34
        ],
        "ORH3": [
            (32.9312, 39.7342, 32.9413, 39.7571, 28),  # 11
            (32.9254, 39.7333, 32.9182, 39.7577, 28),  # 29
        ],
        "ORH3NW": [(33.0707, 39.5871, 33.0821, 39.6044, 28)],  # 12
        "ORH3SW": [(32.7391, 39.5939, 32.7486, 39.6089, 28)],  # 10
        "ORK1": [(35.5181, 44.2895, 35.5073, 44.2791, 28)],  # 32
        "ORKK": [
            (35.4658, 44.3378, 35.4765, 44.3513, 28),  # 13
            (35.4623, 44.3470, 35.4751, 44.3575, 28),  # 31
        ],
        "ORQW": [(35.7534, 43.1151, 35.7782, 43.1295, 35)],  # 15
        "ORSU": [(35.5514, 45.3022, 35.5702, 45.3273, 35)],  # 13
        "ORTI": [(33.5305, 44.2594, 33.5171, 44.2541, 28)],  # 34
        "ORTL": [
            (34.6595, 43.5290, 34.6763, 43.5438, 28),  # 14
            (34.6718, 43.5451, 34.6887, 43.5599, 28),  # 32
        ],
    },
    "Kola": {
        "EFET": [(68.3695, 23.4130, 68.3555, 23.4352, 28)],  # 3
        "EFHS": [(65.8923, 25.7203, 65.8999, 25.6874, 28)],  # 24
        "EFIV": [(68.5995, 27.4195, 68.6147, 27.3902, 35)],  # 22
        "EFKE": [(65.7707, 24.5827, 65.7922, 24.5818, 38)],  # 18
        "EFKS": [(65.9829, 29.2170, 65.9923, 29.2618, 28)],  # 12
        "EFKT": [(67.6918, 24.8376, 67.7102, 24.8562, 35)],  # 16
        "EFRO": [(66.5539, 25.8454, 66.5758, 25.8156, 35)],  # 21
        "EFSO": [(67.3895, 26.6124, 67.4006, 26.6259, 28)],  # 16
        "EFVU": [(67.0608, 26.5565, 67.0774, 26.5231, 28)],  # 22
        "ENAN": [(69.2878, 16.1248, 69.3073, 16.1461, 35)],  # 14
        "ENAT": [(69.9803, 23.3833, 69.9743, 23.3485, 30)],  # 29
        "ENBO": [(67.2692, 14.3349, 67.2692, 14.3958, 38)],  # 7
        "ENDU": [(69.0589, 18.5660, 69.0518, 18.5210, 35)],  # 28
        "ENEV": [(68.4799, 16.6812, 68.5025, 16.6751, 35)],  # 17
        "ENKR": [(69.7205, 29.9084, 69.7303, 29.8717, 35)],  # 23
        "ENNA": [(70.0796, 24.9803, 70.0580, 24.9668, 28)],  # 34
        "ESNJ": [(66.4892, 20.1349, 66.5035, 20.1592, 28)],  # 14
        "ESNQ": [(67.8137, 20.3522, 67.8303, 20.3214, 38)],  # 21
        "ESNX": [(65.5846, 19.2587, 65.5984, 19.2969, 35)],  # 12
        "ESPA": [(65.5335, 22.0972, 65.5541, 22.1465, 35)],  # 14
        "ESPB": [(65.8084, 21.6921, 65.8102, 21.6969, 20)],  # 13
        "ESPE": [(65.8708, 20.1295, 65.8797, 20.1703, 35)],  # 11
        "ESUK": [(67.7601, 20.2492, 67.7698, 20.2528, 28)],  # 17
        "ESUT": [(65.8115, 15.0880, 65.7994, 15.0792, 28)],  # 33
        "ULAF": [(67.4562, 32.8109, 67.4584, 32.7571, 30)],  # 28
        "ULAM": [(68.8767, 33.7283, 68.8574, 33.7079, 38)],  # 35
        "ULAS": [(69.0236, 33.3943, 69.0374, 33.4517, 38)],  # 14
        "ULKK": [(68.7756, 32.7267, 68.7877, 32.7760, 38)],  # 13
        "ULKL": [(65.2070, 31.1359, 65.2124, 31.1319, 18)],  # 20
        "ULKY": [(69.2387, 31.1966, 69.2637, 31.1962, 28)],  # 19
        "ULMA": [(66.9765, 30.3702, 66.9690, 30.3269, 28)],  # 30
        "ULMK": [(67.9992, 33.0163, 67.9788, 33.0210, 38)],  # 1
        "ULMK2": [(69.0858, 32.4112, 69.1040, 32.3899, 28)],  # 21
        "ULMP": [(69.3970, 30.9939, 69.4077, 30.9879, 28)],  # 20
        "ULPD": [(64.9161, 34.2858, 64.9212, 34.2402, 30)],  # 27
        "ULWC": [(68.1370, 33.4617, 68.1665, 33.4669, 38)],  # 19
    },
    "MarianaIslands": {
        "PGFT": [(15.0011, 145.6083, 14.9973, 145.6300, 35)],  # 8
        "PGOR": [(13.4364, 144.6467, 13.4400, 144.6377, 28)],  # 25
        "PGPG": [(18.1223, 145.7610, 18.1240, 145.7653, 30)],  # 11
        "PGRO": [(14.1740, 145.2325, 14.1748, 145.2497, 35)],  # 9
        "PGSN": [(15.1229, 145.7189, 15.1150, 145.7394, 35)],  # 7
        "PGUA": [
            (13.5874, 144.9175, 13.5760, 144.9446, 35),  # 6
            (13.5921, 144.9159, 13.5807, 144.9430, 35),  # 24
        ],
        "PGUM": [
            (13.4900, 144.7848, 13.4795, 144.8089, 35),  # 6
            (13.4876, 144.7841, 13.4771, 144.8082, 35),  # 24
        ],
    },
    "MarianaIslandsWWII": {
        "WAF3": [(15.0676, 145.6312, 15.0685, 145.6382, 28)],  # 10
        "WAGN": [(13.4847, 144.7838, 13.4804, 144.7955, 28)],  # 7
        "WCKA": [(15.1646, 145.7030, 15.1563, 145.7089, 28)],  # 3
        "WGRG": [(15.0018, 145.5943, 15.0020, 145.6033, 28)],  # 9
        "WISL": [(15.1195, 145.7224, 15.1197, 145.7299, 35)],  # 9
        "WKAG": [(15.1675, 145.7688, 15.1677, 145.7782, 28)],  # 9
        "WMRP": [(15.2804, 145.8091, 15.2831, 145.8159, 28)],  # 11
        "WORO": [(13.4350, 144.6335, 13.4397, 144.6450, 28)],  # 11
        "WPAG": [(18.1230, 145.7619, 18.1242, 145.7679, 18)],  # 11
        "WROT": [(14.1742, 145.2373, 14.1746, 145.2468, 28)],  # 9
        "WUSH": [(15.0778, 145.6321, 15.0786, 145.6413, 28)],  # 9
    },
    "Nevada": {
        "K0L7": [
            (35.7644, -115.3262, 35.7740, -115.3329, 18),  # 20
            (35.7632, -115.3259, 35.7728, -115.3327, 18),  # 2
        ],
        "K0L9": [(36.3121, -114.4692, 36.3100, -114.4586, 18)],  # 6
        "K1L1": [(37.7813, -114.4200, 37.7934, -114.4198, 18)],  # 17
        "K3Q0": [(38.3850, -118.0934, 38.3746, -118.1000, 35)],  # 13
        "K67L": [(36.8392, -114.0596, 36.8270, -114.0522, 18)],  # 1
        "KBTY": [(36.8536, -116.7865, 36.8684, -116.7864, 18)],  # 16
        "KBVU": [
            (35.9535, -114.8600, 35.9438, -114.8637, 18),  # 33
            (35.9470, -114.8549, 35.9457, -114.8673, 18),  # 15
        ],
        "KHND": [
            (35.9805, -115.1328, 35.9675, -115.1333, 35),  # 35
            (35.9783, -115.1352, 35.9652, -115.1357, 35),  # 17
        ],
        "KIFP": [(35.1464, -114.5608, 35.1658, -114.5581, 35)],  # 16
        "KINS": [
            (36.5837, -115.6868, 36.5839, -115.6660, 35),  # 8
            (36.5839, -115.6790, 36.5975, -115.6669, 35),  # 26
        ],
        "KLAS": [
            (36.0770, -115.1622, 36.0759, -115.1271, 35),  # 7
            (36.0742, -115.1612, 36.0731, -115.1261, 35),  # 25
        ],
        "KLSV": [
            (36.2453, -115.0431, 36.2251, -115.0229, 35),  # 3
            (36.2471, -115.0456, 36.2269, -115.0255, 35),  # 21
        ],
        "KPMS": [(37.1093, -116.3149, 37.0947, -116.3107, 35)],  # 36
        "KTNX": [(37.8136, -116.7729, 37.7842, -116.7887, 35)],  # 32
        "KTPH": [
            (38.0666, -117.0757, 38.0582, -117.0908, 18),  # 29
            (38.0650, -117.0872, 38.0509, -117.0919, 18),  # 11
        ],
        "KVGT": [
            (36.2131, -115.1868, 36.2139, -115.2028, 18),  # 25
            (36.2144, -115.1909, 36.2057, -115.2028, 18),  # 7
            (36.2043, -115.1970, 36.2126, -115.1858, 18),  # 30
        ],
        "KXTA": [(37.2470, -115.7845, 37.2194, -115.8001, 35)],  # 32
    },
    "Normandy": {
        # no runway data — map not owned
    },
    "PersianGulf": {
        "OIBA": [(25.8769, 55.0214, 25.8751, 55.0445, 35)],  # 8
        "OIBK": [
            (26.5262, 53.9650, 26.5301, 53.9971, 35),  # 10
            (26.5235, 53.9647, 26.5274, 53.9969, 35),  # 28
        ],
        "OIBL": [(26.5336, 54.8131, 26.5309, 54.8362, 35)],  # 8
        "OIBP": [(26.8065, 53.3418, 26.8157, 53.3648, 35)],  # 11
        "OIBS": [(25.9159, 54.5481, 25.9033, 54.5304, 35)],  # 30
        "OIBT": [(26.2663, 55.3113, 26.2515, 55.3202, 18)],  # 3
        "OIBTK": [(26.2429, 55.1493, 26.2438, 55.1418, 18)],  # 26
        "OIKB": [(27.2318, 56.3705, 27.2036, 56.3875, 35)],  # 3
        "OIKJ": [(28.7158, 57.6638, 28.7313, 57.6864, 20)],  # 13
        "OIKK": [(30.2884, 56.9585, 30.2578, 56.9446, 35)],  # 34
        "OIKP": [(27.1564, 56.1831, 27.1601, 56.1610, 35)],  # 26
        "OIKQ": [(26.7430, 55.9181, 26.7663, 55.8867, 35)],  # 23
        "OISL": [(27.6744, 54.3683, 27.6751, 54.3980, 35)],  # 9
        "OISS": [
            (29.5497, 52.6093, 29.5321, 52.5728, 35),  # 29
            (29.5459, 52.6074, 29.5284, 52.5709, 35),  # 11
        ],
        "OIZJ": [(25.6592, 57.7923, 25.6501, 57.8105, 20)],  # 6
        "OMAA": [
            (24.4424, 54.6395, 24.4650, 54.6691, 35),  # 13
            (24.4424, 54.6688, 24.4198, 54.6391, 35),  # 31
            (24.4328, 54.6278, 24.4503, 54.6507, 35),  # 31
        ],
        "OMAB": [(24.4220, 54.4508, 24.4341, 54.4664, 35)],  # 13
        "OMAD": [
            (24.2384, 54.5344, 24.2581, 54.5610, 35),  # 13
            (24.2212, 54.5377, 24.2409, 54.5643, 35),  # 31
        ],
        "OMAL": [(24.2461, 55.6118, 24.2768, 55.6067, 35)],  # 19
        "OMAW": [(23.6406, 53.8128, 23.6610, 53.8361, 20)],  # 13
        "OMDB": [
            (25.2646, 55.3792, 25.2482, 55.3513, 35),  # 30
            (25.2524, 55.3939, 25.2360, 55.3660, 35),  # 12
        ],
        "OMDM": [(25.0271, 55.3837, 25.0267, 55.3478, 35)],  # 27
        "OMDW": [(24.9056, 55.1748, 24.8885, 55.1457, 35)],  # 30
        "OMFJ": [(25.1160, 56.3405, 25.1059, 56.3142, 35)],  # 29
        "OMQS": [(22.7763, 55.0771, 22.7759, 55.0495, 20)],  # 27
        "OMRK": [(25.6247, 55.9420, 25.6023, 55.9356, 35)],  # 35
        "OMSA": [(25.2174, 54.2370, 25.2163, 54.2303, 18)],  # 28
        "OMSJ": [
            (25.3386, 55.5314, 25.3228, 55.5052, 35),  # 30
            (25.3364, 55.5305, 25.3205, 55.5043, 35),  # 12
        ],
        "OMSN": [(24.4340, 54.5147, 24.4482, 54.5194, 20)],  # 16
        "OOKB": [(26.1598, 56.2430, 26.1798, 56.2373, 18)],  # 19
    },
    "SinaiMap": {
        "HEAR": [
            (31.0496, 33.8251, 31.0261, 33.8131, 35),  # 34
            (31.0850, 33.8419, 31.0614, 33.8298, 35),  # 16
        ],
        "HEAS": [
            (30.5803, 32.1099, 30.5705, 32.0827, 35),  # 29
            (30.5703, 32.1104, 30.5698, 32.0809, 35),  # 11
        ],
        "HEAU": [(28.8940, 33.1952, 28.9051, 33.2095, 30)],  # 13
        "HEBA": [
            (30.9047, 29.6845, 30.9291, 29.7033, 18),  # 14
            (30.9059, 29.6865, 30.9302, 29.7053, 18),  # 32
            (30.8911, 29.6835, 30.9155, 29.7023, 35),  # 14
            (30.9048, 29.6711, 30.9291, 29.6900, 35),  # 32
        ],
        "HEBH": [
            (26.5670, 33.1289, 26.5457, 33.1132, 35),  # 32
            (26.5681, 33.1306, 26.5467, 33.1149, 35),  # 14
        ],
        "HEBL": [
            (30.4111, 31.6097, 30.3863, 31.6049, 35),  # 35
            (30.3890, 31.6107, 30.3871, 31.5818, 35),  # 17
            (30.4070, 31.5862, 30.3920, 31.6041, 35),  # 27
        ],
        "HEBN": [
            (29.2128, 31.0159, 29.1830, 31.0221, 35),  # 36
            (29.2270, 30.9995, 29.2107, 31.0287, 35),  # 18
            (29.2105, 31.0138, 29.1860, 31.0190, 35),  # 5
        ],
        "HEBR": [
            (30.8474, 30.9441, 30.8267, 30.9279, 30),  # 32
            (30.8468, 30.9433, 30.8261, 30.9271, 30),  # 14
        ],
        "HEBZ": [(30.9978, 32.5612, 31.0017, 32.5432, 18)],  # 25
        "HECA": [
            (30.1197, 31.4197, 30.0983, 31.4499, 35),  # 5
            (30.1221, 31.3988, 30.1007, 31.4290, 35),  # 23
            (30.1400, 31.3780, 30.1186, 31.4082, 35),  # 5
        ],
        "HECW": [
            (30.1236, 30.8994, 30.0932, 30.8919, 35),  # 34
            (30.1199, 30.9380, 30.1101, 30.9040, 35),  # 16
            (30.1320, 30.9178, 30.1064, 30.9115, 35),  # 28
        ],
        "HEDS": [
            (30.4277, 32.3353, 30.4238, 32.3354, 28),  # 36
            (30.4230, 32.3403, 30.4229, 32.3358, 28),  # 18
        ],
        "HEFD": [(30.3293, 32.2821, 30.3288, 32.2528, 35)],  # 27
        "HEGB": [
            (30.5264, 30.5463, 30.5501, 30.5591, 35),  # 15
            (30.5301, 30.5695, 30.5560, 30.5651, 35),  # 33
        ],
        "HEGN": [
            (27.1597, 33.7865, 27.1932, 33.7969, 38),  # 16
            (27.1606, 33.7961, 27.1941, 33.8066, 38),  # 34
        ],
        "HEGR": [(31.0756, 34.1378, 31.0704, 34.1589, 18)],  # 8
        "HEIN": [
            (30.3415, 31.4372, 30.3270, 31.4560, 35),  # 4
            (30.3294, 31.4352, 30.3303, 31.4604, 35),  # 22
        ],
        "HEIS": [(30.6075, 32.2467, 30.5901, 32.2224, 35)],  # 31
        "HEJK": [
            (30.8148, 30.1808, 30.8298, 30.2040, 35),  # 12
            (30.8119, 30.1765, 30.8227, 30.2027, 35),  # 30
        ],
        "HEKB": [
            (30.2517, 32.5002, 30.2353, 32.4822, 28),  # 32
            (30.2530, 32.5017, 30.2366, 32.4837, 28),  # 14
        ],
        "HEKH": [
            (30.3116, 30.8730, 30.3131, 30.8759, 18),  # 11
            (30.3110, 30.8729, 30.3135, 30.8711, 18),  # 29
            (30.3103, 30.8750, 30.3118, 30.8740, 18),  # 20
        ],
        "HEKW": [
            (29.5628, 30.8985, 29.5445, 30.8885, 30),  # 33
            (29.5646, 30.8998, 29.5451, 30.8937, 30),  # 15
        ],
        "HEMN": [
            (28.1128, 30.7348, 28.0893, 30.7245, 35),  # 34
            (28.1133, 30.7361, 28.0897, 30.7258, 35),  # 16
        ],
        "HEMS": [
            (30.9748, 31.4408, 30.9556, 31.4222, 35),  # 32
            (30.9813, 31.4399, 30.9570, 31.4331, 35),  # 14
        ],
        "HEMZ": [
            (30.4187, 33.1565, 30.4012, 33.1430, 35),  # 33
            (30.4175, 33.1591, 30.3999, 33.1456, 35),  # 15
        ],
        "HEQS": [(30.5673, 31.1262, 30.5907, 31.1318, 35)],  # 16
        "HERM": [(31.0543, 30.6686, 31.0325, 30.6602, 35)],  # 34
        "HESC": [(28.6937, 34.0643, 28.6766, 34.0610, 28)],  # 35
        "HESH": [
            (27.9887, 34.3834, 27.9688, 34.4031, 35),  # 4
            (27.9861, 34.3869, 27.9662, 34.4067, 35),  # 22
        ],
        "HESL": [
            (30.8072, 32.0379, 30.7830, 32.0472, 35),  # 2
            (30.8064, 32.0448, 30.7822, 32.0541, 35),  # 20
        ],
        "HETB": [(30.2010, 33.4258, 30.1883, 33.3999, 30)],  # 30
        "HETB2": [(29.5748, 34.7910, 29.6013, 34.7655, 38)],  # 22
        "HEWJ": [
            (30.0875, 31.8283, 30.0576, 31.8383, 35),  # 1
            (30.0647, 31.8330, 30.0348, 31.8431, 35),  # 19
        ],
        "HEWR": [
            (28.9543, 31.7038, 28.9877, 31.6935, 35),  # 19
            (28.9548, 31.7017, 28.9882, 31.6914, 35),  # 1
        ],
        "HEZQ": [
            (30.6074, 31.6637, 30.5823, 31.6655, 35),  # 36
            (30.6073, 31.6647, 30.5822, 31.6665, 35),  # 18
        ],
        "LLBG": [
            (32.0174, 34.8870, 31.9967, 34.8992, 35),  # 3
            (32.0177, 34.8636, 32.0129, 34.8902, 35),  # 21
            (32.0134, 34.8940, 32.0006, 34.8673, 35),  # 8
        ],
        "LLER": [(29.7118, 35.0176, 29.7423, 35.0104, 35)],  # 19
        "LLES": [(32.4414, 35.0136, 32.4403, 35.0014, 28)],  # 10
        "LLHB": [
            (31.2409, 34.6699, 31.2363, 34.6472, 35),  # 28
            (31.2311, 34.6755, 31.2265, 34.6528, 35),  # 10
        ],
        "LLHS": [
            (31.7665, 34.7161, 31.7544, 34.7346, 30),  # 5
            (31.7647, 34.7448, 31.7579, 34.7230, 30),  # 23
            (31.7631, 34.7439, 31.7564, 34.7221, 30),  # 29
        ],
        "LLKM": [(31.2622, 34.6486, 31.2590, 34.6313, 28)],  # 28
        "LLMG": [(32.5973, 35.2200, 32.5970, 35.2405, 30)],  # 9
        "LLNV": [
            (31.2121, 34.9961, 31.2046, 35.0281, 35),  # 8
            (31.2144, 34.9914, 31.2069, 35.0234, 35),  # 26
            (31.1935, 35.0098, 31.1877, 35.0344, 35),  # 8
        ],
        "LLOV": [
            (29.9512, 34.9298, 29.9304, 34.9385, 35),  # 3
            (29.9501, 34.9332, 29.9293, 34.9419, 35),  # 21
        ],
        "LLPM": [(31.9107, 34.6884, 31.8928, 34.6974, 28)],  # 3
        "LLRD": [
            (32.6585, 35.1767, 32.6745, 35.1915, 35),  # 15
            (32.6674, 35.1647, 32.6653, 35.1885, 35),  # 33
            (32.6567, 35.1641, 32.6619, 35.1856, 35),  # 9
        ],
        "LLRM": [
            (30.7824, 34.6541, 30.7728, 34.6782, 28),  # 7
            (30.7797, 34.6563, 30.7701, 34.6803, 28),  # 25
        ],
        "LLSD": [(32.1094, 34.7853, 32.1200, 34.7793, 28)],  # 21
        "LLTN": [
            (31.8460, 34.8177, 31.8261, 34.8180, 30),  # 36
            (31.8463, 34.8328, 31.8293, 34.8208, 30),  # 18
            (31.8468, 34.8388, 31.8297, 34.8266, 35),  # 33
        ],
        "OEKF": [(30.3493, 36.1637, 30.3381, 36.1311, 35)],  # 29
        "OETB": [
            (28.3630, 36.5949, 28.3790, 36.6174, 38),  # 13
            (28.3692, 36.6486, 28.3813, 36.6232, 38),  # 31
        ],
        "OLBA": [
            (33.8108, 35.4786, 33.8381, 35.4879, 38),  # 16
            (33.8231, 35.4821, 33.7985, 35.4992, 38),  # 34
        ],
        "OSDI": [
            (33.4063, 36.4975, 33.3846, 36.5230, 38),  # 5
            (33.4364, 36.5056, 33.4147, 36.5311, 38),  # 23
        ],
        "OSKH": [
            (33.0690, 36.5328, 33.0889, 36.5486, 30),  # 15
            (33.0702, 36.5595, 33.0625, 36.5864, 30),  # 33
        ],
        "OSMZ": [(33.4841, 36.2121, 33.4712, 36.2351, 28)],  # 6
    },
    "SouthAtlantic": {
        # no runway data — map not owned
    },
    "Syria": {
        "LCEN": [(35.1503, 33.4906, 35.1600, 33.5128, 35)],  # 11
        "LCGK": [(35.2347, 33.7074, 35.2373, 33.7344, 35)],  # 9
        "LCLK": [(34.8800, 33.6129, 34.8663, 33.6336, 35)],  # 4
        "LCLT": [(35.1029, 33.3216, 35.1063, 33.3217, 28)],  # 17
        "LCNC": [
            (35.1620, 33.2811, 35.1433, 33.2690, 38),  # 32
            (35.1542, 33.2622, 35.1561, 33.2878, 38),  # 14
        ],
        "LCPH": [(34.7128, 32.4724, 34.7235, 32.4972, 35)],  # 11
        "LCPN": [(35.2693, 33.2673, 35.2784, 33.2691, 18)],  # 16
        "LCRA": [(34.5857, 32.9753, 34.5951, 33.0002, 38)],  # 10
        "LCRA2": [(35.0132, 33.7217, 35.0165, 33.7123, 28)],  # 24
        "LLBG": [
            (31.9992, 34.8714, 32.0129, 34.8935, 35),  # 12
            (31.9974, 34.9006, 32.0169, 34.8857, 35),  # 30
            (32.0141, 34.8910, 32.0165, 34.8627, 35),  # 21
        ],
        "LLES": [(32.4423, 35.0146, 32.4395, 34.9994, 35)],  # 27
        "LLHA": [(32.8151, 35.0449, 32.8064, 35.0421, 28)],  # 34
        "LLHS": [
            (31.7551, 34.7356, 31.7657, 34.7149, 35),  # 23
            (31.7551, 34.7224, 31.7642, 34.7441, 35),  # 5
            (31.7657, 34.7451, 31.7566, 34.7235, 35),  # 11
        ],
        "LLHZ": [(32.1816, 34.8440, 32.1772, 34.8318, 28)],  # 28
        "LLIB": [(32.9860, 35.5727, 32.9793, 35.5688, 28)],  # 33
        "LLKS": [(33.2192, 35.5924, 33.2124, 35.5993, 35)],  # 3
        "LLMG": [(32.5963, 35.2202, 32.5979, 35.2399, 35)],  # 9
        "LLPM": [
            (31.9058, 34.6886, 31.8950, 34.6957, 38),  # 3
            (31.9058, 34.6868, 31.8950, 34.6940, 38),  # 21
        ],
        "LLRD": [
            (32.6575, 35.1777, 32.6753, 35.1906, 28),  # 15
            (32.6554, 35.1630, 32.6634, 35.1859, 28),  # 33
            (32.6662, 35.1640, 32.6665, 35.1884, 28),  # 11
        ],
        "LLTN": [
            (31.8472, 34.8374, 31.8295, 34.8278, 38),  # 33
            (31.8265, 34.8193, 31.8459, 34.8165, 38),  # 15
            (31.8468, 34.8319, 31.8286, 34.8220, 38),  # 18
        ],
        "LTAF": [(36.9760, 35.2918, 36.9878, 35.2682, 35)],  # 23
        "LTAG": [(37.0092, 35.4122, 36.9949, 35.4400, 35)],  # 5
        "LTAJ": [(36.9443, 37.4628, 36.9519, 37.4939, 35)],  # 10
        "LTCH": [(37.4355, 38.9126, 37.4606, 38.8841, 35)],  # 22
        "LTDA": [(36.3537, 36.2985, 36.3710, 36.2764, 35)],  # 22
        "LTFG": [(36.2990, 32.2860, 36.2989, 32.3093, 28)],  # 8
        "OJAM": [(32.0121, 36.2320, 31.9989, 36.2154, 28)],  # 31
        "OJAM2": [(31.9673, 36.0072, 31.9783, 35.9762, 35)],  # 24
        "OJH3": [
            (32.9318, 39.7324, 32.9406, 39.7592, 35),  # 11
            (32.9280, 39.7349, 32.9174, 39.7608, 35),  # 29
        ],
        "OJH3NW": [(33.0812, 39.6069, 33.0707, 39.5863, 38)],  # 30
        "OJH3SW": [(32.7485, 39.6125, 32.7384, 39.5919, 38)],  # 30
        "OJH4": [(32.5416, 38.2064, 32.5370, 38.1838, 38)],  # 28
        "OJMA": [(32.3648, 36.2699, 32.3486, 36.2498, 35)],  # 31
        "OJMF": [
            (31.8162, 36.7908, 31.8190, 36.7666, 35),  # 26
            (31.8404, 36.7927, 31.8261, 36.7749, 35),  # 8
        ],
        "OJPH": [(32.1694, 37.1604, 32.1520, 37.1384, 35)],  # 31
        "OJRW": [(32.4059, 39.1423, 32.4040, 39.1188, 35)],  # 27
        "OJTH": [(32.7097, 36.4026, 32.6984, 36.4250, 35)],  # 5
        "OLBA": [
            (33.8181, 35.4878, 33.8365, 35.4875, 35),  # 17
            (33.8189, 35.4846, 33.8041, 35.4978, 35),  # 35
            (33.8162, 35.4813, 33.8341, 35.4848, 35),  # 3
        ],
        "OLKA": [(34.5943, 35.9985, 34.5843, 36.0244, 38)],  # 6
        "OLRA": [(33.8590, 35.9766, 33.8432, 35.9981, 35)],  # 4
        "OLWH": [(34.2758, 35.6841, 34.2869, 35.6761, 28)],  # 20
        "OSABD": [(35.7333, 37.1188, 35.7313, 37.0895, 35)],  # 27
        "OSAN": [(33.9108, 36.8755, 33.9264, 36.8562, 35)],  # 22
        "OSAP": [(36.1824, 37.2383, 36.1789, 37.2104, 38)],  # 27
        "OSDI": [
            (33.4353, 36.5039, 33.4157, 36.5331, 35),  # 5
            (33.4052, 36.4957, 33.3856, 36.5250, 35),  # 23
        ],
        "OSDR": [(33.6049, 36.7626, 33.6145, 36.7357, 38)],  # 24
        "OSDZ": [(35.2814, 40.1612, 35.2895, 40.1909, 35)],  # 10
        "OSHM": [(35.1202, 36.7254, 35.1159, 36.6993, 35)],  # 27
        "OSJI": [(36.0943, 37.9209, 36.0994, 37.9522, 38)],  # 10
        "OSKH": [
            (33.0683, 36.5349, 33.0884, 36.5473, 28),  # 15
            (33.0686, 36.5592, 33.0637, 36.5855, 28),  # 33
        ],
        "OSKW": [(36.1856, 37.5704, 36.1894, 37.5925, 35)],  # 10
        "OSLK": [(35.3918, 35.9505, 35.4116, 35.9503, 35)],  # 17
        "OSMN": [
            (36.5200, 37.0336, 36.5228, 37.0490, 35),  # 10
            (36.5276, 37.0321, 36.5183, 37.0430, 35),  # 28
        ],
        "OSMR": [(33.2931, 36.4442, 33.2844, 36.4667, 38)],  # 6
        "OSMS1": [(33.5004, 36.4664, 33.5002, 36.4679, 28)],  # 8
        "OSMS2": [(33.4872, 36.4745, 33.4872, 36.4763, 28)],  # 9
        "OSMZ": [(33.4731, 36.2352, 33.4825, 36.2132, 35)],  # 24
        "OSPR": [(34.5562, 38.3311, 34.5583, 38.3023, 35)],  # 26
        "OSQS": [(34.5720, 36.5853, 34.5666, 36.5576, 35)],  # 28
        "OSQS2": [(33.4591, 36.3570, 33.4584, 36.3584, 28)],  # 5
        "OSSH": [(34.4856, 36.8946, 34.4948, 36.9207, 38)],  # 11
        "OSSQ": [(33.6795, 37.2041, 33.6802, 37.2301, 35)],  # 8
        "OSTB": [(35.7540, 38.5512, 35.7555, 38.5817, 38)],  # 9
        "OSTF": [(35.9749, 36.7859, 35.9733, 36.7770, 35)],  # 28
        "OSTI": [(34.5228, 37.6458, 34.5225, 37.6145, 35)],  # 27
        "OSTS": [(36.2616, 38.9240, 36.2632, 38.9326, 28)],  # 10
    },
    "TheChannel": {
        # no runway data — map not owned
    },
}


import math as _math


def _on_runway(
    ac_lat: float, ac_lon: float, ac_alt_ft: float,
    field_elev_ft: float,
    icao: str,
    map_name: str,
    agl_limit_ft: float = 200.0,
) -> bool:
    """
    Return True if the aircraft is within any runway corridor at the given airfield.
    Uses a centerline + half-width corridor check in local Cartesian space.
    """
    if ac_alt_ft > field_elev_ft + agl_limit_ft:
        return False

    runways = RUNWAYS.get(map_name, {}).get(icao.upper(), [])
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


def runway_lookup(
    icao: str, map_name: str
) -> list[tuple[float, float, float, float, int]]:
    """Return runway threshold data for an ICAO code on the given map."""
    return RUNWAYS.get(map_name, {}).get(icao.upper(), [])


def validate_airfield(map_name: str, icao: str) -> bool:
    """Return True if the given ICAO is present on the given map."""
    return icao.upper() in MAP_AIRFIELDS.get(map_name, set())


def maps_for_airfield(icao: str) -> list[str]:
    """Return the list of maps containing the given ICAO."""
    icao = icao.upper()
    return sorted(m for m, icaos in MAP_AIRFIELDS.items() if icao in icaos)


def airfields_on_map(map_name: str) -> list[str]:
    """Return sorted list of ICAOs present on the given map."""
    return sorted(MAP_AIRFIELDS.get(map_name, set()))


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
        "rsbn": [("09", 18)],
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


# ---------------------------------------------------------------------------
# TAXIWAYS — taxiway names and routing for common DCS airfields.
#
# Structure:
#   ICAO: {
#     "to_runway": { "RWY": ["taxiway", ...] },   — route from parking to runway
#     "to_parking": { "RWY": ["taxiway", ...] },   — route from runway to parking
#   }
#
# Only popular airfields are included. Airports without entries will use
# generic taxi instructions without taxiway names.
# ---------------------------------------------------------------------------

TAXIWAYS: dict[str, dict[str, dict[str, list[str]]]] = {

    # -------------------------------------------------------------------------
    # CAUCASUS
    # -------------------------------------------------------------------------
    "UGSB": {  # Batumi
        "to_runway": {"13": ["Alpha", "Bravo"], "31": ["Alpha"]},
        "to_parking": {"13": ["Alpha"], "31": ["Bravo", "Alpha"]},
    },
    "UGKS": {  # Kobuleti
        "to_runway": {"07": ["Alpha"], "25": ["Alpha", "Bravo"]},
        "to_parking": {"07": ["Bravo", "Alpha"], "25": ["Alpha"]},
    },
    "UGSN": {  # Senaki-Kolkhi
        "to_runway": {"09": ["Alpha", "Bravo"], "27": ["Alpha"]},
        "to_parking": {"09": ["Alpha"], "27": ["Bravo", "Alpha"]},
    },
    "UGKO": {  # Kutaisi
        "to_runway": {"08": ["Alpha", "Bravo"], "26": ["Alpha"]},
        "to_parking": {"08": ["Alpha"], "26": ["Bravo", "Alpha"]},
    },
    "URKA": {  # Anapa
        "to_runway": {"22": ["Alpha", "Bravo"], "04": ["Alpha"]},
        "to_parking": {"22": ["Alpha"], "04": ["Bravo", "Alpha"]},
    },
    "URSS": {  # Sochi-Adler
        "to_runway": {"06": ["Alpha", "Bravo"], "24": ["Alpha"]},
        "to_parking": {"06": ["Alpha"], "24": ["Bravo", "Alpha"]},
    },
    "URKH": {  # Maykop-Khanskaya
        "to_runway": {"04": ["Alpha"], "22": ["Alpha", "Bravo"]},
        "to_parking": {"04": ["Bravo", "Alpha"], "22": ["Alpha"]},
    },
    "URMZ": {  # Mozdok
        "to_runway": {"08": ["Alpha", "Bravo"], "26": ["Alpha"]},
        "to_parking": {"08": ["Alpha"], "26": ["Bravo", "Alpha"]},
    },

    # -------------------------------------------------------------------------
    # PERSIAN GULF
    # -------------------------------------------------------------------------
    "OMAD": {  # Al Dhafra AB
        "to_runway": {"13": ["Alpha", "Bravo"], "31": ["Alpha", "Charlie"]},
        "to_parking": {"13": ["Charlie", "Alpha"], "31": ["Bravo", "Alpha"]},
    },
    "OMAA": {  # Abu Dhabi International
        "to_runway": {"13": ["Mike", "November"], "31": ["Mike", "Lima"]},
        "to_parking": {"13": ["Lima", "Mike"], "31": ["November", "Mike"]},
    },
    "OMDM": {  # Al Minhad AB
        "to_runway": {"09": ["Alpha", "Bravo"], "27": ["Alpha"]},
        "to_parking": {"09": ["Alpha"], "27": ["Bravo", "Alpha"]},
    },
    "OMDB": {  # Dubai International
        "to_runway": {"12": ["Alpha", "Bravo"], "30": ["Alpha", "Charlie"]},
        "to_parking": {"12": ["Charlie", "Alpha"], "30": ["Bravo", "Alpha"]},
    },
    "OIKB": {  # Bandar Abbas
        "to_runway": {"21": ["Alpha", "Bravo"], "03": ["Alpha"]},
        "to_parking": {"21": ["Alpha"], "03": ["Bravo", "Alpha"]},
    },

    # -------------------------------------------------------------------------
    # SYRIA / CYPRUS / TURKEY
    # -------------------------------------------------------------------------
    "LCRA": {  # RAF Akrotiri
        "to_runway": {"10": ["Alpha", "Bravo"], "28": ["Alpha"]},
        "to_parking": {"10": ["Alpha"], "28": ["Bravo", "Alpha"]},
    },
    "LCLK": {  # Larnaca
        "to_runway": {"04": ["Alpha", "Bravo"], "22": ["Alpha"]},
        "to_parking": {"04": ["Alpha"], "22": ["Bravo", "Alpha"]},
    },
    "LCPH": {  # Paphos
        "to_runway": {"11": ["Alpha"], "29": ["Alpha", "Bravo"]},
        "to_parking": {"11": ["Bravo", "Alpha"], "29": ["Alpha"]},
    },
    "LTAG": {  # Incirlik AB
        "to_runway": {"05": ["Alpha", "Bravo"], "23": ["Alpha"]},
        "to_parking": {"05": ["Alpha"], "23": ["Bravo", "Alpha"]},
    },
    "OSLK": {  # Latakia (Basil Al Assad)
        "to_runway": {"17": ["Alpha", "Bravo"], "35": ["Alpha"]},
        "to_parking": {"17": ["Alpha"], "35": ["Bravo", "Alpha"]},
    },

    # -------------------------------------------------------------------------
    # NEVADA (NTTR)
    # -------------------------------------------------------------------------
    "KLSV": {  # Nellis AFB
        "to_runway": {"03": ["Alpha", "Bravo"], "21": ["Alpha", "Charlie"]},
        "to_parking": {"03": ["Charlie", "Alpha"], "21": ["Bravo", "Alpha"]},
    },
    "KLAS": {  # Las Vegas McCarran
        "to_runway": {"07": ["Alpha", "Bravo"], "25": ["Alpha", "Charlie"]},
        "to_parking": {"07": ["Charlie", "Alpha"], "25": ["Bravo", "Alpha"]},
    },
    "KINS": {  # Creech AFB
        "to_runway": {"08": ["Alpha"], "26": ["Alpha", "Bravo"]},
        "to_parking": {"08": ["Bravo", "Alpha"], "26": ["Alpha"]},
    },

    # -------------------------------------------------------------------------
    # MARIANA ISLANDS
    # -------------------------------------------------------------------------
    "PGUA": {  # Andersen AFB
        "to_runway": {"06": ["Alpha", "Bravo"], "24": ["Alpha", "Charlie"]},
        "to_parking": {"06": ["Charlie", "Alpha"], "24": ["Bravo", "Alpha"]},
    },
    "PGUM": {  # Guam (Won Pat)
        "to_runway": {"06": ["Alpha", "Bravo"], "24": ["Alpha"]},
        "to_parking": {"06": ["Alpha"], "24": ["Bravo", "Alpha"]},
    },

    # -------------------------------------------------------------------------
    # NORMANDY / CHANNEL
    # -------------------------------------------------------------------------
    "LFRC": {  # Cherbourg-Maupertus
        "to_runway": {"10": ["Alpha"], "28": ["Alpha", "Bravo"]},
        "to_parking": {"10": ["Bravo", "Alpha"], "28": ["Alpha"]},
    },
    "EGMH": {  # Manston
        "to_runway": {"10": ["Alpha", "Bravo"], "28": ["Alpha"]},
        "to_parking": {"10": ["Alpha"], "28": ["Bravo", "Alpha"]},
    },

    # -------------------------------------------------------------------------
    # SOUTH ATLANTIC
    # -------------------------------------------------------------------------
    "EGYP": {  # Mount Pleasant
        "to_runway": {"10": ["Alpha", "Bravo"], "28": ["Alpha"]},
        "to_parking": {"10": ["Alpha"], "28": ["Bravo", "Alpha"]},
    },

    # -------------------------------------------------------------------------
    # SINAI
    # -------------------------------------------------------------------------
    "HEAR": {  # El Arish
        "to_runway": {"04": ["Alpha"], "22": ["Alpha", "Bravo"]},
        "to_parking": {"04": ["Bravo", "Alpha"], "22": ["Alpha"]},
    },
    "HECA": {  # Cairo International
        "to_runway": {"05": ["Alpha", "Bravo", "Charlie"], "23": ["Alpha", "Delta"]},
        "to_parking": {"05": ["Delta", "Alpha"], "23": ["Charlie", "Bravo", "Alpha"]},
    },

    # -------------------------------------------------------------------------
    # AFGHANISTAN
    # -------------------------------------------------------------------------
    "OAKS": {  # Kandahar
        "to_runway": {"05": ["Alpha", "Bravo"], "23": ["Alpha", "Charlie"]},
        "to_parking": {"05": ["Charlie", "Alpha"], "23": ["Bravo", "Alpha"]},
    },
    "OAIX": {  # Bagram
        "to_runway": {"03": ["Alpha", "Bravo"], "21": ["Alpha"]},
        "to_parking": {"03": ["Alpha"], "21": ["Bravo", "Alpha"]},
    },

    # -------------------------------------------------------------------------
    # KOLA
    # -------------------------------------------------------------------------
    "ENBO": {  # Bodø
        "to_runway": {"07": ["Alpha", "Bravo"], "25": ["Alpha"]},
        "to_parking": {"07": ["Alpha"], "25": ["Bravo", "Alpha"]},
    },
    "ULAS": {  # Severomorsk-1
        "to_runway": {"01": ["Alpha"], "19": ["Alpha", "Bravo"]},
        "to_parking": {"01": ["Bravo", "Alpha"], "19": ["Alpha"]},
    },
}


def taxiway_lookup(icao: str, runway: str = "", direction: str = "to_runway") -> list[str]:
    """
    Return the taxiway route for an airport/runway combination.
    direction: "to_runway" (departure) or "to_parking" (arrival).
    Returns empty list if no taxiway data exists.
    """
    data = TAXIWAYS.get(icao.upper(), {})
    routes = data.get(direction, {})
    if runway:
        # Try exact match, then strip L/R/C suffix
        route = routes.get(runway) or routes.get(runway.rstrip("LRC"))
        if route:
            return route
    # Fallback: return first available route for this direction
    if routes:
        return next(iter(routes.values()))
    return []


def preferred_runway(icao: str) -> str | None:
    """
    Return the preferred runway designator for an airfield.
    Uses the first ILS entry in NAVAIDS as the primary approach runway.
    Returns None for airports with no ILS data (caller should require manual override).
    """
    navaids = NAVAIDS.get(icao.upper(), {})
    ils = navaids.get("ils", [])
    return ils[0][0] if ils else None


def best_runway_for_wind(
    preferred: str,
    wind_dir_mag: float,
    wind_speed_kts: float,
    calm_threshold_kts: float = 3.0,
) -> str:
    """
    Pick the best runway (preferred or its reciprocal) based on wind.

    DCS reports wind as degrees FROM (meteorological convention). Runway numbers
    are based on magnetic heading of the landing direction (e.g. runway 28 =
    280° magnetic). Aircraft land INTO the wind, so the best runway is the one
    whose heading is closest to the direction the wind is coming FROM.

    The headwind component is wind_speed * cos(wind_from - runway_heading).
    Positive = headwind, negative = tailwind. Pick the runway with the larger
    headwind component.

    Below calm_threshold_kts the wind is effectively calm and the preferred
    runway is returned unchanged.
    """
    import math

    if wind_speed_kts < calm_threshold_kts:
        return preferred

    # Parse the preferred runway to find its reciprocal
    num_str = ""
    suffix = ""
    for ch in preferred:
        if ch.isdigit():
            num_str += ch
        else:
            suffix = ch
            break
    if not num_str:
        return preferred
    recip_num = (int(num_str) + 18) % 36
    if recip_num == 0:
        recip_num = 36
    suffix_map = {"L": "R", "R": "L", "C": "C"}
    recip_suffix = suffix_map.get(suffix.upper(), "")
    reciprocal = f"{recip_num:02d}{recip_suffix}"

    pref_hdg = runway_to_heading(preferred)
    recip_hdg = runway_to_heading(reciprocal)

    pref_headwind = wind_speed_kts * math.cos(math.radians(wind_dir_mag - pref_hdg))
    recip_headwind = wind_speed_kts * math.cos(math.radians(wind_dir_mag - recip_hdg))

    return preferred if pref_headwind >= recip_headwind else reciprocal


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
