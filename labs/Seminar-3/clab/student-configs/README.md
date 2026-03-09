# Student Lab Configurations

This directory contains pre-configured startup files for the **Student Lab Guide** exercise.

## 📁 Files

- **r2.cfg** - R2 configuration with interfaces configured, OSPF to be configured by student
- **edge2.cfg** - Edge2 configuration with interfaces configured, OSPF and BGP to be configured by student

## 🎯 Purpose

These configurations are used for the **STUDENT_LAB_GUIDE.md** exercise where students:
1. Configure OSPF entirely on R2
2. Configure BGP on Edge2

All other devices (R1, R3, Edge1, SW1, SW2) use the full configurations from `../init-configs/`.

## 🚀 How to Use

### Option 1: Use with Modified Topology (Recommended for Student Lab)

Create a student-specific topology file that uses these configs for R2 and Edge2:

```yaml
# In topology-student.clab.yml
nodes:
  r2:
    startup-config: student-configs/r2.cfg
  edge2:
    startup-config: student-configs/edge2.cfg
  # All other nodes use init-configs
```

### Option 2: Manual Deployment

1. Deploy the lab normally:
```bash
make start
```

2. Copy the student configs to the running containers:
```bash
# For R2
docker cp clab/student-configs/r2.cfg r2:/tmp/student-config.txt

# For Edge2
docker cp clab/student-configs/edge2.cfg edge2:/tmp/student-config.txt
```

3. On each device, load the config:
```bash
ssh admin@r2
configure replace file:/tmp/student-config.txt
```

### Option 3: Reset Specific Devices

If you want to reset just R2 and Edge2 during the lab:

```bash
# SSH to the device
ssh admin@r2

# Enter configuration mode
configure terminal

# Remove OSPF configuration
no router ospf 1

# Remove OSPF from interfaces
interface Ethernet1
   no ip ospf network
   no ip ospf area
   exit

interface Ethernet2
   no ip ospf network
   no ip ospf area
   exit

interface Loopback0
   no ip ospf area
   exit

# Save
write memory
```

## 📝 What's Pre-Configured

### R2 (r2.cfg)
✅ **Configured:**
- Hostname: r2
- Management access (SSH, API)
- Interface IP addresses:
  - Ethernet1: 192.168.12.2/30 (Link to R1)
  - Ethernet2: 192.168.23.1/30 (Link to R3)
  - Loopback0: 2.2.2.2/32
- IP routing enabled

❌ **NOT Configured (Student Task):**
- OSPF process
- OSPF router-id
- OSPF area assignments on interfaces
- OSPF network types

### Edge2 (edge2.cfg)
✅ **Configured:**
- Hostname: edge2
- Management access (SSH, API)
- Interface IP addresses:
  - Ethernet1: 192.168.3.2/30 (Link to R3)
  - Ethernet2: 172.16.12.2/30 (Link to Edge1)
  - Loopback0: 10.0.2.1/32
  - Loopback100: 100.64.2.1/32 (External network)
- IP routing enabled

❌ **NOT Configured (Student Task):**
- OSPF process
- OSPF router-id
- OSPF area assignments on interfaces
- OSPF network types
- BGP process
- BGP AS number
- BGP neighbor configuration
- BGP network advertisement
- BGP route redistribution into OSPF

## 🔍 Verification

After students complete their configuration, they should verify:

### R2 Verification
```bash
# Should show 2 OSPF neighbors (R1 and R3)
show ip ospf neighbor

# Should show OSPF routes
show ip route ospf

# Should be able to ping all loopbacks
ping 1.1.1.1 source 2.2.2.2
ping 3.3.3.3 source 2.2.2.2
```

### Edge2 Verification
```bash
# Should show BGP neighbor in Established state
show ip bgp summary

# Should show BGP routes
show ip bgp

# Should show OSPF neighbors
show ip ospf neighbor

# Should be able to ping Edge1's external network
ping 100.64.1.1 source 100.64.2.1
```

## 📚 Related Files

- **[STUDENT_LAB_GUIDE.md](../../STUDENT_LAB_GUIDE.md)** - Complete student lab guide with step-by-step instructions
- **[../init-configs/](../init-configs/)** - Full configurations for all devices (reference/solution)
- **[../../README.md](../../README.md)** - Main lab documentation

## 💡 Tips for Instructors

1. **Pre-Lab Setup**: Deploy the lab with student configs before class
2. **Checkpoints**: Have students verify each section before moving on
3. **Common Issues**: 
   - Forgetting to configure `ip ospf area` on interfaces
   - Wrong AS numbers in BGP
   - Forgetting to activate BGP neighbors in address-family
4. **Time Estimate**: 
   - OSPF configuration: 15-20 minutes
   - BGP configuration: 20-25 minutes
   - Verification and testing: 15-20 minutes
   - Total: ~60 minutes

## 🎓 Learning Objectives

Students will learn:
- How to configure OSPF from scratch
- How to verify OSPF neighbor adjacencies
- How to configure eBGP peering
- How to redistribute routes between protocols
- How to troubleshoot routing issues
- How to verify end-to-end connectivity

---

**Note**: These configurations are designed to work with the topology defined in `../topology.clab.yml`. All other devices (R1, R3, Edge1, SW1, SW2, hosts) should use their full configurations from `../init-configs/`.

