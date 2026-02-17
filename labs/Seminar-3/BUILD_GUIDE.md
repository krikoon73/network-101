# Layer-3 Lab - Progressive Build Guide

This guide walks you through building the lab configuration step-by-step from scratch, without the pre-configured initial configs. You'll configure each component progressively to understand how the complete network is built.

## Two Ways to Use This Guide

### Option A: Build Mode (Recommended for Learning)
Start with minimal configurations and build everything yourself following this guide.

### Option B: Pre-Built Mode (Recommended for Testing/Verification)
Use the pre-configured lab to see the final result, then optionally rebuild it.

---

## Setup Instructions

### For Build Mode (Start from Scratch)

```bash
cd labs/Seminar-3

# Backup the pre-built configs
mkdir -p backup
cp -r clab/init-configs backup/

# Use minimal configs
cp clab/minimal-configs/* clab/init-configs/

# Deploy the lab
make start

# Wait for all devices to boot (2-3 minutes)
make inspect
```

Now you're ready to follow the configuration steps below!

### For Pre-Built Mode (Use Complete Configs)

```bash
cd labs/Seminar-3

# Just start the lab with pre-built configs
make start

# Verify everything is working
make inspect

# You can explore the configurations and then optionally rebuild
```

### Switching Between Modes

```bash
# Switch to minimal configs (build mode)
cp clab/minimal-configs/* clab/init-configs/
make stop && make start

# Switch back to pre-built configs
cp backup/init-configs/* clab/init-configs/
make stop && make start
```

---

## Phase 1: Basic Device Configuration

Configure basic settings on all devices (hostname, management, routing).

### R1 Configuration
```bash
ssh admin@r1
configure
hostname r1
ip routing
interface Loopback0
   ip address 1.1.1.1/32
exit
exit
write memory
```

### R2 Configuration
```bash
ssh admin@r2
configure
hostname r2
ip routing
interface Loopback0
   ip address 2.2.2.2/32
exit
exit
write memory
```

### R3 Configuration
```bash
ssh admin@r3
configure
hostname r3
ip routing
interface Loopback0
   ip address 3.3.3.3/32
exit
exit
write memory
```

### Edge1 Configuration
```bash
ssh admin@edge1
configure
hostname edge1
ip routing
interface Loopback0
   ip address 10.0.1.1/32
interface Loopback100
   description External Network 1
   ip address 100.64.1.1/32
exit
exit
write memory
```

### Edge2 Configuration
```bash
ssh admin@edge2
configure
hostname edge2
ip routing
interface Loopback0
   ip address 10.0.2.1/32
interface Loopback100
   description External Network 2
   ip address 100.64.2.1/32
exit
exit
write memory
```

### SW1 Configuration
```bash
ssh admin@sw1
configure
hostname sw1
ip routing
vlan 10
   name Users
vlan 20
   name Servers
exit
exit
write memory
```

### SW2 Configuration
```bash
ssh admin@sw2
configure
hostname sw2
ip routing
vlan 10
   name Users
vlan 20
   name Servers
exit
exit
write memory
```

---

## Phase 2: OSPF Core Network

Configure the OSPF core triangle (R1-R2-R3) and edge connections.

### R1 OSPF Configuration
```bash
ssh admin@r1
configure
interface Ethernet1
   description Link to R2
   no switchport
   ip address 192.168.12.1/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
interface Ethernet2
   description Link to R3
   no switchport
   ip address 192.168.13.1/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
interface Ethernet3
   description Link to Edge1
   no switchport
   ip address 192.168.1.1/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
interface Loopback0
   ip ospf area 0.0.0.0
router ospf 1
   router-id 1.1.1.1
   max-lsa 12000
exit
exit
write memory
```

### R2 OSPF Configuration
```bash
ssh admin@r2
configure
interface Ethernet1
   description Link to R1
   no switchport
   ip address 192.168.12.2/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
interface Ethernet2
   description Link to R3
   no switchport
   ip address 192.168.23.1/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
interface Loopback0
   ip ospf area 0.0.0.0
router ospf 1
   router-id 2.2.2.2
   max-lsa 12000
exit
exit
write memory
```

