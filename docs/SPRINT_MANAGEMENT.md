# Sprint Management System

**Version:** 1.0  
**Last Updated:** 2025-10-03  
**Status:** Active

---

## Overview

The Sprint Management System provides automated tools for managing OODATCAA sprints, including:

- **Real-time Sprint Dashboard** - View current sprint status, progress, and metrics
- **Sprint Completion Automation** - Finalize sprints with full archival and retrospectives  
- **Sprint Initialization** - Bootstrap new sprints with proper structure and metadata

This system integrates with the OODATCAA (Observe → Orient → Decide → Act → Test → Check → Adapt → Archive) development protocol, providing visibility and automation for sprint transitions.

### Key Features

- **📊 Live Sprint Status** - Real-time progress tracking and WIP monitoring
- **✅ Exit Criteria Tracking** - Automatic validation of sprint completion requirements
- **🔄 Atomic Transitions** - Safe sprint transitions with rollback capability
- **📁 Automatic Archival** - Log rotation, report archiving, git tagging
- **🔍 Machine-Readable Metrics** - JSON status file for automation and dashboards
- **⚡ Fast Performance** - All commands complete in < 5 seconds

---

## Quick Start

```bash
# View current sprint status
make sprint-status

# Complete current sprint (when exit criteria met)
make sprint-complete

# Initialize new sprint
make sprint-new
```

---

## Command Reference

### `make sprint-status`

**Purpose:** Display real-time sprint dashboard with progress, task counts, WIP utilization, and exit criteria.

**Aliases:**
```bash
make sprint-status
bash scripts/sprint-dashboard.sh
```

**Output Sections:**
1. **Sprint Header** - Sprint ID, goal, status
2. **Progress** - Percentage complete, task breakdown
3. **Task Counts** - done, in_progress, ready, blocked, etc.
4. **WIP Utilization** - Current/limit for each agent role
5. **Exit Criteria** - Requirements for sprint completion
6. **Recent Activity** - Last N completed tasks
7. **Next Actions** - Ready tasks to pick up

**Example Output:**
```
======================================
  Sprint Status: SPRINT-2025-002
======================================

Sprint: OODATCAA Process Improvement
Status: in_progress
Progress: 35% complete (9 of 26 tasks)

Tasks:
  ✅ Done:          9 tasks
  🔄 In Progress:   2 task(s)
  ⏳ Ready:         5 task(s)
  🚫 Blocked:       8 task(s)
  📝 Planning:      2 task(s)

WIP Utilization:
  Builder:    1 / 3  (33%)
  Tester:     1 / 2  (50%)
  Integrator: 0 / 1  (0%)

Exit Criteria:
  ✅ P001: Daemon System Complete
  🔄 P002: Log Rotation System (in progress)
  ⏳ P003: Sprint Management System (ready)
```

**Generated Artifacts:**
- `.oodatcaa/work/SPRINT_STATUS.json` - Machine-readable sprint metrics (see Schema section)

**Performance:** < 2 seconds (typical), < 5 seconds (maximum)

**Use Cases:**
- Daily standup summaries
- Sprint review data collection
- Automated monitoring scripts
- Negotiator decision-making input

---

### `make sprint-complete`

**Purpose:** Finalize current sprint with full archival, retrospective generation, and git tagging.

**Aliases:**
```bash
make sprint-complete          # Normal mode (with confirmation)
make sprint-complete FORCE=1  # Skip confirmation prompt
bash scripts/sprint-complete.sh
bash scripts/sprint-complete.sh --force
```

**Options:**
- `--force` / `FORCE=1` - Skip confirmation prompt
- `--dry-run` - Show actions without executing (for testing)
- `--help` - Display usage information

**Workflow Steps:**

1. **Pre-Flight Validation**
   - Verify all exit criteria met
   - Check no tasks in "in_progress" status
   - Validate no active leases
   - Ensure SPRINT_STATUS.json exists (generates if missing)

2. **Archival Phase**
   - Trigger log rotation (calls `scripts/rotate-logs.sh`)
   - Archive SPRINT_QUEUE.json to `archive/sprint_N/`
   - Archive SPRINT_STATUS.json
   - Preserve all reports

