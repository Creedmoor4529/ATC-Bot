"""
SRS (SimpleRadioStandalone) external audio bot client — v2.x protocol.

UDP audio packet layout (SRS v2.x):
  [2 bytes]  total packet length (including these 2 bytes)
  [N bytes]  Opus encoded audio
  per radio:
    [8 bytes]  frequency (float64 LE, Hz)
    [4 bytes]  modulation (int32 LE)
    [4 bytes]  encryption (int32 LE, 0 = none)
  [1 byte]   number of radios
  [4 bytes]  unit ID (uint32 LE)
  [8 bytes]  packet ID (uint64 LE)
  [22 bytes] short GUID (base64 ASCII, NOT 36-char UUID)
  [1 byte]   retransmission count

TCP messages are newline-delimited JSON using the standard 36-char UUID in the
ClientGuid field — only the UDP layer uses the 22-char short GUID.
"""

import asyncio
import base64
import json
import logging
import socket
import struct
import threading
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

import opuslib

from config import SRS_HOST, SRS_PORT, AUDIO_SAMPLE_RATE, SRS_EAM_PASSWORD

_SRS_IP: str = socket.gethostbyname(SRS_HOST)

logger = logging.getLogger(__name__)

MSG_UPDATE          = 0
MSG_PING            = 1
MSG_SYNC            = 2
MSG_SERVER_SETTINGS = 4
MSG_CLIENT_DISCONNECT = 5
MSG_VERSION_MISMATCH  = 6
MSG_EAM_PASSWORD    = 7
MSG_EAM_DISCONNECT  = 8

MODULATION_AM       = 0
MODULATION_FM       = 1
MODULATION_INTERCOM = 2

OPUS_FRAME_MS      = 40
OPUS_FRAME_SAMPLES = int(AUDIO_SAMPLE_RATE * OPUS_FRAME_MS / 1000)

SRS_VERSION = "2.1.0.2"


def _make_short_guid() -> str:
    """Generate a 22-character base64 GUID as used by SRS v2.x."""
    raw = base64.b64encode(uuid.uuid4().bytes).decode("ascii")
    return raw.replace("/", "_").replace("+", "-")[:22]


@dataclass
class SRSRadio:
    frequency: float
    modulation: int = MODULATION_AM
    name: str = "ATC"
    callsign: str = ""


@dataclass
class SRSClient:
    name: str
    radios: list = field(default_factory=list)
    # SRS uses two GUID forms:
    #   long_guid  — 36-char UUID string for TCP JSON messages
    #   short_guid — 22-char base64 for UDP packets
    long_guid: str  = field(default_factory=lambda: str(uuid.uuid4()))
    short_guid: str = field(default_factory=_make_short_guid)
    coalition: int  = 2
    lat: float = 0.0
    lon: float = 0.0
    alt: float = 0.0


