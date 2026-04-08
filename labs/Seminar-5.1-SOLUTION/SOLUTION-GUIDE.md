# Seminar 5.1 — Solution Guide (Instructor Only)

## Application Layer: HTTP/1.1, HTTP/2, HTTP/3

> **DO NOT DISTRIBUTE TO STUDENTS**

---

## Instructor Notes

### Timing guidance

| Phase | Recommended action |
|-------|--------------------|
| T+0   | Distribute student guide, run `setup.sh` / `setup.ps1` together on screen |
| T+10  | Students start TP1 code (TODO 1-5) |
| T+25  | All students should have server running → run `client.py` → start Wireshark |
| T+60  | Move to TP2 |
| T+75  | TP2 code — check everyone's CERT_FILE path is correct |
| T+110 | Move to TP3 |
| T+125 | TP3 client TODOs (HOST, PORT, ALPN) — common error: using "localhost" instead of "127.0.0.1" |
| T+155 | Comparative table + wrap-up discussion |

### Common student errors

| Error | Cause | Fix |
|-------|-------|-----|
| `PORT = ????` left as-is | Forgot to replace placeholder | Replace with an integer e.g. `8080` |
| `SyntaxError: invalid syntax` on `????` | `????` is not valid Python | Replace ALL `????` with real values |
| TP1 client prints `File size: 0` | `do_HEAD` not implemented in server | Server is correct — client uses `Range: bytes=0-0` probe; check server is running |
| TP2 client shows `HTTP/1.1` not `HTTP/2` | `httpx` missing `h2` package | Run `pip install httpx[http2]` or reinstall `requirements.txt` |
| TP3 client times out silently | `HOST = "localhost"` resolving to IPv6 `::1` | Change `HOST` to `"127.0.0.1"` |
| No QUIC packets in Wireshark (TP3) | Server not binding UDP | Check `config.quic_bind` TODO is complete |
| `ModuleNotFoundError: quart` | venv not activated | `source venv/bin/activate` (macOS/Linux) or `.\venv\Scripts\Activate.ps1` (Windows) |
| Data file not found | setup.sh/setup.ps1 not run | Run `./setup.sh` (or `.\setup.ps1`) from `Seminar-5.1/` |

---

## TP1 — Code Solutions

### TODO 1 — Port number
```python
PORT = 8080
```
Any integer > 1024 is valid. 8080 is conventional for HTTP development servers.

### TODO 2 — Range header name
```python
range_header = self.headers.get("Range")
```
The header is exactly `Range` (capital R). HTTP headers are case-insensitive per
RFC 7230, but Python's `http.server` preserves the case sent by the client.
`self.headers.get()` performs a case-insensitive lookup.

### TODO 3 — Parse start and end
```python
range_spec = range_header.replace("bytes=", "")
parts      = range_spec.split("-")
start      = int(parts[0])
end        = int(parts[1]) if parts[1] else file_size - 1
```
Walkthrough with `range_header = "bytes=0-1048575"`:
- `replace("bytes=", "")` → `"0-1048575"`
- `split("-")` → `["0", "1048575"]`
- `int(parts[0])` → `0`
- `int(parts[1])` → `1048575`

Edge case: `"bytes=5000000-"` → `parts[1]` is `""` (empty string, falsy) → use `file_size - 1`.

### TODO 4 — Status code
```python
self.send_response(206)
```
`206 Partial Content` is defined in RFC 7233 for range request responses.
Returning `200 OK` with a partial body would be incorrect — browsers would
assume the full file was received and stop requesting further chunks.

### TODO 5 — Content-Range header
```python
self.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
```
`file_size` is the variable computed by `os.path.getsize(VIDEO_PATH)` earlier.
The format `bytes START-END/TOTAL` is mandatory per RFC 7233 §4.2.

---

## TP1 — Wireshark Expected Observations

### Expected answers

**Question 1 — TCP handshakes**
The `client.py` output shows how many chunks were fetched (typically 5 for a ~5 MB
file with 1 MB chunks, plus 1 probe). Students should count 6 SYN packets in
Wireshark — one probe + one per chunk. Each SYN → SYN-ACK → ACK sequence is one
TCP connection.

