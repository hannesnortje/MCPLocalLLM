# Autonomous Workflow Guide

## Overview
The OODATCAA system operates fully autonomously. You define the product objective, and agents handle everything else: sprint planning, work breakdown, implementation, testing, integration, and completion detection.

## User Responsibilities (Minimal!)
1. **Edit OBJECTIVE.md** — Define vision, success criteria, constraints
2. **Launch Negotiator** — Start the autonomous coordinator in Cursor
3. **Monitor progress** — Watch agents work (optional)
4. **Review PRs** — Approve/merge if you want human oversight (optional)

That's it! Agents handle the rest.

---

## Autonomous Agent Lifecycle

### Phase 1: Initialization (First Run)
**Human:** Edit `.oodatcaa/objectives/OBJECTIVE.md` with product vision
**Human:** Launch Negotiator agent in Cursor (run in background)

**Negotiator:**
- Reads OBJECTIVE.md
- Detects no sprint exists
- Triggers Sprint Planner

**Sprint Planner:**
- Analyzes OBJECTIVE.md success criteria
- Generates Sprint 1 goal (foundation work)
- Creates initial backlog in SPRINT_BACKLOG.md
- Initializes SPRINT_QUEUE.json with tasks
- Returns control to Negotiator

---

### Phase 2: Sprint Execution
**Negotiator (runs every 15-30 min):**
- Reads sprint queue
- Assigns tasks to available agents
- Enforces WIP limits
- Manages leases
- Monitors progress

**Planner (triggered by Negotiator):**
- Takes tasks marked "needs_plan"
- Creates detailed AGENT_PLAN.md with steps
- Defines acceptance criteria in TEST_PLAN.md
- Enqueues builder tasks

**Builder (1-3 parallel instances):**
- Takes task from queue
- Creates feature branch
- Implements code changes
- Runs gates (black, ruff, mypy, tests)
- Pushes branch
- Marks task "awaiting_test"

**Tester:**
- Takes tasks marked "awaiting_test"
- Runs acceptance tests
- Checks performance benchmarks
- Validates coverage thresholds
- Marks "ready_for_integrator" or "needs_adapt"

**Refiner (if needed):**
- Takes tasks marked "needs_adapt"
- Analyzes failures
- Decides: quick fix vs rollback
- Updates plan or resets to baseline

**Integrator:**
- Takes tasks marked "ready_for_integrator"
- Opens PR (or auto-merges if configured)
- Updates CHANGELOG
- Tags release (if applicable)
- Marks task "done"

---

### Phase 3: Sprint Completion
**Negotiator (monitors):**
- Checks sprint exit criteria
- When ALL criteria met:
  - Marks sprint as "completed"
  - Logs summary in SPRINT_LOG.md

**Sprint Planner (triggered):**
- Reads completed sprint
- Calculates objective progress (% toward completion)
- Analyzes remaining success criteria
- Generates Sprint 2 goal (next milestone)
- Repeats cycle

---

### Phase 4: Project Completion
**Sprint Planner (every sprint close):**
- Evaluates OBJECTIVE.md success criteria
- If ALL success criteria met (100%):
  - Marks project as "complete"
  - Generates PROJECT_COMPLETION_REPORT.md
  - Logs final summary

**Negotiator (detects completion):**
- Reads project status
- Stops coordination loop
- Logs: "🎉 Project objective achieved!"

---

## Monitoring & Observability

### Real-time Status
Watch these files for live updates:
- `.oodatcaa/objectives/SPRINT_GOAL.md` → Current sprint & objective progress %
- `.oodatcaa/work/SPRINT_QUEUE.json` → Task status (ready/in_progress/done)
- `.oodatcaa/work/AGENT_LOG.md` → Detailed execution log
- `.oodatcaa/work/SPRINT_LOG.md` → Sprint summaries & heartbeats

### Key Metrics (from Negotiator heartbeats)
- **Objective progress:** X% toward completion
- **Sprint progress:** ✅ N/M exit criteria met
- **WIP:** How many tasks in progress per role
- **Blocked tasks:** Dependencies or issues
- **Velocity:** Tasks completed per sprint

---

## Advanced: Manual Intervention

### Override Sprint Goal
If agents pick the wrong direction, edit `.oodatcaa/objectives/SPRINT_GOAL.md` manually and set status to `in_progress`. Negotiator will respect your changes.

