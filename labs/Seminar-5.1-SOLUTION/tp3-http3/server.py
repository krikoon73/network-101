"""
TP3 — HTTP/3 File Transfer Server — SOLUTION
=============================================
FOR INSTRUCTOR USE ONLY
"""

import asyncio
import os

from quart import Quart, Response, request, send_file
from hypercorn.config import Config
from hypercorn.asyncio import serve as hypercorn_serve

CERTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "certs")

# TODO 1 SOLUTION:
CERT_FILE = os.path.join(CERTS_DIR, "server.crt")

# TODO 2 SOLUTION:
KEY_FILE = os.path.join(CERTS_DIR, "server.key")

# TODO 3 SOLUTION: "h3" is the IANA-registered ALPN token for HTTP/3.
# Defined in RFC 9114 §7.1. Follows the pattern: h2 → h3.
# Hypercorn negotiates this automatically when quic_bind is active.
HTTP3_ALPN_TOKEN = "h3"

PORT = 8443

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "data.txt")
app = Quart(__name__)


@app.route("/")
async def index():
    return await send_file(
        os.path.join(os.path.dirname(__file__), "..", "..", "tp3-http3", "index.html")
    )


@app.route("/data")
async def data():
    file_size    = os.path.getsize(DATA_PATH)
    range_header = request.headers.get("Range")

    if range_header:
        range_spec = range_header.replace("bytes=", "")
        parts      = range_spec.split("-")
        start      = int(parts[0])
        end        = int(parts[1]) if parts[1] else file_size - 1
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


async def main():
    config = Config()

    # TODO 4 SOLUTION: same port as TP2 — TCP for HTTP/2 initial connection
    config.bind = [f"0.0.0.0:{PORT}"]

    # TODO 5 SOLUTION: same TLS config as TP2
    config.certfile = CERT_FILE
    config.keyfile  = KEY_FILE

    # TODO 6 SOLUTION:
    # quic_bind activates:
    #   (a) UDP listeners for QUIC/HTTP/3
    #   (b) automatic injection of Alt-Svc: h3=":8443"; ma=3600 in HTTP/2 responses
    #
    # WHY TWO ADDRESSES?
    # On macOS, "localhost" resolves to ::1 (IPv6) first.
    # Chrome sends its QUIC Initial packet to ::1:8443.
    # UDP has no "connection refused" signal, so the packet is silently dropped.
    # Chrome marks the origin as "QUIC broken" and falls back to h2 permanently.
    # Binding both IPv4 (0.0.0.0) and IPv6 (:::) fixes this.
    config.quic_bind = [f"0.0.0.0:{PORT}", f":::{PORT}"]

    print(f"\n  HTTP/3 server started")
    print(f"  TCP  port {PORT} → HTTP/1.1 + HTTP/2 (fallback)")
    print(f"  UDP  port {PORT} → HTTP/3 / QUIC     (primary)")
    print(f"\n  ALPN token for HTTP/3: {HTTP3_ALPN_TOKEN}")
    print(f"  Wireshark filter: quic  (or: udp.port == {PORT})")
    print(f"\n  In a second terminal, run:  python client.py")
    print("  Press Ctrl+C to stop.\n")

    await hypercorn_serve(app, config)


if __name__ == "__main__":
    asyncio.run(main())
