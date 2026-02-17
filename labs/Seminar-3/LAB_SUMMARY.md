# Seminar-3 Lab Summary

## Overview
This lab provides a comprehensive Layer-3 networking environment covering:
- **Inter-VLAN Routing** using Switched Virtual Interfaces (SVIs)
- **OSPF** (Open Shortest Path First) for internal routing
- **BGP** (Border Gateway Protocol) for external routing

## Lab Components

### Network Devices (7 total)
1. **R1, R2, R3** - Core routers running OSPF Area 0
2. **Edge1, Edge2** - Edge routers running BGP (AS 65001 and AS 65002)
3. **SW1, SW2** - Access layer switches with VLAN support

### End Hosts (4 total)
- **Host1** - VLAN 10 at Site 1 (10.10.10.10/24)
- **Host2** - VLAN 20 at Site 1 (10.10.20.10/24)
- **Host3** - VLAN 10 at Site 2 (10.20.10.10/24)
- **Host4** - VLAN 20 at Site 2 (10.20.20.10/24)

## Key Features

### 1. Inter-VLAN Routing
- Two VLANs (10 and 20) deployed across two sites
- R1 and R3 act as default gateways for their respective sites
- Demonstrates Layer-3 switching and routing between VLANs

### 2. OSPF Configuration
- All core routers (R1, R2, R3) and edge routers participate in OSPF Area 0
- Point-to-point network type for faster convergence
- Loopback interfaces used for stable router IDs
- VLAN interfaces configured as passive interfaces

### 3. BGP Configuration
- Two autonomous systems: AS 65001 (Edge1) and AS 65002 (Edge2)
- eBGP peering between Edge1 and Edge2
- Each edge router advertises an external network (100.64.x.x)
- BGP routes redistributed into OSPF for internal reachability

## Network Architecture

```
Internet/External Networks
         |
    [BGP Layer]
    Edge1 ↔ Edge2
         |
    [OSPF Core]
    R1 - R2 - R3
         |
   [Access Layer]
    SW1     SW2
     |       |
   Hosts   Hosts
```

## Learning Path

### Beginner Level
1. Verify basic connectivity between hosts
2. Understand VLAN configuration
3. Test inter-VLAN routing
4. View OSPF neighbor relationships

### Intermediate Level
1. Analyze OSPF routing tables
2. Test OSPF convergence with link failures
3. Verify BGP peering status
4. Trace packet paths through the network

### Advanced Level
1. Understand route redistribution between BGP and OSPF
2. Modify BGP path attributes
3. Implement route filtering
4. Optimize OSPF metrics

## Files Created

### Configuration Files
- `clab/init-configs/r1.cfg` - R1 initial configuration
- `clab/init-configs/r2.cfg` - R2 initial configuration
- `clab/init-configs/r3.cfg` - R3 initial configuration
- `clab/init-configs/edge1.cfg` - Edge1 initial configuration
- `clab/init-configs/edge2.cfg` - Edge2 initial configuration
- `clab/init-configs/sw1.cfg` - SW1 initial configuration
- `clab/init-configs/sw2.cfg` - SW2 initial configuration

### Serial Number Files
- `clab/sn/*.txt` - Device serial numbers and MAC addresses

### Lab Files
- `clab/topology.clab.yml` - Containerlab topology definition
- `Makefile` - Lab management commands
- `README.md` - Comprehensive lab guide with verification exercises
- `BUILD_GUIDE.md` - Step-by-step configuration guide (build from scratch)
- `QUICK_REFERENCE.md` - Quick command reference
- `LAB_SUMMARY.md` - This file
- `clab/init-configs/` - Pre-built device configurations
- `clab/minimal-configs/` - Minimal configs for build mode

## Quick Start

### Pre-Built Mode (Explore & Verify)
```bash
# Navigate to lab directory
cd labs/Seminar-3

# Start the lab with pre-built configs
make start

# Wait for all containers to start (about 2-3 minutes)

# Verify lab is running
make inspect

# Access a device
ssh admin@r1

# Test connectivity
docker exec -it clab-Layer-3-Part1-host1 ping 10.10.20.10
```

### Build Mode (Configure from Scratch)
```bash
# Navigate to lab directory
cd labs/Seminar-3

# Backup pre-built configs
mkdir -p backup
cp -r clab/init-configs backup/

# Use minimal configs
cp clab/minimal-configs/* clab/init-configs/

# Start the lab
make start

# Follow BUILD_GUIDE.md to configure step-by-step
```

## Expected Lab Duration
- **Setup**: 5 minutes
- **Basic exercises**: 30-45 minutes
- **Advanced exercises**: 1-2 hours
- **Total**: 2-3 hours for complete lab

## Prerequisites
- Understanding of IP addressing and subnetting
- Basic knowledge of VLANs
- Familiarity with routing concepts
- Containerlab installed and configured
- Arista cEOS image (ceos:4.35.0F) available

## Success Criteria

After completing this lab, you should be able to:
- ✅ Configure and verify Inter-VLAN routing
- ✅ Configure OSPF on multiple routers
- ✅ Verify OSPF neighbor relationships and routing tables
- ✅ Configure eBGP between different autonomous systems
- ✅ Redistribute routes between BGP and OSPF
- ✅ Troubleshoot Layer-3 connectivity issues
- ✅ Understand the difference between IGP and EGP
- ✅ Analyze routing protocol convergence

## Troubleshooting Resources

If you encounter issues:
1. Check the README.md for detailed troubleshooting steps
2. Use QUICK_REFERENCE.md for command syntax
3. Verify all containers are running: `make inspect`
4. Check device logs: `docker logs clab-Layer-3-Part1-<device>`
5. Restart the lab: `make stop && make start`

## Next Steps

After mastering this lab, proceed to:
- **Seminar-4**: Advanced BGP with EVPN-VXLAN
- Experiment with route filtering and manipulation
- Implement advanced OSPF features (areas, summarization)
- Add redundancy and test failover scenarios

## Notes

- All devices use passwordless authentication for lab convenience
- The lab uses private IP addressing (RFC 1918)
- BGP AS numbers are from the private range (64512-65534)
- OSPF uses Area 0 (backbone area) for simplicity
- External networks (100.64.x.x) use CGNAT address space for simulation


