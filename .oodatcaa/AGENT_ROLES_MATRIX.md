# Agent Roles Matrix — OODATCAA Multi-Agent System

**Version:** 1.0  
**Last Updated:** 2025-10-04  
**Status:** Active

---

## Overview

This matrix documents the 11 autonomous agents in the OODATCAA development system, including their roles, responsibilities, inputs/outputs, decision authority, success criteria, and Sprint 1/2 usage patterns.

**Agent Types:**
- **Core Development (8 agents):** Negotiator, Sprint Planner, Planner, Builder, Tester, Refiner, Integrator, Project Completion Detector
- **Utilities (3 agents):** Sprint Close, Releaser, Triage

**Evidence Base:**
- **Sprint 1:** 34 tasks completed, 91.9% success rate, 4 adaptation cycles
- **Sprint 2:** 30 tasks planned, 5 completed (P002-B01, P003-B01/B02, P004, P005 planning)

---

## Core Development Agents

### 1. Negotiator (Coordinator)

**Role:** Autonomous Control Plane — Continuous sprint and agent coordination

**OODATCAA Stage:** Observe → Orient (system state) → Decide (task assignment)

**Responsibilities:**
- Sprint lifecycle management (trigger Sprint Planner when needed)
- Work coordination (enforce WIP limits, manage leases, unblock dependencies)
- Sprint progress monitoring (check exit criteria, log heartbeats)
- Adaptive actions (detect issues, optimize bottlenecks, trigger Refiner if needed)
- Agent scaling suggestions

**Inputs:**
- `.oodatcaa/objectives/OBJECTIVE.md` (product goal)
- `.oodatcaa/objectives/SPRINT_GOAL.md` (current sprint)
- `.oodatcaa/work/SPRINT_QUEUE.json` (task status)
- `.oodatcaa/work/SPRINT_PLAN.md` (assignments)
- `.oodatcaa/work/AGENT_LOG.md` (recent activity)
- `.leases/*.json` (active agent work)

**Outputs:**
- Updated `.oodatcaa/work/SPRINT_PLAN.md` (task assignments)
- Updated `.oodatcaa/work/SPRINT_QUEUE.json` (status changes: blocked → ready)
- `.oodatcaa/work/SPRINT_LOG.md` (coordination heartbeats, sprint completions)
- Agent commands (formatted instructions for other agents)
- Stale lease cleanup (lease file deletion, task status reset)

**Decision Authority:**
- **High:** Sprint completion detection, task status transitions (blocked → ready), stale lease takeover
- **Medium:** Agent assignment (round-robin), WIP enforcement, sprint replan suggestions
- **Low:** Cannot change OBJECTIVE.md, cannot modify core agent protocols

**Success Criteria:**
- All agents have work when available
- No deadlocks (circular dependencies)
- WIP limits respected
- Stale leases cleaned up within TTL window
- Sprint completion triggered when all exit criteria met
- Heartbeat logged at regular intervals

**Sprint 1/2 Usage:**
- **Sprint 1:** 5 manual interventions noted in logs (protocol coordination pattern issues addressed in P005)
- **Sprint 2:** Autonomous operation validated with P005 planning (no pre-assignment, agent discovered task autonomously)
- **Typical Cadence:** Continuous operation (checks every 10-15 minutes or on-demand)

**Related Prompts:** [`negotiator.md`](.oodatcaa/prompts/negotiator.md)

---

### 2. Sprint Planner

**Role:** Autonomous Sprint Goal Generation

**OODATCAA Stage:** Orient (objective decomposition) → Decide (sprint scope)

**Responsibilities:**
- Assess current objective completion percentage
- Detect project completion (100% objective achieved)
- Decompose objective into sprint-sized milestones
- Generate sprint goals with exit criteria
- Create sprint backlog (work items for Planner)
- Auto-increment sprint numbers