3. **Status Updates**
   - Update SPRINT_QUEUE.json status to "completed"
   - Set completion timestamp
   - Calculate final metrics

4. **Retrospective Generation**
   - Create `.oodatcaa/work/SPRINT_RETROSPECTIVE_N.md`
   - Include: goals, achievements, metrics, challenges, lessons learned
   - Template for team review

5. **Git Tagging**
   - Create annotated tag: `sprint-N-complete`
   - Tag message includes: completion date, task counts, sprint goal
   - Example: `git tag -a sprint-2-complete -m "Sprint 2 Complete\n\nCompleted: 26 of 26 tasks\nGoal: OODATCAA Process Improvement\nDate: 2025-10-03T20:00:00Z"`

6. **Cleanup**
   - Remove stale leases
   - Clear temporary lock files
   - Update archive index

**Example Run:**
```bash
$ make sprint-complete

=== Sprint Completion Workflow ===

Sprint ID: SPRINT-2025-002
Sprint Number: 2
Goal: OODATCAA Process Improvement

=== Pre-Flight Checks ===
✅ Exit criteria met (3/3 objectives complete)
✅ No tasks in progress
✅ No active leases
✅ Status JSON exists

=== Archival ===
✅ Logs rotated (AGENT_LOG.md, SPRINT_LOG.md)
✅ SPRINT_QUEUE.json archived
✅ Reports preserved

=== Status Updates ===
✅ Sprint marked complete
✅ Final metrics calculated

=== Retrospective ===
✅ Generated: .oodatcaa/work/SPRINT_RETROSPECTIVE_2.md

=== Git Tag ===
✅ Created tag: sprint-2-complete

Sprint 2 completed successfully! 🎉
Ready to initialize Sprint 3 with: make sprint-new
```

**Error Handling:**
- **Exit criteria not met:** Aborts with error message listing incomplete objectives
- **Tasks in progress:** Requires all tasks to be done/blocked/ready (no in_progress)
- **Active leases:** Must release or break stale leases first
- **File operation failures:** Atomic operations ensure no partial state

**Rollback:**
If sprint-complete fails mid-execution, manual rollback steps:
```bash
# 1. Restore SPRINT_QUEUE.json from backup
cp .oodatcaa/work/SPRINT_QUEUE.json.backup .oodatcaa/work/SPRINT_QUEUE.json

# 2. Remove incomplete tag (if created)
git tag -d sprint-N-complete

# 3. Check for partial archives (manually review)
ls .oodatcaa/work/archive/sprint_N/

# 4. Re-run with --dry-run to diagnose
bash scripts/sprint-complete.sh --dry-run
```

---

### `make sprint-new`

**Purpose:** Initialize a new sprint with proper directory structure, metadata, and clean state.

**Aliases:**
```bash
make sprint-new              # Normal mode (with confirmation)
make sprint-new FORCE=1      # Skip confirmation prompt
bash scripts/sprint-new.sh
bash scripts/sprint-new.sh --force
```

**Options:**
- `--force` / `FORCE=1` - Skip confirmation prompt
- `--help` - Display usage information

**Workflow Steps:**

1. **Pre-Flight Validation**
   - Verify current sprint is "completed"
   - Check no active tasks remain (all done/cancelled)
   - Ensure no active leases
   - Validate archive exists for previous sprint

2. **Sprint Number Calculation**
   - Read current sprint number from SPRINT_QUEUE.json
   - Increment by 1 (e.g., 2 → 3)
   - Generate new sprint ID: SPRINT-YYYY-NNN
     - YYYY: Current year
     - NNN: Zero-padded sprint number (e.g., 003)

3. **Directory Setup**
   - Create `.oodatcaa/work/archive/sprint_N/` (if not exists)
   - Create `.oodatcaa/work/reports/sprint_N/` (for new sprint reports)
   - Preserve existing structure

4. **File Initialization**
   - **AGENT_LOG.md** - Reset with header for new sprint
   - **SPRINT_LOG.md** - Reset with sprint metadata
   - **SPRINT_PLAN.md** - Reset with "Pending Sprint Planner" message
   - **SPRINT_QUEUE.json** - Initialize with new sprint metadata

