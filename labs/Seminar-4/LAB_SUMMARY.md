# Layer-4 Lab Summary

## Overview

This lab demonstrates **Layer-4 (Transport Layer) services** focusing on UDP and TCP protocols in a realistic multi-tier network architecture.

## Lab Components

### Network Infrastructure (4 Routers)
- **External-Access**: Entry point for client traffic
- **Core**: Central routing hub
- **Services**: Hosts security and proxy services
- **Internal-Access**: Backend server connectivity

All routers run **OSPF Area 0** for dynamic routing.

### Service Layer (5 Containers)
- **Firewall**: Linux iptables for packet filtering
- **Reverse Proxy**: NGINX for HTTP load balancing
- **Web Server**: NGINX serving static and dynamic content
- **Database**: MariaDB for data storage
- **DHCP Server**: ISC DHCP for IP address management

### Client Layer (2 Containers)
- **UDP Client**: Tests DHCP service
- **TCP Client**: Tests HTTP service

## Key Technologies

### Protocols
- **OSPF**: Dynamic routing protocol
- **UDP**: Connectionless transport (DHCP)
- **TCP**: Connection-oriented transport (HTTP)
- **DHCP**: Dynamic Host Configuration Protocol
- **HTTP**: Hypertext Transfer Protocol

### Services
- **NGINX**: Web server and reverse proxy
- **MariaDB**: Relational database
- **iptables**: Linux firewall
- **ISC DHCP**: DHCP server

## Network Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Layer                         │
│  UDP Client (DHCP)          TCP Client (10.100.2.10)   │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────┐
│                  Routing Layer (OSPF)                   │
│  External-Access → Core → Services → Internal-Access   │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────┴────────┐      ┌─────────┴──────────────────────┐
│ Service Layer  │      │      Backend Layer             │
│ - Firewall     │      │ - Web Server (10.100.4.10)    │
│ - Reverse Proxy│      │ - Database (10.100.4.20)      │
│   (10.100.3.x) │      │ - DHCP Server (10.100.4.30)   │
└────────────────┘      └────────────────────────────────┘
```

## Traffic Flows

### TCP Flow (HTTP)
1. TCP Client sends HTTP request
2. Routes through External-Access → Core → Services
3. Reverse Proxy receives request
4. Firewall inspects traffic
5. Routes through Internal-Access
6. Web Server processes and responds

### UDP Flow (DHCP)
1. UDP Client broadcasts DHCP Discover
2. Routes through External-Access → Core → Services
3. Firewall allows DHCP traffic
4. Routes through Internal-Access
5. DHCP Server responds with IP offer

## Learning Objectives

After completing this lab, you will understand:

1. **Transport Layer Protocols**
   - Differences between TCP and UDP
   - When to use each protocol
   - Protocol behavior and characteristics

2. **UDP Services**
   - DHCP DORA process
   - Broadcast vs unicast
   - Stateless communication

3. **TCP Services**
   - 3-way handshake
   - Connection management
   - Stateful communication

4. **Service Architecture**
   - Multi-tier application design
   - Reverse proxy benefits
   - Firewall placement strategies

5. **Troubleshooting**
   - Packet capture and analysis
   - Layer-4 connectivity testing
   - Service health monitoring

## Lab Exercises

### Part 0: Setup and Verification
- Deploy the lab
- Verify OSPF routing
- Test basic connectivity

### Part 1: Basic Services
- Configure and test DHCP
- Access web services via HTTP
- Analyze protocol behavior

### Part 2: Troubleshooting
- Diagnose DHCP issues
- Troubleshoot HTTP connectivity
- Analyze network paths

### Part 3: Advanced Topics
- Configure firewall rules
- Monitor service performance
- Implement health checks

## Quick Start

```bash
# Start the lab
cd labs/Seminar-4
make start

# Wait 2-3 minutes for containers to start

# Verify OSPF
ssh admin@core
show ip ospf neighbor

# Test DHCP
docker exec -it clab-Layer-4-udp-client udhcpc -i eth1

# Test HTTP
docker exec -it clab-Layer-4-tcp-client curl http://10.100.5.10/

# Stop the lab
make stop
```

## Expected Outcomes

✅ All OSPF neighbors in FULL state  
✅ UDP client receives IP via DHCP  
✅ TCP client can access web server  
✅ Traffic flows through reverse proxy  
✅ Firewall allows legitimate traffic  
✅ All services respond to health checks  

## Time Estimates

- **Quick Exploration**: 30 minutes
- **Complete Exercises**: 2-3 hours
- **Advanced Topics**: 1-2 hours
- **Total Lab Time**: 3-5 hours

## Prerequisites

- Basic understanding of TCP/IP
- Familiarity with Linux command line
- Knowledge of routing protocols (OSPF)
- Docker and Containerlab installed

## Resources

- **README.md**: Detailed lab instructions
- **QUICK_REFERENCE.md**: Command reference
- **BUILD_GUIDE.md**: Progressive configuration guide
- **INDEX.md**: Navigation hub