**Question 2 — Range header value**
The client sends `bytes=0-1048575` for the first chunk, `bytes=1048576-2097151` for
the second, etc. Students can verify by comparing the Wireshark `Range` header with
the client's printed output. Both must match exactly.

**Question 3 — Security risk**
Yes, the filename and all header values are readable in plain text.
Risk: an attacker on the same network (or a compromised router) can:

- See which files are being accessed (`/data`, but in production could be `/invoice_2024.pdf`)
- Read all HTTP request/response metadata including byte offsets
- Potentially modify the response (inject malicious content)

**Question 4 — Content-Range header**
Format: `bytes 0-1048575/5242880` (for a ~5 MB data.txt file).
Students should confirm the format matches their TODO 5 implementation.

**Question 5 — Multiple connections**
Correct — every chunk request appears as a separate SYN in Wireshark.
The `client.py` explicitly creates a new `HTTPConnection` object for each chunk,
demonstrating the stateless, connection-per-request nature of HTTP/1.1.

---

## TP2 — Code Solutions

### TODO 1 — Certificate filename
```python
CERT_FILE = os.path.join(CERTS_DIR, "server.crt")
```
The `.crt` file is the public certificate sent to the browser during the TLS handshake.

### TODO 2 — Key filename
```python
KEY_FILE = os.path.join(CERTS_DIR, "server.key")
```
The `.key` file is the private key kept secret on the server. It must never be shared.

### TODO 3 — ALPN token
```python
HTTP2_ALPN_TOKEN = "h2"
```
`"h2"` is the IANA-registered ALPN Protocol ID for HTTP/2 (RFC 7540, §11.1).
This value is printed at server startup so students know what to search for in
the Wireshark ClientHello ALPN extension.
Hypercorn sets ALPN to `["h2", "http/1.1"]` internally when the `h2` package
is installed — students observe this in Wireshark, not configure it directly.

### TODO 4 — Port
```python
config.bind = [f"0.0.0.0:{PORT}"]   # → "0.0.0.0:8443"
```
Port 8443 is a common alternative to 443 for HTTPS in development (no root required).

### TODO 5 — TLS configuration
```python
config.certfile = CERT_FILE
config.keyfile  = KEY_FILE
```
**Important for instructors:** `config.ssl` (passing an `ssl.SSLContext` directly)
is NOT supported by Hypercorn — it is silently ignored, causing the server to start
in plain HTTP mode and the browser to return `ERR_SSL_PROTOCOL_ERROR`.
Always use `config.certfile` and `config.keyfile`.

---

## TP2 — Wireshark Expected Observations

### Expected answers

**Question 1 — ALPN in ClientHello**
The Python `httpx` client proposes `h2` and `http/1.1` (in that order).
In Wireshark: TLS → Extension: application_layer_protocol_negotiation →
ALPN Protocol: h2, ALPN Protocol: http/1.1

**Question 2 — Maximum TLS version in ClientHello**
`TLS 1.3` (shown as version 0x0304 in the raw bytes). The "legacy version" field
may show 1.2 for compatibility — this is normal; the actual version is in the
`supported_versions` extension.

**Question 3 — Server-selected ALPN**
`h2` — matching the first entry in the student's `ALPN_PROTOCOLS` list.

**Question 4 — Negotiated TLS version**
TLS 1.3 (if students set `TLSv1_3`). Visible in the ServerHello
`supported_versions` extension.

