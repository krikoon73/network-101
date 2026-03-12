# Layer-3 Lab

This lab covers fundamental Layer-3 routing concepts including:
- **Inter-VLAN Routing**: Routing between different VLANs
- **OSPF Routing**: Dynamic routing within an autonomous system
- **BGP Routing**: External routing between different autonomous systems

## Lab topology

```
      CLIENT    
         │      
         │      
        ISP     
         │      
         │      
   +---EDGE---+ 
   │          │ 
   │          │ 
  R1---------R2 
   │          │ 
   │          │ 
SITE1      SITE2
```

- CLIENT - Linux container 
- ISP - CEOS router 
- EDGE - CEOS router 
- R1 - CEOS router 
- R2 - CEOS router 
- SITE1 - Linux container 
- SITE2 - Linux container 

There is:
- eBGP running between ISP and EDGE
- OSPF running between R1, R2 and EDGE
- Static routes between SITE1/SITE2 and CLIENT

## Lab tasks and objectives

What is already configured:
- IP addresses on all interfaces
- Static routes between SITE1/SITE2 and CLIENT
- SITE1 is connected to R1 with VLAN10 on subnet 10.1.10.0/24
- SITE2 is connected to R2 with VLAN10 on subnet 10.2.10.0/24
- VLAN10 is never propagated between R1 and R2
- CLIENT is connected to ISP with VLAN10 on subnet 10.3.10.0/24
- All other connections are /30 subnets belongin to 172.16.100.0/24
- EDGE, ISP, R1 and R2 have loopback interfaces with addresses 172.16.0.1, 172.16.0.2, 172.16.0.3 and 172.16.0.4/32

### Task 1: configure OSPF on R1 and R2

Task1.1: Configure OSPF on R1 and R2 to redistribute static routes learned from SITE1 and SITE2 to EDGE. 
Task1.2: Verify that SITE1 and SITE2 can communicate with each other via ping.

### Task 2: configure OSPF on EDGE

Task2.1: Configure OSPF on EDGE.
Task2.2: Verify that EDGE, R1 and R2 can ping each other's loopback interfaces.
Task2.3: Verify that SITE1 can reach 172.16.0.1 (EDGE) via ping
Task2.4: Verify that SITE2 can reach 172.16.0.1 (EDGE) via ping

### Task 3: configure external BGP on EDGE and on ISP

Task 3.1: Configure eBGP on EDGE and on ISP.
Task 3.2: Capture via Wireshark on EDGE the BGP session establishment.
Task 3.3: Redistribute SITE1 and SITE2 routes into BGP on EDGE.
Task 3.4: Redistribute CLIENT route into BGP on ISP.
Task 3.5: Veryfy routing tables on all devices to verify the routes.
Task 3.6: Verify that SITE1 can reach 10.3.10.10 (CLIENT) via ping and traceroute
Task 3.7: Verify that SITE2 can reach 10.3.10.10 (CLIENT) via ping and traceroute










