# Layer-4 Lab - Progressive Build Guide

This guide provides step-by-step instructions to build the Layer-4 lab from scratch using minimal configurations.

## Overview

You will configure:
1. **Phase 1**: Basic interface configuration and IP addressing
2. **Phase 2**: Static routing configuration
3. **Phase 3**: Verify routing and connectivity
4. **Phase 4**: Configure and test services
5. **Phase 5**: Final verification and testing

**Estimated Time**: 2-3 hours

---

## Prerequisites

- Lab deployed with minimal configurations
- Basic understanding of Arista EOS CLI
- Familiarity with static routing concepts

---

## Lab Architecture

This lab demonstrates two different web service architectures:

### 1. HTTPS Service (Encrypted) 🔒
```
tcp-client → external-access → firewall → core → reverse-proxy (HTTPS)
                                                       ↓
                                                  (re-encrypt)
                                                       ↓
                                              web-server (HTTPS)
```

**Features**:
- Virtual IP (VIP): 10.100.100.10/32 for client access
- Two-interface reverse proxy (frontend + backend)
- End-to-end encryption with TLS 1.2/1.3
- Automatic SSL/TLS certificate generation
- HTTP to HTTPS redirect (301)

**Security**: All traffic is encrypted from client to web server

### 2. HTTP Service (Unencrypted) 🔓
```
tcp-client → external-access → firewall → core → basic-http-server (HTTP)
```

**Features**:
- Direct HTTP access on port 80
- NO encryption
- NO SSL/TLS certificates
- Educational warnings about security risks

**Security**: All traffic is in plain text - INSECURE!

### Purpose

This dual-architecture design allows students to:
- Compare encrypted vs unencrypted traffic side-by-side
- Understand the importance of HTTPS
- Analyze packet captures to see the difference
- Learn about SSL/TLS certificates and encryption

---

## Phase 1: Basic Interface Configuration

### 1.1 Configure External-Access Router

```bash
ssh admin@external-access
configure

! Loopback Interface
interface Loopback0
   description Router ID
   ip address 1.1.1.1/32
   no shutdown
   exit

! UDP Client Network
interface Ethernet1
   description UDP Client Network
   no switchport
   ip address 10.100.1.1/24
   no shutdown
   exit

! TCP Client Network
interface Ethernet2
   description TCP Client Network
   no switchport
   ip address 10.100.2.1/24
   no shutdown
   exit

! Link to Firewall (Outside)
interface Ethernet3
   description Link to Firewall Outside
   no switchport
   ip address 10.100.3.1/24
   no shutdown
   exit

! Enable IP routing
ip routing

write memory
exit
```

### 1.2 Configure Core Router

```bash
ssh admin@core
configure

! Loopback Interface
interface Loopback0
   description Router ID
   ip address 2.2.2.2/32
   no shutdown
   exit

! Link from Firewall (Inside)
interface Ethernet1
   description Link from Firewall Inside
   no switchport
   ip address 10.100.3.21/24
   no shutdown
   exit

! Reverse Proxy Network
interface Ethernet2
   description Reverse Proxy Network
   no switchport
   ip address 10.100.5.1/24
   no shutdown
   exit

! Web Server Network
interface Ethernet3
   description Web Server Network
   no switchport
   ip address 10.100.4.1/24
   no shutdown
   exit

! DNS Server Network
interface Ethernet4
   description DNS Server Network
   no switchport
   ip address 10.100.4.1/24
   no shutdown
   exit

! Enable IP routing
ip routing

write memory
exit
```

---

## Phase 2: Static Routing Configuration

### 2.1 Configure Static Routes on External-Access

```bash
ssh admin@external-access
configure

! Static routes to reach networks behind firewall
ip route 10.100.4.0/24 10.100.3.10
ip route 10.100.5.0/24 10.100.3.10

write memory
exit
```

**Explanation**:
- Routes to web server (10.100.4.0/24) and reverse proxy (10.100.5.0/24) networks
- Next-hop is the firewall outside interface (10.100.3.10)