### R3 OSPF Configuration
```bash
ssh admin@r3
configure
interface Ethernet1
   description Link to R2
   no switchport
   ip address 192.168.23.2/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
interface Ethernet2
   description Link to R1
   no switchport
   ip address 192.168.13.2/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
interface Ethernet3
   description Link to Edge2
   no switchport
   ip address 192.168.3.1/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
interface Loopback0
   ip ospf area 0.0.0.0
router ospf 1
   router-id 3.3.3.3
   max-lsa 12000
exit
exit
write memory
```

### Edge1 OSPF Configuration
```bash
ssh admin@edge1
configure
interface Ethernet1
   description Link to R1
   no switchport
   ip address 192.168.1.2/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
interface Loopback0
   ip ospf area 0.0.0.0
router ospf 1
   router-id 10.0.1.1
   max-lsa 12000
exit
exit
write memory
```

### Edge2 OSPF Configuration
```bash
ssh admin@edge2
configure
interface Ethernet1
   description Link to R3
   no switchport
   ip address 192.168.3.2/30
   ip ospf network point-to-point
   ip ospf area 0.0.0.0
interface Loopback0
   ip ospf area 0.0.0.0
router ospf 1
   router-id 10.0.2.1
   max-lsa 12000
exit
exit
write memory
```

---

## Phase 3: Inter-VLAN Routing Configuration

Configure VLANs and inter-VLAN routing on R1, R3, SW1, and SW2.

### R1 Inter-VLAN Configuration
```bash
ssh admin@r1
configure
vlan 10,20
interface Vlan10
   description VLAN 10 - Users
   ip address 10.10.10.1/24
   ip ospf area 0.0.0.0
interface Vlan20
   description VLAN 20 - Servers
   ip address 10.10.20.1/24
   ip ospf area 0.0.0.0
interface Ethernet4
   description Trunk to SW1
   switchport mode trunk
   switchport trunk allowed vlan 10,20
router ospf 1
   passive-interface Vlan10
   passive-interface Vlan20
exit
exit
write memory
```

### R3 Inter-VLAN Configuration
```bash
ssh admin@r3
configure
vlan 10,20
interface Vlan10
   description VLAN 10 - Users
   ip address 10.20.10.1/24
   ip ospf area 0.0.0.0
interface Vlan20
   description VLAN 20 - Servers
   ip address 10.20.20.1/24
   ip ospf area 0.0.0.0
interface Ethernet4
   description Trunk to SW2
   switchport mode trunk
   switchport trunk allowed vlan 10,20
router ospf 1
   passive-interface Vlan10
   passive-interface Vlan20
exit
exit
write memory
```

### SW1 Access Layer Configuration
```bash
ssh admin@sw1
configure
interface Ethernet1
   description Trunk to R1
   switchport mode trunk
   switchport trunk allowed vlan 10,20
interface Ethernet2
   description Host1 - VLAN 10
   switchport mode access
   switchport access vlan 10
interface Ethernet3
   description Host2 - VLAN 20
   switchport mode access
   switchport access vlan 20
interface Vlan10
   ip address 10.10.10.254/24
exit
exit
write memory
```

### SW2 Access Layer Configuration
```bash
ssh admin@sw2
configure
interface Ethernet1
   description Trunk to R3
   switchport mode trunk
   switchport trunk allowed vlan 10,20
interface Ethernet2
   description Host3 - VLAN 10
   switchport mode access
   switchport access vlan 10
interface Ethernet3
   description Host4 - VLAN 20
   switchport mode access
   switchport access vlan 20
interface Vlan10
   ip address 10.20.10.254/24
exit
exit
write memory
```

---

## Phase 4: BGP Configuration

Configure BGP peering between Edge1 and Edge2, and redistribute routes.

### Edge1 BGP Configuration
```bash
ssh admin@edge1
configure
interface Ethernet2
   description Link to Edge2 (eBGP)
   no switchport
   ip address 172.16.12.1/30
router bgp 65001
   router-id 10.0.1.1
   neighbor 172.16.12.2 remote-as 65002
   neighbor 172.16.12.2 description eBGP to Edge2
   network 100.64.1.1/32
   address-family ipv4
      neighbor 172.16.12.2 activate
router ospf 1
   redistribute bgp
exit
exit
write memory
```

