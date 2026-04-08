"""
TP2 — HTTP/2 Client
====================
Demonstrates HTTP/2 over TLS 1.3.

Key differences from TP1:
  - Single TCP connection reused for all requests (multiplexing)
  - All traffic is TLS-encrypted (unreadable in Wireshark)
  - ALPN negotiation in TLS handshake selects "h2"

Run: python client.py   (server must be running in another terminal)
"""

import httpx

HOST = "localhost"
PORT = 8443
PATH = "/data"

print(f"\n  Connecting to https://{HOST}:{PORT} ...")
print(f"  Wireshark filter: tls  (or: tcp.port == {PORT})\n")

# verify=False because the server uses a self-signed certificate.
# In production, you would use verify=True with a trusted CA.
with httpx.Client(http2=True, verify=False) as client:

    # ── Request 1: HEAD to get file size ─────────────────────────
    r = client.head(f"https://{HOST}:{PORT}{PATH}")
    file_size = int(r.headers.get("content-length", 0))

    print(f"  HEAD {PATH}")
    print(f"    Protocol : {r.http_version}")
    print(f"    Status   : {r.status_code}")
    print(f"    File size: {file_size:,} bytes\n")

    # ── Request 2: GET first 1 MB chunk ──────────────────────────
    r = client.get(
        f"https://{HOST}:{PORT}{PATH}",
        headers={"Range": "bytes=0-1048575"},
    )
    print(f"  GET {PATH}  Range: bytes=0-1048575")
    print(f"    Protocol      : {r.http_version}")
    print(f"    Status        : {r.status_code}")
    print(f"    Content-Range : {r.headers.get('content-range')}")
    print(f"    Bytes received: {len(r.content):,}\n")

    # ── Request 3: GET second 1 MB chunk ─────────────────────────
    r = client.get(
        f"https://{HOST}:{PORT}{PATH}",
        headers={"Range": "bytes=1048576-2097151"},
    )
    print(f"  GET {PATH}  Range: bytes=1048576-2097151")
    print(f"    Protocol      : {r.http_version}")
    print(f"    Status        : {r.status_code}")
    print(f"    Content-Range : {r.headers.get('content-range')}")
    print(f"    Bytes received: {len(r.content):,}\n")

print(f"  All 3 requests used the SAME TCP connection (HTTP/2 multiplexing).")
print(f"  In Wireshark: only ONE SYN packet visible — compare with TP1.")
print(f"  The HTTP headers and data are encrypted inside TLS Application Data.\n")