**Question 5 — Certificate issuer**
The issuer is `CN=localhost, O=Network101Lab, C=FR` — the values used in
`setup.sh`'s `openssl` command. The browser warns because this certificate
was not signed by a trusted CA (e.g. Let's Encrypt, DigiCert). Browsers
ship with a built-in list of trusted CAs; a self-signed cert is not on it.

**Question 6 — Application Data content**
The payload shows only `Application Data (N bytes)` — no readable content.
Unlike TP1, the HTTP/2 frames (including headers and file content) are fully
encrypted. An attacker can see that an encrypted connection exists but cannot
read the URL, headers, or file content.

**Question 7 — TCP connection count**
**1 TCP connection** for the entire session. HTTP/2 streams (numbered 1, 3, 5, …)
multiplex all requests inside this single TCP connection.
Compare with TP1: 6+ connections for the same data transfer.

---

## TP3 — Code Solutions

### TODO 1 — Certificate files
```python
CERT_FILE = os.path.join(CERTS_DIR, "server.crt")
KEY_FILE  = os.path.join(CERTS_DIR, "server.key")
```
Identical to TP2. QUIC uses TLS certificates in the same X.509 format.
The difference is that TLS runs *inside* QUIC, not on top of TCP.

### TODO 2 — QUIC port
```python
QUIC_PORT = 4433
```
Port 443 is the HTTP/3 standard but requires root privileges on macOS/Linux.
4433 is a common convention for development. Any port in range 1024-65535 works.

### TODO 3 — Idle timeout
```python
IDLE_TIMEOUT = 30
```
QUIC connections are closed after `IDLE_TIMEOUT` seconds of inactivity.
This is a QUIC-level concept (unlike TCP which has OS-level keepalive).
In Wireshark, after 30s of silence, the connection simply disappears —
there is no FIN or RST packet (QUIC uses a CONNECTION_CLOSE frame if
the connection is explicitly closed).

### TODO 4 — ALPN for HTTP/3
```python
ALPN_PROTOCOLS = H3_ALPN   # H3_ALPN = ["h3"]
```
`"h3"` is the IANA-registered ALPN Protocol ID for HTTP/3 (RFC 9114, §5.5.1).
`H3_ALPN` is a convenience constant exported by the `aioquic` library.

---

## TP3 — Client Code Solutions

### TODO 1 — HOST

```python
HOST = "127.0.0.1"
```

**Not** `"localhost"`. On many systems `localhost` resolves to `::1` (IPv6) first.
UDP has no "connection refused" signal, so a packet sent to an unbound IPv6 address
is silently dropped — QUIC times out without any error message.

### TODO 2 — PORT

```python
PORT = 8443
```

Must match the UDP port in `server.py` (`config.quic_bind`).

### TODO 3 — ALPN

```python
ALPN = H3_ALPN
```
`H3_ALPN` is imported at the top of `client.py` from `aioquic.h3.connection`.
It equals `["h3"]`. Students should not type the string literal — using the
constant ensures consistency with the library.

---

## TP3 — Wireshark Expected Observations

### Expected answers

**Question 1 — Transport protocol**
UDP. In the packet details: `Internet Protocol → User Datagram Protocol`.
There is no SYN, SYN-ACK, or ACK because UDP has no connection establishment.
QUIC manages its own connection state (Connection IDs, sequence numbers).

**Question 2 — TLS in QUIC Initial**
Yes — the TLS ClientHello is embedded inside the QUIC Initial packet.
In TP2, the TCP handshake (3 packets) happened first, THEN the TLS ClientHello.
In TP3, the first UDP packet already contains the TLS ClientHello.
This is why QUIC is called "1-RTT" — TLS starts in the very first packet.

**Question 3 — ALPN in QUIC Initial**
`h3`. The ALPN extension is visible inside the embedded TLS ClientHello.
Students should look at: QUIC → Payload → TLS → ClientHello →
Extension: application_layer_protocol_negotiation → `h3`

**Question 4 — Round trips before first data**
Students should count 2 QUIC Initial packets (one each direction) = 1 RTT before
HTTP/3 data flows. Compare:

- HTTP/1.1: 1.5 RTT (SYN+SYN-ACK=1 RTT, then request)
- HTTP/2: 1.5 RTT (TCP) + 1 RTT (TLS 1.3) = 2.5 RTT total
- HTTP/3: 1 RTT (QUIC Initial contains TLS ClientHello)

For a returning connection with 0-RTT data: 0 RTT (client sends data immediately).

**Question 5 — QUIC Connection ID**
The Connection ID is visible in the QUIC packet header in Wireshark.
It is a QUIC-level identifier, independent of IP address and port.
Role: allows QUIC connections to survive network changes (e.g. switching from
Wi-Fi to 4G). TCP connections are identified by the 4-tuple (src IP, src port,
dst IP, dst port) and break on network change. QUIC connections persist because
the server recognises the Connection ID regardless of which IP/port the client
is now using.

**Question 6 — UDP firewall block**
HTTP/3 cannot be established — the Python client would time out with a
`ConnectionError`. In a real browser, it falls back to HTTP/2 or HTTP/1.1 over
TCP (Alt-Svc fallback). Result: HTTP/3 is transparent to users but may not be
usable on all networks. Recommendation: ensure HTTP/2 is properly configured
as fallback.

---

## TP4 — Code Solutions

### TODO 1 — Port number
```python
PORT = 50051
```
50051 is the conventional gRPC development port (analogous to 8080 for HTTP).
Any port > 1024 is technically valid.

### TODO 2 — Build a MetricUpdate message
```python
update = metrics_pb2.MetricUpdate(
    timestamp    = datetime.datetime.now().isoformat(timespec="seconds"),
    bandwidth_mb = round(random.uniform(10.0, 100.0), 2),
    latency_ms   = round(random.uniform(1.0, 50.0), 2),
    packet_loss  = random.randint(0, 5),
)
```
`metrics_pb2.MetricUpdate` is a class generated by `grpc_tools.protoc` from
`metrics.proto`. Each field name matches a field defined in the `.proto` file.
Protobuf performs type checking — passing a string where an `int32` is expected
raises a `TypeError` immediately.

### TODO 3 — Yield the update
```python
yield update
```
The `StreamMetrics` method is a Python generator. Each `yield` sends one
`MetricUpdate` message to the client immediately via the gRPC framework.
The HTTP/2 DATA frame is sent after every `yield` — students can confirm this
by watching DATA frames appear in Wireshark one per second.

Common error: students write `return update` instead of `yield update`.
`return` ends the stream after one message; `yield` keeps it open.

### TODO 4 — Register the servicer
```python
metrics_pb2_grpc.add_MetricsServiceServicer_to_server(MetricsServicer(), server)
```
`grpc_tools` generates one registration function per service defined in the
`.proto` file. The naming convention is always:
`add_<ServiceName>Servicer_to_server`. Here the service is `MetricsService`.

---

## TP4 — Client Code Solutions

### TODO 1 — Port number (client)
```python
PORT = 50051
```
Must match the server. Common error: student uses a different port on one side.

### TODO 2 — Open an insecure channel
```python
channel = grpc.insecure_channel(f"{HOST}:{PORT}")
```
`grpc.insecure_channel` creates an unencrypted HTTP/2 channel — traffic is
visible in plain HTTP/2 frames in Wireshark (though payload is protobuf binary).
In production, use `grpc.secure_channel` with TLS credentials.

### TODO 3 — Build request and call RPC
```python
request = metrics_pb2.MetricsRequest(client_id="student-1")
stream  = stub.StreamMetrics(request)
```
`stub.StreamMetrics(request)` is a blocking call that returns an iterator.
The iterator yields `MetricUpdate` objects as the server sends them — the
`for update in stream:` loop blocks until each message arrives.
The RPC name `StreamMetrics` must match exactly the name in `metrics.proto`.

---

## TP4 — Wireshark Expected Answers

**Question 1 — TCP connection count**
Exactly **1** TCP 3-way handshake for the entire 10-message stream.
All 10 `MetricUpdate` messages travel over the same persistent HTTP/2 connection.
Compare with TP1 where each of the 5 chunks opened a new TCP connection.
This confirms that gRPC inherits HTTP/2's connection multiplexing.

**Question 2 — Payload readability**
Students cannot read metric values in the TCP stream — the content appears
as binary data. gRPC uses **Protocol Buffers** (protobuf) for serialization.
Unlike TP1 where Range headers and file content were plain text, protobuf
encodes field numbers and values in a compact binary wire format.

**Question 3 — HTTP method and :path**
gRPC always uses `POST` as the HTTP method.
The `:path` pseudo-header is `/MetricsService/StreamMetrics` — it encodes
the service name and method name from the `.proto` file, separated by `/`.
This is the gRPC wire format convention (defined in the gRPC HTTP/2 spec).

**Question 4 — HTTP/2 framing vs protobuf payload**
Wireshark knows the HTTP/2 protocol natively and can decode framing headers
(HEADERS frames, DATA frames, stream IDs, flags) because HTTP/2 is a standardised
IETF protocol with a public specification.
However, the protobuf payload inside DATA frames is application-specific binary
data. Without the `.proto` schema, Wireshark cannot know which bytes represent
which fields. Wireshark has a gRPC dissector plugin that *can* decode protobuf
if given the `.proto` file, but this is not enabled by default.

---

## Comparative Table — Expected Answers

| Criterion | HTTP/1.1 | HTTP/2 | HTTP/3 | gRPC |
|-----------|----------|--------|--------|------|
| Transport protocol | TCP | TCP | UDP (QUIC) | TCP |
| Visible TCP SYN in Wireshark? | Yes (many) | Yes (one) | No | Yes (one) |
| TCP connections (1 data transfer) | Many (5-6+) | 1 | 0 (UDP) | 1 |
| Encryption | None | TLS 1.3 | TLS 1.3 (built-in QUIC) | None (in this lab) |
| Payload readable in Wireshark? | Yes (plain text) | No (TLS) | No (TLS) | No (binary protobuf) |
| ALPN / protocol token | None | `h2` | `h3` | None (insecure) |
| Round trips before first data | 1.5 RTT | 2.5 RTT | 1 RTT | 1.5 RTT |
| Blocked by UDP firewall? | No | No | Yes | No |
| Risk of man-in-the-middle attack | High | Low | Low | High (no TLS here) |

---

## Wrap-up Questions — Expected Answers

**Question 1 — TP1 interception risks**
An attacker on the same network can observe:

- The exact file path (`/data`) and server hostname
- All request headers: User-Agent, Accept, Range byte positions
- All response headers: Content-Length, Content-Type, server software version
- Potentially the entire file content (depending on whether they can reassemble TCP)
- Timing of requests (can infer what the user is downloading)

**Question 2 — TLS 1.2 vs 1.3**
With TLS 1.2, the handshake requires 2 RTTs instead of 1 RTT.
TLS 1.2 also supports weaker cipher suites (RC4, DES, export-grade) though
modern clients won't negotiate them. Students might see different cipher suites
in the Wireshark ServerHello.

**Question 3 — Why QUIC integrates TLS**
HTTP/1.1 and HTTP/2 were designed to run on TCP, which provides a reliable
byte stream. TLS was then layered on top of this byte stream as a separate
protocol. QUIC was designed from scratch knowing that TLS is required, so
TLS record processing is integrated into the QUIC handshake state machine.
This avoids the impedance mismatch between TCP's byte stream and TLS's record
boundaries, and eliminates a full round trip.

**Question 4 — Slow transfers on corporate network**
HTTP/3 is affected because QUIC runs on UDP. The firewall blocks UDP → QUIC fails.
Recommendation:

1. Ensure your server supports HTTP/2 as fallback (Hypercorn does this automatically)
2. Verify the `Alt-Svc` header is sent so clients know HTTP/3 is available
3. Contact the network team to allow UDP port 443 outbound if needed
4. Monitor fallback rates to quantify the impact

**Question 5 — gRPC is not HTTP/2 + JSON**
The statement is wrong in two ways:
- gRPC uses **Protocol Buffers** (protobuf), not JSON. Protobuf is a binary
  serialization format defined by a `.proto` schema.
- Advantages over JSON: smaller message size (no field names on the wire),
  faster serialization/deserialization, strict typing enforced by the schema,
  and backward-compatible schema evolution.

**Question 6 — gRPC on port 443**
Changes needed:
1. Add TLS to the gRPC server: use `grpc.ssl_server_credentials()` instead of
   `add_insecure_port` — gRPC over TLS on port 443 is the standard production setup.
2. Change the client to `grpc.secure_channel()` with appropriate credentials.
3. Configure the server to bind on port 443 (requires root or `CAP_NET_BIND_SERVICE`
   on Linux, or use a reverse proxy like nginx or Envoy on port 443).