### Edge2 BGP Configuration
```bash
ssh admin@edge2
configure
interface Ethernet2
   description Link to Edge1 (eBGP)
   no switchport
   ip address 172.16.12.2/30
router bgp 65002
   router-id 10.0.2.1
   neighbor 172.16.12.1 remote-as 65001
   neighbor 172.16.12.1 description eBGP to Edge1
   network 100.64.2.1/32
   address-family ipv4
      neighbor 172.16.12.1 activate
router ospf 1
   redistribute bgp
exit
exit
write memory
```

---

## Phase 5: Verification Commands

After completing all phases, verify the configuration:

### Verify OSPF
```bash
# On any core router (R1, R2, R3)
ssh admin@r1
show ip ospf neighbor
show ip route ospf
show ip ospf database
```

### Verify BGP
```bash
# On Edge routers
ssh admin@edge1
show ip bgp summary
show ip bgp
show ip bgp neighbors 172.16.12.2
```

### Verify Inter-VLAN Routing
```bash
# On R1 or R3
ssh admin@r1
show vlan
show ip interface brief
show ip route
```

### Verify End-to-End Connectivity
```bash
# From your terminal
docker exec -it clab-Layer-3-Part1-host1 ping -c 3 10.10.20.10   # Host1 to Host2
docker exec -it clab-Layer-3-Part1-host1 ping -c 3 10.20.10.10   # Host1 to Host3
docker exec -it clab-Layer-3-Part1-host1 ping -c 3 10.20.20.10   # Host1 to Host4
docker exec -it clab-Layer-3-Part1-host1 ping -c 3 100.64.1.1    # Host1 to Edge1 external
docker exec -it clab-Layer-3-Part1-host1 ping -c 3 100.64.2.1    # Host1 to Edge2 external
docker exec -it clab-Layer-3-Part1-host1 traceroute 100.64.2.1   # Trace path
```

---

## Configuration Summary

### What You Built

1. **Phase 1**: Basic device setup with loopbacks and IP routing
2. **Phase 2**: OSPF core network with full mesh connectivity
3. **Phase 3**: Inter-VLAN routing with SVIs and trunk ports
4. **Phase 4**: BGP peering and route redistribution
5. **Phase 5**: Verification of all components

### Expected Results

- ✅ All OSPF neighbors in FULL state
- ✅ BGP peers in Established state
- ✅ All VLAN networks reachable via OSPF
- ✅ BGP external networks (100.64.x.x) reachable from all hosts
- ✅ Full connectivity between all hosts across VLANs and sites

### Troubleshooting Tips

If something doesn't work:

1. **OSPF not forming neighbors**:
   - Check interface IP addresses match the /30 subnets
   - Verify `ip ospf area 0.0.0.0` is configured on interfaces
   - Ensure interfaces are `no switchport` for routed ports

2. **BGP not establishing**:
   - Verify IP connectivity between 172.16.12.1 and 172.16.12.2
   - Check AS numbers (65001 and 65002)
   - Ensure neighbor statements are correct

3. **Inter-VLAN routing not working**:
   - Verify VLANs exist on both switches and routers
   - Check trunk configuration between switches and routers
   - Ensure VLAN interfaces have IP addresses
   - Verify hosts have correct default gateways

4. **Routes not propagating**:
   - Check `redistribute bgp` under OSPF
   - Verify `network` statements under BGP
   - Use `show ip route` to see what routes are installed

---

## Next Steps

After successfully building the lab:

1. Experiment with OSPF metrics and path selection
2. Add route filtering with route-maps
3. Implement BGP path attributes (MED, Local Preference)
4. Test failover scenarios by shutting down links
5. Add additional VLANs and extend the network

## Saving Your Configuration

To save your work for future use:

```bash
# On each device
ssh admin@<device>
show running-config | redirect flash:my-config.cfg

# Or from your terminal, save all configs
ssh admin@r1 "show running-config" > r1-built.cfg
ssh admin@r2 "show running-config" > r2-built.cfg
ssh admin@r3 "show running-config" > r3-built.cfg
ssh admin@edge1 "show running-config" > edge1-built.cfg
ssh admin@edge2 "show running-config" > edge2-built.cfg
ssh admin@sw1 "show running-config" > sw1-built.cfg
ssh admin@sw2 "show running-config" > sw2-built.cfg
```

---

## Restoring Pre-Built Configuration

If you want to go back to the pre-built configuration:

```bash
cd labs/Seminar-3
make stop
cp -r backup/init-configs clab/
make start
```