5. **SPRINT_QUEUE.json Template:**
```json
{
  "sprint": 3,
  "status": "needs_planning",
  "wip_limits": {
    "builder": 3,
    "tester": 2,
    "integrator": 1
  },
  "metadata": {
    "sprint_id": "SPRINT-2025-003",
    "sprint_goal": "TBD - Awaiting Sprint Planner",
    "start_date": "2025-10-04T00:00:00Z",
    "target_date": null,
    "total_tasks": 0,
    "done_tasks": 0
  },
  "tasks": []
}
```

6. **SPRINT_GOAL.md Updates**
   - Update status to "planning"
   - Set sprint number and ID
   - Clear previous sprint objectives
   - Add "Awaiting Sprint Planner" note

7. **Cleanup**
   - Remove all stale leases (`.leases/*.json`)
   - Clear temporary lock files (`.locks/*.lock`)
   - Clean up any orphaned temp files

8. **Validation**
   - Verify JSON syntax valid
   - Check all required directories exist
   - Confirm sprint number incremented correctly

**Example Run:**
```bash
$ make sprint-new

=== Sprint Initialization Workflow ===

Current Sprint: 2 (SPRINT-2025-002)
Status: completed
Next Sprint: 3 (SPRINT-2025-003)

=== Pre-Flight Checks ===
✅ Current sprint completed
✅ No active tasks
✅ No active leases
✅ Archive exists for Sprint 2

=== Directory Setup ===
✅ Created: .oodatcaa/work/archive/sprint_3/
✅ Created: .oodatcaa/work/reports/sprint_3/

=== File Initialization ===
✅ Reset: AGENT_LOG.md
✅ Reset: SPRINT_LOG.md
✅ Reset: SPRINT_PLAN.md
✅ Initialized: SPRINT_QUEUE.json

=== Cleanup ===
✅ Removed 2 stale leases
✅ Cleared 1 lock file

Sprint 3 (SPRINT-2025-003) initialized successfully! 🚀
Next: Run Sprint Planner to define sprint goal and backlog
```

**Error Handling:**
- **Sprint not completed:** Aborts if current sprint status ≠ "completed"
- **Active tasks:** Requires all tasks done/cancelled before new sprint
- **Active leases:** Must be cleaned up first
- **JSON errors:** Validates syntax before writing files

**Next Steps After Initialization:**
1. Run Sprint Planner to generate SPRINT_GOAL.md
2. Sprint Planner populates SPRINT_QUEUE.json with tasks
3. Run Negotiator to begin work

---

## SPRINT_STATUS.json Schema

The `SPRINT_STATUS.json` file provides machine-readable sprint metrics for automation, dashboards, and agent decision-making.

**Location:** `.oodatcaa/work/SPRINT_STATUS.json`

**Generated By:** `scripts/sprint-dashboard.sh`

**Update Frequency:** On-demand (call `make sprint-status`)

### Schema Definition

