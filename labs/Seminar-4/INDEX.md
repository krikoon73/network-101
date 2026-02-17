# Layer-4 Lab - Documentation Index

Welcome to the **Layer-4 Lab**! This lab focuses on UDP and TCP services in a multi-tier network architecture.

## 📚 Documentation

### Getting Started
- **[LAB_SUMMARY.md](LAB_SUMMARY.md)** - Quick overview and learning objectives
- **[README.md](README.md)** - Complete lab instructions and exercises
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Command reference and IP addressing

### Building the Lab
- **[BUILD_GUIDE.md](BUILD_GUIDE.md)** - Progressive configuration guide (coming soon)

### Navigation
- **[INDEX.md](INDEX.md)** - This file

---

## 🚀 Quick Start Guides

### Option 1: Pre-Built Configuration (Recommended for First Time)

```bash
# 1. Start the lab with pre-built configs
cd labs/Seminar-4
make start

# 2. Wait 2-3 minutes for all containers to start

# 3. Verify OSPF routing
ssh admin@core
show ip ospf neighbor
show ip route

# 4. Test DHCP service
docker exec -it clab-Layer-4-udp-client udhcpc -i eth1

# 5. Test HTTP service
docker exec -it clab-Layer-4-tcp-client curl http://10.100.5.10/

# 6. Follow exercises in README.md
```

### Option 2: Build From Scratch (Advanced)

```bash
# 1. Start with minimal configs
cd labs/Seminar-4
# Edit topology to use minimal-configs (when available)

# 2. Follow BUILD_GUIDE.md step-by-step

# 3. Configure OSPF, services, and test
```

---

## 📖 Learning Paths

### Path 1: Quick Exploration (30 minutes)
1. Read [LAB_SUMMARY.md](LAB_SUMMARY.md)
2. Start the lab with pre-built configs
3. Complete Part 0 in [README.md](README.md) (Setup and Verification)
4. Test DHCP and HTTP services (Part 1)

### Path 2: Hands-On Practice (2-3 hours)
1. Complete Path 1
2. Work through Part 2 (Troubleshooting exercises)
3. Experiment with packet captures
4. Analyze TCP and UDP traffic

### Path 3: Advanced Topics (4-5 hours)
1. Complete Paths 1 and 2
2. Work through Part 3 (Advanced exercises)
3. Configure firewall rules
4. Implement monitoring and health checks
5. Experiment with service failures

### Path 4: Build From Scratch (5+ hours)
1. Read [BUILD_GUIDE.md](BUILD_GUIDE.md) (when available)
2. Start with minimal configurations
3. Build the lab progressively
4. Complete all exercises

---

## 🎯 Lab Components

### Network Devices (OSPF Area 0)
- **external-access** (1.1.1.1) - Client entry point
- **core** (2.2.2.2) - Central routing hub
- **services** (3.3.3.3) - Security and proxy services
- **internal-access** (4.4.4.4) - Backend server access

### Service Containers
- **firewall** (10.100.3.10) - iptables packet filtering
- **reverse-proxy** (10.100.5.10) - NGINX reverse proxy
- **web-server** (10.100.4.10) - NGINX web server
- **database** (10.100.6.10) - MariaDB database
- **dhcp-server** (10.100.7.10) - ISC DHCP server

### Client Containers
- **udp-client** - DHCP client (dynamic IP)
- **tcp-client** (10.100.2.10) - HTTP client

---

## 🔧 Common Tasks

### Lab Management
```bash
make start      # Deploy the lab
make inspect    # Check lab status
make stop       # Destroy the lab
```

### Access Devices
```bash
# Routers
ssh admin@<router-name>

# Containers
docker exec -it clab-Layer-4-<container-name> sh
```

### Verify OSPF
```bash
ssh admin@core
show ip ospf neighbor
show ip route ospf
```

### Test Services
```bash
# DHCP
docker exec -it clab-Layer-4-udp-client udhcpc -i eth1

# HTTP
docker exec -it clab-Layer-4-tcp-client curl http://10.100.5.10/
```

### Capture Traffic
```bash
ssh admin@external-access
bash
tcpdump -i eth3 port 80 -nn -v
```

---

## 📋 Lab Exercises

### Part 0: Setup and Verification
- Deploy the lab
- Verify OSPF routing
- Test basic connectivity

### Part 1: Basic UDP and TCP Connectivity
- **Exercise 1.1**: DHCP (UDP Service)
  - Configure DHCP client
  - Verify DHCP server
  - Capture DHCP traffic
- **Exercise 1.2**: HTTP (TCP Service)
  - Test web server access
  - Test through reverse proxy
  - Capture HTTP traffic

### Part 2: Troubleshooting
- **Exercise 2.1**: Troubleshooting DHCP Issues
  - DHCP server not responding
  - DHCP relay issues
- **Exercise 2.2**: Troubleshooting HTTP Issues
  - Web server down
  - Reverse proxy misconfiguration
  - Network path issues
- **Exercise 2.3**: Protocol Analysis
  - TCP connection analysis
  - UDP packet analysis

### Part 3: Advanced Exercises
- **Exercise 3.1**: Implement Firewall Rules
- **Exercise 3.2**: Monitor Service Performance
- **Exercise 3.3**: Service Health Checks

---

## 🆘 Getting Help

### Troubleshooting
See the **Troubleshooting Guide** section in [README.md](README.md)

### Common Issues

**DHCP not working?**
- Check DHCP server is running: `docker ps | grep dhcp-server`
- Verify connectivity: `ping 10.100.7.10`
- Check logs: `docker logs clab-Layer-4-dhcp-server`

**HTTP not working?**
- Check web server is running: `docker ps | grep web-server`
- Test connectivity: `ping 10.100.4.10`
- Verify routing: `show ip route 10.100.4.10`

**OSPF neighbors not forming?**
- Check interface status: `show ip interface brief`
- Verify OSPF config: `show run section ospf`
- Check OSPF interfaces: `show ip ospf interface brief`

### Quick Reference
See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for:
- IP addressing tables
- Common commands
- Traffic flow diagrams
- Troubleshooting scenarios

---

## 📊 Lab Topology

```
                    UDP Client (DHCP)
                         |
                    TCP Client (10.100.2.10)
                         |
                  External-Access (1.1.1.1)
                         |
                      Core (2.2.2.2)
                    /          \
              Services       Internal-Access
             (3.3.3.3)          (4.4.4.4)
                 |                  |
         +-------+-------+    +-----+-----+-----+
         |               |    |     |     |     |
    Firewall      Reverse  Web   DB   DHCP
   (10.100.3.10)  Proxy  Server Server Server
                (10.100.5.10) (10.100.4.x)
```

---

## ✅ Expected Outcomes

After completing this lab, you should be able to:

- ✅ Explain the differences between TCP and UDP
- ✅ Configure and troubleshoot DHCP services
- ✅ Configure and troubleshoot HTTP services
- ✅ Analyze TCP and UDP packet captures
- ✅ Implement basic firewall rules
- ✅ Monitor service health and performance
- ✅ Troubleshoot Layer-4 connectivity issues

---

## 📝 Additional Resources

- **Containerlab Documentation**: https://containerlab.dev
- **Arista EOS Documentation**: https://www.arista.com/en/support/product-documentation
- **NGINX Documentation**: https://nginx.org/en/docs/
- **ISC DHCP Documentation**: https://www.isc.org/dhcp/


