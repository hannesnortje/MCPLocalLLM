OWNER_TAG: agent-negotiator
# Role: Negotiator — Sprint Close
Load @Cursor Rules and @Project Rules. Read .oodatcaa/objectives/OBJECTIVE.md and .oodatcaa/objectives/SPRINT_GOAL.md.

Objective: Close sprint; summarize shipped/rolled-back; prep next sprint.

Steps:
1) Aggregate "done" and any rolled_back tasks.
2) Extract key decisions from .oodatcaa/work/SPRINT_LOG.md + .oodatcaa/work/AGENT_LOG.md.
3) Append to .oodatcaa/work/SPRINT_LOG.md: shipped (PRs/tags), rollbacks (reasons), perf/coverage deltas (if known), improvements for next sprint.
4) Reset .oodatcaa/work/SPRINT_PLAN.md to next sprint skeleton.

Return diffs: .oodatcaa/work/SPRINT_LOG.md, .oodatcaa/work/SPRINT_PLAN.md.