### Add Urgent Work
Add task to `.oodatcaa/work/SPRINT_BACKLOG.md` with high priority. Negotiator will assign it on next run.

### Pause Agents
Stop the Negotiator background job. Other agents will finish current tasks but won't start new ones.

### Resume
Restart Negotiator. It will pick up where it left off.

---

## Troubleshooting

### "Agents aren't starting"
- Verify Cursor Rules are loaded (User + Project)
- Check Negotiator is running in background
- Look for errors in Cursor chat logs

### "Sprint stuck on same task"
- Check AGENT_LOG.md for failures
- Refiner should auto-trigger after multiple failures
- Manual: set task status to "needs_adapt" in SPRINT_QUEUE.json

### "Sprint taking too long"
- Negotiator will detect if timeline exceeded by 50%
- Sprint Planner will suggest replan
- Manual: trigger sprint-close and force new sprint

### "Objective never completes"
- Review OBJECTIVE.md success criteria — are they measurable?
- Check if tests exist to validate criteria
- Look at PROJECT_COMPLETION_REPORT.md for gaps

---

## Best Practices

### Writing Good Objectives
✅ **Good:** "Parse 100% of RFC 4180 test cases with p95 < 100ms"
❌ **Bad:** "Make a good parser"

✅ **Good:** "≥ 85% line coverage; 0 high-severity audit issues"
❌ **Bad:** "Have good quality"

### Success Criteria Tips
- Make them **measurable** (agents need tests to verify)
- Include **functional**, **performance**, **quality**, and **documentation**
- Use checkboxes so agents can track completion
- Be specific about thresholds (not "fast", but "p95 < 100ms")

### Let Agents Decide
- Don't pre-plan sprints — let Sprint Planner decide scope
- Don't write detailed tasks — let Planner break them down
- Don't dictate timeline — agents estimate based on complexity
- Trust the autonomous loop!

---

## Example: Full Autonomous Run

**Day 1 (5 minutes of your time):**
```
1. Edit OBJECTIVE.md: "Build a CSV parser with RFC 4180 support, p95 < 100ms"
2. Launch Negotiator in Cursor
3. Go make coffee ☕
```

**Day 1-3 (Agents work):**
```
Sprint 1: "Foundation — Project structure, tooling, first smoke test"
- Planner: Creates setup tasks
- Builder: Creates src/csv_parser/, tests/, CI config
- Tester: Validates smoke test passes
- Integrator: Merges, tags v0.1.0
Sprint 1 complete ✅ (Objective: 20%)
```

**Day 4-7:**
```
Sprint 2: "Core — Implement RFC 4180 tokenizer"
- Builder: Implements CSV tokenizer
- Tester: Adds RFC 4180 test suite
- Integrator: Merges, tags v0.2.0
Sprint 2 complete ✅ (Objective: 60%)
```

**Day 8-10:**
```
Sprint 3: "Performance — Optimize to meet p95 < 100ms"
- Builder: Adds benchmarks, optimizes hot paths
- Tester: Validates perf tests pass
Sprint 3 complete ✅ (Objective: 85%)
```

**Day 11:**
```
Sprint 4: "Polish — Documentation & final QA"
- Builder: Completes README, API docs
- Tester: Final validation
Sprint 4 complete ✅ (Objective: 100%)

🎉 PROJECT COMPLETE!
PROJECT_COMPLETION_REPORT.md generated
```

**Total human time:** ~5 minutes to define objective + optional PR reviews

---

## FAQ

**Q: Do I need to manually create sprints?**
A: No! Sprint Planner does this automatically based on your objective.

**Q: How do agents know when the project is done?**
A: Sprint Planner checks success criteria in OBJECTIVE.md. When all ✅, project is complete.

**Q: Can I run multiple projects in parallel?**
A: Yes, each project should have its own repo/OBJECTIVE.md. Launch separate Negotiators.

**Q: What if I want to change direction mid-project?**
A: Update OBJECTIVE.md and trigger sprint-planner manually. Agents will adjust course.

**Q: Do I need to approve PRs?**
A: Optional. Integrator can auto-merge if you trust the gates. Or review PRs for quality control.

**Q: How many agents should I run?**
A: Negotiator (1), Planner (1), Builder (1-3), Tester (1-2), Refiner (1), Integrator (1). Start with just Negotiator — it will coordinate others.

