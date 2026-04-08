"""
TP3 — HTTP/3 Client
====================
Protocol stack: HTTP/3 → QUIC (TLS 1.3 built-in) → UDP → IP

Key differences from TP2:
  - Transport is UDP, not TCP (no SYN / FIN packets in Wireshark)
  - TLS is integrated into QUIC (ClientHello is in the first UDP packet)
  - Connection established in 1 RTT instead of 2.5 RTT for HTTP/2

Instructions
------------
Complete the 3 TODO sections below, then run:
    python client.py   (server must be running in another terminal)
"""

import asyncio
import ssl

from aioquic.asyncio import connect
from aioquic.asyncio.protocol import QuicConnectionProtocol
from aioquic.h3.connection import H3Connection, H3_ALPN
from aioquic.h3.events import DataReceived, HeadersReceived
from aioquic.quic.configuration import QuicConfiguration
from aioquic.quic.events import QuicEvent

# ──────────────────────────────────────────────────────────────────
# CONFIGURATION — Complete TODOs 1, 2, and 3
# ──────────────────────────────────────────────────────────────────

# TODO 1: Set the server address.
#
#   Use "127.0.0.1" (not "localhost").
#   Reason: on many systems "localhost" resolves to ::1 (IPv6) first.
#   UDP has no "connection refused" signal, so a packet sent to an
#   unbound IPv6 port is silently dropped — QUIC times out silently.
#   Using the explicit IPv4 address avoids this ambiguity.
#
HOST = "????"


# TODO 2: Set the server port.
#
#   Use the same port as server.py (the UDP port, not a TCP port).
#
PORT = ????


# TODO 3: Set the ALPN protocol list for HTTP/3.
#
#   ALPN tells the server which application protocol the client wants.
#   For HTTP/3, the IANA-registered token is defined in RFC 9114 §7.
#   It follows the same pattern as "h2" for HTTP/2.
#
#   H3_ALPN is a convenience constant exported by the aioquic library.
#   It equals ["h3"].
#
#   Replace ???? with H3_ALPN  (the imported constant above).
#
ALPN = ????

PATH = "/data"

# ──────────────────────────────────────────────────────────────────
# HTTP/3 PROTOCOL HANDLER (provided — do not modify)
# ──────────────────────────────────────────────────────────────────

class Http3Client(QuicConnectionProtocol):
    """Minimal HTTP/3 client built on top of aioquic's QUIC transport."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._h3: H3Connection | None = None
        self._pending: dict[int, asyncio.Future] = {}
        self._events:  dict[int, list]           = {}

    def quic_event_received(self, event: QuicEvent) -> None:
        if self._h3 is None:
            self._h3 = H3Connection(self._quic, enable_webtransport=False)
        for h3_ev in self._h3.handle_event(event):
            sid = getattr(h3_ev, "stream_id", None)
            if sid is not None and sid in self._events:
                self._events[sid].append(h3_ev)
                if getattr(h3_ev, "stream_ended", False) and sid in self._pending:
                    fut = self._pending.pop(sid)
                    if not fut.done():
                        fut.set_result(self._events.pop(sid))

    async def get(self, path: str, headers: dict | None = None) -> list:
        """Send an HTTP/3 GET request and return the list of H3 events."""
        stream_id = self._quic.get_next_available_stream_id()
        self._events[stream_id]  = []
        self._pending[stream_id] = self._loop.create_future()

        req_headers = [
            (b":method",    b"GET"),
            (b":scheme",    b"https"),
            (b":authority", f"{HOST}:{PORT}".encode()),
            (b":path",      path.encode()),
        ]
        if headers:
            req_headers += [(k.encode(), v.encode()) for k, v in headers.items()]

        self._h3.send_headers(stream_id=stream_id, headers=req_headers, end_stream=True)
        self.transmit()
        return await self._pending[stream_id]


# ──────────────────────────────────────────────────────────────────
# MAIN (provided — do not modify)
# ──────────────────────────────────────────────────────────────────

async def main() -> None:
    # Build QUIC configuration
    config = QuicConfiguration(is_client=True)
    config.alpn_protocols = ALPN
    # TLS is always on in QUIC — we cannot disable it.
    # For this lab the server uses a self-signed cert, so we skip verification.
    # In production: config.verify_mode = ssl.CERT_REQUIRED (default)
    config.verify_mode = ssl.CERT_NONE

    print(f"\n  Connecting to {HOST}:{PORT} via QUIC (UDP) ...")
    print(f"  ALPN      : {ALPN}")
    print(f"  Transport : UDP  — no TCP SYN in Wireshark")
    print(f"  Wireshark filter: quic  (or: udp.port == {PORT})\n")

    async with connect(HOST, PORT, configuration=config,
                       create_protocol=Http3Client) as client:

        # ── Request 1: HEAD to get file size ─────────────────────
        events = await client.get(PATH)
        status    = next((dict(e.headers).get(b":status", b"?").decode()
                          for e in events if isinstance(e, HeadersReceived)), "?")
        file_size = next((int(dict(e.headers).get(b"content-length", b"0"))
                          for e in events if isinstance(e, HeadersReceived)), 0)

        print(f"  HEAD {PATH}")
        print(f"    Status    : {status}")
        print(f"    File size : {file_size:,} bytes\n")

        # ── Request 2: GET first 1 MB chunk ──────────────────────
        events = await client.get(PATH, headers={"range": "bytes=0-1048575"})
        hdrs   = next((dict(e.headers) for e in events
                       if isinstance(e, HeadersReceived)), {})
        body   = b"".join(e.data for e in events if isinstance(e, DataReceived))

        status        = hdrs.get(b":status", b"?").decode()
        content_range = hdrs.get(b"content-range", b"").decode()

        print(f"  GET {PATH}  Range: bytes=0-1048575")
        print(f"    Status        : {status}")
        print(f"    Content-Range : {content_range}")
        print(f"    Bytes received: {len(body):,}\n")

    print(f"  Transport confirmed: UDP/QUIC — no TCP used.")
    print(f"  TLS is built into QUIC: the ClientHello is inside the first UDP packet.")
    print(f"  In Wireshark: filter 'quic' — observe QUIC Initial and 1-RTT packets.\n")


if __name__ == "__main__":
    asyncio.run(main())
