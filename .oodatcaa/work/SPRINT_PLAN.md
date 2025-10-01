# Sprint Plan (AGENT-GENERATED)

> **This file is managed by agents.** The Negotiator assigns work to agents based on capacity and priorities.

**Status:** Sprint planning triggered — Launch Sprint Planner to generate Sprint 1

---

## Current Sprint Assignments

*Sprint Planner needed to create Sprint 1 based on OBJECTIVE.md*
*Once sprint is created, work assignments will appear here.*

---

## Example Sprint Plan (What Agents Generate)

```markdown
# Sprint Plan — Sprint 1 (Foundation)

## Active Assignments (WIP: 3/6)
- **Planner-A:** Creating AGENT_PLAN.md for W002 (CLI entry point)
- **Builder-A:** Implementing W001 (project structure) — Step 1/3
- **Builder-B:** Implementing W004 (file discovery) — Step 2/2
- **Tester-A:** Waiting for tasks (0 awaiting_test)
- **Integrator-A:** Idle
- **Negotiator:** Coordinating (heartbeat every 20min)

## Queue Status
- Ready: 1 task (W003)
- Needs plan: 0 tasks
- In progress: 3 tasks (W001, W002, W004)
- Awaiting test: 0 tasks
- Blocked: 0 tasks

## Sprint Progress
- Completed: 0/4 tasks (0%)
- Exit criteria: 0/5 met
- Estimated completion: On track for Oct 8

## Next Actions
- W003 will be assigned to Builder-A after W001 completes
- Tester-A will activate when first task reaches "awaiting_test"
```

---

## Role Responsibilities

**Negotiator (You):**
- Coordinates all other agents
- Manages sprint lifecycle
- Assigns work based on WIP limits
- Detects and resolves blockers

**Sprint Planner (Autonomous):**
- Generates sprint goals from OBJECTIVE.md
- Creates backlog items
- Detects project completion

**Planner (Autonomous):**
- Takes tasks marked "needs_plan"
- Creates detailed AGENT_PLAN.md
- Defines test plan and acceptance criteria

**Builder (1-3 parallel):**
- Takes tasks marked "ready"
- Implements on feature branches
- Runs gates (black/ruff/mypy/tests)
- Pushes code for testing

**Tester (1-2 parallel):**
- Takes tasks marked "awaiting_test"
- Validates acceptance criteria
- Checks performance benchmarks
- Approves or sends back to Builder

**Refiner (on-demand):**
- Takes tasks marked "needs_adapt"
- Decides: quick fix vs rollback
- Updates plan if needed

**Integrator (1):**
- Takes tasks marked "ready_for_integrator"
- Opens/merges PRs
- Updates CHANGELOG
- Tags releases

---

## WIP Limits (Configurable in SPRINT_QUEUE.json)
- Planner: 1
- Builder: 3 (parallel work)
- Tester: 2
- Refiner: 1
- Integrator: 1

*Negotiator enforces these limits to prevent overload*

