# Minimal Configurations

This directory contains minimal starting configurations for the Layer-4 lab routers.

## Purpose

These configurations provide a clean starting point for students who want to build the lab from scratch following the BUILD_GUIDE.md.

## What's Included

Each router configuration includes only:
- Basic AAA and management settings
- Hostname
- IP routing enabled
- All interfaces in shutdown state
- No IP addresses configured
- No OSPF configuration

## What's NOT Included

Students will need to configure:
- IP addresses on all interfaces
- Loopback interfaces
- OSPF routing protocol
- OSPF areas and router IDs
- Passive interfaces
- Point-to-point network types

## Using Minimal Configs

### Option 1: Start Lab with Minimal Configs

Edit the topology file to use minimal configs:

```bash
cd labs/Seminar-4
# Edit clab/topology.clab.yml
# Change: startup-config: init-configs/<router>.cfg
# To:     startup-config: minimal-configs/<router>.cfg
```

Then start the lab:
```bash
make start
```

### Option 2: Copy Minimal Configs After Starting

```bash
# Start lab with full configs
make start

# Copy minimal config to running config
ssh admin@external-access
configure
copy file:minimal-configs/external-access.cfg running-config
```

## Files

- `external-access.cfg` - Minimal config for external-access router
- `core.cfg` - Minimal config for core router
- `services.cfg` - Minimal config for services router
- `internal-access.cfg` - Minimal config for internal-access router

## Next Steps

After starting with minimal configs, follow the **BUILD_GUIDE.md** in the parent directory for step-by-step configuration instructions.

## Switching Back to Full Configs

To use the pre-built configurations:

```bash
# Edit clab/topology.clab.yml
# Change: startup-config: minimal-configs/<router>.cfg
# To:     startup-config: init-configs/<router>.cfg

# Restart the lab
make stop
make start
```


