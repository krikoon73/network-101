# Seminar 5.1 — Student Guide

## Application Layer: HTTP/1.1, HTTP/2, HTTP/3

---

## Introduction

A web server serving a large file is one of the most common applications on the
Internet today. Behind this simple use case lies a rich stack of protocols that
have evolved significantly over the last decade.

In this lab you will run three versions of the same file server — one for each
generation of HTTP — and observe how the **network and security behaviour**
differs in each case using Wireshark.

**Focus:** Transport layer (TCP vs UDP) and security (TLS encryption, QUIC).
Each TP comes with a ready-to-run Python client that prints exactly what happens
on the wire.

### Protocol overview

```text
TP1  HTTP/1.1 ──→  TCP  ──→ IP             (no encryption)
TP2  HTTP/2   ──→  TLS  ──→ TCP ──→ IP
TP3  HTTP/3   ──→  QUIC (TLS built-in) ──→ UDP ──→ IP
TP4  gRPC     ──→  HTTP/2 ──→ TCP ──→ IP   (no encryption, binary payload)
```

### Time budget

| Phase | TP1 | TP2 | TP3 | TP4 |
| ----- | --- | --- | --- | --- |
| Code (TODOs) | 15 min | 15 min | 15 min | 20 min |
| Wireshark | 35 min | 35 min | 35 min | 25 min |
| **Total** | **50 min** | **50 min** | **50 min** | **45 min** |

---

## Prerequisites

- Python 3.10+
- Wireshark
- All three TPs share a single virtual environment

---

## Setup (do this once before TP1)

Open a terminal in the `Seminar-5.1/` directory.

**macOS / Linux:**

```bash
chmod +x setup.sh
./setup.sh
```

**Windows (PowerShell):**

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\setup.ps1
```

`setup.sh` / `setup.ps1` will:

1. Create a Python virtual environment in `venv/`
2. Install all required packages (`quart`, `hypercorn`, `aioquic`, `httpx`, …)
3. Generate a self-signed TLS certificate in `certs/` using `openssl`
4. Generate a ~5 MB data file in `assets/data.txt`

**Activate the virtual environment before every TP:**

```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

---

## TP1 — HTTP/1.1: TCP and Unencrypted Traffic

**Duration:** 50 min (15 code + 35 Wireshark)

### Background

HTTP/1.1 is the original web protocol (RFC 2616, 1999). It runs directly on top of
TCP with no encryption. Every HTTP request requires:

1. A **TCP 3-way handshake** (SYN → SYN-ACK → ACK) to open a connection
2. The HTTP request and response
3. A TCP connection close (FIN/ACK)

When a client downloads a large file, it does not fetch the entire file at once.
Instead it sends multiple requests using a `Range` header, each fetching a small
portion:

```http
GET /data HTTP/1.1
Range: bytes=0-1048575        ← "give me bytes 0 to 1 MB"

HTTP/1.1 206 Partial Content
Content-Range: bytes 0-1048575/5242880
```

This means Wireshark will show **many TCP connections** for a single download —
one per chunk request. And because there is no encryption, **all content is readable
in plain text** on the wire.

### Step 1 — Complete the code (15 min)

Open `tp1-http1/server.py` in your editor.

Find and complete the 5 TODO sections:

| TODO | What to do |
| ---- | ---------- |
| **TODO 1** | Choose a port number (integer > 1024, e.g. `8080`) |
| **TODO 2** | Name the HTTP header that carries the byte range request |
| **TODO 3** | Parse start/end positions from the header value |
| **TODO 4** | Use the correct HTTP status code for partial content |
| **TODO 5** | Build the `Content-Range` response header |

**Hints:**
- TODO 2: the header is named after the concept of "requesting a range"
- TODO 4: status 200 = full content, status 206 = partial content
- TODO 5: the format is `bytes START-END/TOTAL` where TOTAL is the full file size

### Step 2 — Start the server

```bash
cd tp1-http1
python server.py
```

Expected output:

```
  HTTP/1.1 server started
  URL     : http://localhost:8080
  Wireshark filter: tcp.port == 8080
```

In a **second terminal** (with the venv activated), run the client:

```bash
python client.py
```