class SRSAudioBot:
    def __init__(
        self,
        client: SRSClient,
        on_audio_received: Optional[Callable[[bytes, float], None]] = None,
    ):
        self.client = client
        self.on_audio_received = on_audio_received

        self._tcp_reader: Optional[asyncio.StreamReader] = None
        self._tcp_writer: Optional[asyncio.StreamWriter] = None
        self._udp_sock: Optional[socket.socket] = None
        self._running = False
        self._packet_id = 0
        self._loop: Optional[asyncio.AbstractEventLoop] = None

        self._encoder = opuslib.Encoder(AUDIO_SAMPLE_RATE, 1, opuslib.APPLICATION_VOIP)
        self._decoder = opuslib.Decoder(AUDIO_SAMPLE_RATE, 1)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def connect(self):
        self._loop = asyncio.get_event_loop()
        logger.info(f"Connecting to SRS at {SRS_HOST} ({_SRS_IP}):{SRS_PORT}")
        logger.info(f"Bot GUID short={self.client.short_guid}  long={self.client.long_guid}")

        self._tcp_reader, self._tcp_writer = await asyncio.open_connection(
            _SRS_IP, SRS_PORT
        )
        self._running = True

        # UDP — connected socket (mirrors how SRS client and SkyEye connect)
        # Using connect() creates a strong NAT mapping and ensures return traffic arrives
        self._udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._udp_sock.bind(("0.0.0.0", 0))
        self._udp_sock.connect((_SRS_IP, SRS_PORT))
        self._udp_sock.settimeout(1.0)
        local_port = self._udp_sock.getsockname()[1]
        logger.info(f"UDP connected to {_SRS_IP}:{SRS_PORT} from local port {local_port}")

        t = threading.Thread(target=self._udp_recv_thread, daemon=True)
        t.start()

        await self._send_sync()
        if SRS_EAM_PASSWORD:
            await self._send_eam_password()
        self._send_udp_ping()

        asyncio.create_task(self._tcp_receive_loop())
        asyncio.create_task(self._heartbeat_loop())
        asyncio.create_task(self._udp_ping_loop())

        logger.info("SRS connected.")

    async def disconnect(self):
        self._running = False
        if self._tcp_writer:
            self._tcp_writer.close()
            await self._tcp_writer.wait_closed()
        if self._udp_sock:
            self._udp_sock.close()

    async def transmit(self, pcm_bytes: bytes, radio_index: int = 0):
        if not self._udp_sock:
            logger.warning("UDP not ready")
            return
        radio = self.client.radios[radio_index]
        frames = self._pcm_to_opus_frames(pcm_bytes)
        for frame in frames:
            pkt = self._build_audio_packet(frame, radio.frequency, radio.modulation)
            self._udp_sock.send(pkt)
            self._packet_id += 1
            await asyncio.sleep(OPUS_FRAME_MS / 1000)

    # ------------------------------------------------------------------
    # UDP receive thread
    # ------------------------------------------------------------------

    def _udp_recv_thread(self):
        logger.info("UDP receive thread started.")
        while self._running:
            try:
                data = self._udp_sock.recv(65535)
                if len(data) == 22:
                    logger.debug(f"UDP ping echo: {data.decode('ascii', errors='ignore')}")
                    continue  # ping echo, not audio
                logger.debug(f"UDP recv {len(data)} bytes | {data[:6].hex()}")
                self._parse_audio_packet(data)
            except socket.timeout:
                continue
            except OSError:
                break
        logger.info("UDP receive thread stopped.")

    def _parse_audio_packet(self, data: bytes):
        """
        Parse an incoming SRS v2.x UDP voice packet.
        Layout:
          [0:2]   PacketLength (uint16 LE)
          [2:4]   AudioSegmentLength (uint16 LE)
          [4:6]   FrequenciesSegmentLength (uint16 LE)
          [6:6+AudioSegmentLength]  Opus audio bytes
          [6+AudioSegmentLength : 6+AudioSegmentLength+FrequenciesSegmentLength]
                  Frequencies: each 10 bytes (float64 freq + byte mod + byte enc)
          [PacketLength-57 : PacketLength-53]  UnitID (uint32)
          [PacketLength-53 : PacketLength-45]  PacketID (uint64)
          [PacketLength-45]                    Hops (uint8)
          [PacketLength-44 : PacketLength-22]  RelayGUID (22 bytes)
          [PacketLength-22 : PacketLength]     OriginGUID (22 bytes)
        """
        try:
            if len(data) < 6:
                return

            packet_length        = struct.unpack_from("<H", data, 0)[0]
            audio_segment_length = struct.unpack_from("<H", data, 2)[0]
            freq_segment_length  = struct.unpack_from("<H", data, 4)[0]

            # Audio
            opus_data = data[6 : 6 + audio_segment_length]

            # Frequencies (10 bytes each: float64 + byte + byte)
            freq_offset = 6 + audio_segment_length
            frequencies = []
            for i in range(freq_segment_length // 10):
                off  = freq_offset + i * 10
                freq = struct.unpack_from("<d", data, off)[0]
                mod  = data[off + 8]
                enc  = data[off + 9]
                frequencies.append((freq, mod, enc))

            # Fixed tail (57 bytes from end)
            origin_guid = data[packet_length - 22 : packet_length].decode("ascii", errors="ignore")

            if not opus_data:
                return
            if origin_guid == self.client.short_guid:
                return  # own transmission

            primary_freq = frequencies[0][0] if frequencies else 0.0
            logger.debug(
                f"Audio origin={origin_guid[:8]}.. freq={primary_freq/1e6:.3f}MHz "
                f"freqs={len(frequencies)} audio={len(opus_data)}B"
            )

            if self.on_audio_received and self._loop:
                self._loop.call_soon_threadsafe(
                    self.on_audio_received, opus_data, primary_freq
                )

        except Exception as e:
            logger.debug(f"Packet parse error: {e} | data={data[:20].hex()}")

    def _send_udp_ping(self):
        """Send the 22-byte GUID ping so the server registers our UDP endpoint."""
        try:
            self._udp_sock.send(self.client.short_guid.encode("ascii"))
            logger.debug("UDP ping sent.")
        except Exception as e:
            logger.debug(f"UDP ping error: {e}")

    async def _udp_ping_loop(self):
        while self._running:
            await asyncio.sleep(5)
            self._send_udp_ping()

    # ------------------------------------------------------------------
    # TCP
    # ------------------------------------------------------------------

    async def _send_eam_password(self):
        logger.info("Sending EAM password...")
        await self._send_tcp({
            "MsgType": MSG_EAM_PASSWORD,
            "ExternalAWACSModePassword": SRS_EAM_PASSWORD,
            "Client": self._client_dict(),
            "Version": SRS_VERSION,
        })

    async def _send_sync(self):
        await self._send_tcp({
            "MsgType": MSG_SYNC,
            "Client": self._client_dict(),
            "Version": SRS_VERSION,
        })

    async def _send_update(self):
        await self._send_tcp({
            "MsgType": MSG_UPDATE,
            "Client": self._client_dict(),
            "Version": SRS_VERSION,
        })

    async def _send_tcp(self, msg: dict):
        data = (json.dumps(msg) + "\n").encode("utf-8")
        self._tcp_writer.write(data)
        await self._tcp_writer.drain()

    async def _tcp_receive_loop(self):
        while self._running:
            try:
                line = await self._tcp_reader.readline()
                if not line:
                    logger.warning("SRS TCP stream ended.")
                    break
                try:
                    msg = json.loads(line.decode("utf-8"))
                    mt = msg.get("MsgType", "?")
                    logger.info(f"SRS TCP type={mt} raw={line[:200]!r}")
                    if mt == MSG_VERSION_MISMATCH:
                        sv = msg.get("Version", "?")
                        logger.warning(f"SRS VERSION MISMATCH server={sv} us={SRS_VERSION}")
                    elif mt == MSG_SERVER_SETTINGS:
                        logger.info("SRS server settings received.")
                    elif mt == MSG_EAM_PASSWORD:
                        logger.info("EAM authentication accepted.")
                    elif mt == MSG_EAM_DISCONNECT:
                        logger.error("EAM authentication REJECTED — check SRS_EAM_PASSWORD in .env")
                except json.JSONDecodeError:
                    logger.debug(f"SRS non-JSON: {line[:80]!r}")
            except (asyncio.IncompleteReadError, ConnectionResetError):
                logger.warning("SRS TCP closed.")
                break
            except Exception as e:
                logger.error(f"SRS TCP error: {e}")
        self._running = False

    async def _heartbeat_loop(self):
        while self._running:
            await asyncio.sleep(10)
            try:
                await self._send_tcp({"MsgType": MSG_PING, "Client": self._client_dict(), "Version": SRS_VERSION})
                await self._send_update()
                self._send_udp_ping()
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")

    # ------------------------------------------------------------------
    # Packet building
    # ------------------------------------------------------------------

    def _build_audio_packet(self, opus_frame: bytes, frequency: float, modulation: int) -> bytes:
        """
        Build SRS v2.x UDP voice packet:
          [0:2]  PacketLength
          [2:4]  AudioSegmentLength
          [4:6]  FrequenciesSegmentLength
          [6:6+audio]  Opus audio
          [6+audio : 6+audio+10]  Frequency: float64 + byte mod + byte enc
          [PacketLength-57 : -53]  UnitID (uint32)
          [PacketLength-53 : -45]  PacketID (uint64)
          [PacketLength-45]        Hops (byte)
          [PacketLength-44 : -22]  RelayGUID (22 bytes)
          [PacketLength-22 : end]  OriginGUID (22 bytes)
        """
        guid_bytes        = self.client.short_guid.encode("ascii")  # 22 bytes
        audio_len         = len(opus_frame)
        freq_data         = (
            struct.pack("<d", frequency)    # 8 bytes
            + struct.pack("<B", modulation) # 1 byte
            + struct.pack("<B", 0)          # 1 byte encryption
        )  # 10 bytes
        freq_len          = len(freq_data)
        fixed_len         = 57  # UnitID(4)+PacketID(8)+Hops(1)+RelayGUID(22)+OriginGUID(22)
        packet_length     = 6 + audio_len + freq_len + fixed_len

        b = bytearray(packet_length)
        struct.pack_into("<H", b, 0, packet_length)
        struct.pack_into("<H", b, 2, audio_len)
        struct.pack_into("<H", b, 4, freq_len)
        b[6 : 6 + audio_len]                       = opus_frame
        b[6 + audio_len : 6 + audio_len + freq_len] = freq_data
        struct.pack_into("<I", b, packet_length - 57, 100000)
        struct.pack_into("<Q", b, packet_length - 53, self._packet_id)
        b[packet_length - 45]                       = 0  # hops
        b[packet_length - 44 : packet_length - 22]  = guid_bytes  # relay
        b[packet_length - 22 : packet_length]       = guid_bytes  # origin
        return bytes(b)

    def _pcm_to_opus_frames(self, pcm_bytes: bytes) -> list[bytes]:
        frame_size = OPUS_FRAME_SAMPLES * 2
        frames = []
        for i in range(0, len(pcm_bytes), frame_size):
            chunk = pcm_bytes[i: i + frame_size]
            if len(chunk) < frame_size:
                chunk = chunk.ljust(frame_size, b"\x00")
            frames.append(self._encoder.encode(chunk, OPUS_FRAME_SAMPLES))
        return frames

    def _client_dict(self) -> dict:
        return {
            "ClientGuid": self.client.short_guid,  # SRS uses 22-char short GUID everywhere
            "Name": self.client.name,
            "Coalition": self.client.coalition,
            "LatLngPosition": {
                "lat": self.client.lat,
                "lng": self.client.lon,
                "alt": self.client.alt,
            },
            "RadioInfo": {
                "radios": [
                    {
                        "freq": r.frequency,
                        "modulation": r.modulation,
                        "name": r.name,
                        "secFreq": 0.0,
                        "retransmit": False,
                        "enc": False,
                        "encKey": 0,
                        "encMode": 0,
                        "freqMin": 1.0,
                        "freqMax": 1.0,
                        "volMode": 0,
                        "expansion": False,
                        "channel": -1,
                        "simul": False,
                    }
                    for r in self.client.radios
                ],
                "unit": self.client.name,
                "unitId": 100000,
                "iff": {
                    "control": 0,
                    "mode1": 0,
                    "mode3": 0,
                    "mode4": False,
                    "mic": -1,
                    "status": 0,
                },
            },
        }