```json
{
  "sprint_id": "SPRINT-2025-002",
  "sprint_number": 2,
  "status": "in_progress",
  "generated_at": "2025-10-03T20:30:00Z",
  "progress": {
    "total_tasks": 26,
    "completed": 9,
    "in_progress": 2,
    "ready": 5,
    "blocked": 8,
    "needs_plan": 0,
    "planning": 2,
    "awaiting_test": 0,
    "percentage": 35
  },
  "wip": {
    "builder": { "current": 1, "limit": 3, "utilization": 33 },
    "tester": { "current": 1, "limit": 2, "utilization": 50 },
    "integrator": { "current": 0, "limit": 1, "utilization": 0 }
  },
  "exit_criteria": [
    {
      "name": "P001: Daemon System",
      "status": "done",
      "progress": 100
    },
    {
      "name": "P002: Log Rotation",
      "status": "in_progress",
      "progress": 50
    },
    {
      "name": "P003: Sprint Management",
      "status": "ready",
      "progress": 25
    }
  ]
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `sprint_id` | string | Unique sprint identifier (SPRINT-YYYY-NNN) |
| `sprint_number` | integer | Sequential sprint number |
| `status` | string | Sprint status: needs_planning, planning, in_progress, completed |
| `generated_at` | string (ISO8601) | Timestamp of status generation |
| `progress.total_tasks` | integer | Total tasks in sprint |
| `progress.completed` | integer | Tasks with status="done" |
| `progress.in_progress` | integer | Tasks currently being worked on |
| `progress.ready` | integer | Tasks ready to pick up |
| `progress.blocked` | integer | Tasks blocked by dependencies |
| `progress.needs_plan` | integer | Tasks awaiting planner |
| `progress.planning` | integer | Tasks currently being planned |
| `progress.awaiting_test` | integer | Tasks completed, awaiting tester |
| `progress.percentage` | integer | Overall completion percentage (0-100) |
| `wip.{role}.current` | integer | Current WIP for role |
| `wip.{role}.limit` | integer | WIP limit for role |
| `wip.{role}.utilization` | integer | Utilization percentage (0-100) |
| `exit_criteria[].name` | string | Exit criterion name (typically objective ID) |
| `exit_criteria[].status` | string | Criterion status (done, in_progress, ready, blocked) |
| `exit_criteria[].progress` | integer | Criterion progress percentage (0-100) |

### Usage Examples

#### Query Sprint Progress
```bash
# Get overall completion percentage
jq '.progress.percentage' .oodatcaa/work/SPRINT_STATUS.json

# Get task breakdown
jq '.progress | {done: .completed, total: .total_tasks}' .oodatcaa/work/SPRINT_STATUS.json
```

#### Check WIP Availability
```bash
# Check if builder can take more work
BUILDER_WIP=$(jq '.wip.builder.current' .oodatcaa/work/SPRINT_STATUS.json)
BUILDER_LIMIT=$(jq '.wip.builder.limit' .oodatcaa/work/SPRINT_STATUS.json)
if [ "$BUILDER_WIP" -lt "$BUILDER_LIMIT" ]; then
  echo "Builder capacity available"
fi
```

#### Monitor Exit Criteria
```bash
# List incomplete exit criteria
jq '.exit_criteria[] | select(.status != "done") | .name' .oodatcaa/work/SPRINT_STATUS.json
```

#### Automated Sprint Completion Detection
```bash
# Check if sprint ready for completion
ALL_DONE=$(jq '[.exit_criteria[] | select(.status != "done")] | length == 0' .oodatcaa/work/SPRINT_STATUS.json)
NO_WIP=$(jq '.progress.in_progress == 0' .oodatcaa/work/SPRINT_STATUS.json)

if [ "$ALL_DONE" = "true" ] && [ "$NO_WIP" = "true" ]; then
  echo "Sprint ready for completion"
  make sprint-complete
fi
```

---

## Workflow Examples

### Typical Sprint Lifecycle

```bash
# 1. Monitor current sprint
make sprint-status

# 2. Work on tasks (builders, testers, integrators)
# ... (agents work on tasks)

# 3. Check progress periodically
make sprint-status

# 4. When exit criteria met
make sprint-status | grep "Exit Criteria"
# All criteria show ✅

# 5. Complete current sprint
make sprint-complete
# Confirms: Archives logs, generates retrospective, creates git tag

# 6. Initialize next sprint
make sprint-new
# Creates Sprint 3 structure

# 7. Run Sprint Planner (defines new sprint goal/tasks)
# (Negotiator or manual Sprint Planner invocation)

# 8. Begin new sprint
make sprint-status  # Shows Sprint 3 progress
```

### Emergency Sprint Rollback

If sprint-complete fails or sprint needs to be reverted:

```bash
# 1. Check current state
make sprint-status
git status

# 2. Restore SPRINT_QUEUE.json from backup
cp .oodatcaa/work/SPRINT_QUEUE.json.backup .oodatcaa/work/SPRINT_QUEUE.json

# 3. Remove incomplete git tag
git tag -d sprint-N-complete  # Replace N with sprint number

# 4. Check archive for partial files
ls .oodatcaa/work/archive/sprint_N/

