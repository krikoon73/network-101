# Layer-3 Lab Quick Reference

## Device Access

### SSH to Network Devices
```bash
ssh admin@r1        # Core Router 1
ssh admin@r2        # Core Router 2
ssh admin@r3        # Core Router 3
ssh admin@edge1     # Edge Router 1 (BGP AS 65001)
ssh admin@edge2     # Edge Router 2 (BGP AS 65002)
ssh admin@sw1       # Access Switch 1
ssh admin@sw2       # Access Switch 2
```
*No password required (configured with nopassword)*

### Access Linux Hosts
```bash
docker exec -it clab-Layer-3-Part1-host1 sh
docker exec -it clab-Layer-3-Part1-host2 sh
docker exec -it clab-Layer-3-Part1-host3 sh
docker exec -it clab-Layer-3-Part1-host4 sh
```

## Essential Commands

### OSPF Verification
```bash
show ip ospf neighbor                    # Check OSPF neighbors
show ip ospf interface brief             # OSPF-enabled interfaces
show ip ospf database                    # OSPF LSDB
show ip route ospf                       # OSPF routes only
show ip ospf neighbor detail             # Detailed neighbor info
```

### BGP Verification
```bash
show ip bgp summary                      # BGP peer status
show ip bgp                              # BGP routing table
show ip bgp neighbors <ip>               # Detailed neighbor info
show ip bgp neighbors <ip> advertised-routes  # Routes sent to peer
show ip bgp neighbors <ip> routes        # Routes received from peer
show ip route bgp                        # BGP routes in routing table
```

### Inter-VLAN Routing
```bash
show vlan                                # VLAN database
show interfaces trunk                    # Trunk port status
show ip interface brief                  # Interface IP addresses
show interfaces status                   # Interface status
show ip route                            # Full routing table
```

### General Troubleshooting
```bash
show running-config                      # Current configuration
show ip interface brief                  # Interface summary
show interfaces <interface>              # Detailed interface info
ping <ip>                                # Test connectivity
traceroute <ip>                          # Trace packet path
show arp                                 # ARP table
show mac address-table                   # MAC address table (switches)
```

## IP Address Summary

### Loopbacks (Router IDs)
| Device | Loopback IP | OSPF Router ID |
|--------|-------------|----------------|
| R1     | 1.1.1.1/32  | 1.1.1.1        |
| R2     | 2.2.2.2/32  | 2.2.2.2        |
| R3     | 3.3.3.3/32  | 3.3.3.3        |
| Edge1  | 10.0.1.1/32 | 10.0.1.1       |
| Edge2  | 10.0.2.1/32 | 10.0.2.1       |

### OSPF Core Links
| Link      | R1 Side       | R2/R3 Side    |
|-----------|---------------|---------------|
| R1-R2     | 192.168.12.1  | 192.168.12.2  |
| R2-R3     | 192.168.23.1  | 192.168.23.2  |
| R3-R1     | 192.168.13.2  | 192.168.13.1  |
| R1-Edge1  | 192.168.1.1   | 192.168.1.2   |
| R3-Edge2  | 192.168.3.1   | 192.168.3.2   |

### BGP Configuration
| Device | AS Number | BGP Peer      | Peer AS | External Network |
|--------|-----------|---------------|---------|------------------|
| Edge1  | 65001     | 172.16.12.2   | 65002   | 100.64.1.1/32    |
| Edge2  | 65002     | 172.16.12.1   | 65001   | 100.64.2.1/32    |

### VLAN Networks
| VLAN | Description | Site 1 Gateway (R1) | Site 2 Gateway (R3) |
|------|-------------|---------------------|---------------------|
| 10   | Users       | 10.10.10.1/24       | 10.20.10.1/24       |
| 20   | Servers     | 10.10.20.1/24       | 10.20.20.1/24       |

### Host IP Addresses
| Host   | IP Address     | VLAN | Default Gateway |
|--------|----------------|------|-----------------|
| Host1  | 10.10.10.10/24 | 10   | 10.10.10.1      |
| Host2  | 10.10.20.10/24 | 20   | 10.10.20.1      |
| Host3  | 10.20.10.10/24 | 10   | 10.20.10.1      |
| Host4  | 10.20.20.10/24 | 20   | 10.20.20.1      |

## Common Test Scenarios

### Test Inter-VLAN Routing
```bash
# From Host1 (VLAN 10) to Host2 (VLAN 20)
docker exec -it clab-Layer-3-Part1-host1 ping 10.10.20.10
```

### Test OSPF Routing
```bash
# From Host1 to R2's loopback
docker exec -it clab-Layer-3-Part1-host1 ping 2.2.2.2

# Traceroute to see OSPF path
docker exec -it clab-Layer-3-Part1-host1 traceroute 10.20.10.10
```

### Test BGP Routing
```bash
# From Host1 to Edge2's external network
docker exec -it clab-Layer-3-Part1-host1 ping 100.64.2.1

# From Host1 to Edge1's external network
docker exec -it clab-Layer-3-Part1-host1 ping 100.64.1.1
```

## Troubleshooting Flowchart

1. **No connectivity between hosts**
   - Check VLAN configuration on switches
   - Verify trunk ports are up
   - Check SVI (VLAN interface) configuration on routers
   - Verify host default gateway configuration

2. **OSPF neighbors not forming**
   - Verify interface IP addresses
   - Check OSPF area configuration
   - Ensure interfaces are not shutdown
   - Verify OSPF network type matches

3. **BGP peers not establishing**
   - Verify IP connectivity between peers
   - Check AS numbers match configuration
   - Verify neighbor IP addresses are correct
   - Check if BGP is enabled on interfaces

4. **Routes not appearing in routing table**
   - Verify routing protocol is advertising the network
   - Check route redistribution configuration
   - Verify no route filtering is applied
   - Check administrative distance

## Lab Management

```bash
# Start the lab
cd labs/Seminar-3
make start

# Check lab status
make inspect

# Stop the lab
make stop

# View help
make help
```

## Expected Outcomes

✅ All OSPF neighbors should be in FULL state  
✅ BGP peers should be in Established state  
✅ All hosts should be able to ping each other  
✅ Hosts should be able to reach external networks (100.64.x.x)  
✅ OSPF should converge within seconds after link failure  
✅ BGP routes should be redistributed into OSPF  


