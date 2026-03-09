# Seminar-4.1 Quick Reference Guide

## Lab Deployment

```bash
# Start the lab
cd labs/Seminar-4.1
make start

# Check status
make inspect

# Stop the lab
make stop
```

## Access Devices

```bash
# Core router
ssh admin@core
# Password: admin

# Clients
docker exec -it http-client sh
docker exec -it udp-client sh

# Servers
docker exec -it basic-http-server sh
docker exec -it dns-server sh
```

## IP Addresses

| Device | IP Address | Network |
|--------|-----------|---------|
| http-client | 10.100.1.10/24 | Client Network |
| udp-client | 10.100.2.10/24 | Client Network |
| basic-http-server | 10.100.3.10/24 | Server Network |
| dns-server | 10.100.4.10/24 | Server Network |
| core (eth1) | 10.100.1.1/24 | HTTP Client Gateway |
| core (eth2) | 10.100.2.1/24 | UDP Client Gateway |
| core (eth3) | 10.100.3.1/24 | HTTP Server Gateway |
| core (eth4) | 10.100.4.1/24 | DNS Server Gateway |

---

## Quick Test Scenarios

### Scenario 1: Test HTTP Service

```bash
# Access HTTP client
docker exec -it http-client sh

# Test HTTP service
curl http://10.100.3.10/

# Test health endpoint
curl http://10.100.3.10/health

# Test API endpoint
curl http://10.100.3.10/api

# Download large file (Les Trois Mousquetaires - 500KB)
curl http://10.100.3.10/3mq.txt -o /tmp/3mq.txt

# View the interactive HTML page
curl http://10.100.3.10/3mq.html

# Download with statistics
curl -w "\nBytes: %{size_download}\nSpeed: %{speed_download} B/s\nTime: %{time_total}s\n" \
  -o /dev/null http://10.100.3.10/3mq.txt
```

### Scenario 2: Capture TCP Traffic

```bash
# Terminal 1: Start capture on core router
ssh admin@core
bash
tcpdump -i eth3 'host 10.100.3.10 and port 80' -nn -v

# Terminal 2: Generate HTTP traffic
docker exec -it http-client curl http://10.100.3.10/health
```

### Scenario 3: Test UDP Service

```bash
# Access UDP client
docker exec -it udp-client sh

# Ping DNS server
ping -c 3 10.100.4.10

# Test UDP with netcat
echo "test" | nc -u 10.100.4.10 53
```

### Scenario 4: Capture UDP Traffic

```bash
# Terminal 1: Start capture on core router
ssh admin@core
bash
tcpdump -i eth4 'host 10.100.4.10 and udp' -nn -v

# Terminal 2: Generate UDP traffic
docker exec -it udp-client sh
echo "UDP Test" | nc -u 10.100.4.10 53
```

### Scenario 5: Large File Transfer Analysis

**Objective**: Analyze TCP segmentation and flow control with a 500KB file transfer.

```bash
# Terminal 1: Start packet capture
ssh admin@core
bash
tcpdump -i eth3 'host 10.100.3.10 and port 80' -nn -vv -w /tmp/3mq_transfer.pcap

# Terminal 2: Download the large file
docker exec -it http-client sh
curl -w "\nBytes: %{size_download}\nSpeed: %{speed_download} B/s\nTime: %{time_total}s\n" \
  -o /tmp/3mq.txt http://10.100.3.10/3mq.txt

# Stop capture (Ctrl+C in Terminal 1)

# Copy capture file to local machine
docker cp core:/tmp/3mq_transfer.pcap ./3mq_transfer.pcap

# Analyze in Wireshark:
# - Filter: tcp.stream eq 0
# - Follow TCP Stream
# - Statistics → TCP Stream Graphs → Time-Sequence (Stevens)
# - Look for: TCP segmentation, window scaling, sequence numbers
```

**What to observe**:
- Multiple TCP segments (file is split into ~350+ segments)
- Maximum Segment Size (MSS) negotiation
- TCP window scaling
- Sequence number progression
- Flow control in action

### Scenario 6: Compare TCP vs UDP