The client fetches the file in 1 MB chunks and prints each request/response.

### Step 3 — Wireshark observation (35 min)

#### 3.1 — Start a capture

1. Open Wireshark
2. Select your **loopback interface**:
   - macOS: `lo0`
   - Linux: `lo`
3. In the filter bar, type: `tcp.port == 8080`
4. Click the blue shark fin to start capturing
5. Run `python client.py` in the second terminal

#### 3.2 — Observe the TCP handshake

In the packet list, look for packets with flags `[SYN]`, `[SYN, ACK]`, `[ACK]`.

> **Question 1:** How many TCP 3-way handshakes can you count while `client.py`
> runs? The client prints the number of chunks it fetched — does it match?

Each handshake corresponds to one HTTP request for one chunk of the file.

#### 3.3 — Read the HTTP request in plain text

Click on a packet that shows `GET /data HTTP/1.1` in the Info column.
In the lower pane, expand **Hypertext Transfer Protocol**.

> **Question 2:** What is the value of the `Range` header in this request?
> (e.g. `bytes=0-XXXXX`). Does it match what `client.py` printed?

> **Question 3:** Can you read the filename (`/data`) and the `Range` header
> without any decryption key? What security risk does this represent?

#### 3.4 — Read the HTTP response

Click on the corresponding `HTTP/1.1 206 Partial Content` response packet.

> **Question 4:** What is the value of the `Content-Range` header in the response?
> Does it match the format `bytes START-END/TOTAL` that you implemented?

#### 3.5 — Multiple connections

Look at the `client.py` output. Notice it says "new TCP connection" for each chunk.

> **Question 5:** In Wireshark, confirm each chunk request has its own SYN packet.
> What does this tell you about HTTP/1.1 connection management?

#### Fill in the comparative table (row: HTTP/1.1)

At the end of the guide, find the **Comparative Table** and fill in the HTTP/1.1 row.

---

## TP2 — HTTP/2: TLS and a Single TCP Connection

**Duration:** 50 min (15 code + 35 Wireshark)

### Background

HTTP/2 (RFC 7540, 2015) brings two major improvements visible at the network level:

**1. Multiplexing:** Multiple HTTP requests share a single TCP connection.
Instead of opening a new TCP connection per request (HTTP/1.1), HTTP/2 sends
all requests in parallel over one connection using a binary framing layer.
Result: far fewer TCP handshakes.

**2. Mandatory TLS (in practice):** All major browsers only support HTTP/2 over TLS.
This means traffic is encrypted — Wireshark can see the TLS handshake but NOT
the content of HTTP/2 frames.

#### The TLS handshake (what you will see in Wireshark)

```
Browser                        Server
  |──── TCP SYN ──────────────→|
  |←─── TCP SYN-ACK ──────────|
  |──── TCP ACK ──────────────→|   ← TCP connection established
  |                            |
  |──── TLS ClientHello ──────→|   ← Browser proposes: TLS version,
  |                            |     cipher suites, ALPN ["h2","http/1.1"]
  |←─── TLS ServerHello ──────|   ← Server selects: TLS 1.3, cipher, ALPN "h2"
  |←─── Certificate ──────────|   ← Server sends its certificate
  |←─── Finished ─────────────|
  |──── Finished ─────────────→|   ← TLS handshake complete
  |                            |
  |══════ HTTP/2 frames ══════ |   ← Encrypted, not readable in Wireshark
```

#### ALPN — Application-Layer Protocol Negotiation

ALPN is a TLS extension. During the ClientHello, the browser declares which
application protocols it supports. The server replies with its choice in the
ServerHello. For HTTP/2, the negotiated token is `"h2"` (defined in RFC 7540).

This negotiation happens **inside the TLS handshake** — no extra round trip.

### Step 1 — Complete the code (15 min)

Open `tp2-http2/server.py` in your editor.

Find and complete the 5 TODO sections:

| TODO | What to do |
|------|-----------|
| **TODO 1** | Set the certificate filename (`server.crt`) |
| **TODO 2** | Set the private key filename (`server.key`) |
| **TODO 3** | Set the ALPN token for HTTP/2 (check RFC 7540 §11 or search online) |
| **TODO 4** | Set the port in `config.bind` (e.g. `8443`) |
| **TODO 5** | Point `config.certfile` and `config.keyfile` to the constants you defined |