### 2.2 Configure Static Routes on Core

```bash
ssh admin@core
configure

! Static routes to reach client networks through firewall
ip route 10.100.1.0/24 10.100.3.10
ip route 10.100.2.0/24 10.100.3.10

write memory
exit
```

**Explanation**:
- Routes to UDP client (10.100.1.0/24) and TCP client (10.100.2.0/24) networks
- Next-hop is the firewall inside interface (10.100.3.10)

---

## Phase 3: Verify Routing and Connectivity

### 3.1 Verify Routing Tables

Check that static routes are configured correctly:

```bash
# On External-Access
ssh admin@external-access
show ip route

# Should see:
# - C 10.100.1.0/24 directly connected, Ethernet1
# - C 10.100.2.0/24 directly connected, Ethernet2
# - C 10.100.3.0/24 directly connected, Ethernet3
# - S 10.100.4.0/24 via 10.100.3.10, Ethernet3
# - S 10.100.5.0/24 via 10.100.3.10, Ethernet3
```

```bash
# On Core
ssh admin@core
show ip route

# Should see:
# - S 10.100.1.0/24 via 10.100.3.10, Ethernet1
# - S 10.100.2.0/24 via 10.100.3.10, Ethernet1
# - C 10.100.3.0/24 directly connected, Ethernet1
# - C 10.100.4.0/24 directly connected, Ethernet3
# - C 10.100.5.0/24 directly connected, Ethernet2
```

### 3.2 Verify Firewall Configuration

Check firewall routing and IP forwarding:

```bash
# Access firewall container
docker exec -it firewall sh

# Check IP addresses
ip addr show

# Should see:
# - eth1: 10.100.3.10/24 (outside interface)
# - eth2: 10.100.3.20/24 (inside interface)

# Check routing table
ip route show

# Should see routes to all networks:
# - 10.100.1.0/24 via 10.100.3.1 dev eth1
# - 10.100.2.0/24 via 10.100.3.1 dev eth1
# - 10.100.4.0/24 via 10.100.3.21 dev eth2
# - 10.100.5.0/24 via 10.100.3.21 dev eth2

# Verify IP forwarding is enabled
sysctl net.ipv4.ip_forward
# Should return: net.ipv4.ip_forward = 1

exit
```

### 3.3 Test Connectivity

Test ping from clients to services:

```bash
# From TCP client to web server
docker exec -it tcp-client ping -c 3 10.100.4.10

# From TCP client to reverse proxy
docker exec -it tcp-client ping -c 3 10.100.5.10

# From UDP client to DNS server
docker exec -it udp-client ping -c 3 10.100.4.20
```

**Expected**: All pings should succeed.

### 3.4 Verify Traffic Path

Use traceroute to verify traffic goes through firewall:

```bash
# From TCP client to web server
docker exec -it tcp-client traceroute -n 10.100.4.10

# Expected path:
# 1. 10.100.2.1 (external-access)
# 2. 10.100.3.10 (firewall outside)
# 3. 10.100.3.21 (core)
# 4. 10.100.4.10 (web-server)
```

---

## Phase 4: Configure and Test Services

### 4.1 Test HTTP Service

Test web server directly:

```bash
# Access TCP client
docker exec -it tcp-client sh

# Test web server
curl http://10.100.4.10/

# Test health endpoint
curl http://10.100.4.10/health

# Test API endpoint
curl http://10.100.4.10/api
```

Test through reverse proxy:

```bash
# From TCP client
curl http://10.100.5.10/

# Test proxy health
curl http://10.100.5.10/health
```

**Expected**: All HTTP requests should return 200 OK.

### 4.2 Test DNS Server

The DNS server container is configured but DNS service needs to be started:

```bash
# Access DNS server
docker exec -it dns-server sh

# Check if DNS service is running
ps aux | grep dns

# Test connectivity
ping 10.100.4.1
```

### 4.3 Capture Traffic

Capture HTTP traffic on firewall:

