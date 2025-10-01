# Branch Protection Policy (suggested)
- main: require PR, at least 1 review, CI checks passing, linear history.
- No force pushes to main; only Integrator merges.
- Status checks: black, ruff, mypy, unit, acceptance, coverage, build, pip-audit.

