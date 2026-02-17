# Layer-4 Lab - Quick Reference

## IP Addressing

### Loopback Addresses (Router IDs)
| Router | Loopback0 | Router ID |
|--------|-----------|-----------|
| external-access | 1.1.1.1/32 | 1.1.1.1 |
| core | 2.2.2.2/32 | 2.2.2.2 |

### Client Networks
| Network | Gateway | Client IP | Description |
|---------|---------|-----------|-------------|
| 10.100.1.0/24 | 10.100.1.1 | 10.100.1.10 | UDP Client Network |
| 10.100.2.0/24 | 10.100.2.1 | 10.100.2.10 | TCP Client Network |

### Firewall Transit Network
| Network | Device | IP Address | Description |
|---------|--------|------------|-------------|
| 10.100.3.0/24 | external-access | 10.100.3.1/24 | Router interface |
| 10.100.3.0/24 | firewall (outside) | 10.100.3.10/24 | Firewall outside |
| 10.100.3.0/24 | firewall (inside) | 10.100.3.20/24 | Firewall inside |
| 10.100.3.0/24 | core | 10.100.3.21/24 | Router interface |

### Service Networks
| Network | Gateway | Services | Description |
|---------|---------|----------|-------------|
| 10.100.4.0/24 | 10.100.4.1 | web-server (10.100.4.10) | Web Server Network |
| 10.100.5.0/24 | 10.100.5.1 | reverse-proxy frontend (10.100.5.10) | Reverse Proxy Frontend |
| 10.100.6.0/24 | 10.100.6.1 | reverse-proxy backend (10.100.6.10) | Backend Network |
| 10.100.7.0/24 | 10.100.7.1 | basic-http-server (10.100.7.10) | Basic HTTP (Unencrypted) |
| 10.100.8.0/24 | 10.100.8.1 | dns-server (10.100.8.20) | DNS Server Network |

### Service IP Addresses
| Service | IP Address | Port | Protocol | Encryption | MTU |
|---------|------------|------|----------|------------|-----|
| firewall | 10.100.3.10 / 10.100.3.20 | - | - | - | 1500 |
| reverse-proxy (frontend) | 10.100.5.10 + VIP 10.100.100.10 | 443 | TCP | HTTPS (TLS 1.2/1.3) | 1500 |
| reverse-proxy (backend) | 10.100.6.10 | 443 | TCP | HTTPS (TLS 1.2/1.3) | 1500 |
| web-server | 10.100.4.10 | 443 | TCP | HTTPS (TLS 1.2/1.3) | 1500 |
| basic-http-server | 10.100.7.10 | 80 | TCP | ❌ NONE | 1500 |
| dns-server | 10.100.8.20 | 53 | UDP | - | 1500 |
| tcp-client | 10.100.2.10 | - | - | - | 1500 |
| udp-client | 10.100.1.10 | - | - | - | 1500 |

---

## Common Commands

### Lab Management
```bash
# Start the lab
make start

# Check lab status
make inspect

# Stop the lab
make stop
```

### Router Access
```bash
# SSH to routers (password: admin)
ssh admin@external-access
ssh admin@core
```

### Container Access
```bash
# Access service containers (no clab-Layer-4- prefix needed)
docker exec -it firewall sh
docker exec -it reverse-proxy sh
docker exec -it web-server sh
docker exec -it dns-server sh

# Access client containers
docker exec -it udp-client sh
docker exec -it tcp-client sh
```

### Static Routing Verification
```bash
# Show routing table
show ip route

# Show specific route
show ip route 10.100.4.0

# Show interface status
show ip interface brief
```

### Service Testing
```bash
# HTTPS service (encrypted) - Use VIP
curl -k https://10.100.100.10/           # Main page
curl -k https://10.100.100.10/health     # Health check
curl -k https://10.100.100.10/api        # API endpoint
curl -k https://10.100.100.10/hostname   # Server hostname
curl -kv https://10.100.100.10/          # Verbose output

# HTTP service (unencrypted) - Direct access
curl http://10.100.7.10/                 # Main page (with security warnings)
curl http://10.100.7.10/health           # Health check
curl http://10.100.7.10/api              # API endpoint
curl http://10.100.7.10/hostname         # Server hostname

# Compare both services
curl -k https://10.100.100.10/health && curl http://10.100.7.10/health

# DNS/UDP testing
ping -c 3 10.100.8.20                    # Test DNS server connectivity
traceroute -n 10.100.8.20                # Trace path to DNS server

# UDP echo test
docker exec -d dns-server sh -c "while true; do nc -u -l -p 5353 -e /bin/cat; done"
echo 'Test UDP' | nc -u -w 2 10.100.8.20 5353  # Send UDP packet and get response
```

### Network Troubleshooting
```bash
# Connectivity
ping <ip>
traceroute <ip>

# Routing
ip route                    # On containers
show ip route              # On routers

# Interfaces
ip addr                    # On containers
show ip interface brief    # On routers

# Port testing
nc -zv <ip> <port>         # Check if port is open
netstat -an | grep <port>  # Show connections
```

### Packet Capture
```bash
# On routers (enter bash first)
bash
tcpdump -i <interface> <filter>

# Examples
tcpdump -i eth6 port 80 -A -s 0             # HTTP traffic (unencrypted - readable!)
tcpdump -i eth2 port 443 -A -s 0            # HTTPS traffic (encrypted - unreadable)
tcpdump -i eth2 'port 67 or port 68' -v     # DHCP traffic
tcpdump -i eth3 -A -s 0                     # All traffic with ASCII
tcpdump -i eth1 'tcp[tcpflags] & tcp-syn != 0'  # SYN packets

# Capture to file for Wireshark analysis
tcpdump -i eth6 port 80 -w /tmp/http.pcap
tcpdump -i eth2 port 443 -w /tmp/https.pcap
```

