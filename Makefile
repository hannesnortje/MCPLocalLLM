.PHONY: fmt gates test check build audit ship tag rollback validate-env

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

