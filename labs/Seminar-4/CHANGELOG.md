# Seminar-4 Lab Changelog

## Major Topology Simplification (2026-02-16)

### Overview
The lab topology has been significantly simplified to make it more accessible for educational purposes while maintaining the core learning objectives around Layer-4 protocols and services.

### Key Changes

#### Topology Changes
- **Reduced from 4 routers to 2 routers**
  - Removed: `services` router
  - Removed: `internal-access` router
  - Kept: `external-access` and `core` routers

- **Firewall repositioned**
  - Old: Connected to services router
  - New: Positioned between external-access and core routers
  - Acts as a gateway between the two routing domains

- **Service consolidation**
  - All services now connect directly to core router
  - Removed: database container
  - Renamed: dhcp-server → dns-server

#### Routing Changes
- **Removed: OSPF dynamic routing**
  - No more OSPF configuration
  - No more router-id configuration
  - No more passive interfaces

- **Added: Static routing**
  - Simple static routes on both routers
  - Routes point to firewall as next-hop
  - Easier to understand and troubleshoot

- **Removed: VRF and PBR**
  - No VRF OUTSIDE or VRF INSIDE
  - No Policy-Based Routing
  - No route leaking configuration

#### IP Addressing Changes
- **Simplified addressing scheme**
  - Removed inter-router /30 links (10.0.12.0/30, 10.0.23.0/30, 10.0.24.0/30)
  - Firewall uses 10.100.3.0/24 network for both interfaces
  - All services on /24 networks

- **New IP assignments**
  - Firewall outside: 10.100.3.10/24
  - Firewall inside: 10.100.3.20/24
  - External-access to firewall: 10.100.3.1/24
  - Core from firewall: 10.100.3.21/24

### Traffic Flow

**Old Complex Path:**
```
tcp-client → external-access → core → services [PBR+VRF] → firewall → 
services [VRF] → reverse-proxy → services → internal-access → web-server
```

**New Simple Path:**
```
tcp-client → external-access → firewall → core → web-server
```

### Configuration Files Updated

1. **labs/Seminar-4/clab/topology.clab.yml**
   - Reduced from 11 nodes to 8 nodes
   - Updated links to reflect new topology
   - Simplified firewall configuration

2. **labs/Seminar-4/clab/init-configs/external-access.cfg**
   - Removed OSPF configuration
   - Removed PBR configuration
   - Added static routes
   - Updated interface assignments

3. **labs/Seminar-4/clab/init-configs/core.cfg**
   - Removed OSPF configuration
   - Removed PBR configuration
   - Added static routes
   - Updated interface assignments

4. **labs/Seminar-4/BUILD_GUIDE.md**
   - Complete rewrite for simplified topology
   - Removed OSPF configuration steps
   - Added static routing configuration steps
   - Updated all verification commands
   - Updated troubleshooting section

### Files No Longer Needed

- `labs/Seminar-4/clab/init-configs/services.cfg`
- `labs/Seminar-4/clab/init-configs/internal-access.cfg`

### Deployment Status

✅ Lab successfully deployed with 8 containers
✅ All routing verified and working
✅ Traffic flows through firewall as expected
✅ HTTP services accessible from clients
✅ Documentation updated

### Benefits of Simplification

1. **Easier to understand** - Fewer routers and simpler routing
2. **Faster deployment** - Fewer containers to start
3. **Simpler troubleshooting** - Static routes are easier to debug than OSPF
4. **Clear traffic path** - Easy to see how packets flow through the network
5. **Educational focus** - Emphasizes Layer-4 concepts without routing complexity

### Learning Objectives Maintained

✅ Understanding of TCP and UDP protocols
✅ HTTP service configuration and testing
✅ Reverse proxy concepts
✅ Network segmentation with firewall
✅ Static routing configuration
✅ Traffic flow analysis with traceroute
✅ Packet capture and analysis

### Reason for Change

The previous topology attempted to implement complex VRF-based Policy-Based Routing to force traffic through a service chain. However, Arista EOS 4.35.0F does not support the `set ip next-hop vrf` command required for cross-VRF PBR. Rather than work around this limitation with increasingly complex configurations, the decision was made to simplify the entire lab to focus on the core Layer-4 learning objectives.