# 5. Manually clean up if needed
rm .oodatcaa/work/archive/sprint_N/SPRINT_QUEUE.json  # If partial
rm .oodatcaa/work/SPRINT_RETROSPECTIVE_N.md  # If incomplete

# 6. Verify sprint state restored
make sprint-status

# 7. Fix root cause before retrying sprint-complete
```

### Manual Sprint Transition (Without Automation)

If automation scripts unavailable:

```bash
# 1. Archive logs
bash scripts/rotate-logs.sh

# 2. Copy SPRINT_QUEUE.json to archive
SPRINT_NUM=$(jq -r '.sprint' .oodatcaa/work/SPRINT_QUEUE.json)
mkdir -p .oodatcaa/work/archive/sprint_${SPRINT_NUM}
cp .oodatcaa/work/SPRINT_QUEUE.json .oodatcaa/work/archive/sprint_${SPRINT_NUM}/

# 3. Update sprint status
jq '.status = "completed" | .metadata.end_date = "'$(date -Iseconds)'"' .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue.json
mv /tmp/queue.json .oodatcaa/work/SPRINT_QUEUE.json

# 4. Create git tag
git tag -a sprint-${SPRINT_NUM}-complete -m "Sprint ${SPRINT_NUM} Complete"

# 5. Initialize new sprint (increment sprint number)
NEXT_SPRINT=$((SPRINT_NUM + 1))
# Manually edit SPRINT_QUEUE.json to increment sprint number and reset tasks
```

---

## Troubleshooting

### Common Issues

#### Issue: "Exit criteria not met" when running sprint-complete

**Symptoms:**
- `make sprint-complete` aborts with error
- Message: "❌ Exit criteria not met: X of Y objectives incomplete"

**Diagnosis:**
```bash
# Check current exit criteria status
make sprint-status | grep -A 10 "Exit Criteria"

# List incomplete objectives
jq '.exit_criteria[] | select(.status != "done")' .oodatcaa/work/SPRINT_STATUS.json
```

**Solution:**
- Complete all objectives before sprint completion
- OR negotiate with Planner/Negotiator to defer incomplete objectives to next sprint
- Update SPRINT_QUEUE.json to mark deferred objectives as "cancelled" or move to next sprint

**Prevention:**
- Monitor exit criteria regularly (`make sprint-status`)
- Adjust sprint scope if objectives at risk

---

#### Issue: "Tasks still in progress" blocking sprint-complete

**Symptoms:**
- `make sprint-complete` fails
- Message: "❌ Cannot complete sprint: N tasks still in progress"

**Diagnosis:**
```bash
# List in-progress tasks
jq '.tasks[] | select(.status == "in_progress") | {id, title, agent, lease}' .oodatcaa/work/SPRINT_QUEUE.json
```

**Solution:**
1. Wait for agents to complete their work
2. OR check for stale leases:
   ```bash
   # Identify stale leases (heartbeat + TTL expired)
   find .leases -name "*.json" -mmin +90  # Older than 90 minutes
   
   # Manually break stale leases (use caution)
   rm .leases/P003-B02.json
   
   # Update task status to "ready" or "awaiting_test"
   jq '.tasks |= map(if .id == "P003-B02" then .status = "awaiting_test" | .lease = null else . end)' .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue.json
   mv /tmp/queue.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

**Prevention:**
- Use Builder protocol lease heartbeats
- Implement lease TTL monitoring
- Negotiator should enforce WIP limits

---

#### Issue: SPRINT_STATUS.json not found during sprint-complete

**Symptoms:**
- Error: `fatal: pathspec '.oodatcaa/work/SPRINT_STATUS.json' did not match any files`

**Diagnosis:**
```bash
# Check if file exists
test -f .oodatcaa/work/SPRINT_STATUS.json && echo "EXISTS" || echo "MISSING"
```

**Solution:**
The `sprint-complete.sh` script automatically handles this by running `sprint-dashboard.sh` if STATUS file missing:

```bash
# Manual fix if needed
make sprint-status  # Generates SPRINT_STATUS.json
make sprint-complete
```

**Prevention:**
- Run `make sprint-status` periodically
- Updated `sprint-complete.sh` (v1.1+) auto-generates if missing