```bash
# On firewall
docker exec -it firewall sh
tcpdump -i eth1 port 80 -A -s 0

# From another terminal, make HTTP request
docker exec -it tcp-client curl http://10.100.4.10/

# Observe TCP handshake and HTTP request/response
```

Capture traffic on Core router:

```bash
# On Core router
ssh admin@core
bash
tcpdump -i eth3 port 80 -v

# From another terminal, make HTTP request
docker exec -it tcp-client curl http://10.100.4.10/

# Observe traffic to web server
```

---

## Phase 5: Final Verification

### 5.1 Verify Complete Topology

Check all components are working:

```bash
# 1. Static routing
ssh admin@external-access
show ip route

ssh admin@core
show ip route

# 2. HTTP service
docker exec -it tcp-client curl -s http://10.100.4.10/ | grep "Layer-4"

# 3. Reverse proxy
docker exec -it tcp-client curl -s http://10.100.5.10/

# 4. All services reachable from clients
docker exec -it tcp-client ping -c 2 10.100.3.10  # Firewall
docker exec -it tcp-client ping -c 2 10.100.5.10  # Reverse Proxy
docker exec -it tcp-client ping -c 2 10.100.4.10  # Web Server
docker exec -it tcp-client ping -c 2 10.100.4.20  # DNS Server
```

### 5.2 Test End-to-End Connectivity

Verify complete traffic paths through firewall:

```bash
# TCP path: Client → External-Access → Firewall → Core → Web Server
docker exec -it tcp-client traceroute -n 10.100.4.10

# Expected path:
# 1. 10.100.2.1 (external-access)
# 2. 10.100.3.10 (firewall outside)
# 3. 10.100.3.21 (core)
# 4. 10.100.4.10 (web-server)

# Path to reverse proxy
docker exec -it tcp-client traceroute -n 10.100.5.10

# Expected path:
# 1. 10.100.2.1 (external-access)
# 2. 10.100.3.10 (firewall outside)
# 3. 10.100.3.21 (core)
# 4. 10.100.5.10 (reverse-proxy)
```

### 5.3 Verify Service Health

Run health checks on all services:

```bash
# Web server health
docker exec -it tcp-client curl http://10.100.4.10/health

# Reverse proxy health
docker exec -it tcp-client curl http://10.100.5.10/health

# API endpoint
docker exec -it tcp-client curl http://10.100.4.10/api
```

---

## Configuration Summary

### IP Addressing

| Device | Interface | IP Address | Description |
|--------|-----------|------------|-------------|
| External-Access | Lo0 | 1.1.1.1/32 | Router ID |
| External-Access | Eth1 | 10.100.1.1/24 | UDP Clients |
| External-Access | Eth2 | 10.100.2.1/24 | TCP Clients |
| External-Access | Eth3 | 10.100.3.1/24 | To Firewall (Outside) |
| Core | Lo0 | 2.2.2.2/32 | Router ID |
| Core | Eth1 | 10.100.3.21/24 | From Firewall (Inside) |
| Core | Eth2 | 10.100.5.1/24 | Reverse Proxy |
| Core | Eth3 | 10.100.4.1/24 | Web Server |
| Core | Eth4 | 10.100.4.1/24 | DNS Server |
| Firewall | eth1 | 10.100.3.10/24 | Outside (to External-Access) |
| Firewall | eth2 | 10.100.3.20/24 | Inside (to Core) |

### Static Routing Configuration

**External-Access Router:**
```
ip route 10.100.4.0/24 10.100.3.10
ip route 10.100.5.0/24 10.100.3.10
```

**Core Router:**
```
ip route 10.100.1.0/24 10.100.3.10
ip route 10.100.2.0/24 10.100.3.10
```

**Firewall:**
```
ip route add 10.100.1.0/24 via 10.100.3.1 dev eth1
ip route add 10.100.2.0/24 via 10.100.3.1 dev eth1
ip route add 10.100.4.0/24 via 10.100.3.21 dev eth2
ip route add 10.100.5.0/24 via 10.100.3.21 dev eth2
```

### Service IPs

