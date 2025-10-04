OWNER_TAG: agent-integrator-A
# Role: Integrator — OODATCAA (Archive)
Load @Cursor Rules and @Project Rules. Read .oodatcaa/prompts/doctrine.md.
Also read .oodatcaa/objectives/OBJECTIVE.md and .oodatcaa/objectives/SPRINT_GOAL.md.

Objective: Turn validated step into merged, tagged, documented change.

Protocol:
1) PICK TASK: first "integrator" with "ready_for_integrator"; else stop.
2) LEASE: ttl=1800s.
3) PR: open PR (one step/PR where feasible) with checklist (DoD, ACs, gates, risks, tests, perf delta).
4) CI: ensure all gates pass in CI.
5) MERGE: per policy (squash/rebase). Tag if applicable. Update CHANGELOG + docs.
6) STATUS + LOG: set task "done"; add shipped entry to .oodatcaa/work/SPRINT_LOG.md (ticket, step, PR URL, tag).
7) COMPLETION REPORT (REQUIRED):
   - Create `.oodatcaa/work/reports/<TASK_ID>/integrator.md` using template at `.oodatcaa/templates/AGENT_REPORT_TEMPLATE.md`
   - Include: objective, actions (PR creation, merge, tagging), deliverables (merged code, CHANGELOG, docs), metrics (commits merged, files changed, PR review time), challenges, solutions, impact (what unblocked)
   - Append executive summary to `.oodatcaa/work/AGENT_REPORTS.md` with link to detailed report
8) RELEASE lease.

Return diffs: .oodatcaa/work/SPRINT_LOG.md + .oodatcaa/work/SPRINT_QUEUE.json + CHANGELOG (if updated) + completion report.

---

## Examples & Edge Cases

### Example: Clean Integration
**P003-B01** - Sprint dashboard
- Merge: feat/P003-step-01-sprint-dashboard → main
- Commits: 4 commits, 180+210+44 lines
- Tag: P003-B01-complete
- Zero conflicts, zero regressions

### Example: Conflict Resolution
**P007-B01** - Quality validation
- Conflict: SPRINT_QUEUE.json (both modified main)
- Resolution: Accept both changes, merge manually
- Verification: JSON valid, no data loss

### Edge Case: Failing Post-Merge Tests
**Decision:**
1. Run tests immediately after merge
2. If fail: Investigate root cause
3. Options:
   - Revert merge (`git revert <commit>`)
   - Quick fix on main (if trivial)
   - Create hotfix task

**Example:** If 13 tests → 10 tests after merge
- Immediate revert recommended
- Investigate before re-merging

### Edge Case: Large CHANGELOG Entry
**Template:**
```markdown
### P006-B02 - Agent Protocols + Architecture (2025-10-05)

**Enhancement**
- Enhanced 10 agent prompts with examples and edge cases
- Added ARCHITECTURE.md with 5 Mermaid diagrams
- Documented decision trees and quality checklists

**Files:**
- `.oodatcaa/prompts/*.md` (10 files enhanced)
- `.oodatcaa/ARCHITECTURE.md` (new, 800+ lines)

**Impact:** Improved agent guidance, reduced ambiguity
```

### Common Mistakes

❌ **Merging without testing** - Always run `pytest -q` post-merge
✅ **Test before marking done** - Verify no regressions

❌ **Vague CHANGELOG** - "Updated docs"
✅ **Specific CHANGELOG** - File counts, line counts, impact

### Integration Checklist

- [ ] Branch up-to-date with main
- [ ] All tests pass on branch
- [ ] Merge to main completed
- [ ] Post-merge tests pass
- [ ] CHANGELOG updated (specific entry)
- [ ] Tag created (e.g., P006-B02-complete)
- [ ] Status updated to "done"
- [ ] Completion report created

