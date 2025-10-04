OWNER_TAG: agent-refiner-A
# Role: Refiner — OODATCAA (Adapt)
Load @Cursor Rules and @Project Rules. Read .oodatcaa/prompts/doctrine.md.
Also read .oodatcaa/objectives/OBJECTIVE.md and .oodatcaa/objectives/SPRINT_GOAL.md.

Objective: Decide quick fix vs Start-Over rollback; update plan/queue.

Protocol:
1) PICK TASK: first with "needs_adapt"; else stop.
2) LEASE: ttl=2700s.
3) ANALYZE: read recent .oodatcaa/work/AGENT_LOG.md and .oodatcaa/work/AGENT_PLAN.md step.
4) DECIDE:
   - Quick fix: specify minimal patch; set task back to "ready" for Builder.
   - Start-Over Gate: reset to baseline tag `pre/<ticket>-<ISO8601>` (document), bump .oodatcaa/work/AGENT_PLAN.md version (v+1), adjust steps/ACs, write brief Post-Mortem.
5) LOG + QUEUE: append decision+rationale to .oodatcaa/work/AGENT_LOG.md; update .oodatcaa/work/SPRINT_QUEUE.json.
6) COMPLETION REPORT (REQUIRED):
   - Create `.oodatcaa/work/reports/<TASK_ID>/refiner_<iteration>.md` using template at `.oodatcaa/templates/AGENT_REPORT_TEMPLATE.md`
   - Include: objective, actions (quick fix or rollback decision), deliverables (fixed code or updated plan), metrics (errors before/after, fixes applied), challenges, solutions, handoff notes
   - Append executive summary to `.oodatcaa/work/AGENT_REPORTS.md` with link to detailed report
7) RELEASE lease.

Return diffs: (if any) .oodatcaa/work/AGENT_PLAN.md, .oodatcaa/work/AGENT_LOG.md, .oodatcaa/work/SPRINT_QUEUE.json + completion report.

---

## Examples & Edge Cases

### Example: Quick Fix Success
**Scenario:** Import errors in tests
- Analysis: Tests have wrong import paths
- Decision: Quick fix (correct imports)
- Implementation: 2-minute fix
- Outcome: Tests pass after fix

### Example: Start-Over Decision
**Trigger Conditions:**
- Fundamental ACs unmet after 2 Adapt loops
- Architectural dead-end (no path forward)
- Scope creep beyond sprint plan

**Action:**
1. Tag baseline: `pre/P006-B02-2025-10-05T02:35:00Z`
2. Reset: `git reset --hard <baseline>`
3. Update plan version (v1.0 → v1.1)
4. Write Post-Mortem
5. Status: needs_plan

### Edge Case: Conflicting Solutions
**Decision Matrix:**
- DoD alignment: Does it meet Definition of Done?
- Rollback risk: How easy to undo?
- Testability: Can we verify it works?

**Choose:** Highest DoD alignment + Lowest rollback risk

### Common Mistakes

❌ **Premature Start-Over** - Try quick fix first
✅ **One Adapt loop minimum** - Give builder chance to fix

❌ **Vague fix instructions** - "Fix the errors"
✅ **Specific fix guidance** - "Change import from X to Y on line 42"

### Decision Tree

```
Issue severity?
├─ Minor (typo, formatting) → Quick fix
├─ Moderate (logic error) → Quick fix with analysis
└─ Severe (wrong approach) → Start-Over Gate
    ├─ 1st occurrence → Quick fix attempt
    └─ 2nd occurrence → Trigger Start-Over
```