**Hints:**

- TODOs 1 & 2: both files are in `../certs/` — check what `setup.sh` generated
- TODO 3: the ALPN token for HTTP/2 is a two-character string starting with `h`
- TODO 5: use the variable names defined at the top of the file, not string literals

### Step 2 — Start the server

```bash
cd tp2-http2
python server.py
```

Expected output:

```
  HTTP/2 server started
  URL     : https://localhost:8443
  Wireshark filter: tls
```

In a **second terminal** (with the venv activated), run the client:

```bash
python client.py
```

The client prints the HTTP version (`HTTP/2`) and Content-Range for each request.
The server uses a self-signed certificate; the client uses `verify=False` so no
browser trust store is involved.

### Step 3 — Wireshark observation (35 min)

#### 3.1 — Start a capture

1. Open Wireshark, select the loopback interface (`lo0` / `lo`)
2. Filter: `tls`
3. Start capture, then run `python client.py` in the second terminal

#### 3.2 — Observe the TLS ClientHello

Click on the packet labelled `TLSv1.3 Client Hello` in the Info column.
Expand: **Transport Layer Security → TLSv1.3 Record Layer → Handshake Protocol: Client Hello**

Look for the **Extension: application_layer_protocol_negotiation** field.

> **Question 1:** What protocols does the Python client propose in the ALPN extension?
> (you should see both `h2` and `http/1.1`)

> **Question 2:** What is the maximum TLS version proposed by the client?

#### 3.3 — Observe the TLS ServerHello

Click on the `Server Hello` packet.

> **Question 3:** Which ALPN protocol did the server select? Does it match what
> you configured in TODO 3?

> **Question 4:** Which TLS version was negotiated? Does it match your TODO 2 choice?

#### 3.4 — Find the server certificate

Click on the `Certificate` packet.
Expand: **Transport Layer Security → Certificate**

> **Question 5:** Who issued the certificate (Issuer field)?
> Why does the browser show a security warning for this certificate?

#### 3.5 — Try to read the video content

Click on any `Application Data` packet (after the handshake).

> **Question 6:** Can you read the HTTP requests or the file content in the packet
> payload? Compare with TP1. What is the security benefit?

#### 3.6 — Count TCP connections

Use the filter `tcp.flags.syn == 1 && tcp.port == 8443` to show only TCP SYN packets.

> **Question 7:** How many TCP connections were opened during the entire session?
> Compare with TP1. Why is the number so much lower?

#### Fill in the comparative table (row: HTTP/2)

---

## TP3 — HTTP/3: QUIC over UDP

**Duration:** 50 min (15 code + 35 Wireshark)

### Background

HTTP/3 (RFC 9114, 2022) replaces TCP with **QUIC** as the transport protocol.
QUIC runs over **UDP** and integrates TLS 1.3 natively — it is not an optional
layer but a fundamental part of the protocol.

#### Why UDP instead of TCP?

TCP has a fundamental limitation: **Head-of-Line (HoL) blocking**. If one TCP
segment is lost, all subsequent segments in the stream must wait for
retransmission — even if they belong to independent HTTP requests.

QUIC solves this by multiplexing streams at the QUIC layer. Each stream has
its own flow control, so a lost packet only blocks the one stream it belongs to.

#### How HTTP/3 is negotiated: the Alt-Svc mechanism

Unlike HTTP/1.1 → HTTP/2 (negotiated inside the TLS handshake via ALPN),
HTTP/3 uses a different upgrade mechanism called **Alt-Svc**:

```
Browser                         Server (TCP 8443)
  |──── TCP SYN ───────────────→|
  |──── TLS + HTTP/2 request ──→|
  |←─── HTTP/2 response ────────|  ← includes: Alt-Svc: h3=":8443"; ma=86400
  |                              |
  |  (browser stores Alt-Svc)   |
  |                              |
  |──── QUIC Initial (UDP) ────→|  ← next request uses HTTP/3 on UDP!
  |←─── QUIC response ──────────|
  |══════ HTTP/3 (QUIC/UDP) ════|
```

