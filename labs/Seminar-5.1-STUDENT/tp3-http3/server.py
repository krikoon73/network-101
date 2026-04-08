"""
TP3 — HTTP/3 File Transfer Server
======================================
Protocol stack: HTTP/3 → QUIC (TLS 1.3 built-in) → UDP → IP
Encryption    : TLS 1.3 integrated into QUIC — always on, cannot be disabled

How HTTP/3 is negotiated in practice (Alt-Svc mechanism)
---------------------------------------------------------
Unlike HTTP/1.1 → HTTP/2 (which is negotiated inside the TLS handshake via ALPN),
HTTP/3 uses a different upgrade path:

  1. The browser connects via TCP + TLS → HTTP/2  (first visit)
  2. The server responds with:  Alt-Svc: h3=":8443"; ma=86400
     This means: "I also speak HTTP/3 on port 8443 — try it next time."
  3. On the next request, the browser opens a QUIC connection on UDP port 8443.
  4. Subsequent requests use HTTP/3 over QUIC.

This server listens on BOTH:
  - TCP port 8443  →  HTTP/1.1 and HTTP/2  (initial connection + fallback)
  - UDP port 8443  →  HTTP/3 / QUIC        (after Alt-Svc upgrade)

Instructions
------------
Complete the 6 TODO sections below (15 minutes).
Do NOT modify any code outside the TODO sections.

Run the server with:  python server.py
Then in a second terminal: python client.py
"""

import asyncio
import os

from quart import Quart, Response, request, send_file
from hypercorn.config import Config
from hypercorn.asyncio import serve as hypercorn_serve

# ──────────────────────────────────────────────────────────────────
# CONFIGURATION — Complete TODOs 1, 2, and 3
# ──────────────────────────────────────────────────────────────────

CERTS_DIR = os.path.join(os.path.dirname(__file__), "..", "certs")

# TODO 1: Set the filename of the TLS certificate (same file as TP2).
#
CERT_FILE = os.path.join(CERTS_DIR, "????")


# TODO 2: Set the filename of the TLS private key (same file as TP2).
#
KEY_FILE = os.path.join(CERTS_DIR, "????")


# TODO 3: Set the ALPN token for HTTP/3.
#
#   In TP2 you used "h2" for HTTP/2. HTTP/3 has its own IANA-registered
#   ALPN token, defined in RFC 9114 §7.
#   It follows the same naming pattern as "h2" — what comes after "h2"?
#
#   This value will be printed at startup so you know what to look for
#   in the Wireshark QUIC Initial packet.
#
HTTP3_ALPN_TOKEN = "????"

PORT = 8443

# ──────────────────────────────────────────────────────────────────
# QUART APPLICATION (provided — do not modify)
# ──────────────────────────────────────────────────────────────────

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "data.txt")
app = Quart(__name__)


@app.route("/")
async def index():
    return await send_file(os.path.join(os.path.dirname(__file__), "index.html"))


@app.route("/data")
async def data():
    """Serve the data file with Range request support (same logic as TP1 and TP2)."""
    file_size = os.path.getsize(DATA_PATH)
    range_header = request.headers.get("Range")

    if range_header:
        range_spec = range_header.replace("bytes=", "")
        parts = range_spec.split("-")
        start = int(parts[0])
        end   = int(parts[1]) if parts[1] else file_size - 1
        chunk_size = end - start + 1

        def generate():
            with open(DATA_PATH, "rb") as f:
                f.seek(start)
                yield f.read(chunk_size)

        headers = {
            "Content-Range":  f"bytes {start}-{end}/{file_size}",
            "Content-Length": str(chunk_size),
            "Accept-Ranges":  "bytes",
        }
        return Response(generate(), status=206, headers=headers, mimetype="text/plain")
    else:
        return await send_file(DATA_PATH, mimetype="text/plain")


# ──────────────────────────────────────────────────────────────────
# SERVER STARTUP — Complete TODOs 4, 5, and 6
# ──────────────────────────────────────────────────────────────────

async def main():
    config = Config()

    # TODO 4: Set the TCP listening address and port.
    #
    #   This is the same as TP2. Hypercorn will handle HTTP/1.1 and HTTP/2
    #   over TCP on this address, and also serve the initial page before
    #   the browser upgrades to HTTP/3.
    #
    config.bind = [f"0.0.0.0:????"]

    # TODO 5: Configure TLS — same certfile and keyfile as TP2.
    #
    config.certfile = ????
    config.keyfile  = ????

    # TODO 6: Enable HTTP/3 by activating the QUIC/UDP listener.
    #
    #   Setting quic_bind does two things automatically:
    #     (a) Hypercorn also listens on UDP at these addresses → HTTP/3 over QUIC
    #     (b) Hypercorn adds "Alt-Svc: h3=\":8443\"; ma=3600" to HTTP/2 responses
    #
    #   The Alt-Svc header is how the server advertises HTTP/3 to the browser.
    #   When Chrome sees it, it will upgrade the next connection to QUIC (UDP).
    #
    #   WHY TWO ADDRESSES?
    #   On macOS, "localhost" resolves to ::1 (IPv6) first.  Chrome sends its
    #   first QUIC packet to ::1:8443.  UDP has no "connection refused" signal,
    #   so a packet to an unbound port is silently dropped.  Chrome waits,
    #   times out, marks the origin as "QUIC broken", and falls back to h2.
    #   Binding both 0.0.0.0 (IPv4) and ::: (IPv6 wildcard) fixes this.
    #
    config.quic_bind = [f"0.0.0.0:????", f":::????"]

    print(f"\n  HTTP/3 server started")
    print(f"  TCP  port {PORT} → HTTP/1.1 + HTTP/2 (initial connection)")
    print(f"  UDP  port {PORT} → HTTP/3 / QUIC     (after Alt-Svc upgrade)")
    print(f"\n  ALPN token for HTTP/3: {HTTP3_ALPN_TOKEN} (look in QUIC Initial packet)")
    print(f"\n  In a second terminal, run:  python client.py")
    print(f"  Wireshark filter: quic  (or: udp.port == {PORT})")
    print("  Press Ctrl+C to stop.\n")

    await hypercorn_serve(app, config)


if __name__ == "__main__":
    asyncio.run(main())
