"""
TP2 — HTTP/2 File Transfer Server — SOLUTION
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

# TODO 3 SOLUTION: "h2" is the IANA-registered ALPN token for HTTP/2.
# Defined in RFC 7540 Section 11.1.
# Hypercorn sets this automatically via its internal _ssl_context() method
# when the h2 package is installed. The value here is printed at startup
# so students know what to search for in the Wireshark ClientHello.
HTTP2_ALPN_TOKEN = "h2"

PORT = 8443

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "data.txt")
app = Quart(__name__)


@app.route("/")
async def index():
    return await send_file(
        os.path.join(os.path.dirname(__file__), "..", "..", "tp2-http2", "index.html")
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

    # TODO 4 SOLUTION: port 8443 (HTTPS convention, no root required)
    config.bind = [f"0.0.0.0:{PORT}"]

    # TODO 5 SOLUTION: Hypercorn reads certfile/keyfile to set up TLS.
    # It then calls ssl.SSLContext.set_alpn_protocols(["h2", "http/1.1"])
    # internally — which is why "h2" appears in the Wireshark ClientHello.
    # Note: config.ssl (passing an SSLContext directly) is NOT supported
    # by Hypercorn — always use config.certfile and config.keyfile.
    config.certfile = CERT_FILE
    config.keyfile  = KEY_FILE

    print(f"\n  HTTP/2 server started")
    print(f"  Listening on: https://localhost:{PORT}")
    print(f"  Wireshark filter: tls  (or: tcp.port == {PORT})")
    print(f"\n  Expected ALPN token in Wireshark ClientHello: {HTTP2_ALPN_TOKEN}")
    print(f"\n  In a second terminal, run:  python client.py")
    print("  Press Ctrl+C to stop.\n")

    await hypercorn_serve(app, config)


if __name__ == "__main__":
    asyncio.run(main())
