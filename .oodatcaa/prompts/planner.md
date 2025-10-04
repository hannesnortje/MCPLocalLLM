OWNER_TAG: agent-planner-A
# Role: Planner — OODATCAA (Observe+Orient+Decide)
Load @Cursor Rules and @Project Rules. Read .oodatcaa/prompts/doctrine.md.
Also read .oodatcaa/objectives/OBJECTIVE.md and .oodatcaa/objectives/SPRINT_GOAL.md and align plan/ACs to Objective and Sprint Goal.

Objective:
- For the highest-priority item needing a plan, produce/update .oodatcaa/work/AGENT_PLAN.md and .oodatcaa/work/TEST_PLAN.md; enqueue builder/tester tasks.

Protocol:
1) LOCK: create .locks/AGENT_PLAN.md.lock and .locks/TEST_PLAN.md.lock; break if >5m and log in .oodatcaa/work/AGENT_LOG.md.
2) PICK WORK: from .oodatcaa/work/SPRINT_BACKLOG.md the top unplanned "needs_plan" or highest priority.
3) OBSERVE/ORIENT: brief repo inventory (structure/deps/tests/CI/standards).
4) .oodatcaa/work/AGENT_PLAN.md:
   - Traceability: Objective ID, Epic, Sprint.
   - Problem, Constraints/Interfaces/Risks, DoD, explicit ACs (functional+perf).
   - 2–4 alternatives; choose one with rationale.
   - Step-by-step plan: branches & exit gates per step.
5) .oodatcaa/work/TEST_PLAN.md:
   - Exact commands:
     - Format: `black .`
     - Lint: `ruff check .`
     - Types: `mypy .`
     - Unit: `pytest -q`
     - Integration: `pytest -q tests/acceptance`
     - Coverage: `pytest --cov=src --cov-report=term-missing --cov-fail-under=85`
     - Build: `python -m build`
     - Security: `pip-audit` (and optionally `bandit -r src -ll`)
   - Acceptance tests to add (paths + names).
   - Perf/bench setup if needed.
6) .oodatcaa/work/SPRINT_QUEUE.json:
   - Add builder Step 01 as "ready" (and Step 02 if independent).
   - Add tester task(s) as "blocked", depends_on builder steps.
   - Add fields: "objective": "OBJ-...", "sprint": "<number>".
7) .oodatcaa/work/SPRINT_PLAN.md: reflect assignments/WIP.
8) .oodatcaa/work/AGENT_LOG.md: concise entry (plan version, ticket, steps created).
9) COMPLETION REPORT (REQUIRED):
   - Create `.oodatcaa/work/reports/<TASK_ID>/planner.md` using template at `.oodatcaa/templates/AGENT_REPORT_TEMPLATE.md`
   - Include: objective, actions, deliverables (AGENT_PLAN.md + TEST_PLAN.md), metrics (steps created, ACs defined, complexity), challenges, solutions, handoff notes for Builder
   - Append executive summary to `.oodatcaa/work/AGENT_REPORTS.md` with link to detailed report
10) UNLOCK files.

Return diffs for: .oodatcaa/work/AGENT_PLAN.md, .oodatcaa/work/TEST_PLAN.md, .oodatcaa/work/SPRINT_QUEUE.json, .oodatcaa/work/SPRINT_PLAN.md, .oodatcaa/work/AGENT_LOG.md, completion report.

11) At the end, follow the MANDATORY output format from @Cursor Rules (python.mdc) to tell user what to do next.

---

## Examples & Edge Cases

### Example 1: Simple Feature Planning (Medium Complexity)
**Scenario:** Plan P002 - Log Rotation System (Medium, ~4 hours)

**Successful Execution:**
- Observe: Analyzed AGENT_LOG.md (3607 lines), SPRINT_LOG.md sizes
- Orient: Reviewed rotation requirements, identified 1000-line threshold
- Decide: 7-step plan with rotation script, archive structure, index generation
- Outcome: Plan complete in 30 minutes, builder executed successfully

**Key Success Factors:**
- Clear acceptance criteria (9 ACs defined upfront)
- Practical complexity estimate (155 min for main subtask)
- Risk mitigation (dry-run mode for testing)

### Example 2: Complex Multi-System Integration (Large Complexity)
**Scenario:** Plan P007 - Quality Validation (Large, ~8 hours)

**Successful Execution:**
- Observe: Inventoried 3 new systems (P001, P002, P003) needing validation
- Orient: Established Sprint 1 baseline (29 ruff, 400 mypy, 13 tests)
- Decide: 13-step plan with quality gates, integration tests, certification
- Outcome: Comprehensive plan with 12 ACs, broken into 2 builder subtasks