---

#### Issue: Sprint number not incrementing correctly

**Symptoms:**
- `make sprint-new` creates sprint with wrong number
- Sprint ID format incorrect

**Diagnosis:**
```bash
# Check current sprint number
jq '.sprint' .oodatcaa/work/SPRINT_QUEUE.json

# Check sprint_id format
jq '.metadata.sprint_id' .oodatcaa/work/SPRINT_QUEUE.json

# Verify against objective files
ls .oodatcaa/objectives/SPRINT_*
```

**Solution:**
```bash
# Manually correct sprint number in SPRINT_QUEUE.json
jq '.sprint = 3 | .metadata.sprint_id = "SPRINT-2025-003"' .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue.json
mv /tmp/queue.json .oodatcaa/work/SPRINT_QUEUE.json

# Update SPRINT_GOAL.md
sed -i 's/SPRINT-2025-002/SPRINT-2025-003/g' .oodatcaa/objectives/SPRINT_GOAL.md
```

**Prevention:**
- Always use `make sprint-new` for new sprints
- Verify sprint number immediately after initialization
- Check git tags for sprint history: `git tag -l "sprint-*"`

---

#### Issue: Makefile target "sprint-status" not found

**Symptoms:**
- `make: *** No rule to make target 'sprint-status'`

**Diagnosis:**
```bash
# Check if targets exist in Makefile
grep -E "sprint-status|sprint-complete|sprint-new" Makefile
```

**Solution:**
```bash
# Verify on correct branch
git branch --show-current

# Check if Makefile has sprint targets
git log --oneline --all --grep="sprint.*management" -- Makefile

# If missing, integrate from P003-B02:
git show feat/P003-step-02-sprint-init:Makefile | grep -A 10 "Sprint Management"
```

**Prevention:**
- Ensure P003-B02 integrated to main
- Pull latest changes: `git pull origin main`

---

#### Issue: Performance degradation (commands taking > 5 seconds)

**Symptoms:**
- `make sprint-status` slow
- Scripts taking longer than expected

**Diagnosis:**
```bash
# Benchmark each command
time make sprint-status
time bash scripts/sprint-dashboard.sh
time bash scripts/sprint-complete.sh --dry-run

# Check SPRINT_QUEUE.json size
wc -l .oodatcaa/work/SPRINT_QUEUE.json
du -h .oodatcaa/work/SPRINT_QUEUE.json

# Profile script execution
bash -x scripts/sprint-dashboard.sh 2>&1 | head -100
```

**Solution:**
1. **Large SPRINT_QUEUE.json**: Archive completed sprints to reduce file size
2. **Slow jq queries**: Optimize queries to avoid full array scans
3. **Disk I/O**: Check disk health, free space

```bash
# Archive old sprints if SPRINT_QUEUE.json > 10KB
# (sprint-complete should handle this automatically)

# Check disk space
df -h .oodatcaa/work

# Verify no background processes interfering
ps aux | grep -E "jq|bash.*sprint"
```

**Prevention:**
- Regular sprint completion and archival
- Monitor log file sizes (use log rotation)
- Optimize jq queries in scripts

---

## Integration with OODATCAA Loop

The Sprint Management System integrates with each stage of the OODATCAA protocol:

### Observe
- **Sprint Dashboard (`make sprint-status`)** provides real-time system state
- **SPRINT_STATUS.json** supplies structured data for agent decision-making
- Negotiator uses sprint metrics to assess progress

### Orient
- **Exit Criteria** help agents understand sprint goals
- **WIP Utilization** guides task selection (avoid overload)
- **Task Status** informs planning decisions

### Decide
- Sprint Planner uses **Sprint Completion retrospectives** for future planning
- Negotiator decides when to trigger **sprint-complete** based on exit criteria
- Agents reference **ready task counts** to pick next work

### Act
- Builders/Testers/Integrators work on sprint tasks
- Status updates reflected in real-time dashboard
- WIP limits enforced through sprint queue

### Test
- Testers validate exit criteria met
- Integration tests run before sprint completion
- Quality gates verified by sprint-complete script