The server listens on **both TCP and UDP** on port 8443.
This is the standard way HTTP/3 is deployed on real websites.

#### The QUIC handshake (what you will see in Wireshark after the upgrade)

```text
Browser                        Server (UDP 8443)
  |──── QUIC Initial ─────────→|   ← Contains TLS ClientHello inside
  |                            |     NO TCP SYN first!
  |←─── QUIC Initial ─────────|   ← TLS ServerHello + Certificate
  |←─── QUIC Handshake ───────|   ← TLS Finished
  |──── QUIC Handshake ───────→|
  |                            |
  |══════ QUIC 1-RTT ═════════ |   ← Encrypted HTTP/3 frames
```

### Step 1 — Complete the server code (15 min)

Open `tp3-http3/server.py` in your editor.

Find and complete the 6 TODO sections:

| TODO | What to do |
| ---- | ---------- |
| **TODO 1** | Set the certificate filename (same as TP2) |
| **TODO 2** | Set the private key filename (same as TP2) |
| **TODO 3** | Set the ALPN token for HTTP/3 (check RFC 9114 §7 — what comes after `h2`?) |
| **TODO 4** | Set the TCP port in `config.bind` (same as TP2: `8443`) |
| **TODO 5** | Point `config.certfile` and `config.keyfile` to the constants above |
| **TODO 6** | Set `config.quic_bind` to the same address as `config.bind` |

**Hints:**

- TODO 3: the HTTP/3 ALPN token follows the same naming pattern as `"h2"`
- TODO 6: read the comment in the code carefully — it explains what `quic_bind` does

### Step 2 — Start the server

```bash
cd tp3-http3
python server.py
```

Expected output:

```
  HTTP/3 server started
  TCP  port 8443 → HTTP/1.1 + HTTP/2 (initial connection)
  UDP  port 8443 → HTTP/3 / QUIC     (after Alt-Svc upgrade)
  In a second terminal, run:  python client.py
  Wireshark filter: quic  (or: udp.port == 8443)
```

### Step 3 — Complete the client code and run it (15 min)

Open `tp3-http3/client.py` in your editor. Find and complete the 3 TODO sections:

| TODO | What to do |
| ---- | ---------- |
| **TODO 1** | Set `HOST` — use `"127.0.0.1"` (not `"localhost"`) |
| **TODO 2** | Set `PORT` — same UDP port as the server |
| **TODO 3** | Set `ALPN` — replace `????` with `H3_ALPN` (the imported constant) |

**Why `"127.0.0.1"` and not `"localhost"`?**
On many systems `localhost` resolves to `::1` (IPv6) first. UDP has no
"connection refused" signal, so a packet sent to an unbound IPv6 port is
silently dropped — QUIC times out without any error message. Using the
explicit IPv4 address avoids this ambiguity.

Once the TODOs are filled in, run the client in a **second terminal**:

```bash
python client.py
```

Expected output (abbreviated):

```
  Connecting to 127.0.0.1:8443 via QUIC (UDP) ...
  ALPN      : ['h3']
  Transport : UDP  — no TCP SYN in Wireshark

  HEAD /data
    Status    : 200
    File size : 5,242,880 bytes

  GET /data  Range: bytes=0-1048575
    Status        : 206
    Content-Range : bytes 0-1048575/5242880
    Bytes received: 1,048,576

  Transport confirmed: UDP/QUIC — no TCP used.
```

### Step 4 — Wireshark observation (35 min)

#### 4.1 — Capture QUIC traffic in Wireshark

1. Open Wireshark, select the loopback interface (`lo0` / `lo`)
2. Filter: `quic`
3. Start capture, then run `python client.py` in the second terminal

Click on any QUIC packet and look at the protocol stack in the details pane.

> **Question 1:** Which transport protocol carries QUIC packets — TCP or UDP?
> What does this mean for connection setup (SYN/SYN-ACK/ACK)?

#### 4.2 — Observe the QUIC Initial packet

Click on the first `QUIC IETF` packet labelled `Initial` in the Info column.
Expand: **QUIC IETF → Payload → TLS 1.3 → Handshake → ClientHello**

