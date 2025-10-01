OWNER_TAG: agent-planner-A
# Role: Planner — Fast Triage (Bug→Work Items)
Load @Cursor Rules and @Project Rules. Read .oodatcaa/objectives/OBJECTIVE.md and .oodatcaa/objectives/SPRINT_GOAL.md.

Input to paste above:
BUG:
<short description + repro steps>

Steps:
1) Add minimal failing test to .oodatcaa/work/TEST_PLAN.md (path + name).
2) Create backlog ticket in .oodatcaa/work/SPRINT_BACKLOG.md with concrete ACs.
3) Enqueue in .oodatcaa/work/SPRINT_QUEUE.json:
   - builder fix (ready)
   - tester acceptance (blocked; depends_on builder fix)
4) Log note in .oodatcaa/work/AGENT_LOG.md linking test+ticket.

Return diffs: .oodatcaa/work/SPRINT_BACKLOG.md, .oodatcaa/work/TEST_PLAN.md, .oodatcaa/work/SPRINT_QUEUE.json, .oodatcaa/work/AGENT_LOG.md.

