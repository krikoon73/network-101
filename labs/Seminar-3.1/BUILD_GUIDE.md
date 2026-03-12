# Layer-3 Advanced Routing Lab - Build Guide

> **👨‍🏫 Instructor Guide**: This document explains the lab structure and how it was built.

## 📁 Lab Structure

```
labs/Seminar-3.1/
├── README.md                    # Original lab requirements
├── STUDENT_LAB_GUIDE.md         # Comprehensive student guide with tasks and tips
├── BUILD_GUIDE.md               # This file - instructor guide
├── Makefile                     # Easy deployment commands
└── clab/
    ├── topology.clab.yml        # Fully configured lab topology
    ├── topology-student.clab.yml # Student lab topology (routing not configured)
    ├── init-configs/            # Fully configured device configs
    │   ├── isp.cfg
    │   ├── edge.cfg
    │   ├── r1.cfg
    │   └── r2.cfg
    └── student-configs/         # Student configs (routing not configured)
        ├── isp.cfg
        ├── edge.cfg
        ├── r1.cfg
        └── r2.cfg
```

## 🏗️ Network Design

### Topology

```
      CLIENT (10.3.10.10/24)
         │      
         │ VLAN 10
        ISP (AS 65001)
         │      
         │ eBGP (172.16.100.0/30)
       EDGE (AS 65000)
       /    \
      /      \
     /        \
   R1 -------- R2 (OSPF Area 0)
    │          │
    │          │
 SITE1      SITE2
(10.1.10.10) (10.2.10.10)
```

### IP Addressing Scheme

| Network | Subnet | Purpose |
|---------|--------|---------|
| 10.1.10.0/24 | SITE1 | R1 VLAN 10 - Site 1 network |
| 10.2.10.0/24 | SITE2 | R2 VLAN 10 - Site 2 network |
| 10.3.10.0/24 | CLIENT | ISP VLAN 10 - Client network |
| 172.16.100.0/30 | ISP-EDGE | eBGP peering link |
| 172.16.100.4/30 | EDGE-R1 | OSPF link |
| 172.16.100.8/30 | EDGE-R2 | OSPF link |
| 172.16.100.12/30 | R1-R2 | OSPF link |
| 172.16.0.1/32 | EDGE Lo0 | EDGE loopback/router-id |
| 172.16.0.2/32 | ISP Lo0 | ISP loopback/router-id |
| 172.16.0.3/32 | R1 Lo0 | R1 loopback/router-id |
| 172.16.0.4/32 | R2 Lo0 | R2 loopback/router-id |

### Routing Protocols

1. **OSPF Area 0**
   - Devices: R1, R2, EDGE
   - Purpose: Internal dynamic routing (IGP)
   - Redistributes: Static routes from R1 and R2

2. **BGP**
   - AS 65000: EDGE
   - AS 65001: ISP
   - Purpose: External routing between autonomous systems (EGP)
   - Redistributes: OSPF routes into BGP on EDGE

3. **Static Routes**
   - R1: 10.1.10.0/24 → Vlan10 (redistributed into OSPF)
   - R2: 10.2.10.0/24 → Vlan10 (redistributed into OSPF)
   - ISP: 10.3.10.0/24 → Vlan10 (advertised in BGP)

## 🎓 Student Learning Objectives

### Task 1: OSPF on R1 and R2
**Skills learned:**
- Configuring OSPF process and router-id
- Adding networks to OSPF areas
- Redistributing static routes into OSPF
- Verifying OSPF adjacencies
- Understanding OSPF route types (O, O E2)

### Task 2: OSPF on EDGE
**Skills learned:**
- Extending OSPF domain to edge routers
- Verifying multi-neighbor OSPF adjacencies
- Understanding OSPF route propagation
- Testing end-to-end connectivity within OSPF domain

### Task 3: BGP on EDGE and ISP
**Skills learned:**
- Configuring eBGP between different AS numbers
- Establishing BGP peering sessions
- Redistributing IGP routes into BGP
- Advertising networks in BGP
- Verifying BGP session state
- Understanding BGP route propagation
- Testing end-to-end connectivity across routing domains

## 🔧 Configuration Differences

### Fully Configured Lab (init-configs/)
- All routing protocols configured
- OSPF running on R1, R2, EDGE
- BGP running on EDGE and ISP
- All redistributions configured
- Full end-to-end connectivity

### Student Lab (student-configs/)
- Only IP addressing configured
- Static routes configured
- NO OSPF configuration
- NO BGP configuration
- Students must configure all routing protocols

## 📝 Key Configuration Points

### R1 and R2 OSPF Configuration
```
router ospf 1
   router-id <loopback-ip>
   network <loopback>/32 area 0.0.0.0
   network <link-to-edge>/30 area 0.0.0.0
   network <link-to-other-router>/30 area 0.0.0.0
   redistribute static
   max-lsa 12000
```

### EDGE OSPF Configuration
```
router ospf 1
   router-id 172.16.0.1
   network 172.16.0.1/32 area 0.0.0.0
   network 172.16.100.4/30 area 0.0.0.0
   network 172.16.100.8/30 area 0.0.0.0
   max-lsa 12000
```

### EDGE BGP Configuration
```
router bgp 65000
   router-id 172.16.0.1
   neighbor 172.16.100.1 remote-as 65001
   redistribute ospf
   address-family ipv4
      neighbor 172.16.100.1 activate
      redistribute ospf
```

### ISP BGP Configuration
```
router bgp 65001
   router-id 172.16.0.2
   neighbor 172.16.100.2 remote-as 65000
   network 10.3.10.0/24
   address-family ipv4
      neighbor 172.16.100.2 activate
```

## ✅ Verification Points

### After Task 1 (OSPF on R1 and R2)
- [ ] R1 and R2 have OSPF adjacency (FULL state)
- [ ] SITE1 can ping SITE2
- [ ] R1 has route to 10.2.10.0/24 (O E2)
- [ ] R2 has route to 10.1.10.0/24 (O E2)

### After Task 2 (OSPF on EDGE)
- [ ] EDGE has 2 OSPF neighbors (R1 and R2)
- [ ] All routers can ping each other's loopbacks
- [ ] EDGE has routes to SITE1 and SITE2 (O E2)
- [ ] SITE1 and SITE2 can ping EDGE loopback

### After Task 3 (BGP on EDGE and ISP)
- [ ] BGP session between EDGE and ISP is Established
- [ ] ISP receives 2 BGP routes (10.1.10.0/24, 10.2.10.0/24)
- [ ] EDGE receives 1 BGP route (10.3.10.0/24)
- [ ] SITE1 can ping CLIENT (10.3.10.10)
- [ ] SITE2 can ping CLIENT (10.3.10.10)
- [ ] Traceroute shows correct path through OSPF and BGP domains

## 🚀 Deployment

### For Students
```bash
cd labs/Seminar-3.1
make start-student
```

### For Instructors (Reference)
```bash
cd labs/Seminar-3.1
make start
```

### Cleanup
```bash
make stop
```

## 📚 Additional Resources

- **STUDENT_LAB_GUIDE.md**: Comprehensive guide with step-by-step instructions, tips, and verification commands
- **README.md**: Original lab requirements and objectives
- **Arista EOS Documentation**: https://www.arista.com/en/support/product-documentation

## 🎯 Expected Outcomes

By completing this lab, students will:
1. Understand OSPF configuration and operation
2. Understand BGP configuration and eBGP peering
3. Understand route redistribution between protocols
4. Be able to troubleshoot multi-protocol routing environments
5. Understand the difference between IGP (OSPF) and EGP (BGP)
6. Gain hands-on experience with enterprise routing scenarios