- **Firewall Outside**: 10.100.3.10
- **Firewall Inside**: 10.100.3.20
- **Reverse Proxy**: 10.100.5.10
- **Web Server**: 10.100.4.10
- **DNS Server**: 10.100.4.20
- **TCP Client**: 10.100.2.10
- **UDP Client**: 10.100.1.10

---

## Troubleshooting

### Static Routes Not Working

```bash
# Check interface status
show ip interface brief

# Check routing table
show ip route

# Verify static routes are configured
show run | grep "ip route"

# Verify IP addresses
show ip interface
```

### Services Not Reachable

```bash
# Check routing
show ip route <service-ip>

# Test connectivity
ping <service-ip>

# Check service status
docker ps | grep <service-name>

# Check service logs
docker logs <service-name>
```

### Firewall Not Forwarding Traffic

```bash
# Verify firewall container is running
docker ps | grep firewall

# Check IP forwarding is enabled
docker exec -it firewall sysctl net.ipv4.ip_forward
# Should return: net.ipv4.ip_forward = 1

# Check firewall routing table
docker exec -it firewall ip route show

# Check firewall interfaces
docker exec -it firewall ip addr show

# Capture traffic on firewall
docker exec -it firewall tcpdump -i eth1 -n
```

### HTTPS Not Working

```bash
# Check reverse-proxy status
docker ps | grep reverse-proxy

# Check reverse-proxy logs
docker logs reverse-proxy

# Check web-server logs
docker logs web-server

# Test HTTPS connectivity
docker exec -it tcp-client curl -k https://10.100.100.10/health

# Test port 443
docker exec -it tcp-client nc -zv 10.100.100.10 443

# Check SSL certificates exist
docker exec -it reverse-proxy ls -la /etc/nginx/certs/

# Verify traffic path with traceroute
docker exec -it tcp-client traceroute -n 10.100.100.10
```

### HTTP (Basic Server) Not Working

```bash
# Check basic-http-server status
docker ps | grep basic-http-server

# Check basic-http-server logs
docker logs basic-http-server

# Test HTTP connectivity
docker exec -it tcp-client curl http://10.100.7.10/health

# Test port 80
docker exec -it tcp-client nc -zv 10.100.7.10 80

# Verify traffic path with traceroute
docker exec -it tcp-client traceroute -n 10.100.7.10
```

### Certificate Generation Issues

```bash
# Check if certificates exist
ls -la labs/Seminar-4/clab/services/certs/

# Regenerate certificates
cd labs/Seminar-4
rm -f clab/services/certs/*.pem
make certs

# Verify certificate generation
ls -la clab/services/certs/
# Should see: ca-cert.pem, ca-key.pem, reverse-proxy-cert.pem,
#             reverse-proxy-key.pem, web-server-cert.pem, web-server-key.pem
```

---

## Next Steps

After completing this build guide:

1. **Complete Lab Exercises**: Work through README.md exercises
2. **Experiment**: Try breaking and fixing configurations
3. **Advanced Topics**: Implement firewall rules, monitoring
4. **Documentation**: Review QUICK_REFERENCE.md for commands

---

## Saving Your Configuration

Don't forget to save your configurations:

```bash
# On each router
ssh admin@<router-name>
write memory

# Or from configure mode
configure
write memory
exit
```

---

## Congratulations!

You have successfully built the Layer-4 lab from scratch! You should now have:

✅ 2 routers with static routing
✅ Firewall positioned between routers
✅ HTTPS service with end-to-end encryption (VIP 10.100.100.10)
✅ HTTP service for security comparison (10.100.7.10)
✅ Automatic SSL/TLS certificate generation
✅ Reverse proxy with two-interface architecture
✅ Full connectivity between all networks through firewall
✅ Working HTTP service with reverse proxy
✅ Understanding of UDP and TCP protocols
✅ Hands-on experience with static routing and firewall configuration
✅ Understanding of traffic flow through network security devices

Continue with the exercises in README.md to deepen your understanding of Layer-4 services and troubleshooting!

