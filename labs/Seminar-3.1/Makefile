.PHONY: start stop start-student help status logs

# Default target
help:
	@echo "╔══════════════════════════════════════════════════════════════════════════════╗"
	@echo "║                    Layer-3 Advanced Routing Lab                              ║"
	@echo "╚══════════════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "Available targets:"
	@echo "  make start         - Deploy the fully configured lab (all routing configured)"
	@echo "  make start-student - Deploy the student lab (routing NOT configured)"
	@echo "  make stop          - Stop and remove the lab"
	@echo "  make status        - Show lab status"
	@echo "  make logs          - Show containerlab logs"
	@echo ""
	@echo "Quick Start:"
	@echo "  1. Deploy student lab:  make start-student"
	@echo "  2. Follow the guide:    STUDENT_LAB_GUIDE.md"
	@echo "  3. Clean up:            make stop"
	@echo ""

# Start the fully configured lab
start:
	@echo "╔══════════════════════════════════════════════════════════════════════════════╗"
	@echo "║              Deploying Layer-3 Advanced Lab (Fully Configured)              ║"
	@echo "╚══════════════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "⏳ Starting containerlab topology..."
	@cd clab && sudo containerlab deploy -t topology.clab.yml
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════════════════════╗"
	@echo "║                          Lab Deployed Successfully!                          ║"
	@echo "╚══════════════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📋 Lab Information:"
	@echo "  • Topology: Layer-3-Advanced-Lab"
	@echo "  • Mode: Fully Configured (all routing protocols configured)"
	@echo ""
	@echo "🔐 Device Access (SSH):"
	@echo "  • ISP:   ssh admin@isp   (password: admin)"
	@echo "  • EDGE:  ssh admin@edge  (password: admin)"
	@echo "  • R1:    ssh admin@r1    (password: admin)"
	@echo "  • R2:    ssh admin@r2    (password: admin)"
	@echo ""
	@echo "🐧 Linux Hosts (Docker exec):"
	@echo "  • CLIENT: docker exec -it clab-Layer-3-Advanced-Lab-client sh"
	@echo "  • SITE1:  docker exec -it clab-Layer-3-Advanced-Lab-site1 sh"
	@echo "  • SITE2:  docker exec -it clab-Layer-3-Advanced-Lab-site2 sh"
	@echo ""
	@echo "✅ All routing protocols are pre-configured and working!"
	@echo ""

# Start the student lab (routing not configured)
start-student:
	@echo "╔══════════════════════════════════════════════════════════════════════════════╗"
	@echo "║              Deploying Layer-3 Advanced Lab (Student Mode)                  ║"
	@echo "╚══════════════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "⏳ Starting containerlab topology..."
	@cd clab && sudo containerlab deploy -t topology-student.clab.yml
	@echo ""
	@echo "╔══════════════════════════════════════════════════════════════════════════════╗"
	@echo "║                          Lab Deployed Successfully!                          ║"
	@echo "╚══════════════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📋 Lab Information:"
	@echo "  • Topology: Layer-3-Advanced-Lab-Student"
	@echo "  • Mode: Student (routing protocols NOT configured - your task!)"
	@echo ""
	@echo "🔐 Device Access (SSH):"
	@echo "  • ISP:   ssh admin@isp   (password: admin)"
	@echo "  • EDGE:  ssh admin@edge  (password: admin)"
	@echo "  • R1:    ssh admin@r1    (password: admin)"
	@echo "  • R2:    ssh admin@r2    (password: admin)"
	@echo ""
	@echo "🐧 Linux Hosts (Docker exec):"
	@echo "  • CLIENT: docker exec -it clab-Layer-3-Advanced-Lab-Student-client sh"
	@echo "  • SITE1:  docker exec -it clab-Layer-3-Advanced-Lab-Student-site1 sh"
	@echo "  • SITE2:  docker exec -it clab-Layer-3-Advanced-Lab-Student-site2 sh"
	@echo ""
	@echo "📚 Next Steps:"
	@echo "  1. Open STUDENT_LAB_GUIDE.md for detailed instructions"
	@echo "  2. Configure OSPF on R1 and R2 (Task 1)"
	@echo "  3. Configure OSPF on EDGE (Task 2)"
	@echo "  4. Configure BGP on EDGE and ISP (Task 3)"
	@echo ""
	@echo "⚠️  Routing protocols are NOT configured - you need to configure them!"
	@echo ""

# Stop and remove the lab
stop:
	@echo "╔══════════════════════════════════════════════════════════════════════════════╗"
	@echo "║                        Stopping Layer-3 Advanced Lab                         ║"
	@echo "╚══════════════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "⏳ Destroying containerlab topology..."
	@cd clab && sudo containerlab destroy -t topology.clab.yml --cleanup || true
	@cd clab && sudo containerlab destroy -t topology-student.clab.yml --cleanup || true
	@echo ""
	@echo "✅ Lab stopped and cleaned up successfully!"
	@echo ""

# Show lab status
status:
	@echo "╔══════════════════════════════════════════════════════════════════════════════╗"
	@echo "║                        Layer-3 Advanced Lab Status                           ║"
	@echo "╚══════════════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@sudo containerlab inspect --all || echo "No labs running"
	@echo ""

# Show containerlab logs
logs:
	@echo "╔══════════════════════════════════════════════════════════════════════════════╗"
	@echo "║                      Containerlab Deployment Logs                            ║"
	@echo "╚══════════════════════════════════════════════════════════════════════════════╝"
	@echo ""
	@cd clab && sudo containerlab inspect --all
	@echo ""