### Service Logs
```bash
# View container logs
docker logs clab-Layer-4-<container-name>

# Follow logs
docker logs -f clab-Layer-4-<container-name>

# NGINX logs (inside container)
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## Common Scenarios

### Scenario 1: Test DNS/UDP Service
```bash
# 1. Access UDP client
docker exec -it udp-client sh

# 2. Verify IP address and routing
ip addr show eth1
ip route

# 3. Test DNS server connectivity
ping -c 3 10.100.8.20

# 4. Verify network path
traceroute -n 10.100.8.20

# 5. Test UDP communication
# Terminal 1: Start UDP echo server
docker exec -d dns-server sh -c "while true; do nc -u -l -p 5353 -e /bin/cat; done"

# Terminal 2: Send UDP packet
docker exec -it udp-client sh -c "echo 'Hello DNS' | nc -u -w 2 10.100.8.20 5353"

# 6. Capture UDP packets
docker exec -it dns-server tcpdump -i eth1 -n 'udp port 5353 or icmp'
```

### Scenario 2: Test HTTPS Service (Encrypted)
```bash
# 1. Access TCP client
docker exec -it tcp-client sh

# 2. Test HTTPS service via VIP
curl -k https://10.100.100.10/

# 3. Test health endpoint
curl -k https://10.100.100.10/health

# 4. Check reverse-proxy logs
docker logs reverse-proxy

# 5. Check web-server logs
docker logs web-server
```

### Scenario 3: Test HTTP Service (Unencrypted)
```bash
# 1. Access TCP client
docker exec -it tcp-client sh

# 2. Test HTTP service
curl http://10.100.7.10/

# 3. Test health endpoint
curl http://10.100.7.10/health

# 4. Check basic-http-server logs
docker logs basic-http-server
```

### Scenario 4: Compare HTTP vs HTTPS
```bash
# 1. Access TCP client
docker exec -it tcp-client sh

# 2. Test both services
echo "=== HTTPS (Encrypted) ==="
curl -k https://10.100.100.10/health
echo ""
echo "=== HTTP (Unencrypted) ==="
curl http://10.100.7.10/health

# 3. Capture traffic on core router
# In another terminal:
ssh admin@core
bash
# Capture HTTP (you can read it!)
tcpdump -i eth6 port 80 -A -s 0
# Capture HTTPS (encrypted!)
tcpdump -i eth2 port 443 -A -s 0
```

### Scenario 5: Verify Two HTTPS Sessions (Connection Stitching)
```bash
# This demonstrates that the reverse proxy creates TWO separate TLS sessions

# Terminal 1: Monitor reverse-proxy logs (sees client IP)
docker exec -it reverse-proxy tail -f /var/log/nginx/access.log

# Terminal 2: Monitor web-server logs (sees proxy backend IP)
docker exec -it web-server tail -f /var/log/nginx/access.log

# Terminal 3: Capture Session 1 (Client → Proxy on frontend)
ssh admin@core
bash
tcpdump -i eth2 'host 10.100.5.10 and port 443' -nn -v

# Terminal 4: Capture Session 2 (Proxy → Server on backend)
ssh admin@core
bash
tcpdump -i eth3 'host 10.100.6.10 and port 443' -nn -v

# Terminal 5: Generate traffic
docker exec -it tcp-client curl -k https://10.100.100.10/health

# Observe:
# - Reverse proxy log shows: 10.100.2.10 (client IP)
# - Web server log shows: 10.100.6.10 (proxy backend IP)
# - Two separate TLS handshakes in packet captures
```

### Scenario 5: Troubleshoot Connectivity
```bash
# 1. Test basic connectivity
ping 10.100.4.10

# 2. Trace route
traceroute 10.100.4.10

# 3. Check routing
ip route

# 4. Test port
nc -zv 10.100.4.10 80
```

### Scenario 4: Capture Traffic
```bash
# 1. SSH to router
ssh admin@external-access

# 2. Enter bash
bash

# 3. Capture traffic
tcpdump -i eth3 port 80 -nn -v

# 4. Generate traffic from another terminal
docker exec -it tcp-client curl http://10.100.5.10/
```

---

## Traffic Flow Paths

### HTTP Request Path (via Reverse Proxy)
```
tcp-client (10.100.2.10)
    ↓
external-access (10.100.2.1)
    ↓
firewall (10.100.3.10 → 10.100.3.20)
    ↓
core (10.100.3.21)
    ↓
reverse-proxy (10.100.5.10)
    ↓
web-server (10.100.4.10)
```

### HTTP Request Path (Direct)
```
tcp-client (10.100.2.10)
    ↓
external-access (10.100.2.1)
    ↓
firewall (10.100.3.10 → 10.100.3.20)
    ↓
core (10.100.3.21)
    ↓
web-server (10.100.4.10)
```

### UDP Request Path
```
udp-client (10.100.1.10)
    ↓
external-access (10.100.1.1)
    ↓
firewall (10.100.3.10 → 10.100.3.20)
    ↓
core (10.100.3.21)
    ↓
dns-server (10.100.8.20)
```