**Inputs:**
- `.oodatcaa/objectives/OBJECTIVE.md` (user's product vision)
- `.oodatcaa/objectives/SPRINT_GOAL.md` (current/previous sprints)
- `.oodatcaa/work/SPRINT_LOG.md` (shipped features)
- Current objective completion percentage (calculated from success criteria met)

**Outputs:**
- `.oodatcaa/objectives/SPRINT_GOAL.md` (Sprint N goal, exit criteria, timebox, status, progress)
- `.oodatcaa/work/SPRINT_BACKLOG.md` (work items for next sprint)
- `.oodatcaa/objectives/PROJECT_COMPLETION_REPORT.md` (if project 100% complete)
- `.oodatcaa/work/SPRINT_LOG.md` (sprint initialization entry)

**Decision Authority:**
- **High:** Project completion declaration (set status → `project_complete`), sprint goal definition, exit criteria selection
- **Medium:** Sprint scope (1-2 weeks estimation), backlog prioritization, sprint timebox
- **Low:** Cannot modify OBJECTIVE.md, cannot change sprint numbering convention

**Success Criteria:**
- Sprint goal aligns with OBJECTIVE.md
- Exit criteria are specific and testable (3-6 criteria)
- Backlog has enough work for sprint duration
- Dependencies identified
- Sprint number auto-incremented correctly
- Project completion triggered when 100% objective met

**Sprint 1/2 Usage:**
- **Sprint 1:** Generated Sprint 1 goal from OBJECTIVE.md (W001-W008 backlog)
- **Sprint 2:** Generated Sprint 2 goal (P001-P007 backlog, "OODATCAA Process Improvement")
- **Typical Cadence:** Once per sprint (at start or completion of previous sprint)

**Related Prompts:** [`sprint-planner.md`](.oodatcaa/prompts/sprint-planner.md)

---

### 3. Planner

**Role:** Detailed Task Planning — OODATCAA (Observe+Orient+Decide)

**OODATCAA Stage:** Observe (repo inventory) → Orient (alternatives) → Decide (approach selection, plan creation)

**Responsibilities:**
- Pick highest-priority `needs_plan` item from backlog
- Repository inventory (structure, dependencies, tests, CI, standards)
- Evaluate 2-4 alternatives with rationale
- Create detailed AGENT_PLAN.md (traceability, problem, DoD, step-by-step plan)
- Create TEST_PLAN.md (quality gates, acceptance tests, performance benchmarks)
- Enqueue builder/tester subtasks in SPRINT_QUEUE.json
- Generate completion report

**Inputs:**
- `.oodatcaa/objectives/OBJECTIVE.md` (product vision)
- `.oodatcaa/objectives/SPRINT_GOAL.md` (current sprint goal)
- `.oodatcaa/work/SPRINT_BACKLOG.md` (work items needing plans)
- `.oodatcaa/work/SPRINT_QUEUE.json` (task statuses)
- Repository structure (codebase, tests, dependencies)

**Outputs:**
- `.oodatcaa/work/AGENT_PLAN.md` (detailed implementation plan with steps, alternatives, rationale)
- `.oodatcaa/work/TEST_PLAN.md` (quality gates, acceptance criteria, test commands)
- Updated `.oodatcaa/work/SPRINT_QUEUE.json` (builder steps as "ready", tester tasks as "blocked")
- Updated `.oodatcaa/work/SPRINT_PLAN.md` (assignments reflection)
- `.oodatcaa/work/AGENT_LOG.md` (planning entry)
- `.oodatcaa/work/reports/<TASK_ID>/planner.md` (completion report)
- `.oodatcaa/work/AGENT_REPORTS.md` (executive summary)

**Decision Authority:**
- **High:** Alternative selection (approach chosen), plan structure, acceptance criteria definition, task breakdown
- **Medium:** Subtask complexity estimation (S/M/L), dependencies between subtasks, branch naming
- **Low:** Cannot change OBJECTIVE.md, cannot skip quality gates, must follow DoD template

**Success Criteria:**
- AGENT_PLAN.md complete with traceability, problem, DoD, alternatives, step-by-step plan
- TEST_PLAN.md includes all quality gate commands and acceptance tests
- Builder Step 01 marked "ready" (or Step 02 if independent)
- Tester tasks marked "blocked" with dependencies
- All plans have objective/sprint fields
- Completion report generated

**Sprint 1/2 Usage:**
- **Sprint 1:** Planned W001-W008 (34 tasks total)
- **Sprint 2:** Planned P001, P002, P003, P004, P005, P006 (6 planning tasks)
- **Pattern:** P005 used autonomous discovery (no pre-assignment) — protocol coordination fix validated
- **Typical Cadence:** On-demand when backlog items need detailed plans

**Related Prompts:** [`planner.md`](.oodatcaa/prompts/planner.md)

---

### 4. Builder

**Role:** Implementation — OODATCAA (Act)

**OODATCAA Stage:** Act (implement plan step)

**Responsibilities:**
- Pick first "ready" builder task with satisfied dependencies and no active lease
- Acquire lease (5400s TTL, heartbeat every 10 minutes)
- Read implementation steps from AGENT_PLAN.md
- Implement on feature branch (minimal changes for step)
- Add/adjust tests from TEST_PLAN.md
- Run all quality gates (black, ruff, mypy, pytest, coverage, build, pip-audit)
- Update logs and status
- Generate completion report
- Push branch and release lease

**Inputs:**
- `.oodatcaa/work/SPRINT_QUEUE.json` (ready builder tasks)
- `.oodatcaa/work/AGENT_PLAN.md` (implementation steps, branch name)
- `.oodatcaa/work/TEST_PLAN.md` (required tests)
- `.oodatcaa/objectives/OBJECTIVE.md` (context)
- `.oodatcaa/objectives/SPRINT_GOAL.md` (sprint context)

**Outputs:**
- Code changes (implementation on feature branch)
- Test additions/modifications
- Updated `.oodatcaa/work/AGENT_LOG.md` (build entry with gate results, coverage)
- Updated `.oodatcaa/work/SPRINT_QUEUE.json` (status: "awaiting_test" if gates pass, "needs_adapt" if fails)
- `.oodatcaa/work/reports/<TASK_ID>/builder_<subtask>.md` (completion report)
- `.oodatcaa/work/AGENT_REPORTS.md` (executive summary)
- Git commits ([plan]/[impl]/[test]/[refactor])
- Pushed feature branch

**Decision Authority:**
- **High:** Implementation approach (within plan constraints), code structure, test structure
- **Medium:** Commit granularity, refactoring decisions (if needed for step)
- **Low:** Cannot skip quality gates, must follow plan steps exactly, cannot change DoD

**Success Criteria:**
- All quality gates pass (black, ruff, mypy, pytest, coverage ≥85%, build, pip-audit)
- Tests added/modified as specified in TEST_PLAN.md
- Code implements plan step completely
- Minimal changes (only what's needed for step)
- Feature branch pushed
- Completion report generated
- Lease released

**Sprint 1/2 Usage:**
- **Sprint 1:** 34 builder tasks completed (W001-B01 through W008-B03), 91.9% success rate
- **Sprint 2:** P002-B01 (perfect implementation), P003-B01/B02/B03, P005-B01 (current task)
- **Adaptation Pattern:** 4 adaptations in Sprint 1 (W004, W005, W006-B01, W007-B01, W008-B01) handled by Refiner
- **Typical Cadence:** On-demand when ready builder tasks exist, respects WIP limit (3 concurrent max)

**Related Prompts:** [`builder.md`](.oodatcaa/prompts/builder.md)

---

### 5. Tester

**Role:** Validation — OODATCAA (Test+Check)

**OODATCAA Stage:** Test (run acceptance tests) → Check (verify ACs met)

**Responsibilities:**
- Pick first "awaiting_test" tester task
- Acquire lease (2700s TTL, heartbeat every 10 minutes)
- Execute quality gate commands from TEST_PLAN.md
- Run acceptance/performance tests
- Add minimal regression tests if tests missing
- Log PASS/FAIL per acceptance criterion
- Update status ("ready_for_integrator" if pass, "needs_adapt" if fail)
- Generate completion report
- Release lease

**Inputs:**
- `.oodatcaa/work/SPRINT_QUEUE.json` (awaiting_test tasks)
- `.oodatcaa/work/TEST_PLAN.md` (test commands, acceptance criteria, performance thresholds)
- `.oodatcaa/objectives/OBJECTIVE.md` (context)
- `.oodatcaa/objectives/SPRINT_GOAL.md` (sprint context)
- Builder's feature branch (code to test)

**Outputs:**
- Test additions (if tests missing)
- Updated `.oodatcaa/work/AGENT_LOG.md` (test results per AC, performance numbers, coverage delta)
- Updated `.oodatcaa/work/SPRINT_QUEUE.json` (status: "ready_for_integrator" or "needs_adapt")
- `.oodatcaa/work/reports/<TASK_ID>/tester_<subtask>.md` (completion report)
- `.oodatcaa/work/AGENT_REPORTS.md` (executive summary)
- Test suggestions (if failing)

**Decision Authority:**
- **High:** PASS/FAIL decision per acceptance criterion, regression test additions
- **Medium:** Performance threshold interpretation, test additions (minimal)
- **Low:** Cannot skip ACs, cannot modify acceptance criteria, must follow TEST_PLAN.md

**Success Criteria:**
- All acceptance criteria tested
- All ACs pass (or detailed failures logged)
- Performance thresholds met (if applicable)
- Coverage delta calculated
- Tests added if missing (specified paths)
- Suggestions provided for failures
- Completion report generated
- Lease released

**Sprint 1/2 Usage:**
- **Sprint 1:** Validated all 34 tasks (W001-T01 through W008-T01), 4 rejections leading to adaptations
- **Sprint 2:** P002-T01 (accepted first attempt), P003-T01/T02, P004-T01
- **Pattern:** Thorough validation, clear rejection reasons when ACs not met
- **Typical Cadence:** On-demand when awaiting_test tasks exist, respects WIP limit (2 concurrent max)

**Related Prompts:** [`tester.md`](.oodatcaa/prompts/tester.md)

---

### 6. Refiner

**Role:** Adaptation — OODATCAA (Adapt)

**OODATCAA Stage:** Adapt (decide fix approach)

**Responsibilities:**
- Pick first "needs_adapt" task
- Acquire lease (2700s TTL)
- Analyze recent AGENT_LOG.md and AGENT_PLAN.md step
- Decide: Quick fix (minimal patch) OR Start-Over rollback (reset to baseline tag)
- For quick fix: specify patch, set task back to "ready" for Builder
- For rollback: reset to baseline tag, bump plan version, adjust steps/ACs, write Post-Mortem
- Log decision and rationale
- Update SPRINT_QUEUE.json
- Generate completion report
- Release lease

**Inputs:**
- `.oodatcaa/work/SPRINT_QUEUE.json` (needs_adapt tasks)
- `.oodatcaa/work/AGENT_LOG.md` (failure context, tester feedback)
- `.oodatcaa/work/AGENT_PLAN.md` (original plan step)
- `.oodatcaa/objectives/OBJECTIVE.md` (context)
- `.oodatcaa/objectives/SPRINT_GOAL.md` (sprint context)
- Builder/Tester reports (failure details)

**Outputs:**
- Decision: Quick fix specification OR rollback instructions
- Updated `.oodatcaa/work/AGENT_PLAN.md` (if rollback: version bump, revised steps/ACs, Post-Mortem)
- Updated `.oodatcaa/work/AGENT_LOG.md` (decision + rationale)
- Updated `.oodatcaa/work/SPRINT_QUEUE.json` (status: "ready" for quick fix, or reset for rollback)
- `.oodatcaa/work/reports/<TASK_ID>/refiner_<iteration>.md` (completion report)
- `.oodatcaa/work/AGENT_REPORTS.md` (executive summary)
- Git baseline tag reference (if rollback)

**Decision Authority:**
- **High:** Quick fix vs Start-Over decision, plan revision (version bump), acceptance criteria adjustment
- **Medium:** Post-Mortem content, rollback scope
- **Low:** Cannot skip Start-Over gate if fundamental ACs unmet after two Adapt loops

**Success Criteria:**
- Clear decision made (quick fix or rollback)
- Decision rationale documented
- If quick fix: specific patch instructions provided
- If rollback: baseline tag identified, plan revised, Post-Mortem written
- Task status updated appropriately
- Completion report generated
- Lease released

**Sprint 1/2 Usage:**
- **Sprint 1:** Handled 4 adaptations (W004, W005, W006-B01, W007-B01, W008-B01), all resolved with quick fixes
- **Sprint 2:** No adaptations needed yet (P002-B01 perfect, P003/P004 successful)
- **Pattern:** Quick fixes preferred, Start-Over gate rarely triggered (0 times in Sprint 1)
- **Typical Cadence:** On-demand when needs_adapt tasks exist (reactive, not continuous)

**Related Prompts:** [`refiner.md`](.oodatcaa/prompts/refiner.md)

---

### 7. Integrator

**Role:** Integration — OODATCAA (Archive)

**OODATCAA Stage:** Archive (merge, tag, document)

**Responsibilities:**
- Pick first "ready_for_integrator" task
- Acquire lease (1800s TTL)
- Open Pull Request (one step/PR where feasible) with checklist (DoD, ACs, gates, risks, tests, perf delta)
- Ensure all CI gates pass
- Merge per policy (squash/rebase)
- Tag if applicable (baseline tags, version tags)
- Update CHANGELOG and documentation
- Set task status to "done"
- Log shipped entry to SPRINT_LOG.md
- Generate completion report
- Release lease

**Inputs:**
- `.oodatcaa/work/SPRINT_QUEUE.json` (ready_for_integrator tasks)
- Builder's feature branch (validated code)
- Tester's validation report
- CI pipeline results
- CHANGELOG.md (existing)
- Documentation files

**Outputs:**
- Pull Request (with DoD checklist, AC verification, gate results, risk assessment)
- Merged code (main branch)
- Git tags (baseline: `pre/<ticket>-<ISO8601>`, version: `v<semver>` if applicable)
- Updated CHANGELOG.md
- Updated documentation
- Updated `.oodatcaa/work/SPRINT_LOG.md` (shipped entry: ticket, step, PR URL, tag)
- Updated `.oodatcaa/work/SPRINT_QUEUE.json` (status: "done")
- `.oodatcaa/work/reports/<TASK_ID>/integrator.md` (completion report)
- `.oodatcaa/work/AGENT_REPORTS.md` (executive summary)

**Decision Authority:**
- **High:** Merge decision (squash vs rebase), tag creation, CHANGELOG format
- **Medium:** PR description content, documentation updates
- **Low:** Cannot skip CI gates, must verify all ACs met, must follow merge policy

**Success Criteria:**
- PR opened with complete checklist
- All CI gates pass
- Code merged to main
- Appropriate tags created (baseline, version if applicable)
- CHANGELOG updated
- Documentation updated
- Task marked "done"
- Shipped entry logged
- Completion report generated
- Lease released

**Sprint 1/2 Usage:**
- **Sprint 1:** Integrated all 34 tasks (W001 through W008), all with baseline tags
- **Sprint 2:** Integrated P002-B01, P003-B01/B02, P004 (4 integrations)
- **Pattern:** Clean PR descriptions, consistent tagging, thorough CHANGELOG updates
- **Typical Cadence:** On-demand when ready_for_integrator tasks exist, respects WIP limit (1 concurrent max)

**Related Prompts:** [`integrator.md`](.oodatcaa/prompts/integrator.md)

---

### 8. Project Completion Detector

**Role:** Autonomous Done Detection

**OODATCAA Stage:** Check (verify objective completion)

**Responsibilities:**
- Read OBJECTIVE.md success criteria
- Verify each criterion (functional, performance, quality, documentation)
- Calculate completion percentage
- Decide if project is complete (100% criteria met)
- Generate PROJECT_COMPLETION_REPORT.md if complete
- Update SPRINT_GOAL.md status to `project_complete` if done
- Provide summary and next steps

**Inputs:**
- `.oodatcaa/objectives/OBJECTIVE.md` (success criteria)
- `.oodatcaa/work/SPRINT_LOG.md` (shipped features)
- `tests/acceptance/` (acceptance tests)
- CI pipeline results (performance, quality gates)
- Coverage reports (`pytest --cov`)
- Security audit results (`pip-audit`)
- README.md and documentation

**Outputs:**
- Completion percentage (criteria met / total criteria × 100)
- Completion decision (YES if 100%, NO otherwise)
- `.oodatcaa/objectives/PROJECT_COMPLETION_REPORT.md` (if complete)
- Updated `.oodatcaa/objectives/SPRINT_GOAL.md` (status: `project_complete` if done)
- Unmet criteria report (if incomplete)
- Completion summary

**Decision Authority:**
- **High:** Project completion declaration (100% criteria met), completion report generation
- **Medium:** Criteria interpretation, evidence evaluation
- **Low:** Cannot modify OBJECTIVE.md, cannot lower criteria thresholds, must have objective evidence

**Success Criteria:**
- All success criteria evaluated
- Evidence checked (tests, benchmarks, coverage, documentation)
- Completion percentage calculated accurately
- If complete: PROJECT_COMPLETION_REPORT.md generated, SPRINT_GOAL.md status updated
- If incomplete: unmet criteria listed with evidence gaps
- Clear summary provided

**Sprint 1/2 Usage:**
- **Sprint 1:** Not invoked (Sprint 1 goal was foundation, not full objective completion)
- **Sprint 2:** Not invoked yet (Sprint 2 in progress, not at completion check point)
- **Expected Pattern:** Invoked after each sprint completes, after Integrator merges, or on-demand
- **Typical Cadence:** End of each sprint, or when Sprint Planner requests (typically 1-2 times per sprint)

**Related Prompts:** [`project-completion-detector.md`](.oodatcaa/prompts/project-completion-detector.md)

---

## Utility Agents

### 9. Sprint Close

**Role:** Sprint Finalization

**Responsibilities:**
- Aggregate "done" and "rolled_back" tasks
- Extract key decisions from SPRINT_LOG.md and AGENT_LOG.md
- Append sprint summary to SPRINT_LOG.md (shipped PRs/tags, rollbacks, perf/coverage deltas, improvements for next sprint)
- Reset SPRINT_PLAN.md to next sprint skeleton
- Prepare system for next sprint

**Inputs:**
- `.oodatcaa/work/SPRINT_QUEUE.json` (final sprint task statuses)
- `.oodatcaa/work/SPRINT_LOG.md` (sprint activity)
- `.oodatcaa/work/AGENT_LOG.md` (agent decisions)
- `.oodatcaa/objectives/SPRINT_GOAL.md` (sprint exit criteria)

**Outputs:**
- Updated `.oodatcaa/work/SPRINT_LOG.md` (sprint summary: shipped, rollbacks, metrics, lessons)
- Reset `.oodatcaa/work/SPRINT_PLAN.md` (next sprint skeleton)
- Sprint retrospective (informal, embedded in SPRINT_LOG.md)

**Decision Authority:**
- **Medium:** Sprint summary content, retrospective format, lessons learned
- **Low:** Cannot modify sprint goal, cannot change task statuses, operates on completed sprints only

**Success Criteria:**
- Sprint summary complete (shipped, rollbacks, metrics)
- Key decisions extracted and documented
- Improvements for next sprint identified
- SPRINT_PLAN.md reset
- Clean state for next sprint

**Sprint 1/2 Usage:**
- **Sprint 1:** Used to close Sprint 1 (34 tasks shipped, 4 adaptations, 91.9% success)
- **Sprint 2:** Will be used when Sprint 2 completes
- **Pattern:** Comprehensive summaries, clear metrics, actionable improvements
- **Typical Cadence:** Once per sprint (at sprint completion)

**Related Prompts:** [`sprint-close.md`](.oodatcaa/prompts/sprint-close.md)

**Note:** Sprint Close functionality partially replaced by P003 Sprint Management System (`make sprint-complete`), which includes additional features like log rotation, git tagging, and retrospective generation.

---

### 10. Releaser

**Role:** Release Finalization (RC → GA)

**Responsibilities:**
- Verify all Sprint Goal exit criteria met
- Walk through RELEASE_CHECKLIST.md items
- Confirm CI green on main
- Verify acceptance/performance budgets met
- Check security (pip-audit)
- Version bump (semver) and git tag (e.g., v0.3.0)
- Update CHANGELOG and documentation
- Produce release notes
- Smoke test from clean venv
- Go/No-Go decision
- Finalize release or create remediation tasks

**Inputs:**
- `.oodatcaa/objectives/OBJECTIVE.md` (product vision)
- `.oodatcaa/objectives/SPRINT_GOAL.md` (exit criteria)
- `.oodatcaa/objectives/RELEASE_CHECKLIST.md` (release requirements)
- `.oodatcaa/work/SPRINT_LOG.md` (shipped features)
- CI pipeline results
- CHANGELOG.md
- Version file (pyproject.toml, package.json, etc.)

**Outputs:**
- Updated `.oodatcaa/objectives/RELEASE_CHECKLIST.md` (checkboxes filled, findings recorded)
- Updated CHANGELOG.md (release notes)
- Updated `.oodatcaa/work/SPRINT_LOG.md` (release notes section)
- Git version tag (v<semver>)
- Go/No-Go decision documentation
- Remediation tasks (if No-Go)

**Decision Authority:**
- **High:** Go/No-Go release decision, version bump (following semver), release tag creation
- **Medium:** Release notes content, smoke test interpretation
- **Low:** Cannot skip release checklist items, cannot release without exit criteria met, must follow semver

**Success Criteria:**
- All exit criteria verified
- RELEASE_CHECKLIST.md complete
- CI green on main
- Acceptance/performance budgets met
- Security audit clean (no high-severity issues)
- Version bumped (semver)
- Git tag created (if Go)
- CHANGELOG updated
- Release notes generated
- Smoke test passed (if Go)
- Go/No-Go decision documented

**Sprint 1/2 Usage:**
- **Sprint 1:** Not used (Sprint 1 was foundation, not release-ready)
- **Sprint 2:** Not used yet (Sprint 2 in progress, no releases planned)
- **Expected Pattern:** Used when Sprint Planner or Negotiator determines release readiness
- **Typical Cadence:** As needed for releases (typically end of major milestones, not every sprint)

**Related Prompts:** [`release.md`](.oodatcaa/prompts/release.md)

---

### 11. Triage

**Role:** Fast Bug → Work Item Conversion

**Responsibilities:**
- Receive bug report (description + repro steps)
- Add minimal failing test to TEST_PLAN.md
- Create backlog ticket in SPRINT_BACKLOG.md with concrete acceptance criteria
- Enqueue builder fix (ready) and tester acceptance (blocked) in SPRINT_QUEUE.json
- Log note linking test + ticket

**Inputs:**
- Bug description (short description + repro steps, user input)
- `.oodatcaa/objectives/OBJECTIVE.md` (context)
- `.oodatcaa/objectives/SPRINT_GOAL.md` (sprint context)
- `.oodatcaa/work/TEST_PLAN.md` (existing tests)
- `.oodatcaa/work/SPRINT_BACKLOG.md` (existing backlog)
- `.oodatcaa/work/SPRINT_QUEUE.json` (task queue)

**Outputs:**
- Updated `.oodatcaa/work/TEST_PLAN.md` (minimal failing test added)
- Updated `.oodatcaa/work/SPRINT_BACKLOG.md` (bug ticket with ACs)
- Updated `.oodatcaa/work/SPRINT_QUEUE.json` (builder fix: ready, tester acceptance: blocked)
- Updated `.oodatcaa/work/AGENT_LOG.md` (triage entry linking test + ticket)

**Decision Authority:**
- **Medium:** Bug priority, acceptance criteria definition, test specification
- **Low:** Cannot skip test creation, must link test to ticket, must enqueue both builder and tester tasks

**Success Criteria:**
- Failing test added to TEST_PLAN.md (path + name)
- Backlog ticket created with concrete ACs
- Builder fix task enqueued (status: ready)
- Tester acceptance task enqueued (status: blocked, depends on builder fix)
- AGENT_LOG.md entry links test and ticket
- Fast turnaround (< 10 minutes)

**Sprint 1/2 Usage:**
- **Sprint 1:** Not heavily used (no external bug reports, internal issues handled via adaptation loop)
- **Sprint 2:** Not used yet (no external bug reports)
- **Expected Pattern:** On-demand when bugs reported, creates fast path for bug fixes (bypasses full planning)
- **Typical Cadence:** As needed when bugs reported (reactive, not continuous)

**Related Prompts:** [`triage.md`](.oodatcaa/prompts/triage.md)

---

## Agent Interaction Patterns

### Communication Mechanisms
- **File-Based Messaging:** SPRINT_QUEUE.json (task status), AGENT_LOG.md (chronological activity), SPRINT_LOG.md (sprint-level events)
- **Lease Protocol:** `.leases/*.json` files (TTL-based ownership, heartbeat mechanism)
- **Lock Protocol:** `.locks/*.lock` files (5-minute TTL, breakable with log note)
- **Status Transitions:** ready → in_progress → awaiting_test → ready_for_integrator → done

### Primary Development Flow
1. **Sprint Planner** → Sprint goal + backlog
2. **Planner** → Detailed plan (AGENT_PLAN.md, TEST_PLAN.md) + enqueue tasks
3. **Builder** → Implement step → "awaiting_test"
4. **Tester** → Validate ACs → "ready_for_integrator" (or "needs_adapt")
5. **(Optional) Refiner** → If "needs_adapt" → Fix or rollback → "ready"
6. **Integrator** → Merge + tag + document → "done"

### Adaptation Loop (when needed)
1. **Tester** → Reject (set "needs_adapt")
2. **Refiner** → Analyze → Quick fix OR rollback
3. **Builder** → Re-implement → "awaiting_test"
4. **Tester** → Re-validate → "ready_for_integrator" (or trigger Start-Over gate)

### Sprint Lifecycle
1. **Sprint Planner** → Generate Sprint N goal
2. **Planner** (multiple) → Plan all backlog items
3. **Negotiator** (continuous) → Coordinate agents, enforce WIP, manage leases
4. **Development agents** (parallel) → Build, Test, Refine, Integrate
5. **Sprint Planner** (end) → Check exit criteria → Complete sprint OR request more work
6. **Sprint Close** → Summarize + reset → Ready for Sprint N+1

### Project Completion Flow
1. **Sprint Planner** → Detect potential completion (after sprint)
2. **Project Completion Detector** → Verify all OBJECTIVE.md criteria
3. **Sprint Planner** → If 100% → Set status `project_complete` → Generate PROJECT_COMPLETION_REPORT.md
4. **Negotiator** → Detect `project_complete` status → Stop coordination loop
5. **(Optional) Releaser** → If release needed → Finalize release

---

## Decision Authority Matrix

| Agent | High Authority | Medium Authority | Low Authority / Constraints |
|-------|---------------|------------------|---------------------------|
| **Negotiator** | Sprint completion, task status transitions, stale lease takeover | Agent assignment, WIP enforcement, sprint replan suggestions | Cannot change OBJECTIVE.md, cannot modify protocols |
| **Sprint Planner** | Project completion declaration, sprint goal definition, exit criteria | Sprint scope, backlog prioritization | Cannot modify OBJECTIVE.md, must follow sprint conventions |
| **Planner** | Alternative selection, plan structure, AC definition, task breakdown | Complexity estimation, dependencies, branch naming | Cannot change OBJECTIVE.md, cannot skip gates, must follow DoD |
| **Builder** | Implementation approach, code structure, test structure | Commit granularity, refactoring decisions | Cannot skip quality gates, must follow plan exactly |
| **Tester** | PASS/FAIL decisions, regression test additions | Performance threshold interpretation, test additions | Cannot skip ACs, cannot modify criteria |
| **Refiner** | Quick fix vs rollback decision, plan revision, AC adjustment | Post-Mortem content, rollback scope | Cannot skip Start-Over gate if fundamental ACs unmet (2 loops) |
| **Integrator** | Merge decision, tag creation, CHANGELOG format | PR description, documentation updates | Cannot skip CI gates, must verify ACs, must follow merge policy |
| **Project Completion Detector** | Project completion declaration, completion report generation | Criteria interpretation, evidence evaluation | Cannot modify OBJECTIVE.md, cannot lower thresholds |
| **Sprint Close** | — | Sprint summary content, retrospective format | Cannot modify sprint goal, cannot change task statuses |
| **Releaser** | Go/No-Go decision, version bump, release tag | Release notes content, smoke test interpretation | Cannot skip checklist, must meet exit criteria, must follow semver |
| **Triage** | — | Bug priority, AC definition, test specification | Cannot skip test creation, must link test to ticket |

---

## Sprint 1 Evidence Summary

**Sprint 1 Metrics:**
- **Tasks:** 34 completed (W001 through W008)
- **Success Rate:** 91.9% (31 first-attempt successes, 4 adaptations)
- **Adaptations:** 4 tasks required Refiner intervention (W004, W005, W006-B01, W007-B01, W008-B01)
- **Rollbacks:** 0 (all adaptations resolved with quick fixes)
- **Duration:** ~2 weeks
- **Agent Usage:** All 11 agents operational (Negotiator continuous, Planner 8x, Builder 34x, Tester 34x, Refiner 4x, Integrator 34x, Sprint Planner 1x, Sprint Close 1x)

**Key Learnings:**
1. **High Success Rate:** 91.9% indicates strong agent coordination and effective protocols
2. **Adaptation Loop Effective:** 4 adaptations all resolved quickly (no Start-Over gates triggered)
3. **Refiner Preferred Quick Fixes:** All 4 adaptations used quick fix approach (no rollbacks)
4. **Protocol Coordination Issues:** 5 manual interventions noted (addressed in P005)
   - Pattern: Pre-assignment by Negotiator caused "No tasks ready" for agents
   - Fix: Negotiator now marks tasks "ready", agents discover autonomously
5. **Parallel Execution:** Multiple builders worked simultaneously (WIP limit 3)
6. **Comprehensive Documentation:** All 34 tasks have builder, tester, integrator reports

**Sprint 1 Task Examples:**
- **W001:** MCP server migration foundation (successful first attempt)
- **W002:** Vector store integration (successful first attempt)
- **W003:** Memory management (successful first attempt)
- **W004:** Query optimization (required adaptation - performance issue)
- **W005:** Memory storage (required adaptation - test coverage gap)
- **W006-B01:** Documentation (required adaptation - completeness issue)
- **W007-B01:** Integration tests (required adaptation - flaky tests)
- **W008-B01:** Final polish (required adaptation - lint errors)

---

## Sprint 2 Evidence Summary

**Sprint 2 Metrics (as of 2025-10-04):**
- **Tasks Planned:** 30 (P001 through P007)
- **Tasks Completed:** 5 (P002-B01, P003-B01, P003-B02, P004, P005 planning)
- **Tasks In Progress:** 1 (P005-B01)
- **Success Rate:** 100% so far (5/5 first-attempt successes, 0 adaptations)
- **Duration:** ~1 week (in progress)
- **Agent Usage:** Planner 6x (P001-P006), Builder 4x (P002-B01, P003-B01/B02/B03), Tester 3x, Integrator 3x

**Key Learnings:**
1. **Perfect Execution:** P002-B01 achieved 100% first-attempt success (log rotation system)
2. **Protocol Coordination Fix Validated:** P005 planning used autonomous discovery (no pre-assignment)
   - Planner discovered "needs_plan" task autonomously
   - Planner claimed task with own lease
   - Planner completed planning without manual intervention
   - P005-B01 marked "ready" (not pre-assigned to Builder)
   - Builder (current task) discovered P005-B01 autonomously
3. **Documentation-Heavy Sprint:** Sprint 2 focuses on process improvement (P001-P007 are infra/docs)
4. **Higher Success Rate:** 100% so far (vs 91.9% Sprint 1) — suggests protocol improvements working

**Sprint 2 Task Examples:**
- **P001:** Background agent daemon system (planned, in progress)
- **P002-B01:** Log rotation automation (perfect implementation, 0 adaptations)
- **P003:** Enhanced sprint management system (dashboard, completion, initialization)
- **P004:** OODATCAA loop documentation (comprehensive guide)
- **P005:** Agent role assessment (current task: agent audit)
- **P006:** Process documentation & runbook (planned)
- **P007:** Observability & monitoring (planned)

---

## Usage Patterns by Agent Type

### Continuous Agents
- **Negotiator:** Runs continuously (or every 10-15 minutes), always active during sprint
- **Pattern:** Coordination loop, never stops unless sprint status is `project_complete`

### Per-Sprint Agents
- **Sprint Planner:** Once per sprint (at start or completion)
- **Sprint Close:** Once per sprint (at completion)
- **Pattern:** Bookend agents for sprint lifecycle

### Per-Task Agents
- **Planner:** Once per backlog item needing detailed plan (typically 1-8 times per sprint)
- **Builder:** Once per implementation step (most active agent, 34x Sprint 1, 4x Sprint 2 so far)
- **Tester:** Once per builder step completion (same frequency as Builder)
- **Integrator:** Once per validated step (same frequency as Tester if all pass)
- **Pattern:** Development flow agents, on-demand based on task availability

### Reactive Agents
- **Refiner:** Only when "needs_adapt" tasks exist (4x Sprint 1, 0x Sprint 2 so far)
- **Triage:** Only when bugs reported (0x Sprint 1, 0x Sprint 2)
- **Pattern:** Issue-handling agents, triggered by failures or external input

### Milestone Agents
- **Project Completion Detector:** End of each sprint or on-demand (typically 1-2x per sprint)
- **Releaser:** When release readiness detected (rare, typically end of major milestones)
- **Pattern:** High-level checkpoint agents, infrequent but critical

---

## Cross-References

**Agent Prompts:** [`.oodatcaa/prompts/`](.oodatcaa/prompts/)
- negotiator.md
- sprint-planner.md
- planner.md
- builder.md
- tester.md
- refiner.md
- integrator.md
- project-completion-detector.md
- sprint-close.md
- release.md
- triage.md

**Sprint Evidence:**
- Sprint 1 Reports: `.oodatcaa/work/reports/W001/` through `.oodatcaa/work/reports/W008/`
- Sprint 2 Reports: `.oodatcaa/work/reports/P001/` through `.oodatcaa/work/reports/P007/`
- Sprint Logs: `.oodatcaa/work/SPRINT_LOG.md`
- Agent Logs: `.oodatcaa/work/AGENT_LOG.md`

**Related Documentation:**
- OODATCAA Loop Guide: [`.oodatcaa/OODATCAA_LOOP_GUIDE.md`](.oodatcaa/OODATCAA_LOOP_GUIDE.md)
- Agent Interaction Guide: [`.oodatcaa/AGENT_INTERACTION_GUIDE.md`](.oodatcaa/AGENT_INTERACTION_GUIDE.md) (to be created in P005-B01 Step 2)
- Agent Gap Analysis: [`.oodatcaa/work/AGENT_GAP_ANALYSIS.md`](.oodatcaa/work/AGENT_GAP_ANALYSIS.md) (to be created in P005-B01 Step 3)

---

**Matrix Version:** 1.0  
**Last Updated:** 2025-10-04  
**Next Review:** End of Sprint 2  
**Maintainer:** Builder (P005-B01)