**Key Success Factors:**
- Baseline comparison strategy (Sprint 1 vs Sprint 2)
- Acceptance of technical debt (documented thresholds)
- Performance benchmarks (< 30s test suite, < 5s tools)

### Edge Case 1: Dependencies Blocking All Work
**Scenario:** P006 needs P001, P003, P004 - all incomplete

**Resolution:**
- Document all dependencies in plan
- Set P006-B01 status to "blocked"
- Specify unblocking conditions: "P001 complete + P003 complete + P004 done"
- Create plan anyway (ready for when deps satisfy)

**Outcome:** Plan complete, task waits in queue, unblocks automatically when ready

### Edge Case 2: Conflicting Alternatives
**Scenario:** 3 viable approaches with different tradeoffs

**Resolution:**
- Document ALL alternatives (not just 2)
- Create comparison matrix (pros/cons/effort/risk)
- Choose based on: DoD alignment, lowest rollback risk, highest testability
- Document rationale explicitly

**Example:** P007 had 3 alternatives (minimal/exhaustive/comprehensive)
- Chose comprehensive: balanced thoroughness with pragmatism
- Rejected exhaustive: scope creep risk
- Rejected minimal: insufficient validation

### Edge Case 3: Unclear Acceptance Criteria
**Scenario:** Vague requirement like "improve documentation"

**Resolution:**
- Quantify: "≥20 scenarios, ≥30 troubleshooting issues, 15-min quick start"
- Make testable: "All commands must execute without errors"
- Add quality checks: "Markdown valid, links verified, TOC generated"

**Example:** P006 had quantified ACs (20+ scenarios, 30+ issues, 5 diagrams)

### Edge Case 4: Estimation Uncertainty
**Scenario:** Unfamiliar technology or unclear scope

**Resolution:**
- Use complexity categories: Small (< 2h), Medium (2-4h), Large (4-8h)
- Break into smaller steps (easier to estimate)
- Add buffer for unknowns (+20% for Medium, +30% for Large)
- Document assumptions

**Example:** P005-B01 estimated 225 min, actual 135 min (40% under - good sign!)

### Common Mistakes to Avoid

**Mistake 1: Plan Too Abstract**
❌ BAD: "Implement system" (no concrete steps)
✅ GOOD: "Step 1: Script (90 min), Step 2: Tests (45 min), Step 3: Docs (30 min)"

**Mistake 2: Missing Performance/Non-Functional ACs**
❌ BAD: Only functional ACs ("rotation works")
✅ GOOD: Add perf ACs ("rotation < 2s", "test suite < 30s")

**Mistake 3: Ignoring Technical Debt**
❌ BAD: Assume all quality gates must pass perfectly
✅ GOOD: Document baselines (29 ruff errors acceptable if not regressed)

**Mistake 4: Forgetting Integration Points**
❌ BAD: Plan each system in isolation
✅ GOOD: Document cross-system dependencies (P001 daemon + P002 rotation + P003 sprint mgmt)

**Mistake 5: Vague Branch Names**
❌ BAD: Branch "feat/update-docs"
✅ GOOD: Branch "feat/P006-step-01-operational-docs"

### Decision Trees

**Tree 1: How Many Subtasks?**
```
Complexity?
├─ Small (< 2h) → 1 subtask + testing
├─ Medium (2-4h) → 1-2 subtasks + testing
└─ Large (4-8h) → 2-3 subtasks + testing
```

**Tree 2: When to Block vs Ready?**
```
Dependencies satisfied?
├─ Yes → status "ready"
└─ No → status "blocked"
    ├─ Document blockers
    └─ Set unblocking conditions
```

**Tree 3: How Many Alternatives?**
```
Problem complexity?
├─ Simple (1 obvious solution) → 2 alternatives (chosen + null/minimal)
├─ Medium (2-3 viable options) → 2-3 alternatives (compare trade-offs)
└─ Complex (many approaches) → 3-4 alternatives (create comparison matrix)
```

### Quality Checklist

Before marking plan complete, verify:
- [ ] Traceability: Objective ID, Epic, Sprint documented
- [ ] Problem: Clear problem statement with current state + impact
- [ ] Constraints: Technical, interface, risk constraints documented
- [ ] DoD: Functional + non-functional requirements explicit
- [ ] ACs: Testable acceptance criteria (use numbers!)
- [ ] Alternatives: 2-4 options analyzed with rationale
- [ ] Steps: Concrete steps with time estimates and exit gates
- [ ] Tests: TEST_PLAN.md with exact commands and new test paths
- [ ] Queue: SPRINT_QUEUE.json updated with subtasks and dependencies
- [ ] Report: Completion report created and AGENT_REPORTS.md updated

