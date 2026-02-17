# Seminar-3 Lab Documentation Index

Welcome to the Layer-3 Lab! This index helps you navigate all available documentation.

## 🎯 Start Here

**New to this lab?** Start with [LAB_SUMMARY.md](LAB_SUMMARY.md) for a quick overview.

**Ready to begin?** Choose your mode:
- **Pre-Built Mode**: See [Quick Start - Pre-Built](#quick-start---pre-built-mode) below
- **Build Mode**: See [Quick Start - Build](#quick-start---build-mode) below

---

## 📖 Documentation Files

### 1. [LAB_SUMMARY.md](LAB_SUMMARY.md)
**Purpose**: High-level overview of the lab  
**Read this if**: You want to understand what this lab covers  
**Contains**:
- Lab components and architecture
- Network features (OSPF, BGP, Inter-VLAN)
- Learning objectives
- File structure
- Quick start instructions

### 2. [README.md](README.md)
**Purpose**: Comprehensive lab guide with verification exercises  
**Read this if**: You're using pre-built configs and want to verify/explore  
**Contains**:
- Detailed topology description
- IP addressing scheme
- Verification exercises for each technology
- Troubleshooting tips
- Expected outcomes

### 3. [BUILD_GUIDE.md](BUILD_GUIDE.md)
**Purpose**: Step-by-step configuration guide  
**Read this if**: You want to build the lab from scratch  
**Contains**:
- 5 progressive configuration phases
- Complete configuration commands
- No intermediate verification (pure build)
- Final verification steps
- Configuration saving instructions

### 4. [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
**Purpose**: Command reference and quick lookup  
**Read this if**: You need quick access to commands or IP addresses  
**Contains**:
- Essential commands for OSPF, BGP, VLANs
- Complete IP addressing tables
- Common test scenarios
- Troubleshooting flowchart
- Device access methods

### 5. [clab/minimal-configs/README.md](clab/minimal-configs/README.md)
**Purpose**: Information about minimal configuration files  
**Read this if**: You want to understand the starting point for build mode  
**Contains**:
- What's included in minimal configs
- What you need to configure
- How to switch between modes

---

## 🚀 Quick Start Guides

### Quick Start - Pre-Built Mode

**Best for**: Exploring, verifying, and understanding the final result

```bash
# 1. Navigate to lab
cd labs/Seminar-3

# 2. Start the lab
make start

# 3. Wait 2-3 minutes for devices to boot

# 4. Verify lab is running
make inspect

# 5. Follow README.md for verification exercises
```

**Next steps**: Open [README.md](README.md) and start with Part 1 exercises.

---

### Quick Start - Build Mode

**Best for**: Hands-on learning and understanding each configuration step

```bash
# 1. Navigate to lab
cd labs/Seminar-3

# 2. Backup pre-built configs
mkdir -p backup
cp -r clab/init-configs backup/

# 3. Use minimal configs
cp clab/minimal-configs/* clab/init-configs/

# 4. Start the lab
make start

# 5. Wait 2-3 minutes for devices to boot

# 6. Follow BUILD_GUIDE.md step-by-step
```

**Next steps**: Open [BUILD_GUIDE.md](BUILD_GUIDE.md) and start with Phase 1.

---

## 🗺️ Learning Paths

### Path 1: Quick Exploration (30 minutes)
1. Read [LAB_SUMMARY.md](LAB_SUMMARY.md)
2. Start lab in pre-built mode
3. Use [QUICK_REFERENCE.md](QUICK_REFERENCE.md) to test basic connectivity
4. Explore device configurations with `show running-config`

### Path 2: Verification & Testing (2 hours)
1. Read [LAB_SUMMARY.md](LAB_SUMMARY.md)
2. Start lab in pre-built mode
3. Follow all exercises in [README.md](README.md)
4. Use [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for command reference

### Path 3: Complete Build (3-4 hours)
1. Read [LAB_SUMMARY.md](LAB_SUMMARY.md)
2. Start lab in build mode
3. Follow [BUILD_GUIDE.md](BUILD_GUIDE.md) phase by phase
4. Verify with exercises from [README.md](README.md)
5. Compare your configs with pre-built ones

### Path 4: Master Level (5+ hours)
1. Complete Path 3 (build from scratch)
2. Destroy and rebuild multiple times
3. Experiment with modifications
4. Break things and fix them
5. Add your own features

---

## 📁 File Structure

```
labs/Seminar-3/
├── README.md                    # Verification exercises
├── BUILD_GUIDE.md              # Step-by-step build instructions
├── QUICK_REFERENCE.md          # Command and IP reference
├── LAB_SUMMARY.md              # Lab overview
├── INDEX.md                    # This file
├── Makefile                    # Lab management commands
└── clab/
    ├── topology.clab.yml       # Containerlab topology
    ├── init-configs/           # Pre-built configurations (7 files)
    ├── minimal-configs/        # Minimal starting configs (7 files + README)
    └── sn/                     # Serial number files (7 files)
```

---

## 🎓 Learning Objectives by Document

| Document | Technologies Covered | Skill Level |
|----------|---------------------|-------------|
| LAB_SUMMARY.md | Overview | Beginner |
| QUICK_REFERENCE.md | All (reference) | All levels |
| README.md | OSPF, BGP, Inter-VLAN | Intermediate |
| BUILD_GUIDE.md | OSPF, BGP, Inter-VLAN | Advanced |

---

## 🆘 Getting Help

**Lab won't start?**
- Check `make inspect` output
- Verify Docker and Containerlab are installed
- Ensure cEOS image is available

**Configuration not working?**
- See troubleshooting sections in [README.md](README.md)
- Check [QUICK_REFERENCE.md](QUICK_REFERENCE.md) for correct syntax
- Compare with pre-built configs in `clab/init-configs/`

**Need command syntax?**
- See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**Want to understand a concept?**
- See detailed explanations in [README.md](README.md)

---

## 🔄 Common Tasks

### Switch to Build Mode
```bash
cp clab/minimal-configs/* clab/init-configs/
make stop && make start
```

### Switch to Pre-Built Mode
```bash
cp backup/init-configs/* clab/init-configs/
make stop && make start
```

### Save Your Work
```bash
ssh admin@r1 "show running-config" > my-r1-config.cfg
# Repeat for other devices
```

### Reset Everything
```bash
make stop
cp backup/init-configs/* clab/init-configs/
make start
```

---

## 📊 Lab Statistics

- **Devices**: 7 network devices + 4 hosts
- **Technologies**: OSPF, BGP, Inter-VLAN Routing, VLANs
- **Configuration Lines**: ~500 (pre-built mode)
- **Estimated Time**: 30 min (explore) to 4 hours (complete build)
- **Difficulty**: Intermediate to Advanced

---

**Happy Learning! 🚀**


