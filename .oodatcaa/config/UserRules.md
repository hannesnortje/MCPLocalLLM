# OODATCAA Multi-Agent Doctrine (Global) — Autonomous Mode

Core Loop: Observe → Orient → Decide → Act → Test → Check → Adapt → Archive

## Autonomous Operation
User provides ONLY: `.oodatcaa/objectives/OBJECTIVE.md` (product vision + success criteria)
Agents autonomously: plan sprints, break down work, execute, test, integrate, and detect completion.

## Agent Roles

**Coordination Layer (Autonomous):**
- **Negotiator:** Control plane. Manages sprint lifecycle, coordinates all agents, enforces WIP, detects completion.
- **Sprint Planner:** Generates sprint goals from OBJECTIVE.md, estimates timeline, decides when project complete.

**Development Layer (Executed by Negotiator):**
- **Planner:** Observe+Orient+Decide. Produces AGENT_PLAN.md and TEST_PLAN.md (DoD + ACs).
- **Builder:** Act per plan step in its own branch. Commits labeled: [plan],[impl],[test],[refactor].
- **Tester:** Test+Check. Runs gates, adds missing tests, evaluates ACs.
- **Refiner:** Adapt. Chooses quick fix vs rollback (Start-Over Gate), revises plan.
- **Integrator:** Archive. PRs, merges, tags, CHANGELOG, docs.

Shared Repo Files:
- .oodatcaa/work/ → SPRINT_BACKLOG.md, SPRINT_PLAN.md, SPRINT_QUEUE.json, AGENT_PLAN.md, TEST_PLAN.md, AGENT_LOG.md, SPRINT_LOG.md
- .oodatcaa/objectives/ → OBJECTIVE.md, SPRINT_GOAL.md, RELEASE_CHECKLIST.md
- .oodatcaa/prompts/ → agent prompt templates
- .leases/ (per-task leases), .locks/ (file locks)

Git Protocol:
- Branch: `feat/<ticket>-step-<n>-<slug>`
- Baseline tag before work: `pre/<ticket>-<ISO8601>`
- Rollback: `git reset --hard <baseline>`; `git push --force-with-lease`
- Prefer one plan step per PR; open PRs early (draft ok)

Negotiation Protocol:
1) Conflicts → propose alternatives in `.oodatcaa/work/SPRINT_DISCUSS.md` (pros/cons).
2) Negotiator picks by: DoD alignment, lowest rollback risk, highest testability.
3) Decision + rationale recorded in `.oodatcaa/work/SPRINT_LOG.md`.

Definition of Done (generic):
- All Acceptance Criteria (functional + non-functional) pass.
- Format/lint/type/tests/coverage/build/security pass.
- Docs/CHANGELOG updated if user-visible or API change.

Background Worker Rules:
- Acquire a lease before work; heartbeat at least every 10 minutes.
- If a lease is stale (heartbeat + ttl expired), another worker may take over and MUST note this in `.oodatcaa/work/AGENT_LOG.md`.
- Lock shared docs before writing (`.locks/<file>.lock`); break locks >5 minutes old and log it; remove locks after writing.