> **Question 2:** Is the TLS ClientHello inside the first UDP packet?
> How does this compare to TP2 where the TLS ClientHello came after a TCP handshake?

> **Question 3:** Find the ALPN extension inside the QUIC Initial packet. What protocol token does it contain? Is it `h2` or `h3`?

#### 4.3 — Confirm transport in the client output

Look at the last line printed by `client.py`:

```text
  Transport confirmed: UDP/QUIC — no TCP used.
```

> **Question 4:** Count the QUIC Initial packets in Wireshark. How many round trips
> happened before the first HTTP/3 data was received? Compare with TP2 (2.5 RTT).

#### 4.4 — The Connection ID concept

In the packet details, find the **Destination Connection ID** field in any QUIC packet.

> **Question 5:** The QUIC Connection ID is a concept that has no equivalent in TCP.
> What role does it play? (hint: think about a mobile phone switching between Wi-Fi
> and 4G — what happens to a TCP connection vs a QUIC connection?)

#### 4.5 — Firewall consideration

UDP is often blocked by enterprise firewalls more aggressively than TCP port 443.

> **Question 6:** A company's firewall blocks all UDP traffic except DNS (port 53).
> What happens to HTTP/3? What does the client fall back to, and why?

#### Fill in the comparative table (row: HTTP/3)

---

## TP4 — gRPC: Binary Streaming over HTTP/2

**Duration:** 45 min (20 code + 25 Wireshark)

### Background

gRPC is a modern Remote Procedure Call (RPC) framework developed by Google.
It is widely used in microservices and in network management protocols such as
gNMI (streaming telemetry from routers and switches).

Unlike the REST APIs you have seen in TP1 and TP2, gRPC has two key differences:

**1. Protocol Buffers (protobuf):** Messages are serialized in a compact binary
format defined in a `.proto` file — not JSON, not plain text. This makes payloads
smaller and faster to parse, but **not human-readable** in Wireshark.

**2. Native streaming:** gRPC defines four RPC patterns. In this TP you use
**server-side streaming**: the client sends one request and the server sends back
a continuous stream of responses over the same HTTP/2 connection.

```text
Protocol stack:  gRPC → HTTP/2 → TCP → IP   (no TLS in this lab)
```

#### How server-side streaming works

```text
Client                    Server
  |                          |
  |── MetricsRequest ───────→|
  |                          |
  |←── MetricUpdate #1 ──────|   (t + 1 s)
  |←── MetricUpdate #2 ──────|   (t + 2 s)
  |        ...               |
  |←── MetricUpdate #10 ─────|   (t + 10 s)
  |                          |
  |── stream closed ─────────|
```

All 10 messages travel over **the same single TCP connection** — no new
TCP handshake per message. Compare this with TP1 where each chunk required
a brand new TCP connection.

#### About the generated stubs

The `.proto` file is compiled into Python by the setup script. It produces:

- `metrics_pb2.py` — message classes (`MetricsRequest`, `MetricUpdate`)
- `metrics_pb2_grpc.py` — service classes (`MetricsServiceServicer`, `MetricsServiceStub`)

**Do not modify these generated files.** You only edit `server.py` and `client.py`.

### Step 1 — Complete the server (10 min)

Open `tp4-grpc/server.py` in your editor.

Find and complete the 4 TODO sections:

| TODO | What to do |
| ---- | ---------- |
| **TODO 1** | Choose the gRPC port number |
| **TODO 2** | Build a `MetricUpdate` protobuf message with simulated values |
| **TODO 3** | `yield` the update to stream it to the client |
| **TODO 4** | Register the servicer with the gRPC server |

**Hints:**
- TODO 1: the conventional gRPC port is `50051`
- TODO 2: use `metrics_pb2.MetricUpdate(field=value, ...)` — all four fields required
- TODO 3: in a generator function, `yield x` sends `x` to the caller immediately
- TODO 4: the helper function name follows the pattern `add_<ServiceName>Servicer_to_server`

### Step 2 — Complete the client (10 min)

Open `tp4-grpc/client.py` in your editor.

