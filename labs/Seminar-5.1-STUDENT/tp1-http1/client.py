"""
TP1 — HTTP/1.1 Client
======================
Demonstrates Range Requests (RFC 7233) over HTTP/1.1.

Each chunk is fetched with a NEW TCP connection — observe the TCP SYN
packets in Wireshark while this script runs.

Run: python client.py   (server must be running in another terminal)
"""

import http.client

HOST       = "localhost"
PORT       = 8080
PATH       = "/data"
CHUNK_SIZE = 1024 * 1024   # 1 MB per request

# ── Step 1: Probe request to discover the total file size ─────────
# Range: bytes=0-0 fetches only 1 byte, but the server returns the
# total size in the Content-Range header: "bytes 0-0/TOTAL".
conn = http.client.HTTPConnection(HOST, PORT)
conn.request("GET", PATH, headers={"Range": "bytes=0-0"})
resp = conn.getresponse()
resp.read()   # discard the 1-byte body
content_range = resp.getheader("Content-Range", "bytes 0-0/0")
file_size = int(content_range.split("/")[-1])
conn.close()

print(f"\n  File size : {file_size:,} bytes  ({file_size / 1024 / 1024:.1f} MB)")
print(f"  Chunk size: {CHUNK_SIZE:,} bytes  ({CHUNK_SIZE // 1024} KB)")
print(f"  Expected  : {-(-file_size // CHUNK_SIZE)} chunk(s)\n")
print(f"  Wireshark filter: tcp.port == {PORT}")
print(f"  Watch for TCP SYN packets — one per chunk below.\n")

# ── Step 2: Fetch chunks one by one ──────────────────────────────
chunk_num = 0
start     = 0

while start < file_size:
    end = min(start + CHUNK_SIZE - 1, file_size - 1)

    # Each iteration creates a BRAND NEW TCP connection.
    # HTTP/1.1 has no built-in multiplexing — every request is independent.
    conn = http.client.HTTPConnection(HOST, PORT)
    conn.request("GET", PATH, headers={"Range": f"bytes={start}-{end}"})
    resp = conn.getresponse()
    body = resp.read()
    conn.close()

    chunk_num += 1
    print(f"  Chunk {chunk_num}:")
    print(f"    Request  → GET {PATH}  Range: bytes={start}-{end}")
    print(f"    Response ← HTTP {resp.status}  Content-Range: {resp.getheader('Content-Range')}")
    print(f"    Received : {len(body):,} bytes")
    print(f"    TCP      : new SYN visible in Wireshark for each chunk\n")

    start = end + 1

print(f"  Done — {chunk_num} chunk(s) fetched, {file_size:,} bytes total.")
print(f"  In Wireshark: count the SYN packets — there should be {chunk_num + 1}.")
print(f"  (1 probe + {chunk_num} GET requests, each on its own TCP connection)\n")
