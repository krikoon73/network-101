# Layer-3 Lab (Part #1)

This lab covers fundamental Layer-3 routing concepts including:
- **Inter-VLAN Routing**: Routing between different VLANs
- **OSPF Routing**: Dynamic routing within an autonomous system
- **BGP Routing**: External routing between different autonomous systems

## 📚 Lab Modes

This lab can be used in two ways:

1. **Pre-Built Mode** (Default): Deploy with complete configurations and explore/verify
   - Use this README for verification exercises
   - See [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for commands

2. **Build Mode**: Start from minimal configs and build the lab yourself
   - See [BUILD_GUIDE.md](BUILD_GUIDE.md) for step-by-step configuration
   - Great for hands-on learning and understanding each component

## Lab Topology

The lab consists of:
- **3 Core Routers (R1, R2, R3)**: Running OSPF in Area 0
- **2 Edge Routers (Edge1, Edge2)**: Running BGP (AS 65001 and AS 65002)
- **2 Access Switches (SW1, SW2)**: Providing VLAN access for hosts
- **4 Linux Hosts**: Connected to different VLANs

### Network Diagram

```
                    Edge1 (AS 65001)
                    100.64.1.1/32
                         |
                         | 192.168.1.0/30
                         |
    +--------------------R1--------------------+
    |              1.1.1.1/32                  |
    | 192.168.12.0/30                          | 192.168.13.0/30
    |                                          |
    R2                                         R3
 2.2.2.2/32                                 3.3.3.3/32
    |                                          |
    | 192.168.23.0/30                          | 192.168.3.0/30
    |                                          |
    +------------------------------------------+
                                               |
                                          Edge2 (AS 65002)
                                          100.64.2.1/32

Edge1 <--172.16.12.0/30--> Edge2 (eBGP Peering)

Access Layer:
R1 --- SW1 --- Host1 (VLAN 10: 10.10.10.10/24)
           \--- Host2 (VLAN 20: 10.10.20.10/24)

R3 --- SW2 --- Host3 (VLAN 10: 10.20.10.10/24)
           \--- Host4 (VLAN 20: 10.20.20.10/24)
```

## IP Addressing Scheme

### OSPF Core (Area 0)
- R1-R2 Link: 192.168.12.0/30
- R2-R3 Link: 192.168.23.0/30
- R3-R1 Link: 192.168.13.0/30
- R1-Edge1 Link: 192.168.1.0/30
- R3-Edge2 Link: 192.168.3.0/30

### Loopbacks (OSPF Router IDs)
- R1: 1.1.1.1/32
- R2: 2.2.2.2/32
- R3: 3.3.3.3/32
- Edge1: 10.0.1.1/32
- Edge2: 10.0.2.1/32

### BGP Edge
- Edge1-Edge2 Link: 172.16.12.0/30
- Edge1 External Network: 100.64.1.1/32 (AS 65001)
- Edge2 External Network: 100.64.2.1/32 (AS 65002)

### VLANs
- **VLAN 10** (Users):
  - SW1 Gateway: 10.10.10.1/24 (on R1)
  - SW2 Gateway: 10.20.10.1/24 (on R3)
  - Host1: 10.10.10.10/24
  - Host3: 10.20.10.10/24

- **VLAN 20** (Servers):
  - SW1 Gateway: 10.10.20.1/24 (on R1)
  - SW2 Gateway: 10.20.20.1/24 (on R3)
  - Host2: 10.10.20.10/24
  - Host4: 10.20.20.10/24

## Lab Exercises

### Part 1: Inter-VLAN Routing

#### Exercise 1.1: Verify VLAN Configuration
1. Connect to SW1 and verify VLAN configuration:
```bash
ssh admin@sw1
show vlan
show interfaces status
```

2. Verify trunk configuration to R1:
```bash
show interfaces trunk
```

3. Test connectivity between hosts on the same VLAN:
```bash
# From your terminal
docker exec -it clab-Layer-3-Part1-host1 ping 10.10.10.1
```

#### Exercise 1.2: Test Inter-VLAN Routing
1. From Host1 (VLAN 10), ping Host2 (VLAN 20):
```bash
docker exec -it clab-Layer-3-Part1-host1 ping 10.10.20.10
```

2. Verify the routing table on R1:
```bash
ssh admin@r1
show ip route
```

3. Check which interface the traffic uses:
```bash
show ip route 10.10.20.10
```

### Part 2: OSPF Routing

#### Exercise 2.1: Verify OSPF Neighbors
1. Check OSPF neighbors on R1:
```bash
ssh admin@r1
show ip ospf neighbor
```

Expected output should show R2 and R3 as neighbors.

2. Verify OSPF database:
```bash
show ip ospf database
```

3. Check OSPF interface status:
```bash
show ip ospf interface brief
```

#### Exercise 2.2: Verify OSPF Routes
1. Check the routing table on R2:
```bash
ssh admin@r2
show ip route ospf
```

You should see routes to all VLAN networks and loopbacks.

2. Trace the path from Host1 to R2's loopback:
```bash
docker exec -it clab-Layer-3-Part1-host1 traceroute 2.2.2.2
```

#### Exercise 2.3: OSPF Convergence Test
1. Check current path from R1 to R3:
```bash
ssh admin@r1
show ip route 3.3.3.3
```

2. Shutdown the direct link between R1 and R3:
```bash
configure
interface Ethernet2
shutdown
exit
```

3. Verify OSPF reconverges and uses alternate path through R2:
```bash
show ip route 3.3.3.3
show ip ospf neighbor
```

4. Re-enable the interface:
```bash
configure
interface Ethernet2
no shutdown
exit
```

### Part 3: BGP Routing

#### Exercise 3.1: Verify BGP Peering
1. Check BGP neighbors on Edge1:
```bash
ssh admin@edge1
show ip bgp summary
```

2. Verify BGP routes received:
```bash
show ip bgp
```

You should see the 100.64.2.1/32 route from Edge2.

3. Check detailed BGP neighbor information:
```bash
show ip bgp neighbors 172.16.12.2
```

#### Exercise 3.2: BGP Route Advertisement
1. On Edge1, verify advertised routes:
```bash
ssh admin@edge1
show ip bgp neighbors 172.16.12.2 advertised-routes
```

2. On Edge2, verify received routes:
```bash
ssh admin@edge2
show ip bgp neighbors 172.16.12.1 routes
```

#### Exercise 3.3: BGP and OSPF Redistribution
1. Check if BGP routes are redistributed into OSPF on Edge1:
```bash
ssh admin@edge1
show ip route bgp
show run section ospf
```

2. On R1, verify if external BGP routes appear:
```bash
ssh admin@r1
show ip route
```

Look for routes to 100.64.1.1 and 100.64.2.1.

3. Test connectivity from Host1 to Edge2's external network:
```bash
docker exec -it clab-Layer-3-Part1-host1 ping 100.64.2.1
```

### Part 4: Advanced Troubleshooting

#### Exercise 4.1: End-to-End Connectivity
1. Test connectivity from Host1 to all other hosts:
```bash
docker exec -it clab-Layer-3-Part1-host1 ping -c 3 10.10.20.10  # Host2
docker exec -it clab-Layer-3-Part1-host1 ping -c 3 10.20.10.10  # Host3
docker exec -it clab-Layer-3-Part1-host1 ping -c 3 10.20.20.10  # Host4
```

2. Trace the path to different destinations:
```bash
docker exec -it clab-Layer-3-Part1-host1 traceroute 10.20.10.10
docker exec -it clab-Layer-3-Part1-host1 traceroute 100.64.2.1
```

#### Exercise 4.2: Routing Protocol Verification
1. Create a comprehensive routing table comparison:
```bash
# On each router, save the routing table
ssh admin@r1 "show ip route" > r1_routes.txt
ssh admin@r2 "show ip route" > r2_routes.txt
ssh admin@r3 "show ip route" > r3_routes.txt
```

2. Verify OSPF LSA propagation:
```bash
ssh admin@r1
show ip ospf database router
show ip ospf database network
```

#### Exercise 4.3: BGP Path Selection
1. On Edge1, check BGP path attributes:
```bash
ssh admin@edge1
show ip bgp 100.64.2.1
```

2. Modify BGP attributes (optional advanced exercise):
```bash
configure
router bgp 65001
neighbor 172.16.12.2 route-map SET_MED out
!
route-map SET_MED permit 10
set metric 100
exit
```

3. Clear BGP session to apply changes:
```bash
clear ip bgp * soft
```

## Lab Commands Reference

### Starting the Lab
```bash
cd labs/Seminar-3
make start
```

### Stopping the Lab
```bash
make stop
```

### Inspecting the Lab
```bash
make inspect
```

### Accessing Devices
```bash
# SSH to switches/routers
ssh admin@<hostname>
# Password: admin (no password required)

# Access Linux hosts
docker exec -it clab-Layer-3-Part1-<hostname> sh
```

## Verification Checklist

- [ ] All OSPF neighbors are in FULL state
- [ ] All BGP peers are in Established state
- [ ] Inter-VLAN routing works (hosts in different VLANs can ping each other)
- [ ] OSPF routes are present in routing tables
- [ ] BGP routes are exchanged between Edge1 and Edge2
- [ ] BGP routes are redistributed into OSPF
- [ ] End-to-end connectivity from hosts to external networks (100.64.x.x)
- [ ] OSPF convergence works when links fail

## Learning Objectives

After completing this lab, you should understand:
1. How to configure and verify Inter-VLAN routing using SVIs
2. How OSPF establishes neighbor relationships and exchanges routes
3. How BGP peers establish sessions and exchange routes
4. The difference between IGP (OSPF) and EGP (BGP)
5. How to redistribute routes between routing protocols
6. How to troubleshoot Layer-3 connectivity issues
7. How routing protocols converge after topology changes

## Troubleshooting Tips

- **No OSPF neighbors**: Check interface IP addresses, OSPF area configuration, and network types
- **No BGP peering**: Verify neighbor IP addresses, AS numbers, and IP connectivity
- **No inter-VLAN routing**: Check VLAN configuration, trunk ports, and SVI IP addresses
- **Routing loops**: Verify routing protocol metrics and redistribution configuration
- **No connectivity**: Use `traceroute` to identify where packets are dropped

