CURRENT_DIR := $(shell pwd)

.PHONY: help
help: ## Display help message
	@grep -E '^[0-9a-zA-Z_-]+\.*[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: start
start: ## Deploy the lab
	sudo containerlab deploy --debug --topo "$(CURRENT_DIR)/clab/topology.clab.yml" --max-workers 10 --timeout 5m --reconfigure

.PHONY: stop
stop: ## Destroy the lab
	sudo containerlab destroy --debug --topo "$(CURRENT_DIR)/clab/topology.clab.yml" --cleanup

.PHONY: inspect
inspect: ## Inspect the lab
	@sudo containerlab inspect --topo "$(CURRENT_DIR)/clab/topology.clab.yml"
	@echo ""
	@echo "You can check the lab status, hostnames and management addresses above."
	@echo "To connect to a lab device use \`ssh admin@<hostname>\` and password \`admin\`."

.PHONY: start-student
start-student: ## Deploy the student lab (R2 and Edge2 need configuration)
	sudo containerlab deploy --debug --topo "$(CURRENT_DIR)/clab/topology-student.clab.yml" --max-workers 10 --timeout 5m --reconfigure
	@echo ""
	@echo "=========================================="
	@echo "STUDENT LAB DEPLOYED"
	@echo "=========================================="
	@echo ""
	@echo "📚 See STUDENT_LAB_GUIDE.md for instructions"
	@echo ""
	@echo "⚠️  R2 and Edge2 need configuration:"
	@echo "   - R2: Configure OSPF"
	@echo "   - Edge2: Configure BGP and OSPF"
	@echo ""
	@echo "✅ All other devices are pre-configured"
	@echo ""

.PHONY: stop-student
stop-student: ## Destroy the student lab
	sudo containerlab destroy --debug --topo "$(CURRENT_DIR)/clab/topology-student.clab.yml" --cleanup

.PHONY: inspect-student
inspect-student: ## Inspect the student lab
	@sudo containerlab inspect --topo "$(CURRENT_DIR)/clab/topology-student.clab.yml"
	@echo ""
	@echo "You can check the lab status, hostnames and management addresses above."
	@echo "To connect to a lab device use \`ssh admin@<hostname>\` and password \`admin\`."

.PHONY: clean
clean: ## Clean up all lab artifacts
	sudo containerlab destroy --debug --topo "$(CURRENT_DIR)/clab/topology.clab.yml" --cleanup || true
	sudo containerlab destroy --debug --topo "$(CURRENT_DIR)/clab/topology-student.clab.yml" --cleanup || true
	@echo "All lab artifacts cleaned up"