### Check
- **Sprint Dashboard** provides check mechanism
- **Exit Criteria validation** in sprint-complete
- Retrospective reviews sprint success

### Adapt
- **Retrospectives** capture lessons learned
- Sprint Planner adapts next sprint based on retrospective
- WIP limits adjusted based on utilization metrics

### Archive
- **sprint-complete** triggers full archival
- Logs rotated to archive/sprint_N/
- Git tags create permanent sprint markers
- Retrospectives preserved for future reference

---

## Advanced Topics

### Custom Exit Criteria

Edit SPRINT_QUEUE.json to define custom exit criteria:

```json
{
  "metadata": {
    "exit_criteria": [
      {
        "name": "Custom Objective",
        "description": "Deploy to staging",
        "objective_link": "P999-DEPLOY",
        "required": true
      }
    ]
  }
}
```

Sprint dashboard will automatically track these criteria.

### Sprint Duration Tracking

Add target dates to SPRINT_QUEUE.json:

```json
{
  "metadata": {
    "start_date": "2025-10-01T00:00:00Z",
    "target_date": "2025-10-14T23:59:59Z"
  }
}
```

Calculate sprint duration:
```bash
START=$(jq -r '.metadata.start_date' .oodatcaa/work/SPRINT_QUEUE.json)
TARGET=$(jq -r '.metadata.target_date' .oodatcaa/work/SPRINT_QUEUE.json)
DAYS_REMAINING=$(( ($(date -d "$TARGET" +%s) - $(date +%s)) / 86400 ))
echo "Days remaining: $DAYS_REMAINING"
```

### Multi-Project Sprints

For sprints spanning multiple projects, use objective links to track:

```json
{
  "tasks": [
    {
      "id": "P001-B01",
      "project": "MCPLocalLLM",
      "objective_link": "SPRINT-2025-002"
    },
    {
      "id": "EXT-001",
      "project": "ExternalDependency",
      "objective_link": "SPRINT-2025-002"
    }
  ]
}
```

Filter dashboard by project:
```bash
jq '.tasks[] | select(.project == "MCPLocalLLM")' .oodatcaa/work/SPRINT_QUEUE.json
```

---

## References

- **P003: Enhanced Sprint Management System** - Parent task documentation
- **OODATCAA Loop Guide:** `.oodatcaa/OODATCAA_LOOP_GUIDE.md`
- **Log Rotation System (P002):** `scripts/rotate-logs.sh`, `ROTATION_STATS.md`
- **Agent Management:** `.oodatcaa/AGENT_MANAGEMENT.md`
- **SPRINT_QUEUE.json Schema:** `.oodatcaa/work/SPRINT_QUEUE.json` (current)
- **Sprint Completion Reports:** `.oodatcaa/work/reports/P003/`

---

## Appendix: Script Details

### scripts/sprint-dashboard.sh

- **Lines:** 180
- **Dependencies:** jq, bash 4+
- **Generated Files:** `.oodatcaa/work/SPRINT_STATUS.json`
- **Performance:** < 2 seconds (typical)
- **Author:** Builder agent-builder-B2 (P003-B01)
- **Version:** 1.0

### scripts/sprint-complete.sh

- **Lines:** ~200
- **Dependencies:** jq, git, bash 4+, rotate-logs.sh
- **Modified Files:** SPRINT_QUEUE.json, git tags
- **Generated Files:** SPRINT_RETROSPECTIVE_N.md
- **Performance:** < 5 seconds (dry-run), < 15 seconds (full run)
- **Author:** Builder agent-builder-B2 (P003-B01)
- **Version:** 1.1 (auto-generates SPRINT_STATUS.json if missing)

### scripts/sprint-new.sh

- **Lines:** 273
- **Dependencies:** jq, bash 4+
- **Modified Files:** SPRINT_QUEUE.json, SPRINT_GOAL.md, logs
- **Cleanup:** Leases, locks, temp files
- **Performance:** < 5 seconds
- **Author:** Builder agent-builder-A (P003-B02)
- **Version:** 1.0

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-03  
**Next Review:** End of Sprint 2  
**Maintainer:** OODATCAA Integrator Agent