```bash
# Terminal 1: Capture TCP
ssh admin@core
bash
tcpdump -i eth3 'tcp port 80' -w /tmp/tcp.pcap

# Terminal 2: Capture UDP
ssh admin@core
bash
tcpdump -i eth4 'udp' -w /tmp/udp.pcap

# Terminal 3: Generate TCP traffic
docker exec -it http-client curl http://10.100.3.10/health

# Terminal 4: Generate UDP traffic
docker exec -it udp-client sh
echo "test" | nc -u 10.100.4.10 53

# Copy files for analysis
docker cp core:/tmp/tcp.pcap ./tcp.pcap
docker cp core:/tmp/udp.pcap ./udp.pcap
```

### Scenario 6: HTTP Security Analysis

```bash
# Terminal 1: Capture with ASCII output
ssh admin@core
bash
tcpdump -i eth3 'port 80' -A

# Terminal 2: Send data (INSECURE!)
docker exec -it http-client sh
curl -X POST http://10.100.3.10/api -d "username=student&password=secret123"

# Observe: You can see the password in plain text!
```

---

## Common tcpdump Commands

### Basic Capture
```bash
# Capture on specific interface
tcpdump -i eth3

# Capture specific host
tcpdump host 10.100.3.10

# Capture specific port
tcpdump port 80

# Capture TCP only
tcpdump tcp

# Capture UDP only
tcpdump udp
```

### Advanced Filters
```bash
# HTTP traffic
tcpdump 'tcp port 80'

# DNS traffic
tcpdump 'udp port 53'

# Specific host and port
tcpdump 'host 10.100.3.10 and port 80'

# Multiple ports
tcpdump 'port 80 or port 443'

# Exclude SSH traffic
tcpdump 'not port 22'
```

### Output Options
```bash
# Don't resolve names
tcpdump -nn

# Verbose output
tcpdump -v

# Very verbose
tcpdump -vv

# ASCII output (see HTTP content)
tcpdump -A

# Hex and ASCII
tcpdump -X

# Save to file
tcpdump -w capture.pcap

# Read from file
tcpdump -r capture.pcap
```

---

## Wireshark Filters

### TCP Filters
```
tcp.port == 80
tcp.flags.syn == 1
tcp.flags.syn == 1 && tcp.flags.ack == 0
tcp.analysis.retransmission
tcp.stream eq 0
```

### UDP Filters
```
udp.port == 53
udp
udp.length < 100
```

### HTTP Filters
```
http
http.request.method == "GET"
http.response.code == 200
http contains "password"
http.request.uri contains "/api"
```

---

## Troubleshooting

### Check Container Status
```bash
docker ps | grep -E "http-client|udp-client|basic-http-server|dns-server|core"
```

### Check IP Configuration
```bash
# On client
docker exec -it http-client ip addr show
docker exec -it http-client ip route

# On server
docker exec -it basic-http-server ip addr show
```

### Test Connectivity
```bash
# Ping test
docker exec -it http-client ping -c 3 10.100.3.10

# Traceroute
docker exec -it http-client traceroute 10.100.3.10

# Port test with netcat
docker exec -it http-client nc -zv 10.100.3.10 80
```

### Check Router Configuration
```bash
ssh admin@core
show ip interface brief
show ip route
show interfaces status
```

---

## Performance Testing

### HTTP Response Time
```bash
docker exec -it http-client sh
curl -w "Total Time: %{time_total}s\n" -o /dev/null -s http://10.100.3.10/
```

### Multiple Requests
```bash
for i in {1..10}; do
  curl -w "Request $i: %{time_total}s\n" -o /dev/null -s http://10.100.3.10/health
done
```

---

## Key Learning Points

### TCP Characteristics
- Connection-oriented (3-way handshake)
- Reliable delivery with ACKs
- Ordered packet delivery
- Flow control with window size
- Error detection and retransmission

### UDP Characteristics
- Connectionless (no handshake)
- No delivery guarantee
- No ordering guarantee
- Lower overhead (faster)
- Suitable for real-time applications

### HTTP Security
- HTTP is unencrypted (plain text)
- All data visible with packet capture
- Passwords, cookies, session tokens exposed
- HTTPS is essential for production systems

