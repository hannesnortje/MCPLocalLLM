.PHONY: fmt gates test check build audit ship tag rollback validate-env agents-start agents-stop agents-restart agents-status

validate-env:
	python3 scripts/validate-env.py

fmt:
	black .

gates:
	black --check . && ruff check . && mypy .

test:
	pytest -q && pytest -q tests/acceptance

check: gates test
	pytest --cov=src --cov-report=term-missing --cov-fail-under=85

build:
	python -m build

audit:
	pip-audit || true
	# optional
	# bandit -r src -ll || true

ship:
	git push -u origin HEAD

tag:
	@[ -n "$(TICKET)" ] || (echo "Set TICKET=W123"; exit 1)
	git tag pre/$(TICKET)-$$(date -u +%Y-%m-%dT%H-%M-%S)

rollback:
	@[ -n "$(TAG)" ] || (echo "Set TAG=pre/W123-YYYY-MM-DDTHH-MM-SS"; exit 1)
	git switch main && git reset --hard $(TAG) && git push --force-with-lease

# Agent Daemon Management
agents-start:
	@if command -v systemctl >/dev/null 2>&1 && systemctl --user status >/dev/null 2>&1; then \
		echo "Starting agents via systemd..."; \
		systemctl --user start agent-planner agent-builder agent-tester agent-refiner agent-integrator; \
	else \
		echo "Systemd not available, using fallback mode..."; \
		bash scripts/agents-daemon-cli.sh start; \
	fi

agents-stop:
	@if command -v systemctl >/dev/null 2>&1 && systemctl --user status >/dev/null 2>&1; then \
		echo "Stopping agents via systemd..."; \
		systemctl --user stop agent-planner agent-builder agent-tester agent-refiner agent-integrator; \
	else \
		echo "Systemd not available, using fallback mode..."; \
		bash scripts/agents-daemon-cli.sh stop; \
	fi

agents-restart:
	@if command -v systemctl >/dev/null 2>&1 && systemctl --user status >/dev/null 2>&1; then \
		echo "Restarting agents via systemd..."; \
		systemctl --user restart agent-planner agent-builder agent-tester agent-refiner agent-integrator; \
	else \
		echo "Systemd not available, using fallback mode..."; \
		bash scripts/agents-daemon-cli.sh restart; \
	fi

agents-status:
	@if command -v systemctl >/dev/null 2>&1 && systemctl --user status >/dev/null 2>&1; then \
		echo "Agent daemon status (systemd):"; \
		systemctl --user status agent-planner agent-builder agent-tester agent-refiner agent-integrator --no-pager || true; \
	else \
		echo "Systemd not available, using fallback mode..."; \
		bash scripts/agents-daemon-cli.sh status; \
	fi