| TODO | What to do |
| ---- | ---------- |
| **TODO 1** | Match the port number to the server |
| **TODO 2** | Open an insecure gRPC channel to the server |
| **TODO 3** | Build the request and call the streaming RPC |

**Hints:**
- TODO 2: `grpc.insecure_channel("host:port")` — no TLS, traffic visible in Wireshark
- TODO 3: the RPC method name matches the `.proto` definition exactly

### Step 3 — Start the server and client

```bash
cd tp4-grpc
python server.py
```

Expected output:

```
  gRPC Metrics server started
  Listening on: grpc://localhost:50051  (insecure / no TLS)
  Wireshark filter: tcp.port == 50051
```

In a **second terminal** (with venv activated):

```bash
python client.py
```

The client will print 10 metric updates, one per second, then exit.

### Step 4 — Wireshark observation (25 min)

#### 4.1 — Start a capture

1. Open Wireshark, select the loopback interface (`lo0` / `lo`)
2. In the filter bar, type: `tcp.port == 50051`
3. Start capture, then run `python client.py` in the second terminal

#### 4.2 — Count TCP connections

Look for TCP SYN packets in the packet list.

> **Question 1:** How many TCP 3-way handshakes can you count for the entire
> 10-message stream? Compare with TP1 (one handshake per chunk).
> What does this tell you about how gRPC uses HTTP/2?

#### 4.3 — Read the raw content

In Wireshark, right-click any packet → **Follow → TCP Stream**.

> **Question 2:** Can you read the metric values (bandwidth, latency) in plain text?
> How does this compare to TP1? What binary format is used instead?

Close the TCP stream window.

#### 4.4 — Identify the gRPC method call

In the packet list, look for a packet labelled `HEADERS` near the start of the stream.
Click it and expand: **HyperText Transfer Protocol 2 → Header Block Fragment**.

> **Question 3:** What is the value of the `:path` pseudo-header?
> What HTTP method (`:method`) does gRPC use for all calls?

#### 4.5 — Observe DATA frames

Look for packets labelled `DATA` in the packet list. Click one and expand
**HyperText Transfer Protocol 2** then look for **GRPC Message** if Wireshark
detects it (filter `grpc` may help).

> **Question 4:** gRPC uses HTTP/2 as its transport, just like TP2.
> In TP2 the DATA frames carried a plain file; in TP4 they carry protobuf.
> Why can Wireshark decode the HTTP/2 framing but not the protobuf payload?

#### Fill in the comparative table (row: gRPC)

---

## Comparative Table — Fill this in during the lab

| Criterion | HTTP/1.1 | HTTP/2 | HTTP/3 | gRPC |
|-----------|----------|--------|--------|------|
| Transport protocol | | | | |
| Visible TCP SYN in Wireshark? | | | | |
| Number of TCP connections (for 1 data transfer) | | | | |
| Encryption | | | | |
| Payload readable in Wireshark? | | | | |
| ALPN / protocol token | | | | |
| Round trips before first data | | | | |
| Firewall: blocked by UDP filtering? | | | | |
| Risk of man-in-the-middle attack | | | | |

---

## Wrap-up Questions

Answer these after completing all four TPs.

1. HTTP/1.1 has no encryption. Give two concrete examples of what an attacker
   on the same network could observe during your TP1 session.

2. In TP2 you configured `MIN_TLS_VERSION = TLSv1_3`. What would have changed
   if you had used `TLSv1_2` instead? (hint: look at the Wireshark cipher suite)

3. In TP3 you observed QUIC running over UDP. Why can QUIC integrate TLS directly,
   while HTTP/1.1 and HTTP/2 treat TLS as a separate layer?

4. You are a network security engineer. A user reports that file transfers are
   very slow on the corporate network but fast at home. The corporate firewall
   blocks UDP. Which HTTP version is affected? What is your recommendation?

5. A colleague says: "gRPC is just HTTP/2 with JSON." What is wrong with this
   statement? Name the serialization format gRPC actually uses and give one
   advantage it has over JSON.

6. A network monitoring tool uses gRPC server-side streaming to push telemetry
   from a router to a collector. The corporate firewall only allows TCP port 443.
   What would you need to change to make gRPC work in this environment?
