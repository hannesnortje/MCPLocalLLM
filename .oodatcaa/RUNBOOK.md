# OODATCAA Operational Runbook

**Version:** 1.0  
**Last Updated:** 2025-10-04  
**Status:** Production Ready

---

## Table of Contents

- [Introduction](#introduction)
- [Sprint Operations](#sprint-operations)
- [Agent Operations](#agent-operations)
- [System Maintenance](#system-maintenance)
- [Emergency Procedures](#emergency-procedures)
- [Quick Reference](#quick-reference)

---

## Introduction

This runbook provides step-by-step procedures for common operational tasks in the OODATCAA (Observe → Orient → Decide → Act → Test → Check → Adapt → Archive) multi-agent development system.

**Who Is This For:**
- System operators managing OODATCAA deployments
- Agent coordinators troubleshooting issues
- Developers onboarding to the system

**Prerequisites:**
- Project cloned and setup complete (`./scripts/setup-dev.sh`)
- Environment validated (`make validate-env`)
- Basic understanding of the OODATCAA loop (see `.oodatcaa/OODATCAA_LOOP_GUIDE.md`)

---

## Sprint Operations

### Scenario 1: Starting a New Sprint

**When:** Beginning a new development cycle  
**Goal:** Initialize sprint infrastructure with proper backlog and objectives

#### Procedure:

1. **Review Current Sprint Status**
   ```bash
   make sprint-dashboard
   ```

2. **Complete Previous Sprint (if needed)**
   ```bash
   make sprint-complete
   ```

3. **Create Sprint Objective**
   ```bash
   # Edit sprint objective file
   nano .oodatcaa/objectives/SPRINT_GOAL.md
   ```
   
   Include:
   - Sprint goals (3-5 key objectives)
   - Success criteria (measurable outcomes)
   - Constraints and assumptions
   - Exit criteria

4. **Initialize New Sprint**
   ```bash
   make sprint-new
   ```

5. **Verify Sprint Initialization**
   ```bash
   jq '.sprint, .sprint_id, .total_tasks' .oodatcaa/work/SPRINT_QUEUE.json
   ```

#### Expected Output:
```json
{
  "sprint": 3,
  "sprint_id": "SPRINT-2025-003",
  "total_tasks": 0
}
```

#### Troubleshooting:
- **Issue:** `sprint-new` fails → **Solution:** Ensure previous sprint is complete
- **Issue:** Objectives not found → **Solution:** Verify `.oodatcaa/objectives/SPRINT_GOAL.md` exists
- **Issue:** Git conflicts → **Solution:** Commit/stash local changes first

#### See Also:
- [Scenario 2: Completing a Sprint](#scenario-2-completing-a-sprint)
- [Scenario 3: Checking Sprint Status](#scenario-3-checking-sprint-status)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#sprint-initialization-fails)

---

### Scenario 2: Completing a Sprint

**When:** All sprint tasks are done  
**Goal:** Archive sprint data and prepare for next cycle

#### Procedure:

1. **Verify Sprint Completion**
   ```bash
   make sprint-dashboard
   ```
   
   Check:
   - All tasks status: `done` or `cancelled`
   - Exit criteria met (see `SPRINT_GOAL.md`)

2. **Run Sprint Completion**
   ```bash
   make sprint-complete
   ```

3. **Review Generated Artifacts**
   ```bash
   ls -lh .oodatcaa/work/archive/sprint_N/
   ```
   
   Expected files:
   - `AGENT_LOG_final.md`
   - `SPRINT_LOG_final.md`
   - `SPRINT_PLAN_final.md`
   - `SPRINT_QUEUE_final.json`

4. **Tag Sprint Release**
   ```bash
   git tag sprint-N-complete
   git push origin sprint-N-complete
   ```

5. **Update CHANGELOG**
   ```bash
   nano CHANGELOG.md
   ```
   
   Add sprint summary section.

6. **Commit Sprint Completion**
   ```bash
   git add .oodatcaa/work/archive/ CHANGELOG.md
   git commit -m "[sprint] Sprint N completion - all tasks done"
   git push origin main
   ```

#### Expected Output:
```
✅ Sprint N completion successful
📦 Archives created in .oodatcaa/work/archive/sprint_N/
🏷️  Tag: sprint-N-complete
```

#### Troubleshooting:
- **Issue:** Incomplete tasks → **Solution:** Review `SPRINT_QUEUE.json`, complete or cancel remaining tasks
- **Issue:** Archive directory exists → **Solution:** Incremental archive files created with timestamps
- **Issue:** CHANGELOG conflicts → **Solution:** Merge manually, preserving both sprint summaries

#### See Also:
- [Scenario 1: Starting a New Sprint](#scenario-1-starting-a-new-sprint)
- [Scenario 15: Archiving Logs](#scenario-15-archiving-logs)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#sprint-completion-issues)

---

### Scenario 3: Checking Sprint Status

**When:** Regular status checks (daily standup, progress review)  
**Goal:** Get real-time sprint metrics and task status

#### Procedure:

1. **View Sprint Dashboard**
   ```bash
   make sprint-dashboard
   ```
   
   Displays:
   - Sprint number and ID
   - Task counts by status
   - Completion percentage
   - Active agents
   - Next 5 ready tasks

2. **Check Detailed Status (JSON)**
   ```bash
   cat .oodatcaa/work/SPRINT_STATUS.json | jq
   ```

3. **View Task Breakdown by Agent**
   ```bash
   jq '.tasks | group_by(.agent) | map({agent: .[0].agent, count: length})' .oodatcaa/work/SPRINT_QUEUE.json
   ```

4. **List Blocked Tasks**
   ```bash
   jq '.tasks[] | select(.status == "blocked") | {id, title, blocked_reason}' .oodatcaa/work/SPRINT_QUEUE.json
   ```

5. **Check WIP Limits**
   ```bash
   jq '{wip_limits, in_progress: [.tasks[] | select(.status == "in_progress") | .id]}' .oodatcaa/work/SPRINT_QUEUE.json
   ```

#### Expected Output:
```
=== SPRINT DASHBOARD ===
Sprint: 2 (SPRINT-2025-002)
Status: In Progress

Tasks: 14/34 complete (41%)
- Done: 14
- In Progress: 1
- Ready: 3
- Blocked: 8
- Cancelled: 0

Active Agents: 1
- Builder: 1/3 (33% utilization)

Next 5 Ready Tasks:
1. P006-B01 (priority 6)
2. ...
```

#### Troubleshooting:
- **Issue:** Dashboard shows stale data → **Solution:** Ensure `SPRINT_STATUS.json` is current (`make sprint-dashboard` regenerates)
- **Issue:** WIP exceeded → **Solution:** Review in-progress tasks, ensure leases are active
- **Issue:** No ready tasks → **Solution:** Check dependencies, unblock or complete prerequisites

#### See Also:
- [Scenario 4: Viewing Agent Activity](#scenario-4-viewing-agent-activity)
- [Scenario 9: Checking Agent WIP Limits](#scenario-9-checking-agent-wip-limits)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#sprint-dashboard-issues)

---

### Scenario 4: Viewing Agent Activity

**When:** Investigating agent behavior or progress  
**Goal:** Review detailed agent execution logs

#### Procedure:

1. **View Recent Agent Activity (Last 50 Lines)**
   ```bash
   tail -50 .oodatcaa/work/AGENT_LOG.md
   ```

2. **Search for Specific Agent**
   ```bash
   grep "agent-builder-A" .oodatcaa/work/AGENT_LOG.md | tail -20
   ```

3. **View Agent Reports (Executive Summary)**
   ```bash
   less .oodatcaa/work/AGENT_REPORTS.md
   ```

4. **Find Specific Task Report**
   ```bash
   find .oodatcaa/work/reports/ -name "*P006*" -type f
   cat .oodatcaa/work/reports/P006/builder_P006-B01.md
   ```

5. **Check Agent Completion Times**
   ```bash
   grep "Duration:" .oodatcaa/work/AGENT_REPORTS.md
   ```

#### Expected Output:
```markdown
## 🎯 13th Autonomous Operation Complete: P001-B03

**AGENT:** Builder (agent-builder-cursor)
**TASK:** P001-B03 - Testing + Docs + Quality
**STATUS:** in_progress → awaiting_test
**Duration:** 67 minutes
```

#### Troubleshooting:
- **Issue:** Log file too large → **Solution:** Use `grep`, `less`, or pagination commands
- **Issue:** Missing report → **Solution:** Check if task completed (status `done`/`awaiting_test`)
- **Issue:** Agent not logging → **Solution:** Verify agent is running and has write permissions

#### See Also:
- [Scenario 3: Checking Sprint Status](#scenario-3-checking-sprint-status)
- [Scenario 15: Archiving Logs](#scenario-15-archiving-logs)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#agent-activity-tracking)

---

## Agent Operations

### Scenario 5: Starting Background Agents

**When:** Enabling autonomous agent operation  
**Goal:** Start agent daemons to auto-claim work

#### Procedure:

**Option A: Systemd (Linux)**

1. **Start All Agents**
   ```bash
   make agents-start
   ```

2. **Start Specific Agent**
   ```bash
   systemctl --user start agent-builder
   ```

3. **Check Status**
   ```bash
   make agents-status
   ```

4. **View Logs**
   ```bash
   journalctl --user -u agent-builder -f
   ```

**Option B: CLI (Cross-Platform)**

1. **Start Agent**
   ```bash
   bash scripts/agents-daemon-cli.sh start builder
   ```

2. **Check Status**
   ```bash
   bash scripts/agents-daemon-cli.sh status builder
   ```

3. **View Logs**
   ```bash
   tail -f .agent-daemon-logs/builder.log
   ```

#### Expected Output:
```
✅ agent-builder started (PID: 12345)
✅ agent-tester started (PID: 12346)
✅ agent-planner started (PID: 12347)

All agents running. Poll interval: 60s
```

#### Troubleshooting:
- **Issue:** Systemd not available → **Solution:** Use CLI mode (Option B)
- **Issue:** Agent won't start → **Solution:** Check logs for errors, verify Python dependencies
- **Issue:** Agent crashes immediately → **Solution:** Check `SPRINT_QUEUE.json` is valid JSON

#### See Also:
- [Scenario 6: Stopping Background Agents](#scenario-6-stopping-background-agents)
- [Scenario 9: Checking Agent WIP Limits](#scenario-9-checking-agent-wip-limits)
- [BACKGROUND_AGENTS.md](../docs/BACKGROUND_AGENTS.md)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#agent-daemon-issues)

---

### Scenario 6: Stopping Background Agents

**When:** Pausing autonomous operations, system maintenance  
**Goal:** Gracefully stop agent daemons

#### Procedure:

**Option A: Systemd (Linux)**

1. **Stop All Agents**
   ```bash
   make agents-stop
   ```

2. **Stop Specific Agent**
   ```bash
   systemctl --user stop agent-builder
   ```

3. **Verify Stopped**
   ```bash
   make agents-status
   ```

**Option B: CLI (Cross-Platform)**

1. **Stop Agent**
   ```bash
   bash scripts/agents-daemon-cli.sh stop builder
   ```

2. **Stop All Agents**
   ```bash
   for role in planner builder tester refiner integrator; do
       bash scripts/agents-daemon-cli.sh stop $role
   done
   ```

3. **Verify Stopped**
   ```bash
   bash scripts/agents-daemon-cli.sh status builder
   ```

#### Expected Output:
```
🛑 Stopping agent-builder (PID: 12345)...
✅ agent-builder stopped
✅ Lease released cleanly
```

#### Troubleshooting:
- **Issue:** Agent won't stop → **Solution:** Force kill with `kill -9 <PID>`
- **Issue:** Stale lease after stop → **Solution:** Manually remove `.leases/<task>.json`
- **Issue:** Agent restarted by systemd → **Solution:** Disable auto-restart: `systemctl --user disable agent-builder`

#### See Also:
- [Scenario 5: Starting Background Agents](#scenario-5-starting-background-agents)
- [Scenario 10: Managing Task Leases](#scenario-10-managing-task-leases)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#agent-shutdown-issues)

---

### Scenario 7: Running Agent Manually

**When:** Testing agent behavior, debugging issues  
**Goal:** Execute agent prompt manually with full control

#### Procedure:

1. **Load Agent Prompt**
   ```bash
   cat .oodatcaa/prompts/builder.md
   ```

2. **Execute via Cursor/IDE**
   - Open Cursor
   - Select agent prompt file
   - Run "Load @Cursor Rules and @Project Rules"
   - Run prompt exactly as written

3. **Verify Execution**
   ```bash
   # Check lease created
   ls -la .leases/
   
   # Check queue updated
   jq '.tasks[] | select(.status == "in_progress")' .oodatcaa/work/SPRINT_QUEUE.json
   
   # Check logs
   tail -20 .oodatcaa/work/AGENT_LOG.md
   ```

4. **Monitor Progress**
   ```bash
   watch -n 10 'jq ".tasks[] | select(.id == \"P006-B01\") | {status, lease}" .oodatcaa/work/SPRINT_QUEUE.json'
   ```

#### Expected Output:
```
=== BUILDER PROTOCOL: Step 1 - PICK TASK ===
✅ Task found: P006-B01
Status: ready → in_progress
Lease acquired: .leases/P006-B01.json
Branch created: feat/P006-step-01-operational-docs
```

#### Troubleshooting:
- **Issue:** Agent picks wrong task → **Solution:** Ensure task priorities and dependencies correct in `SPRINT_QUEUE.json`
- **Issue:** Lease conflict → **Solution:** Remove stale lease, verify no other agent running
- **Issue:** Agent stalls → **Solution:** Check logs, verify network/API access if needed

#### See Also:
- [Scenario 8: Claiming a Task](#scenario-8-claiming-a-task)
- [Scenario 10: Managing Task Leases](#scenario-10-managing-task-leases)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#manual-agent-execution)

---

### Scenario 8: Claiming a Task

**When:** Manually assigning work to an agent  
**Goal:** Reserve task and prevent race conditions

#### Procedure:

1. **View Available Tasks**
   ```bash
   jq '.tasks[] | select(.status == "ready" and (.lease == null or .lease == "")) | {id, title, agent}' .oodatcaa/work/SPRINT_QUEUE.json
   ```

2. **Create Lease (Manual)**
   ```bash
   TASK_ID="P006-B01"
   cat > .leases/${TASK_ID}.json <<EOF
   {
     "task_id": "$TASK_ID",
     "agent": "builder",
     "owner": "manual-claim",
     "acquired": "$(date -Iseconds)",
     "ttl": 7200,
     "last_heartbeat": "$(date -Iseconds)"
   }
   EOF
   ```

3. **Update Queue Status**
   ```bash
   jq --arg lease "$(cat .leases/P006-B01.json)" \
      '.tasks |= map(if .id == "P006-B01" then .lease = ($lease | fromjson) | .status = "in_progress" else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

4. **Verify Claim**
   ```bash
   jq '.tasks[] | select(.id == "P006-B01") | {status, lease}' .oodatcaa/work/SPRINT_QUEUE.json
   ```

#### Expected Output:
```json
{
  "status": "in_progress",
  "lease": {
    "task_id": "P006-B01",
    "agent": "builder",
    "owner": "manual-claim",
    "acquired": "2025-10-04T16:35:31+02:00"
  }
}
```

#### Troubleshooting:
- **Issue:** Lease already exists → **Solution:** Check if agent is working on task, remove stale lease if abandoned
- **Issue:** JSON parsing error → **Solution:** Verify `jq` syntax, check quote escaping
- **Issue:** Status not updated → **Solution:** Ensure `mv` succeeded, verify JSON file not locked

#### See Also:
- [Scenario 9: Checking Agent WIP Limits](#scenario-9-checking-agent-wip-limits)
- [Scenario 10: Managing Task Leases](#scenario-10-managing-task-leases)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#task-claiming-failures)

---

### Scenario 9: Checking Agent WIP Limits

**When:** Diagnosing why agent won't claim work  
**Goal:** Verify WIP enforcement is working correctly

#### Procedure:

1. **View Current WIP Limits**
   ```bash
   jq '.wip_limits' .oodatcaa/work/SPRINT_QUEUE.json
   ```

2. **Count In-Progress Tasks by Agent**
   ```bash
   jq '.tasks | group_by(.agent) | map({agent: .[0].agent, in_progress: map(select(.status == "in_progress")) | length})' .oodatcaa/work/SPRINT_QUEUE.json
   ```

3. **Check Specific Agent WIP**
   ```bash
   AGENT="builder"
   IN_PROGRESS=$(jq "[.tasks[] | select(.agent == \"$AGENT\" and .status == \"in_progress\")] | length" .oodatcaa/work/SPRINT_QUEUE.json)
   WIP_LIMIT=$(jq ".wip_limits.$AGENT" .oodatcaa/work/SPRINT_QUEUE.json)
   echo "Agent: $AGENT"
   echo "In Progress: $IN_PROGRESS"
   echo "WIP Limit: $WIP_LIMIT"
   echo "Can Claim: $((IN_PROGRESS < WIP_LIMIT))"
   ```

4. **List In-Progress Tasks**
   ```bash
   jq '.tasks[] | select(.status == "in_progress") | {id, title, agent, lease: .lease.acquired}' .oodatcaa/work/SPRINT_QUEUE.json
   ```

#### Expected Output:
```
Agent: builder
In Progress: 1
WIP Limit: 3
Can Claim: 1 (true)

In-Progress Tasks:
- P006-B01 (builder) - acquired 2025-10-04T16:35:31+02:00
```

#### Troubleshooting:
- **Issue:** WIP at limit but no work happening → **Solution:** Check for stale leases, abandoned tasks
- **Issue:** WIP limit too restrictive → **Solution:** Adjust in `SPRINT_QUEUE.json`, restart agents
- **Issue:** Task stuck in `in_progress` → **Solution:** Review agent logs, complete or release task manually

#### See Also:
- [Scenario 8: Claiming a Task](#scenario-8-claiming-a-task)
- [Scenario 10: Managing Task Leases](#scenario-10-managing-task-leases)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#wip-limit-issues)

---

### Scenario 10: Managing Task Leases

**When:** Handling stale leases, releasing abandoned work  
**Goal:** Clean up lease files and unblock tasks

#### Procedure:

1. **List Active Leases**
   ```bash
   ls -lh .leases/
   ```

2. **View Lease Details**
   ```bash
   cat .leases/P006-B01.json | jq
   ```

3. **Check Lease Expiry**
   ```bash
   LEASE_FILE=".leases/P006-B01.json"
   ACQUIRED=$(jq -r '.acquired' $LEASE_FILE)
   TTL=$(jq -r '.ttl' $LEASE_FILE)
   LAST_HB=$(jq -r '.last_heartbeat' $LEASE_FILE)
   
   echo "Acquired: $ACQUIRED"
   echo "TTL: $TTL seconds"
   echo "Last Heartbeat: $LAST_HB"
   ```

4. **Remove Stale Lease**
   ```bash
   # If lease is expired and agent not active
   rm .leases/P006-B01.json
   echo "✅ Lease removed"
   ```

5. **Update Task Status**
   ```bash
   jq '.tasks |= map(if .id == "P006-B01" then .status = "ready" | .lease = null else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

6. **Verify Task Released**
   ```bash
   jq '.tasks[] | select(.id == "P006-B01") | {status, lease}' .oodatcaa/work/SPRINT_QUEUE.json
   ```

#### Expected Output:
```
✅ Lease removed: .leases/P006-B01.json
✅ Task status: in_progress → ready
✅ Task available for claiming
```

#### Troubleshooting:
- **Issue:** Can't determine if lease is stale → **Solution:** Check agent logs, verify agent still running
- **Issue:** Multiple leases for same task → **Solution:** Remove all, reset task to `ready`
- **Issue:** Lease removal doesn't unblock task → **Solution:** Manually update `SPRINT_QUEUE.json` status

#### See Also:
- [Scenario 8: Claiming a Task](#scenario-8-claiming-a-task)
- [Scenario 9: Checking Agent WIP Limits](#scenario-9-checking-agent-wip-limits)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#lease-management-issues)

---

## System Maintenance

### Scenario 11: Checking System Health

**When:** Regular health checks, investigating issues  
**Goal:** Verify all OODATCAA components operational

#### Procedure:

1. **Check Git Status**
   ```bash
   git status
   ```
   
   Verify:
   - On `main` branch (or feature branch if expected)
   - No unexpected uncommitted changes
   - Branch up to date with origin

2. **Verify Critical Files Exist**
   ```bash
   ls -lh .oodatcaa/work/SPRINT_QUEUE.json
   ls -lh .oodatcaa/work/AGENT_LOG.md
   ls -lh .oodatcaa/work/SPRINT_STATUS.json
   ```

3. **Validate JSON Files**
   ```bash
   jq empty .oodatcaa/work/SPRINT_QUEUE.json && echo "✅ SPRINT_QUEUE.json valid"
   jq empty .oodatcaa/work/SPRINT_STATUS.json && echo "✅ SPRINT_STATUS.json valid"
   ```

4. **Check File Permissions**
   ```bash
   ls -ld .oodatcaa/work .leases .locks
   ```
   
   Verify all directories writable.

5. **Check Disk Space**
   ```bash
   df -h .
   du -sh .oodatcaa/work/
   ```

6. **Verify Agent Scripts Executable**
   ```bash
   ls -l scripts/agent-daemon.py scripts/agents-daemon-cli.sh
   ```

#### Expected Output:
```
✅ Git: On branch main, up to date
✅ SPRINT_QUEUE.json: valid JSON (34 tasks)
✅ AGENT_LOG.md: 9021 lines
✅ Disk: 15GB available
✅ Permissions: All writable
✅ Scripts: Executable
```

#### Troubleshooting:
- **Issue:** JSON parse error → **Solution:** Restore from `.oodatcaa/work/*.json.backup`
- **Issue:** Permission denied → **Solution:** `chmod -R u+w .oodatcaa/work/`
- **Issue:** Low disk space → **Solution:** Archive and compress old sprint data
- **Issue:** Git diverged → **Solution:** Review commits, merge or rebase as needed

#### See Also:
- [Scenario 12: Validating Configuration](#scenario-12-validating-configuration)
- [Scenario 15: Archiving Logs](#scenario-15-archiving-logs)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#system-health-diagnostics)

---

### Scenario 12: Validating Configuration

**When:** After setup, before starting agents  
**Goal:** Ensure environment properly configured

#### Procedure:

1. **Run Environment Validation**
   ```bash
   make validate-env
   ```

2. **Check Python Version**
   ```bash
   python3 --version
   ```
   
   Required: Python 3.11+

3. **Verify Dependencies**
   ```bash
   pip list | grep -E "(jq|pytest|black|ruff)"
   ```

4. **Test Quality Gates**
   ```bash
   # Optional if dev dependencies installed
   python3 -m black --version
   python3 -m ruff --version
   python3 -m pytest --version
   ```

5. **Verify Makefile Commands**
   ```bash
   make help
   ```

6. **Test Sprint Dashboard**
   ```bash
   make sprint-dashboard
   ```

#### Expected Output:
```
✅ Python 3.11.5
✅ jq installed
✅ Git repository valid
✅ Configuration files present
✅ All Makefile targets available
✅ Sprint dashboard operational
```

#### Troubleshooting:
- **Issue:** Python version too old → **Solution:** Install Python 3.11+, update PATH
- **Issue:** Missing dependencies → **Solution:** Run `./scripts/setup-dev.sh` or `pip install -e ".[dev]"`
- **Issue:** `jq` not found → **Solution:** Install via package manager (`apt-get install jq`, `brew install jq`)
- **Issue:** Makefile errors → **Solution:** Verify GNU Make installed (`make --version`)

#### See Also:
- [Scenario 11: Checking System Health](#scenario-11-checking-system-health)
- [ONBOARDING.md](ONBOARDING.md#environment-setup)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#configuration-validation)

---

### Scenario 13: Updating Agent Prompts

**When:** Enhancing agent behavior, fixing issues  
**Goal:** Safely update agent protocols

#### Procedure:

1. **Backup Current Prompts**
   ```bash
   cp -r .oodatcaa/prompts/ .oodatcaa/prompts.backup-$(date +%Y%m%d)
   ```

2. **Edit Agent Prompt**
   ```bash
   nano .oodatcaa/prompts/builder.md
   ```

3. **Validate Markdown**
   ```bash
   # Check for broken links (if tool available)
   markdown-link-check .oodatcaa/prompts/builder.md
   ```

4. **Test Updated Prompt**
   ```bash
   # Run agent manually with updated prompt
   # See Scenario 7
   ```

5. **Commit Changes**
   ```bash
   git add .oodatcaa/prompts/builder.md
   git commit -m "[prompts] Update builder protocol: <description>"
   git push origin main
   ```

6. **Restart Agents (if running)**
   ```bash
   make agents-restart
   ```

#### Expected Output:
```
✅ Prompt updated: builder.md
✅ Validation passed
✅ Test run successful
✅ Changes committed
✅ Agents restarted with new protocol
```

#### Troubleshooting:
- **Issue:** Agent doesn't follow new prompt → **Solution:** Verify agents restarted, check cache/context
- **Issue:** Prompt breaks agent behavior → **Solution:** Restore from backup, review changes
- **Issue:** Syntax error in markdown → **Solution:** Use markdown linter, check formatting

#### See Also:
- [Scenario 7: Running Agent Manually](#scenario-7-running-agent-manually)
- [AGENT_INTERACTION_GUIDE.md](AGENT_INTERACTION_GUIDE.md)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#agent-prompt-issues)

---

### Scenario 14: Managing Log Files

**When:** Log files growing large, investigating issues  
**Goal:** View, search, and manage agent logs

#### Procedure:

1. **Check Log Size**
   ```bash
   wc -l .oodatcaa/work/AGENT_LOG.md
   wc -l .oodatcaa/work/SPRINT_LOG.md
   ```

2. **View Recent Logs**
   ```bash
   tail -100 .oodatcaa/work/AGENT_LOG.md
   ```

3. **Search Logs**
   ```bash
   # Find specific task
   grep "P006-B01" .oodatcaa/work/AGENT_LOG.md
   
   # Find errors
   grep -i "error\|failed\|blocked" .oodatcaa/work/AGENT_LOG.md
   
   # Find agent activity
   grep "agent-builder-A" .oodatcaa/work/AGENT_LOG.md | tail -20
   ```

4. **Check Log Rotation Status**
   ```bash
   ls -lh .oodatcaa/work/archive/
   cat ROTATION_STATS.md
   ```

5. **Trigger Manual Log Rotation (if needed)**
   ```bash
   bash scripts/rotate-logs.sh
   ```

#### Expected Output:
```
AGENT_LOG.md: 9021 lines (within threshold)
SPRINT_LOG.md: 1543 lines (OK)

Recent activity:
- 2025-10-04T16:35: Builder started P006-B01
- 2025-10-04T14:10: Integrator completed P001-B03
```

#### Troubleshooting:
- **Issue:** Log file too large to open → **Solution:** Use `less`, `tail`, `head`, or rotate logs
- **Issue:** Rotation fails → **Solution:** Check permissions, verify archive directory exists
- **Issue:** Logs missing entries → **Solution:** Check agent write permissions, verify logging configuration

#### See Also:
- [Scenario 15: Archiving Logs](#scenario-15-archiving-logs)
- [Scenario 4: Viewing Agent Activity](#scenario-4-viewing-agent-activity)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#log-management)

---

### Scenario 15: Archiving Logs

**When:** Log files exceed 1000 lines, sprint completion  
**Goal:** Archive old log data, maintain searchability

#### Procedure:

1. **Check If Rotation Needed**
   ```bash
   wc -l .oodatcaa/work/AGENT_LOG.md
   wc -l .oodatcaa/work/SPRINT_LOG.md
   ```
   
   Threshold: 1000 lines per file

2. **Run Log Rotation**
   ```bash
   bash scripts/rotate-logs.sh
   ```

3. **Verify Archives Created**
   ```bash
   ls -lh .oodatcaa/work/archive/sprint_N/
   ```

4. **Check Archive Index**
   ```bash
   cat ARCHIVE_INDEX.md
   ```

5. **Update Archive Index (if needed)**
   ```bash
   bash scripts/generate-archive-index.sh
   ```

6. **Commit Archives**
   ```bash
   git add .oodatcaa/work/archive/ ARCHIVE_INDEX.md ROTATION_STATS.md
   git commit -m "[logs] Archive sprint N logs (rotation)"
   git push origin main
   ```

#### Expected Output:
```
✅ Archived: AGENT_LOG.md → archive/sprint_2/AGENT_LOG_archive_003.md
✅ Archived: SPRINT_LOG.md → archive/sprint_2/SPRINT_LOG_archive_001.md
✅ 7384 lines archived, 642 lines retained
✅ Archive index updated
📊 Total archives: 8 files, 65,432 lines
```

#### Troubleshooting:
- **Issue:** Rotation script fails → **Solution:** Check permissions, verify `jq` installed
- **Issue:** Archive directory full → **Solution:** Compress old archives (`gzip archive/sprint_1/*.md`)
- **Issue:** Index out of date → **Solution:** Run `generate-archive-index.sh` manually

#### See Also:
- [Scenario 2: Completing a Sprint](#scenario-2-completing-a-sprint)
- [Scenario 14: Managing Log Files](#scenario-14-managing-log-files)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#log-archiving-issues)

---

## Emergency Procedures

### Scenario 16: Recovering from System Failure

**When:** Critical system error, corruption detected  
**Goal:** Restore system to working state

#### Procedure:

1. **Stop All Agents Immediately**
   ```bash
   make agents-stop
   # OR force kill if needed
   pkill -f agent-daemon
   ```

2. **Backup Current State**
   ```bash
   cp .oodatcaa/work/SPRINT_QUEUE.json .oodatcaa/work/SPRINT_QUEUE.json.emergency-$(date +%Y%m%d-%H%M%S)
   cp .oodatcaa/work/AGENT_LOG.md .oodatcaa/work/AGENT_LOG.md.emergency-$(date +%Y%m%d-%H%M%S)
   ```

3. **Identify Issue**
   ```bash
   # Check for JSON corruption
   jq empty .oodatcaa/work/SPRINT_QUEUE.json
   
   # Check git status
   git status
   
   # Review recent logs
   tail -200 .oodatcaa/work/AGENT_LOG.md
   ```

4. **Restore from Backup**
   ```bash
   # If SPRINT_QUEUE.json corrupted
   cp .oodatcaa/work/SPRINT_QUEUE.json.backup .oodatcaa/work/SPRINT_QUEUE.json
   
   # OR restore from git
   git checkout HEAD -- .oodatcaa/work/SPRINT_QUEUE.json
   ```

5. **Clean Up**
   ```bash
   # Remove stale leases
   rm .leases/*.json
   
   # Remove stale locks
   rm .locks/*.lock
   ```

6. **Verify System Health**
   ```bash
   # See Scenario 11
   make sprint-dashboard
   jq empty .oodatcaa/work/SPRINT_QUEUE.json
   ```

7. **Restart Operations**
   ```bash
   # Restart agents or proceed manually
   make agents-start
   ```

#### Expected Output:
```
✅ Agents stopped
✅ State backed up
✅ Issue identified: JSON corruption
✅ Restored from backup
✅ Leases cleared
✅ System health verified
✅ Operations resumed
```

#### Troubleshooting:
- **Issue:** Backup also corrupted → **Solution:** Restore from git history (`git log --all -- SPRINT_QUEUE.json`)
- **Issue:** Can't identify issue → **Solution:** Check system logs, review agent reports
- **Issue:** Data loss → **Solution:** Reconstruct state from agent reports and commit history

#### See Also:
- [Scenario 11: Checking System Health](#scenario-11-checking-system-health)
- [Scenario 17: Rolling Back Changes](#scenario-17-rolling-back-changes)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#system-recovery)

---

### Scenario 17: Rolling Back Changes

**When:** Bad commit deployed, agent behavior broken  
**Goal:** Safely revert to previous working state

#### Procedure:

1. **Identify Problem Commit**
   ```bash
   git log --oneline -10
   git show <commit-hash>
   ```

2. **Stop Agents**
   ```bash
   make agents-stop
   ```

3. **Create Rollback Branch**
   ```bash
   git checkout -b rollback-<issue>-$(date +%Y%m%d)
   ```

4. **Revert Commit**
   ```bash
   # Revert specific commit (creates new revert commit)
   git revert <commit-hash>
   
   # OR reset to previous commit (destructive)
   git reset --hard <good-commit-hash>
   ```

5. **Test Rollback**
   ```bash
   # Verify system health
   make sprint-dashboard
   jq empty .oodatcaa/work/SPRINT_QUEUE.json
   
   # Test agent manually
   # See Scenario 7
   ```

6. **Deploy Rollback**
   ```bash
   # If using revert (safe)
   git push origin main
   
   # If using reset (force push - CAUTION)
   git push --force-with-lease origin main
   ```

7. **Restart Agents**
   ```bash
   make agents-start
   ```

#### Expected Output:
```
✅ Problem commit identified: abc1234
✅ Agents stopped
✅ Rollback branch created
✅ Changes reverted
✅ System tested OK
✅ Rollback deployed
✅ Agents restarted
```

#### Troubleshooting:
- **Issue:** Force push rejected → **Solution:** Ensure no one else pushing, coordinate team
- **Issue:** Revert creates conflicts → **Solution:** Manually resolve, test thoroughly
- **Issue:** System still broken → **Solution:** Roll back further, check for cascading issues

#### See Also:
- [Scenario 16: Recovering from System Failure](#scenario-16-recovering-from-system-failure)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#rollback-procedures)
- [BRANCH_PROTECTION.md](../docs/BRANCH_PROTECTION.md)

---

### Scenario 18: Handling Stuck Tasks

**When:** Task stuck in progress, no agent activity  
**Goal:** Unblock task and resume workflow

#### Procedure:

1. **Identify Stuck Task**
   ```bash
   jq '.tasks[] | select(.status == "in_progress") | {id, title, lease}' .oodatcaa/work/SPRINT_QUEUE.json
   ```

2. **Check Agent Logs**
   ```bash
   grep "<task-id>" .oodatcaa/work/AGENT_LOG.md | tail -50
   ```

3. **Check for Active Lease**
   ```bash
   cat .leases/<task-id>.json
   ```

4. **Determine Action**
   - If agent crashed: Release lease, reset task
   - If agent still working: Wait or check progress on branch
   - If abandoned: Release lease, may need refiner

5. **Release Task**
   ```bash
   # Remove lease
   rm .leases/<task-id>.json
   
   # Reset task status
   jq '.tasks |= map(if .id == "<task-id>" then .status = "ready" | .lease = null else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

6. **Check Branch State (if work started)**
   ```bash
   git branch -a | grep <task-id>
   git log feat/<task-id>... --oneline
   ```

7. **Decide Next Steps**
   - Work complete: Update status to `awaiting_test`
   - Work partial: May need refiner or new builder
   - Work abandoned: Delete branch, start fresh

#### Expected Output:
```
✅ Stuck task identified: P006-B01
✅ Lease expired (no heartbeat for 3 hours)
✅ Lease released
✅ Task reset to ready
✅ Available for re-claiming
```

#### Troubleshooting:
- **Issue:** Can't determine if work complete → **Solution:** Review branch commits, check deliverables
- **Issue:** Work partially done → **Solution:** Call refiner to assess, adapt or restart
- **Issue:** Recurring stalls → **Solution:** Investigate agent logs, may indicate deeper issue

#### See Also:
- [Scenario 10: Managing Task Leases](#scenario-10-managing-task-leases)
- [Scenario 19: Debugging Agent Failures](#scenario-19-debugging-agent-failures)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#stuck-task-resolution)

---

### Scenario 19: Debugging Agent Failures

**When:** Agent errors, unexpected behavior  
**Goal:** Diagnose and resolve agent issues

#### Procedure:

1. **Check Agent Logs**
   ```bash
   # Daemon logs
   tail -100 .agent-daemon-logs/<role>.log
   
   # System logs (if systemd)
   journalctl --user -u agent-<role> -n 100
   
   # Agent execution logs
   grep "<agent-name>" .oodatcaa/work/AGENT_LOG.md | tail -50
   ```

2. **Review Error Messages**
   ```bash
   grep -i "error\|exception\|failed" .agent-daemon-logs/<role>.log
   ```

3. **Check Agent Reports**
   ```bash
   find .oodatcaa/work/reports/ -name "<agent>*" -mtime -1
   cat .oodatcaa/work/reports/<story>/<agent>_<task>.md
   ```

4. **Verify Dependencies**
   ```bash
   # Python modules
   python3 -c "import json, fcntl, logging" && echo "✅ Imports OK"
   
   # System tools
   which jq git && echo "✅ Tools available"
   ```

5. **Test Agent Manually**
   ```bash
   # See Scenario 7
   # Run agent with minimal test case
   ```

6. **Check for Common Issues**
   ```bash
   # JSON corruption
   jq empty .oodatcaa/work/SPRINT_QUEUE.json
   
   # Permission issues
   ls -ld .oodatcaa/work .leases .locks
   
   # Disk space
   df -h .
   ```

7. **Document Findings**
   ```bash
   # Add to troubleshooting log
   echo "$(date): Agent <role> failure - <issue> - <solution>" >> .oodatcaa/work/TROUBLESHOOTING_LOG.md
   ```

#### Expected Output:
```
✅ Logs reviewed
✅ Error identified: ImportError - missing module
✅ Solution: pip install <module>
✅ Agent test successful
✅ Issue documented
```

#### Troubleshooting:
- **Issue:** No error messages in logs → **Solution:** Increase log verbosity, check for silent failures
- **Issue:** Intermittent failures → **Solution:** Review timing, check for race conditions
- **Issue:** Multiple agents failing → **Solution:** System-wide issue, check infrastructure (disk, memory, network)

#### See Also:
- [Scenario 7: Running Agent Manually](#scenario-7-running-agent-manually)
- [Scenario 11: Checking System Health](#scenario-11-checking-system-health)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

### Scenario 20: Emergency Stop All Operations

**When:** Critical issue detected, need immediate halt  
**Goal:** Stop all agent activity immediately

#### Procedure:

1. **Stop All Background Agents**
   ```bash
   make agents-stop
   ```

2. **Force Kill if Needed**
   ```bash
   pkill -9 -f agent-daemon
   pkill -9 -f agents-daemon-cli
   ```

3. **Verify All Stopped**
   ```bash
   ps aux | grep agent-daemon
   make agents-status
   ```

4. **Pause Active Work**
   ```bash
   # Mark all in-progress as blocked
   jq '.tasks |= map(if .status == "in_progress" then .status = "blocked" | .blocked_reason = "Emergency stop - $(date)" else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

5. **Clear All Leases**
   ```bash
   rm .leases/*.json 2>/dev/null || true
   echo "✅ All leases cleared"
   ```

6. **Document Emergency**
   ```bash
   echo "=== EMERGENCY STOP ===" >> .oodatcaa/work/AGENT_LOG.md
   echo "Time: $(date)" >> .oodatcaa/work/AGENT_LOG.md
   echo "Reason: <reason>" >> .oodatcaa/work/AGENT_LOG.md
   echo "Action: All agents stopped, all leases cleared" >> .oodatcaa/work/AGENT_LOG.md
   ```

7. **Commit State**
   ```bash
   git add .oodatcaa/work/SPRINT_QUEUE.json .oodatcaa/work/AGENT_LOG.md
   git commit -m "[emergency] Emergency stop - <reason>"
   git push origin main
   ```

#### Expected Output:
```
🚨 EMERGENCY STOP INITIATED
✅ All agents stopped
✅ All processes killed
✅ 3 tasks marked as blocked
✅ 3 leases cleared
✅ State committed
🔒 System locked - manual recovery required
```

#### Troubleshooting:
- **Issue:** Agents won't stop → **Solution:** Use `kill -9`, check for zombie processes
- **Issue:** Can't commit state → **Solution:** Save backup copies, resolve git conflicts
- **Issue:** Unclear what went wrong → **Solution:** Review all logs, may need forensic analysis

#### See Also:
- [Scenario 16: Recovering from System Failure](#scenario-16-recovering-from-system-failure)
- [Scenario 6: Stopping Background Agents](#scenario-6-stopping-background-agents)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md#emergency-procedures)

---

## Quick Reference

### Common Commands

| Task | Command |
|------|---------|
| **Sprint Status** | `make sprint-dashboard` |
| **Start Agents** | `make agents-start` |
| **Stop Agents** | `make agents-stop` |
| **Agent Status** | `make agents-status` |
| **View Logs** | `tail -50 .oodatcaa/work/AGENT_LOG.md` |
| **Check Tasks** | `jq '.tasks[] | select(.status == "ready")' .oodatcaa/work/SPRINT_QUEUE.json` |
| **List Leases** | `ls -lh .leases/` |
| **Validate ENV** | `make validate-env` |
| **Archive Logs** | `bash scripts/rotate-logs.sh` |
| **Complete Sprint** | `make sprint-complete` |

### Key File Locations

| File | Purpose |
|------|---------|
| `.oodatcaa/work/SPRINT_QUEUE.json` | Task queue and status |
| `.oodatcaa/work/AGENT_LOG.md` | Detailed agent activity |
| `.oodatcaa/work/SPRINT_LOG.md` | Sprint-level events |
| `.oodatcaa/work/AGENT_REPORTS.md` | Executive summaries |
| `.leases/*.json` | Active task leases |
| `.locks/*.lock` | File locks |
| `.oodatcaa/prompts/*.md` | Agent protocols |
| `.oodatcaa/objectives/SPRINT_GOAL.md` | Current sprint objective |

### Status Values

| Status | Meaning |
|--------|---------|
| `ready` | Task ready to start |
| `in_progress` | Agent working on task |
| `awaiting_test` | Builder done, needs testing |
| `needs_adapt` | Test found issues |
| `ready_for_integrator` | Tests passed |
| `done` | Integrated to main |
| `blocked` | Waiting on dependencies |
| `cancelled` | Not needed |

### Agent Roles

| Agent | Responsibility |
|-------|----------------|
| **Planner** | Create implementation plans |
| **Builder** | Write code/docs |
| **Tester** | Validate acceptance criteria |
| **Refiner** | Fix issues, adapt work |
| **Integrator** | Merge to main, archive |
| **Sprint Planner** | Plan sprints |
| **Negotiator** | Coordinate agents |
| **Project Detector** | Identify completion |
| **Sprint Close** | End sprints |
| **Release** | Create releases |
| **Triage** | Prioritize work |

---

## Additional Resources

- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Diagnostic procedures and solutions
- **[ONBOARDING.md](ONBOARDING.md)** - New user quick start guide
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design
- **[AGENT_INTERACTION_GUIDE.md](AGENT_INTERACTION_GUIDE.md)** - Agent coordination patterns
- **[AGENT_ROLES_MATRIX.md](AGENT_ROLES_MATRIX.md)** - Complete agent capability matrix
- **[BACKGROUND_AGENTS.md](../docs/BACKGROUND_AGENTS.md)** - Daemon system documentation

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-04  
**Maintained By:** OODATCAA System Team

For questions or issues, refer to [CONTRIBUTING.md](../docs/CONTRIBUTING.md) or open an issue.

