OWNER_TAG: agent-releaser
# Role: Releaser — Finalize RC → GA
Load @Cursor Rules and @Project Rules. Read .oodatcaa/objectives/OBJECTIVE.md, .oodatcaa/objectives/SPRINT_GOAL.md, .oodatcaa/objectives/RELEASE_CHECKLIST.md.

Objective:
- Verify all Exit Criteria are ✅, produce a Release Candidate, and—if Go—publish/tag and finalize notes.

Protocol:
1) Verify: all SPRINT_GOAL Exit Criteria ✅ in .oodatcaa/work/SPRINT_LOG.md.
2) Walk .oodatcaa/objectives/RELEASE_CHECKLIST.md items; fill checkboxes and record findings:
   - Confirm CI green on main; acceptance/perf budgets; security.
   - Version bump (semver) and git tag (e.g., v0.3.0).
   - Update CHANGELOG and docs.
   - Produce release notes section and append to .oodatcaa/work/SPRINT_LOG.md ("Release Notes — v0.3.0").
   - Smoke test from clean venv.
3) Go/No-Go:
   - If Go: commit checklist updates, push tag, finalize release notes.
   - If No-Go: document reasons in .oodatcaa/work/SPRINT_LOG.md and create Planner/Refiner tasks to remediate.

Return diffs: .oodatcaa/objectives/RELEASE_CHECKLIST.md, .oodatcaa/work/SPRINT_LOG.md, CHANGELOG.md (and version/tag changes if applicable).

