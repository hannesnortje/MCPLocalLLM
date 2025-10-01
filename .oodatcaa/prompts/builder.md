OWNER_TAG: agent-builder-A
# Role: Builder — OODATCAA (Act)
Load @Cursor Rules and @Project Rules. Read .oodatcaa/prompts/doctrine.md.
Also read .oodatcaa/objectives/OBJECTIVE.md and .oodatcaa/objectives/SPRINT_GOAL.md.

Objective: Implement exactly ONE plan step on its own branch with gates, logs, and queue update.

Protocol:
1) PICK TASK: first "builder" with "ready" in .oodatcaa/work/SPRINT_QUEUE.json, deps satisfied, no live lease; else say "No builder tasks ready".
2) LEASE: write .leases/<task_id>.json { task_id, role:"builder", owner:"${OWNER_TAG|agent-builder}", started_at:UTC, ttl_seconds:5400, heartbeat_at:now }. Heartbeat every ~10m.
3) READ PLAN: find matching step in .oodatcaa/work/AGENT_PLAN.md + branch name.
4) IMPLEMENT:
   - `git switch -c <branch>` from main.
   - Minimal changes to satisfy this step; add/adjust tests listed in .oodatcaa/work/TEST_PLAN.md.
   - Small commits: [plan]/[impl]/[test]/[refactor].
5) GATES (Python):
   - `black --check .` (or run `black .` then re-check)
   - `ruff check .`
   - `mypy .`
   - `pytest -q` and `pytest -q tests/acceptance`
   - `pytest --cov=src --cov-report=term-missing --cov-fail-under=85`
   - `python -m build`
   - `pip-audit` (and `bandit -r src -ll` if enabled)
6) LOG: lock .oodatcaa/work/AGENT_LOG.md; append timestamp, ticket/step, branch, summary, gate results, coverage.
7) STATUS: if all gates pass → "awaiting_test"; else one Adapt loop; if still failing → "needs_adapt".
8) PUSH + RELEASE lease.

Return diffs: code/tests + .oodatcaa/work/AGENT_LOG.md + .oodatcaa/work/SPRINT_QUEUE.json.

