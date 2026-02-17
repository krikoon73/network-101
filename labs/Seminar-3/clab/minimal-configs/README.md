# Minimal Configuration Files

These configuration files provide a minimal starting point for building the Layer-3 lab from scratch.

## What's Included

Each device has only:
- Basic AAA configuration (passwordless admin access)
- Management API enabled
- Hostname configured
- Basic system settings
- Interface definitions (unconfigured)

## What's NOT Included (You'll Configure)

- IP addresses on interfaces
- VLAN configuration
- OSPF configuration
- BGP configuration
- Inter-VLAN routing
- Route redistribution

## How to Use

1. Copy these files to the init-configs directory:
   ```bash
   cp clab/minimal-configs/* clab/init-configs/
   ```

2. Deploy the lab:
   ```bash
   make stop  # If already running
   make start
   ```

3. Follow the BUILD_GUIDE.md to configure each phase:
   - Phase 1: Basic device configuration
   - Phase 2: OSPF core network
   - Phase 3: Inter-VLAN routing
   - Phase 4: BGP configuration
   - Phase 5: Verification

## Devices

- **r1.cfg** - Core Router 1 (minimal)
- **r2.cfg** - Core Router 2 (minimal)
- **r3.cfg** - Core Router 3 (minimal)
- **edge1.cfg** - Edge Router 1 (minimal)
- **edge2.cfg** - Edge Router 2 (minimal)
- **sw1.cfg** - Access Switch 1 (minimal)
- **sw2.cfg** - Access Switch 2 (minimal)

## Restoring Pre-Built Configs

To go back to the fully configured lab:

```bash
cp backup/init-configs/* clab/init-configs/
make stop && make start
```

Or if you didn't create a backup:

```bash
# The original configs are in the parent init-configs directory
# Just redeploy without copying minimal configs
```

## Learning Objectives

By building from these minimal configs, you will:
- Understand the complete configuration process
- Learn the order of configuration steps
- Practice troubleshooting configuration issues
- Gain hands-on experience with OSPF and BGP
- Master inter-VLAN routing concepts

## Tips

- Configure one phase at a time
- Verify each phase before moving to the next
- Use `show running-config` to check your work
- Save configurations with `write memory` after each phase
- Don't skip verification steps in the BUILD_GUIDE.md

