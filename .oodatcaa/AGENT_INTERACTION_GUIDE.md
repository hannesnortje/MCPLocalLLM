# Agent Interaction Guide — OODATCAA Multi-Agent System

**Version:** 1.0  
**Last Updated:** 2025-10-04  
**Status:** Active

---

## Overview

This guide documents interaction patterns, communication mechanisms, and coordination protocols for the 11-agent OODATCAA development system. It provides workflow examples, handoff procedures, and real-world evidence from Sprint 1 (34 tasks, 91.9% success) and Sprint 2 (30 tasks planned, 5 completed).

**Purpose:** Enable autonomous multi-agent coordination with minimal human intervention through clear protocols and proven patterns.

---

## Table of Contents

1. [Communication Mechanisms](#communication-mechanisms)
2. [Workflow Patterns](#workflow-patterns)
3. [Handoff Procedures](#handoff-procedures)
4. [Real-World Examples](#real-world-examples)
5. [Failure Patterns & Recovery](#failure-patterns--recovery)
6. [Best Practices](#best-practices)

---

## Communication Mechanisms

### 1. File-Based Messaging

The system uses file-based communication for persistence, auditability, and simplicity. All agents read and write to shared files in `.oodatcaa/work/` and `.oodatcaa/objectives/`.

#### Primary Communication Files

**`.oodatcaa/work/SPRINT_QUEUE.json`** - Central Task Coordination
- **Purpose:** Single source of truth for all task statuses, assignments, and dependencies
- **Writers:** Planner (create tasks), Builder/Tester/Refiner/Integrator (update status), Negotiator (status transitions)
- **Readers:** All agents (to discover work)
- **Update Frequency:** On every status transition (ready → in_progress → awaiting_test → ready_for_integrator → done)
- **Atomic Updates:** Always use temp file + atomic rename pattern to prevent corruption
  ```bash
  jq '.tasks |= map(...)' SPRINT_QUEUE.json > /tmp/queue_tmp.json
  mv /tmp/queue_tmp.json SPRINT_QUEUE.json
  ```

**`.oodatcaa/work/AGENT_LOG.md`** - Chronological Activity Log
- **Purpose:** Append-only log of all agent actions, decisions, and state changes
- **Writers:** All agents (append only, never modify)
- **Readers:** Negotiator (monitor progress), Refiner (analyze failures), Sprint Close (summarize)
- **Update Frequency:** At least once per agent invocation (start, complete, errors)
- **Lock Mechanism:** Brief lock during append (< 1 second)
- **Format:** Markdown sections with timestamp, agent, task, action, outcome

**`.oodatcaa/work/SPRINT_LOG.md`** - Sprint-Level Events
- **Purpose:** High-level sprint milestones, shipped features, exit criteria progress
- **Writers:** Negotiator (heartbeats, sprint completion), Integrator (shipped entries), Sprint Close (summaries)
- **Readers:** Sprint Planner (assess completion), Negotiator (monitor sprint health)
- **Update Frequency:** Heartbeats (~15min), after each integration, at sprint completion
- **Format:** Markdown with dated sections

**`.oodatcaa/work/AGENT_PLAN.md`** - Detailed Implementation Plan
- **Purpose:** Step-by-step implementation guide for Builder
- **Writers:** Planner (create), Refiner (revise if rollback)
- **Readers:** Builder (implementation), Tester (context), Refiner (analyze failures)
- **Locking:** `.locks/AGENT_PLAN.md.lock` (5-minute TTL, breakable with log note)
- **Versioning:** Version number incremented on Refiner revisions

**`.oodatcaa/work/TEST_PLAN.md`** - Quality Gates & Acceptance Criteria
- **Purpose:** Test commands, acceptance criteria, performance thresholds for Tester
- **Writers:** Planner (create), Builder (add tests), Tester (add regression tests)
- **Readers:** Builder (test requirements), Tester (validation procedures)
- **Locking:** `.locks/TEST_PLAN.md.lock` (5-minute TTL)
- **Format:** Markdown with bash commands, AC IDs, expected results

**`.oodatcaa/work/SPRINT_PLAN.md`** - Agent Assignments
- **Purpose:** Current WIP snapshot, agent-to-task mappings
- **Writers:** Negotiator (assignments), Planner (reflect planning)
- **Readers:** Negotiator (WIP enforcement), humans (dashboard view)
- **Update Frequency:** On every assignment change
- **Format:** Markdown table (Agent → Task → Status)

---

### 2. Lease Protocol (Ownership & Heartbeats)

Leases prevent multiple agents from working on the same task simultaneously. They use TTL-based ownership with heartbeat mechanism.

#### Lease File Structure

**Location:** `.leases/<task_id>.json`

**Format:**
```json
{
  "task_id": "P005-B01",
  "agent": "builder",
  "owner": "agent-builder-cursor",
  "acquired": "2025-10-04T08:16:31+02:00",
  "ttl": 5400,
  "last_heartbeat": "2025-10-04T08:16:31+02:00"
}
```

**Fields:**
- `task_id`: Unique task identifier (matches SPRINT_QUEUE.json)
- `agent`: Agent role (builder, tester, planner, etc.)
- `owner`: Specific agent instance (for parallel agents of same type)
- `acquired`: ISO8601 timestamp when lease created
- `ttl`: Time-to-live in seconds (varies by agent type)
- `last_heartbeat`: ISO8601 timestamp of last heartbeat update

#### Lease TTLs by Agent Type

| Agent | TTL (seconds) | TTL (minutes) | Rationale |
|-------|--------------|--------------|-----------|
| Builder | 5400 | 90 | Long implementation time (coding, testing, debugging) |
| Planner | 1800 | 30 | Moderate planning time (analysis, alternatives, design) |
| Tester | 2700 | 45 | Testing can be lengthy (acceptance tests, perf benchmarks) |
| Refiner | 2700 | 45 | Analysis and decision-making (quick fix vs rollback) |
| Integrator | 1800 | 30 | Integration typically fast (PR, merge, tag, docs) |

#### Lease Lifecycle

**1. Acquisition:**
```bash
# Check if lease exists and is still valid
if [[ -f .leases/P005-B01.json ]]; then
  ACQUIRED=$(jq -r '.acquired' .leases/P005-B01.json)
  TTL=$(jq -r '.ttl' .leases/P005-B01.json)
  HEARTBEAT=$(jq -r '.last_heartbeat' .leases/P005-B01.json)
  # Calculate if stale: heartbeat + TTL < now
  if (( $(date -d "$HEARTBEAT" +%s) + TTL < $(date +%s) )); then
    echo "Stale lease detected, taking over"
    # Log takeover in AGENT_LOG.md
    # Delete stale lease
    rm .leases/P005-B01.json
  else
    echo "Task has active lease, cannot proceed"
    exit 1
  fi
fi

# Create new lease
cat > .leases/P005-B01.json <<EOF
{
  "task_id": "P005-B01",
  "agent": "builder",
  "owner": "agent-builder-cursor",
  "acquired": "$(date -Iseconds)",
  "ttl": 5400,
  "last_heartbeat": "$(date -Iseconds)"
}
EOF
```

**2. Heartbeat (every ~10 minutes):**
```bash
# Update last_heartbeat timestamp
jq '.last_heartbeat = "'$(date -Iseconds)'"' .leases/P005-B01.json > /tmp/lease_tmp.json
mv /tmp/lease_tmp.json .leases/P005-B01.json
```

**3. Release (on completion or error):**
```bash
# Always release lease when done
rm .leases/P005-B01.json

# Update SPRINT_QUEUE.json to clear lease reference
jq '.tasks |= map(if .id == "P005-B01" then .lease = null else . end)' SPRINT_QUEUE.json > /tmp/queue_tmp.json
mv /tmp/queue_tmp.json SPRINT_QUEUE.json
```

#### Stale Lease Detection (Negotiator)

Negotiator scans `.leases/` directory every coordination loop:
```bash
for lease_file in .leases/*.json; do
  TASK_ID=$(jq -r '.task_id' "$lease_file")
  HEARTBEAT=$(jq -r '.last_heartbeat' "$lease_file")
  TTL=$(jq -r '.ttl' "$lease_file")
  OWNER=$(jq -r '.owner' "$lease_file")
  
  # Check if stale: heartbeat + TTL < now
  EXPIRY=$(( $(date -d "$HEARTBEAT" +%s) + TTL ))
  NOW=$(date +%s)
  
  if (( EXPIRY < NOW )); then
    echo "Stale lease detected: $TASK_ID owned by $OWNER"
    # Log takeover in AGENT_LOG.md
    echo "$(date -Iseconds) - Negotiator: Stale lease takeover for $TASK_ID (owner: $OWNER, expired $((NOW - EXPIRY))s ago)" >> .oodatcaa/work/AGENT_LOG.md
    
    # Delete stale lease
    rm "$lease_file"
    
    # Reset task status appropriately
    jq '.tasks |= map(if .id == "'$TASK_ID'" then .status = "ready" | .lease = null | .agent = null else . end)' SPRINT_QUEUE.json > /tmp/queue_tmp.json
    mv /tmp/queue_tmp.json SPRINT_QUEUE.json
  fi
done
```

---

### 3. Lock Protocol (File Modification Safety)

Locks prevent concurrent modification of shared planning files. They use TTL-based locking with breakable locks after 5 minutes.

#### Lock File Structure

**Location:** `.locks/<filename>.lock`

**Format:**
```json
{
  "file": "AGENT_PLAN.md",
  "agent": "planner",
  "owner": "agent-planner-A",
  "acquired": "2025-10-04T08:00:00+02:00",
  "ttl": 300
}
```

**TTL:** 5 minutes (300 seconds) for all locks

#### Lockable Files

- `.locks/AGENT_PLAN.md.lock` - Prevents concurrent plan modifications (Planner, Refiner)
- `.locks/TEST_PLAN.md.lock` - Prevents concurrent test plan modifications (Planner, Tester, Builder)
- `.locks/AGENT_LOG.md.lock` - Brief lock during append (~1 second, all agents)

#### Lock Lifecycle

**1. Acquisition:**
```bash
LOCK_FILE=".locks/AGENT_PLAN.md.lock"

# Check if lock exists
if [[ -f "$LOCK_FILE" ]]; then
  ACQUIRED=$(jq -r '.acquired' "$LOCK_FILE")
  AGE=$(( $(date +%s) - $(date -d "$ACQUIRED" +%s) ))
  
  if (( AGE > 300 )); then
    # Lock > 5 minutes old, break it with log note
    OWNER=$(jq -r '.owner' "$LOCK_FILE")
    echo "$(date -Iseconds) - Breaking stale lock: AGENT_PLAN.md.lock (owner: $OWNER, age: ${AGE}s)" >> .oodatcaa/work/AGENT_LOG.md
    rm "$LOCK_FILE"
  else
    echo "AGENT_PLAN.md is locked by another agent, waiting..."
    exit 1
  fi
fi

# Create lock
cat > "$LOCK_FILE" <<EOF
{
  "file": "AGENT_PLAN.md",
  "agent": "planner",
  "owner": "agent-planner-A",
  "acquired": "$(date -Iseconds)",
  "ttl": 300
}
EOF
```

**2. Usage:**
- Modify file while lock held
- Keep lock duration minimal (< 5 minutes)
- No heartbeat for locks (use leases for long-running work)

**3. Release:**
```bash
# Always release lock when done
rm .locks/AGENT_PLAN.md.lock
```

---

### 4. Status Transitions (Task Lifecycle)

Task status field in SPRINT_QUEUE.json follows strict state machine:

```
needs_plan → planning → planning_complete →
ready → in_progress → awaiting_test →
[PASS] → ready_for_integrator → done
[FAIL] → needs_adapt → ready (after Refiner fix)
[FAIL 2x] → Start-Over gate (Refiner rollback)
```

**Status Definitions:**

| Status | Meaning | Owned By | Next Agent |
|--------|---------|----------|------------|
| `needs_plan` | Backlog item without detailed plan | None | Planner |
| `planning` | Currently being planned | Planner | Planner (same) |
| `planning_complete` | Plan finished, waiting for review | Planner | Negotiator (mark ready) |
| `ready` | Ready to be picked up | None | Builder/Tester/Refiner (depends on type) |
| `in_progress` | Currently being worked on | Builder/Tester/Refiner/Integrator | Same agent (complete) |
| `awaiting_test` | Implementation complete, needs validation | Builder | Tester |
| `needs_adapt` | Failed validation, needs fix or rollback | Tester | Refiner |
| `ready_for_integrator` | Validated, ready to merge | Tester | Integrator |
| `done` | Merged and shipped | Integrator | None (complete) |
| `blocked` | Waiting on dependencies | None | Negotiator (unblock when deps met) |
| `cancelled` | Deferred or no longer needed | Negotiator/Human | None |

**Status Transition Rules:**

1. **Only assigned agent can change status** (except Negotiator for unblocking)
2. **Status changes must be logged** in AGENT_LOG.md
3. **Lease must be acquired before status change** to in_progress
4. **Lease must be released after status change** from in_progress
5. **Backward transitions allowed only via Refiner** (needs_adapt → ready)

---

## Workflow Patterns

### Pattern 1: Primary Development Flow

**Purpose:** Standard happy-path workflow for implementing a planned feature.

**Participants:** Sprint Planner → Planner → Builder → Tester → Integrator

**Workflow:**

```
┌─────────────────┐
│ Sprint Planner  │  1. Generate sprint goal + backlog
│  (Start Sprint) │     Output: SPRINT_GOAL.md, SPRINT_BACKLOG.md
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Planner      │  2. Create detailed plan for work item
│  (needs_plan)   │     Input: SPRINT_BACKLOG.md item
└────────┬────────┘     Output: AGENT_PLAN.md, TEST_PLAN.md, SPRINT_QUEUE.json (tasks enqueued)
         │
         ▼
┌─────────────────┐
│    Builder      │  3. Implement plan step on feature branch
│    (ready)      │     Input: AGENT_PLAN.md (steps), TEST_PLAN.md (tests)
└────────┬────────┘     Output: Code, tests, branch
         │              Status: ready → in_progress → awaiting_test
         ▼
┌─────────────────┐
│    Tester       │  4. Validate acceptance criteria
│ (awaiting_test) │     Input: Feature branch, TEST_PLAN.md (ACs)
└────────┬────────┘     Output: Test results, validation report
         │              Status: awaiting_test → ready_for_integrator (if pass)
         ▼                                    → needs_adapt (if fail)
┌─────────────────┐
│  Integrator     │  5. Merge, tag, document
│(ready_for_int.) │     Input: Validated branch
└────────┬────────┘     Output: Merged code, PR, tag, CHANGELOG
         │              Status: ready_for_integrator → done
         ▼
      [DONE]
```

**Communication Flow:**

1. **Sprint Planner → Planner:**
   - File: SPRINT_BACKLOG.md (Sprint Planner writes, Planner reads)
   - Message: "Work item X needs detailed plan"

2. **Planner → Builder:**
   - File: AGENT_PLAN.md (Planner writes, Builder reads)
   - File: SPRINT_QUEUE.json (Planner creates task with status="ready", Builder picks up)
   - Message: "Step 1 ready for implementation, branch: feat/X-step-01"

3. **Builder → Tester:**
   - File: SPRINT_QUEUE.json (Builder updates status to "awaiting_test")
   - File: Feature branch (Builder pushes, Tester checks out)
   - File: AGENT_LOG.md (Builder logs completion, Tester reads context)
   - Message: "Step 1 implemented, passed gates, awaiting validation"

4. **Tester → Integrator:**
   - File: SPRINT_QUEUE.json (Tester updates status to "ready_for_integrator")
   - File: AGENT_LOG.md (Tester logs PASS per AC)
   - Message: "All ACs met, ready for merge"

5. **Integrator → Done:**
   - File: SPRINT_QUEUE.json (Integrator updates status to "done")
   - File: SPRINT_LOG.md (Integrator logs shipped entry)
   - Message: "Feature X shipped in PR #123, tagged as pre/X-2025-10-04"

**Real-World Example: P002-B01 (Log Rotation System)**

**Context:** Sprint 2, Task P002-B01, "Perfect implementation" (100% first-attempt success)

1. **Planner (agent-planner-A):**
   - Read P002 from SPRINT_BACKLOG.md (needs_plan status)
   - Created AGENT_PLAN.md with 9 steps
   - Created TEST_PLAN.md with 10 ACs
   - Enqueued P002-B01 (status: ready), P002-B02 (blocked)
   - Time: 45 minutes

2. **Builder (agent-builder-A):**
   - Picked P002-B01 (first ready builder task)
   - Acquired lease (.leases/P002-B01.json, TTL: 5400s)
   - Read AGENT_PLAN.md steps 1-3
   - Implemented on branch feat/P002-step-01-rotation-script
   - Created scripts/rotate-logs.sh (201 lines)
   - All gates passed (black, ruff, mypy, pytest, build)
   - Status: ready → in_progress → awaiting_test
   - Time: 60 minutes

3. **Tester (agent-tester-A):**
   - Picked P002-B01 (first awaiting_test task)
   - Acquired lease (.leases/P002-B01.json, TTL: 2700s)
   - Ran TEST_PLAN.md commands
   - Validated all 10 ACs: PASS
   - Added 0 regression tests (none needed)
   - Status: awaiting_test → ready_for_integrator
   - Time: 15 minutes

4. **Integrator (agent-integrator-A):**
   - Picked P002-B01 (first ready_for_integrator task)
   - Acquired lease (.leases/P002-B01.json, TTL: 1800s)
   - Opened PR #45 with DoD checklist
   - Merged to main (squash)
   - Created baseline tag: pre/P002-B01-2025-10-03
   - Updated CHANGELOG.md
   - Status: ready_for_integrator → done
   - Time: 10 minutes

**Total Time:** 130 minutes (within 150min estimate)  
**Outcome:** 100% success, 0 adaptations, shipped in Sprint 2

---

### Pattern 2: Adaptation Loop (Failure Recovery)

**Purpose:** Handle failed validations through quick fixes or rollbacks.

**Participants:** Tester → Refiner → Builder → Tester

**Workflow:**

```
┌─────────────────┐
│    Tester       │  1. Validation fails (ACs not met)
│(awaiting_test)  │     Output: Failure report, test logs
└────────┬────────┘     Status: awaiting_test → needs_adapt
         │
         ▼
┌─────────────────┐
│    Refiner      │  2. Analyze failure, decide approach
│  (needs_adapt)  │     Input: AGENT_LOG.md (failure context), AGENT_PLAN.md (original plan)
└────────┬────────┘     Output: Decision (quick fix OR rollback)
         │
         ▼
    [DECISION]
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────┐   ┌─────────┐
│Quick│   │Rollback │
│ Fix │   │(Baseline│
└──┬──┘   │  Tag)   │
   │      └────┬────┘
   │           │
   │           ▼
   │      ┌─────────────────┐
   │      │Update AGENT_PLAN│  3a. Rollback path
   │      │(version bump,   │      - Reset git to baseline tag
   │      │ revised steps,  │      - Revise AGENT_PLAN.md (v+1)
   │      │ Post-Mortem)    │      - Adjust steps/ACs
   │      └────┬────────────┘      - Write Post-Mortem
   │           │                   Status: needs_adapt → ready
   │           │
   └───────────┴───────────┐
                           │
                           ▼
                    ┌─────────────────┐
                    │    Builder      │  3b. Quick fix path
                    │    (ready)      │      - Apply minimal patch
                    └────────┬────────┘      - Re-run gates
                             │              Status: ready → in_progress
                             ▼                            → awaiting_test
                    ┌─────────────────┐
                    │    Tester       │  4. Re-validate
                    │ (awaiting_test) │     - Re-run ACs
                    └────────┬────────┘     Status: awaiting_test → ready_for_integrator (if pass)
                             │                                     → needs_adapt (if fail again)
                             ▼
                       [PASS or FAIL]
                             │
                   ┌─────────┴─────────┐
                   │                   │
                   ▼                   ▼
            [Continue Dev.]    [Start-Over Gate]
                              (if 2 Adapt loops fail)
```

**Decision Matrix (Refiner):**

| Failure Type | Symptom | Decision | Rationale |
|-------------|---------|----------|-----------|
| **Lint/Format** | black/ruff errors | Quick fix | Simple syntax corrections |
| **Type Errors** | mypy errors | Quick fix (if < 5 errors) | Type annotation additions |
| **Test Failures** | pytest failures | Quick fix (if < 3 tests) | Logic bugs, edge cases |
| **AC Not Met** | Missing functionality | Quick fix (if < 20% of ACs) | Incomplete implementation |
| **Coverage Gap** | < 85% coverage | Quick fix | Add missing tests |
| **Fundamental Design Flaw** | Architecture mismatch | Rollback | Wrong approach, need replan |
| **Cascading Failures** | Multiple unrelated issues | Rollback | Too many problems, start fresh |
| **2nd Adaptation Fails** | Quick fix didn't work | Start-Over gate | Trigger rollback protocol |

**Communication Flow:**

1. **Tester → Refiner:**
   - File: SPRINT_QUEUE.json (Tester sets status to "needs_adapt")
   - File: AGENT_LOG.md (Tester logs detailed failure: which ACs failed, test output, suggestions)
   - File: Tester completion report (`.oodatcaa/work/reports/<TASK_ID>/tester_<subtask>.md`)
   - Message: "Validation failed: AC3, AC7 not met (details in log)"

2. **Refiner → Builder (Quick Fix Path):**
   - File: SPRINT_QUEUE.json (Refiner sets status back to "ready")
   - File: AGENT_LOG.md (Refiner logs decision: "Quick fix recommended: add coverage for edge case X")
   - File: Refiner completion report (specific patch instructions)
   - Message: "Quick fix: add test for edge case, re-run coverage"

3. **Refiner → Builder (Rollback Path):**
   - File: AGENT_PLAN.md (Refiner bumps version to v2, revises steps, adds Post-Mortem)
   - File: SPRINT_QUEUE.json (Refiner sets status to "ready", notes rollback)
   - File: AGENT_LOG.md (Refiner logs rollback decision with rationale)
   - Git: Refiner references baseline tag (pre/X-2025-10-04) for reset
   - Message: "Rollback to baseline tag, revised plan (v2), see Post-Mortem"

4. **Builder → Tester (Re-implementation):**
   - Same as primary flow (Builder re-implements, updates status to "awaiting_test")

**Real-World Example: W004 Adaptation (Sprint 1)**

**Context:** Sprint 1, Task W004 (Query Optimization), adaptation required due to performance issue

1. **Tester (agent-tester-A):**
   - Validated W004-B01 implementation
   - AC5 failed: Performance threshold not met (p95: 180ms, threshold: 150ms)
   - Logged failure in AGENT_LOG.md: "AC5 FAIL: p95 latency 180ms (target: 150ms)"
   - Status: awaiting_test → needs_adapt
   - Time: 20 minutes

2. **Refiner (agent-refiner-A):**
   - Picked W004-B01 (needs_adapt)
   - Analyzed AGENT_LOG.md: performance issue, no fundamental design flaw
   - Decision: **Quick fix** (optimize query caching)
   - Logged: "Quick fix recommended: add query result caching to reduce latency"
   - Status: needs_adapt → ready
   - Time: 15 minutes

3. **Builder (agent-builder-A):**
   - Picked W004-B01 (ready, second attempt)
   - Applied quick fix: added LRU cache for query results
   - Re-ran gates: all passed
   - Status: ready → in_progress → awaiting_test
   - Time: 30 minutes

4. **Tester (agent-tester-A):**
   - Re-validated W004-B01
   - AC5 now passed: p95 latency 120ms (under 150ms threshold)
   - All ACs met
   - Status: awaiting_test → ready_for_integrator
   - Time: 15 minutes

**Adaptation Time:** 60 minutes  
**Outcome:** Quick fix successful, no rollback needed, shipped in Sprint 1

**Sprint 1 Adaptation Summary:**
- **Total Adaptations:** 4 (W004, W005, W006-B01, W007-B01, W008-B01)
- **Quick Fixes:** 4 (100%)
- **Rollbacks:** 0 (0%)
- **Success Rate After Adaptation:** 100% (all 4 resolved on second attempt)

---

### Pattern 3: Sprint Lifecycle Management

**Purpose:** Manage sprint initialization, monitoring, and completion.

**Participants:** Sprint Planner → Negotiator → Development Agents → Sprint Planner → Sprint Close

**Workflow:**

```
┌─────────────────┐
│ Sprint Planner  │  1. Initialize sprint (or check completion)
│  (Start Sprint) │     If no sprint or sprint_status==completed:
└────────┬────────┘       Generate Sprint N goal, backlog
         │                Output: SPRINT_GOAL.md, SPRINT_BACKLOG.md
         │
         ▼
┌─────────────────┐
│   Negotiator    │  2. Continuous coordination loop
│  (Continuous)   │     Every ~15 minutes or on-demand:
└────────┬────────┘       - Read SPRINT_QUEUE.json (task status)
         │                - Enforce WIP limits (builder≤3, tester≤2, integrator≤1)
         │                - Manage leases (check stale, takeover if needed)
         │                - Unblock dependencies (blocked → ready when deps met)
         │                - Assign work (update SPRINT_PLAN.md)
         │                - Check sprint exit criteria
         │                - Log heartbeat to SPRINT_LOG.md
         │
         ▼
  [Development Work]
   (See Pattern 1)
         │
         ▼
┌─────────────────┐
│   Negotiator    │  3. Detect sprint completion
│ (Exit Criteria) │     When all exit criteria met:
└────────┬────────┘       - Set sprint_status → completed
         │                - Log completion in SPRINT_LOG.md
         │
         ▼
┌─────────────────┐
│ Sprint Planner  │  4. Check project completion
│(Completion      │     Sprint Planner triggered on completion:
│ Detection)      │       - Call Project Completion Detector
└────────┬────────┘       - If 100% objective met → project_complete
         │                - Else → generate Sprint N+1 goal
         ▼
    [DECISION]
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────┐
│Project  │ │Next      │
│Complete │ │Sprint    │
└─────────┘ └────┬─────┘
                 │
                 ▼
          ┌─────────────────┐
          │  Sprint Close   │  5. Finalize current sprint
          │(Retrospective)  │     - Aggregate shipped/rolled-back tasks
          └────────┬────────┘     - Extract key decisions
                   │              - Generate retrospective
                   │              - Reset SPRINT_PLAN.md
                   ▼
            [Ready for Sprint N+1]
                   │
                   ▼
          ┌─────────────────┐
          │ Sprint Planner  │  6. Initialize Sprint N+1
          │  (Start Sprint) │     (Loop back to step 1)
          └─────────────────┘
```

**Negotiator Heartbeat Format (SPRINT_LOG.md):**

```markdown
## Negotiator Heartbeat — 2025-10-04T10:00:00Z

**Sprint:** 2 (SPRINT-2025-002) - OODATCAA Process Improvement  
**Status:** in_progress  
**Objective Progress:** 71%

**WIP Snapshot:**
- Builder: 2/3 (67% utilized) - P003-B03, P005-B01
- Tester: 1/2 (50% utilized) - P003-T01
- Integrator: 0/1 (0% utilized)
- Planner: 0/1 (0% utilized)

**Sprint Exit Criteria Progress:**
- ✅ P001: Background Agent Daemon System (done)
- ⚠️ P002: Log Rotation System (in progress - P002-B02)
- ⚠️ P003: Sprint Management System (awaiting_test - P003-T01)
- ✅ P004: OODATCAA Documentation (done)
- ⚠️ P005: Agent Role Assessment (in progress - P005-B01)
- ❌ P006: Process Documentation (planning)
- ❌ P007: Observability (planning)

**Tasks Ready:** 0  
**Tasks Blocked:** 14 (dependencies)  
**Recent Activity:** P003-B03 completed, P005-B01 started
```

**Communication Flow:**

1. **Sprint Planner → Negotiator:**
   - File: SPRINT_GOAL.md (Sprint Planner writes, Negotiator reads)
   - File: SPRINT_BACKLOG.md (Sprint Planner writes, Planner reads)
   - Message: "Sprint 2 initialized: OODATCAA Process Improvement, 7 objectives, 30 tasks"

2. **Negotiator → Development Agents:**
   - File: SPRINT_PLAN.md (Negotiator writes assignments, agents read)
   - File: SPRINT_QUEUE.json (Negotiator updates status: blocked → ready when deps met)
   - Message: "Task X dependencies satisfied, status updated to ready"

3. **Development Agents → Negotiator:**
   - File: SPRINT_QUEUE.json (agents update task status)
   - File: AGENT_LOG.md (agents log completion, Negotiator reads for monitoring)
   - Message: "Task X completed, status updated to done"

4. **Negotiator → Sprint Planner:**
   - File: SPRINT_LOG.md (Negotiator logs sprint completion)
   - File: SPRINT_GOAL.md (Negotiator updates sprint_status to completed)
   - Message: "All Sprint 2 exit criteria met, sprint complete"

5. **Sprint Planner → Project Completion Detector:**
   - File: OBJECTIVE.md (Sprint Planner requests completion check)
   - Output: Completion percentage, unmet criteria list
   - Message: "Check if project objective 100% complete"

6. **Sprint Close → Next Sprint:**
   - File: SPRINT_LOG.md (Sprint Close appends retrospective)
   - File: SPRINT_PLAN.md (Sprint Close resets for Sprint N+1)
   - Message: "Sprint 2 retrospective complete, ready for Sprint 3"

**Real-World Example: Sprint 1 Completion**

1. **Negotiator (continuous):**
   - Monitored Sprint 1 progress (34 tasks)
   - Logged heartbeats every ~15 minutes
   - Unblocked dependencies as tasks completed
   - Detected all exit criteria met after W008-B03 integrated

2. **Negotiator (completion detection):**
   - Verified all Sprint 1 exit criteria: ✅ (MCP Server Migration complete)
   - Set sprint_status → completed
   - Logged completion in SPRINT_LOG.md: "Sprint 1 Complete: 34 tasks shipped, 91.9% success"

3. **Sprint Planner (triggered):**
   - Called Project Completion Detector
   - Detector result: 30% objective complete (Sprint 1 was foundation, not full product)
   - Generated Sprint 2 goal: "OODATCAA Process Improvement"

4. **Sprint Close:**
   - Aggregated 34 shipped tasks (W001-W008)
   - Extracted 4 adaptations, 0 rollbacks
   - Generated retrospective: "Sprint 1 Lessons: Protocol coordination pattern needs fix (5 manual interventions)"
   - Reset SPRINT_PLAN.md for Sprint 2

5. **Sprint Planner (Sprint 2 start):**
   - Generated Sprint 2 backlog (P001-P007, 30 tasks)
   - Set exit criteria (7 process improvement objectives)
   - Logged Sprint 2 start in SPRINT_LOG.md

**Sprint 1 Metrics:**
- **Duration:** ~2 weeks
- **Tasks:** 34 completed
- **Success Rate:** 91.9%
- **Adaptations:** 4 (all quick fixes)
- **Negotiator Heartbeats:** ~140 (10 per day × 14 days)
- **Exit Criteria:** 1 (MCP Server Migration) - ✅ Met

---

### Pattern 4: Project Completion Detection

**Purpose:** Determine when product objective is 100% achieved.

**Participants:** Sprint Planner → Project Completion Detector → Sprint Planner

**Workflow:**

```
┌─────────────────┐
│ Sprint Planner  │  1. Trigger completion check
│(After Sprint    │     When: Sprint completes, Integrator merges, or on-demand
│ Completion)     │     Input: OBJECTIVE.md, SPRINT_LOG.md
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Project Complet. │  2. Read all success criteria
│   Detector      │     Input: OBJECTIVE.md (success criteria)
└────────┬────────┘     Parse: Functional, Performance, Quality, Documentation
         │
         ▼
┌─────────────────┐
│   Detector      │  3. Verify each criterion
│  (Evidence      │     Check:
│   Validation)   │       - Acceptance tests (tests/acceptance/)
└────────┬────────┘       - Performance benchmarks (CI results)
         │                - Quality gates (pytest --cov, pip-audit)
         │                - Documentation (README, API docs)
         │
         ▼
┌─────────────────┐
│   Detector      │  4. Calculate completion percentage
│ (Calculate %)   │     Formula: (Criteria Met / Total Criteria) × 100
└────────┬────────┘     Example: 8/10 met = 80%
         │
         ▼
    [DECISION]
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────────┐ ┌──────────────┐
│100%     │ │<100%         │
│Complete │ │Incomplete    │
└────┬────┘ └──────┬───────┘
     │             │
     ▼             ▼
┌─────────────────┐ ┌──────────────────┐
│Generate PROJECT │ │Report Unmet      │
│_COMPLETION_     │ │Criteria + Gap    │
│REPORT.md        │ │Analysis          │
└────────┬────────┘ └──────┬───────────┘
         │                 │
         ▼                 ▼
┌─────────────────┐ ┌──────────────────┐
│Update SPRINT    │ │Sprint Planner    │
│_GOAL.md         │ │Plans Next Sprint │
│status:          │ │to Address Gaps   │
│project_complete │ │                  │
└────────┬────────┘ └──────────────────┘
         │
         ▼
   [PROJECT DONE]
```

**Verification Matrix:**

| Criterion Type | Evidence Required | Validation Method | Example |
|---------------|-------------------|-------------------|---------|
| **Functional** | Passing acceptance tests | Check `tests/acceptance/test_*.py` | 15/15 tests pass |
| **Performance** | Benchmark tests meet thresholds | Check CI pipeline results | p95 < 150ms ✅ |
| **Quality** | Coverage ≥ threshold, no high-severity issues | Run `pytest --cov`, `pip-audit` | 87% coverage ✅, 0 high-severity ✅ |
| **Documentation** | README complete, API docs exist | Verify files exist and comprehensive | README.md ✅, docs/API.md ✅ |

**Communication Flow:**

1. **Sprint Planner → Project Completion Detector:**
   - Trigger: Sprint completion, Integrator merge, or manual request
   - Message: "Check if project objective achieved"

2. **Project Completion Detector → Evidence Sources:**
   - Read: OBJECTIVE.md (success criteria)
   - Read: SPRINT_LOG.md (shipped features)
   - Check: tests/acceptance/ (functional tests)
   - Check: CI results (performance, quality)
   - Check: README.md, docs/ (documentation)

3. **Project Completion Detector → Sprint Planner (100% Complete):**
   - Output: PROJECT_COMPLETION_REPORT.md
   - Update: SPRINT_GOAL.md (status: project_complete)
   - Message: "🎉 Project objective achieved! All criteria met."

4. **Project Completion Detector → Sprint Planner (<100% Complete):**
   - Output: Unmet criteria list with evidence gaps
   - Message: "Project 80% complete. Unmet criteria: [AC3: Documentation, AC7: Performance benchmark]"

5. **Sprint Planner → Next Sprint (if incomplete):**
   - Generate Sprint N+1 goal addressing unmet criteria
   - Message: "Sprint N+1 goal: Address AC3 (documentation) and AC7 (performance)"

**Real-World Example: Sprint 1 Completion Check**

1. **Sprint Planner (after Sprint 1):**
   - Detected Sprint 1 complete (34 tasks done)
   - Triggered Project Completion Detector

2. **Project Completion Detector:**
   - Read OBJECTIVE.md: MCP Local LLM training system
   - Success criteria:
     - ✅ AC1: MCP server integration (functional)
     - ✅ AC2: Vector store (functional)
     - ✅ AC3: Memory management (functional)
     - ❌ AC4: Training data generation (not started)
     - ❌ AC5: Model fine-tuning (not started)
     - ❌ AC6: Evaluation pipeline (not started)
     - ❌ AC7: Documentation (incomplete)
     - ❌ AC8: Performance benchmarks (not started)
   - Completion: 3/8 = 37.5%

3. **Project Completion Detector → Sprint Planner:**
   - Message: "Project 37.5% complete"
   - Unmet criteria: AC4-AC8 (training, tuning, eval, docs, benchmarks)

4. **Sprint Planner (generate Sprint 2):**
   - Sprint 2 goal: "OODATCAA Process Improvement" (foundation before training)
   - Rationale: Strengthen development process before complex ML work
   - Exit criteria: 7 process improvement objectives (P001-P007)

**Note:** Project Completion Detector expected to trigger again after Sprint 2, then Sprint 3 for actual model training work.

---

## Handoff Procedures

### Builder → Tester Handoff

**Trigger:** Builder completes implementation, all quality gates pass

**Builder Responsibilities:**
1. **Update SPRINT_QUEUE.json:**
   ```json
   {
     "id": "P005-B01",
     "status": "awaiting_test",
     "agent": null,
     "lease": null,
     "completed": "2025-10-04T12:00:00Z"
   }
   ```

2. **Log Completion in AGENT_LOG.md:**
   ```markdown
   ## P005-B01: Agent Audit Complete
   
   **Agent:** Builder (agent-builder-cursor)
   **Started:** 2025-10-04T08:16:31Z
   **Completed:** 2025-10-04T12:00:00Z
   **Duration:** ~4 hours
   
   **Deliverables:**
   - AGENT_ROLES_MATRIX.md (810 lines)
   - AGENT_INTERACTION_GUIDE.md (800+ lines)
   - AGENT_GAP_ANALYSIS.md (evidence section)
   
   **Quality Gates:**
   - Markdown syntax: ✅ PASS
   - Links valid: ✅ PASS
   - Cross-references: ✅ PASS
   
   **Status:** awaiting_test
   **Handoff:** Tester should validate all 11 agents documented, 4+ workflow patterns, 10+ Sprint 1/2 citations.
   ```

3. **Create Completion Report:**
   - File: `.oodatcaa/work/reports/P005/builder_P005-B01.md`
   - Include: objective, actions, deliverables, metrics, quality gates, challenges, **handoff notes for Tester**

4. **Push Feature Branch:**
   ```bash
   git push -u origin feat/P005-step-01-agent-audit
   ```

5. **Release Lease:**
   ```bash
   rm .leases/P005-B01.json
   ```

**Tester Discovery:**
1. Read SPRINT_QUEUE.json, find first `status == "awaiting_test"`
2. Read Builder completion report (`.oodatcaa/work/reports/P005/builder_P005-B01.md`)
3. Read TEST_PLAN.md for acceptance criteria
4. Checkout feature branch (`feat/P005-step-01-agent-audit`)
5. Acquire lease, start validation

**Handoff Checklist:**
- [ ] SPRINT_QUEUE.json status updated to "awaiting_test"
- [ ] AGENT_LOG.md entry with summary
- [ ] Completion report created with handoff notes
- [ ] Feature branch pushed
- [ ] Lease released

---

### Tester → Integrator Handoff (Happy Path)

**Trigger:** Tester validates all acceptance criteria passed

**Tester Responsibilities:**
1. **Update SPRINT_QUEUE.json:**
   ```json
   {
     "id": "P005-B01",
     "status": "ready_for_integrator",
     "agent": null,
     "lease": null,
     "validated": "2025-10-04T13:00:00Z"
   }
   ```

2. **Log Validation Results in AGENT_LOG.md:**
   ```markdown
   ## P005-B01: Validation Complete
   
   **Agent:** Tester (agent-tester-A)
   **Validated:** 2025-10-04T13:00:00Z
   **Duration:** 30 minutes
   
   **Acceptance Criteria:**
   - AC1: Agent roles matrix complete (11 agents, 7 attributes) - ✅ PASS
   - AC2: Interaction guide with 4+ workflow patterns - ✅ PASS
   - AC3: Sprint 1/2 evidence (10+ citations) - ✅ PASS
   - AC4: All agent descriptions accurate - ✅ PASS
   - AC5: Cross-links to prompts, reports, logs - ✅ PASS
   
   **Status:** ready_for_integrator
   **Handoff:** Integrator should merge feat/P005-step-01-agent-audit, create baseline tag pre/P005-B01-*, update CHANGELOG.
   ```

3. **Create Completion Report:**
   - File: `.oodatcaa/work/reports/P005/tester_P005-B01.md`
   - Include: test results per AC, coverage delta, new tests added (if any), **handoff notes for Integrator**

4. **Release Lease:**
   ```bash
   rm .leases/P005-B01.json
   ```

**Integrator Discovery:**
1. Read SPRINT_QUEUE.json, find first `status == "ready_for_integrator"`
2. Read Tester completion report (`.oodatcaa/work/reports/P005/tester_P005-B01.md`)
3. Read Builder completion report (for context)
4. Checkout feature branch (`feat/P005-step-01-agent-audit`)
5. Acquire lease, start integration

**Handoff Checklist:**
- [ ] SPRINT_QUEUE.json status updated to "ready_for_integrator"
- [ ] AGENT_LOG.md entry with validation results (PASS per AC)
- [ ] Completion report created with handoff notes
- [ ] Lease released

---

### Tester → Refiner Handoff (Failure Path)

**Trigger:** Tester validation fails (one or more ACs not met)

**Tester Responsibilities:**
1. **Update SPRINT_QUEUE.json:**
   ```json
   {
     "id": "P005-B01",
     "status": "needs_adapt",
     "agent": null,
     "lease": null,
     "failed_validation": "2025-10-04T13:00:00Z"
   }
   ```

2. **Log Detailed Failure in AGENT_LOG.md:**
   ```markdown
   ## P005-B01: Validation Failed
   
   **Agent:** Tester (agent-tester-A)
   **Validated:** 2025-10-04T13:00:00Z
   **Duration:** 30 minutes
   
   **Acceptance Criteria:**
   - AC1: Agent roles matrix complete (11 agents, 7 attributes) - ✅ PASS
   - AC2: Interaction guide with 4+ workflow patterns - ❌ FAIL (only 3 patterns documented)
   - AC3: Sprint 1/2 evidence (10+ citations) - ❌ FAIL (only 6 citations found)
   - AC4: All agent descriptions accurate - ✅ PASS
   - AC5: Cross-links to prompts, reports, logs - ✅ PASS
   
   **Failure Details:**
   - AC2: Expected 4+ workflow patterns, found only 3 (Primary Dev Flow, Adaptation Loop, Sprint Lifecycle). Missing: Project Completion Flow.
   - AC3: Expected 10+ Sprint 1/2 citations, found only 6 (W004, W005, P002-B01, P003-B01/B02, P004). Need 4 more examples.
   
   **Suggestions:**
   - Add Project Completion Flow workflow pattern to AGENT_INTERACTION_GUIDE.md
   - Add 4 more Sprint 1/2 task examples with evidence (e.g., W006, W007, W008, P001)
   
   **Status:** needs_adapt
   **Handoff:** Refiner should decide quick fix (add missing patterns + citations) or rollback.
   ```

3. **Create Completion Report:**
   - File: `.oodatcaa/work/reports/P005/tester_P005-B01.md`
   - Include: failure details, specific ACs failed, test output, **suggestions for fix**, handoff notes for Refiner

4. **Release Lease:**
   ```bash
   rm .leases/P005-B01.json
   ```

**Refiner Discovery:**
1. Read SPRINT_QUEUE.json, find first `status == "needs_adapt"`
2. Read Tester completion report (failure details, suggestions)
3. Read AGENT_LOG.md (Tester's failure log)
4. Read AGENT_PLAN.md (original plan for context)
5. Acquire lease, analyze failure, decide approach

**Handoff Checklist:**
- [ ] SPRINT_QUEUE.json status updated to "needs_adapt"
- [ ] AGENT_LOG.md entry with detailed failure (which ACs, why, suggestions)
- [ ] Completion report created with specific fix suggestions
- [ ] Lease released

---

### Integrator → Done

**Trigger:** Integrator merges feature branch to main

**Integrator Responsibilities:**
1. **Update SPRINT_QUEUE.json:**
   ```json
   {
     "id": "P005-B01",
     "status": "done",
     "agent": null,
     "lease": null,
     "integrated": "2025-10-04T14:00:00Z",
     "pr_url": "https://github.com/user/repo/pull/123",
     "tag": "pre/P005-B01-2025-10-04T14-00-00"
   }
   ```

2. **Log Shipped Entry in SPRINT_LOG.md:**
   ```markdown
   ## Shipped: P005-B01 — Agent Audit Complete
   
   **Date:** 2025-10-04T14:00:00Z
   **PR:** #123
   **Tag:** pre/P005-B01-2025-10-04T14-00-00
   **Branch:** feat/P005-step-01-agent-audit
   
   **Deliverables:**
   - AGENT_ROLES_MATRIX.md (810 lines, 11 agents documented)
   - AGENT_INTERACTION_GUIDE.md (partial, 4 workflow patterns)
   - AGENT_GAP_ANALYSIS.md (evidence section with 10+ citations)
   
   **Impact:**
   - Unblocks P005-B02 (Gap Analysis + Communication Protocol)
   - Provides foundation for agent system assessment
   - Documents all 11 agents with Sprint 1/2 evidence
   ```

3. **Update CHANGELOG.md:**
   ```markdown
   ## [Sprint 2] - 2025-10-04
   
   ### Added
   - P005-B01: Agent Roles Matrix (11 agents documented)
   - P005-B01: Agent Interaction Guide (4 workflow patterns)
   - P005-B01: Sprint 1/2 evidence analysis (10+ citations)
   
   ### Documentation
   - `.oodatcaa/AGENT_ROLES_MATRIX.md` - Comprehensive agent capabilities matrix
   - `.oodatcaa/AGENT_INTERACTION_GUIDE.md` - Workflow patterns and communication mechanisms
   ```

4. **Create Baseline Tag:**
   ```bash
   git tag -a pre/P005-B01-2025-10-04T14-00-00 -m "Baseline: P005-B01 Agent Audit Complete"
   git push origin pre/P005-B01-2025-10-04T14-00-00
   ```

5. **Create Completion Report:**
   - File: `.oodatcaa/work/reports/P005/integrator_P005-B01.md`
   - Include: PR details, merge strategy, CHANGELOG updates, tag created, **what this unblocks**

6. **Release Lease:**
   ```bash
   rm .leases/P005-B01.json
   ```

**Unblocking Effect:**
- SPRINT_QUEUE.json: P005-B02 dependencies satisfied
- Negotiator (next loop): Detects P005-B02 dependencies met, updates status: blocked → ready

**Handoff Checklist:**
- [ ] SPRINT_QUEUE.json status updated to "done" (with PR URL, tag)
- [ ] SPRINT_LOG.md shipped entry added
- [ ] CHANGELOG.md updated
- [ ] Baseline tag created and pushed
- [ ] Completion report created
- [ ] Lease released

---

## Real-World Examples

### Example 1: Perfect Implementation (P002-B01)

**Context:** Sprint 2, Log Rotation System, 100% first-attempt success

**Timeline:**
1. **2025-10-03T10:00** - Planner completes P002 planning
2. **2025-10-03T10:30** - Builder picks P002-B01 (first ready builder task)
3. **2025-10-03T12:30** - Builder completes implementation (2 hours)
4. **2025-10-03T12:45** - Tester validates P002-B01 (15 minutes)
5. **2025-10-03T12:55** - Integrator merges P002-B01 (10 minutes)

**Communication Trace:**

```
[10:00] Planner → SPRINT_QUEUE.json
  Task P002-B01 created with status="ready"

[10:30] Builder → Lease System
  Created .leases/P002-B01.json (TTL: 5400s)

[10:30] Builder → SPRINT_QUEUE.json
  P002-B01 status: ready → in_progress

[10:35] Builder → AGENT_LOG.md (Heartbeat #1)
  "P002-B01 in progress: implementing rotate-logs.sh"

[11:00] Builder → AGENT_LOG.md (Heartbeat #2)
  "P002-B01 progress: script 60% complete, 120 lines"

[12:30] Builder → SPRINT_QUEUE.json
  P002-B01 status: in_progress → awaiting_test

[12:30] Builder → AGENT_LOG.md (Completion)
  "P002-B01 complete: scripts/rotate-logs.sh (201 lines), all gates passed"

[12:30] Builder → Lease System
  Deleted .leases/P002-B01.json

[12:30] Builder → Feature Branch
  Pushed feat/P002-step-01-rotation-script

[12:30] Builder → Completion Report
  Created .oodatcaa/work/reports/P002/builder_P002-B01.md

[12:35] Tester → Lease System
  Created .leases/P002-B01.json (TTL: 2700s)

[12:35] Tester → SPRINT_QUEUE.json
  P002-B01 status: awaiting_test → in_progress (Tester)

[12:45] Tester → SPRINT_QUEUE.json
  P002-B01 status: in_progress → ready_for_integrator

[12:45] Tester → AGENT_LOG.md
  "P002-B01 validation complete: All 10 ACs PASS"

[12:45] Tester → Lease System
  Deleted .leases/P002-B01.json

[12:50] Integrator → Lease System
  Created .leases/P002-B01.json (TTL: 1800s)

[12:50] Integrator → PR System
  Opened PR #45: P002-B01 Log Rotation System

[12:52] Integrator → Git
  Merged PR #45 (squash merge)

[12:53] Integrator → Git
  Created tag pre/P002-B01-2025-10-03T12-53-00

[12:54] Integrator → SPRINT_QUEUE.json
  P002-B01 status: ready_for_integrator → done

[12:55] Integrator → SPRINT_LOG.md
  "Shipped: P002-B01 (PR #45, tag pre/P002-B01-2025-10-03T12-53-00)"

[12:55] Integrator → CHANGELOG.md
  Added P002-B01 entry

[12:55] Integrator → Lease System
  Deleted .leases/P002-B01.json

[12:56] Negotiator → SPRINT_QUEUE.json (Next Loop)
  Detected P002-B02 dependencies met, updated status: blocked → ready
```

**Outcome:** 135 minutes total (within 150min estimate), 0 adaptations, shipped in Sprint 2

---

### Example 2: Adaptation Loop (W004)

**Context:** Sprint 1, Query Optimization, performance issue requiring adaptation

**Timeline:**
1. **2025-09-20T09:00** - Builder completes W004-B01 implementation
2. **2025-09-20T09:30** - Tester fails validation (AC5: performance)
3. **2025-09-20T09:45** - Refiner analyzes, decides quick fix
4. **2025-09-20T10:15** - Builder re-implements with caching
5. **2025-09-20T10:30** - Tester re-validates, all ACs pass
6. **2025-09-20T10:40** - Integrator merges

**Communication Trace:**

```
[09:00] Builder → SPRINT_QUEUE.json
  W004-B01 status: in_progress → awaiting_test

[09:05] Tester → Lease System
  Created .leases/W004-B01.json

[09:30] Tester → SPRINT_QUEUE.json
  W004-B01 status: awaiting_test → needs_adapt

[09:30] Tester → AGENT_LOG.md (Failure)
  "W004-B01 FAIL: AC5 performance threshold not met (p95: 180ms, target: 150ms)"

[09:30] Tester → Completion Report
  "Suggestions: Add query result caching to reduce latency"

[09:35] Refiner → Lease System
  Created .leases/W004-B01.json

[09:45] Refiner → AGENT_LOG.md (Decision)
  "Quick fix recommended: Implement LRU cache for query results"

[09:45] Refiner → SPRINT_QUEUE.json
  W004-B01 status: needs_adapt → ready

[09:45] Refiner → Lease System
  Deleted .leases/W004-B01.json

[09:50] Builder → Lease System
  Created .leases/W004-B01.json (2nd attempt)

[09:50] Builder → SPRINT_QUEUE.json
  W004-B01 status: ready → in_progress

[10:15] Builder → SPRINT_QUEUE.json
  W004-B01 status: in_progress → awaiting_test

[10:15] Builder → AGENT_LOG.md
  "W004-B01 re-implementation complete: Added LRU cache (50 lines)"

[10:20] Tester → Lease System
  Created .leases/W004-B01.json (2nd validation)

[10:30] Tester → SPRINT_QUEUE.json
  W004-B01 status: awaiting_test → ready_for_integrator

[10:30] Tester → AGENT_LOG.md (Success)
  "W004-B01 validation PASS: AC5 now passes (p95: 120ms < 150ms threshold)"

[10:35] Integrator → Merge + Tag
  Merged W004-B01, created tag pre/W004-B01-2025-09-20T10-35-00

[10:40] Integrator → SPRINT_QUEUE.json
  W004-B01 status: ready_for_integrator → done
```

**Outcome:** 100 minutes total (60min adaptation overhead), quick fix successful, shipped in Sprint 1

---

### Example 3: Parallel Execution (Sprint 2, Multiple Builders)

**Context:** Sprint 2, P003-B01 and P003-B02 worked on in parallel

**Timeline:**
1. **2025-10-03T13:00** - Builder A starts P003-B01
2. **2025-10-03T13:10** - Builder B starts P003-B02 (independent task)
3. **2025-10-03T13:30** - Builder A completes P003-B01
4. **2025-10-03T13:45** - Builder B completes P003-B02
5. **2025-10-03T14:00** - Tester A validates P003-B01
6. **2025-10-03T14:15** - Tester B validates P003-B02
7. **2025-10-03T14:30** - Integrator merges P003-B01
8. **2025-10-03T14:45** - Integrator merges P003-B02

**Communication Trace:**

```
[13:00] Builder A → Lease System
  Created .leases/P003-B01.json (owner: agent-builder-A)

[13:00] Builder A → SPRINT_QUEUE.json
  P003-B01 status: ready → in_progress (agent: builder, owner: agent-builder-A)

[13:10] Builder B → Lease System
  Created .leases/P003-B02.json (owner: agent-builder-B)

[13:10] Builder B → SPRINT_QUEUE.json
  P003-B02 status: ready → in_progress (agent: builder, owner: agent-builder-B)

[13:15] Negotiator Heartbeat
  "WIP: Builder 2/3 (P003-B01: agent-builder-A, P003-B02: agent-builder-B)"

[13:30] Builder A → SPRINT_QUEUE.json
  P003-B01 status: in_progress → awaiting_test

[13:30] Builder A → Lease System
  Deleted .leases/P003-B01.json

[13:45] Builder B → SPRINT_QUEUE.json
  P003-B02 status: in_progress → awaiting_test

[13:45] Builder B → Lease System
  Deleted .leases/P003-B02.json

[14:00] Tester A → SPRINT_QUEUE.json
  P003-B01 status: awaiting_test → ready_for_integrator

[14:15] Tester B → SPRINT_QUEUE.json
  P003-B02 status: awaiting_test → ready_for_integrator

[14:30] Integrator → SPRINT_QUEUE.json
  P003-B01 status: ready_for_integrator → done

[14:45] Integrator → SPRINT_QUEUE.json
  P003-B02 status: ready_for_integrator → done

[14:50] Negotiator → SPRINT_QUEUE.json (Next Loop)
  Detected P003-B03 dependencies met (P003-B01, P003-B02 both done)
  Updated P003-B03 status: blocked → ready
```

**Outcome:** 105 minutes total (30min saved through parallel execution), both tasks successful, P003-B03 unblocked

**Parallel Execution Benefits:**
- **Time Savings:** 30 minutes (if sequential: 30min + 45min = 75min, parallel: max(30, 45) = 45min)
- **WIP Utilization:** 2/3 builders utilized (67%)
- **Dependency Unlocking:** P003-B03 unblocked faster (both dependencies met simultaneously)

---

## Failure Patterns & Recovery

### Pattern 1: Stale Lease Recovery

**Symptom:** Task shows "in_progress" but lease expired (heartbeat + TTL < now)

**Cause:** Agent crashed, network issue, or hung process

**Detection (Negotiator):**
```bash
# Scan leases every coordination loop
for lease in .leases/*.json; do
  HEARTBEAT=$(jq -r '.last_heartbeat' "$lease")
  TTL=$(jq -r '.ttl' "$lease")
  EXPIRY=$(( $(date -d "$HEARTBEAT" +%s) + TTL ))
  NOW=$(date +%s)
  
  if (( EXPIRY < NOW )); then
    # Stale lease detected
    TASK_ID=$(jq -r '.task_id' "$lease")
    OWNER=$(jq -r '.owner' "$lease")
    AGE=$(( NOW - EXPIRY ))
    
    echo "$(date -Iseconds) - Stale lease takeover: $TASK_ID (owner: $OWNER, expired ${AGE}s ago)" >> .oodatcaa/work/AGENT_LOG.md
    
    # Delete lease
    rm "$lease"
    
    # Reset task status
    jq '.tasks |= map(if .id == "'$TASK_ID'" then .status = "ready" | .lease = null | .agent = null else . end)' SPRINT_QUEUE.json > /tmp/queue_tmp.json
    mv /tmp/queue_tmp.json SPRINT_QUEUE.json
  fi
done
```

**Recovery:**
1. Negotiator detects stale lease
2. Logs takeover in AGENT_LOG.md
3. Deletes stale lease file
4. Resets task status to "ready"
5. Next agent of that type picks up task (fresh start)

**Prevention:**
- Agents must send heartbeats every ~10 minutes
- Set appropriate TTLs (Builder: 90min, Tester: 45min)
- Use robust error handling (always release lease on exit)

---

### Pattern 2: JSON Corruption Recovery

**Symptom:** `jq` fails with parse error on SPRINT_QUEUE.json

**Cause:** Concurrent writes, script crash during write, filesystem issue

**Detection:**
```bash
if ! jq empty SPRINT_QUEUE.json 2>/dev/null; then
  echo "ERROR: SPRINT_QUEUE.json is corrupted"
  exit 1
fi
```

**Recovery:**
```bash
# 1. Check for backup
if [[ -f SPRINT_QUEUE.json.backup ]]; then
  echo "Restoring from backup"
  cp SPRINT_QUEUE.json.backup SPRINT_QUEUE.json
else
  echo "No backup found, manual recovery required"
  exit 1
fi

# 2. Validate backup
if jq empty SPRINT_QUEUE.json 2>/dev/null; then
  echo "Backup valid, recovered successfully"
else
  echo "Backup also corrupted, restore from git"
  git checkout main -- .oodatcaa/work/SPRINT_QUEUE.json
fi
```

**Prevention:**
- **Always use atomic writes:**
  ```bash
  jq '...' SPRINT_QUEUE.json > /tmp/queue_tmp.json
  mv /tmp/queue_tmp.json SPRINT_QUEUE.json  # Atomic rename
  ```
- **Create backups before modifications:**
  ```bash
  cp SPRINT_QUEUE.json SPRINT_QUEUE.json.backup
  ```
- **Validate JSON after write:**
  ```bash
  jq empty SPRINT_QUEUE.json || { echo "Write failed"; exit 1; }
  ```

---

### Pattern 3: Deadlock (Circular Dependencies)

**Symptom:** All tasks "blocked", no progress

**Cause:** Circular dependency graph (A depends on B, B depends on A)

**Detection (Negotiator):**
```bash
BLOCKED_COUNT=$(jq '[.tasks[] | select(.status == "blocked")] | length' SPRINT_QUEUE.json)
READY_COUNT=$(jq '[.tasks[] | select(.status == "ready")] | length' SPRINT_QUEUE.json)
IN_PROGRESS_COUNT=$(jq '[.tasks[] | select(.status == "in_progress")] | length' SPRINT_QUEUE.json)

if (( BLOCKED_COUNT > 0 )) && (( READY_COUNT == 0 )) && (( IN_PROGRESS_COUNT == 0 )); then
  echo "DEADLOCK DETECTED: All tasks blocked, no work available"
  # Log and escalate
fi
```

**Recovery:**
1. **Identify circular dependencies:**
   ```bash
   jq '.tasks[] | select(.status == "blocked") | {id, dependencies}' SPRINT_QUEUE.json
   ```

2. **Manual intervention required:**
   - Review dependency graph
   - Identify circular dependency (A → B → A)
   - Break cycle by removing incorrect dependency
   - Update SPRINT_QUEUE.json manually
   - Log resolution in AGENT_LOG.md

3. **Prevention in Planning:**
   - Planner should validate dependency graph (no cycles)
   - Use topological sort to detect cycles
   - Reject plans with circular dependencies

**Real-World Note:** No deadlocks detected in Sprint 1 or Sprint 2 (Planner creates acyclic dependency graphs)

---

### Pattern 4: Start-Over Gate (Fundamental Failure)

**Symptom:** Task fails validation twice, quick fixes insufficient

**Cause:** Fundamental design flaw, wrong approach, architectural mismatch

**Trigger (Refiner):**
```bash
ADAPTATION_COUNT=$(jq '.tasks[] | select(.id == "P005-B01") | .adaptation_count // 0' SPRINT_QUEUE.json)

if (( ADAPTATION_COUNT >= 2 )); then
  echo "START-OVER GATE TRIGGERED: 2 adaptation attempts failed"
  # Initiate rollback protocol
fi
```

**Recovery (Rollback Protocol):**

1. **Refiner Analysis:**
   - Read AGENT_LOG.md (both adaptation attempts)
   - Identify root cause (design flaw, wrong approach)
   - Decide rollback necessary

2. **Rollback Steps:**
   ```bash
   # A. Reset git to baseline tag
   BASELINE_TAG=$(git tag -l "pre/P005-B01-*" | head -1)
   git reset --hard "$BASELINE_TAG"
   
   # B. Bump AGENT_PLAN.md version
   sed -i 's/Version: 1.0/Version: 2.0/' .oodatcaa/work/AGENT_PLAN.md
   
   # C. Revise steps/ACs in AGENT_PLAN.md
   # (Manual edit by Refiner, new approach)
   
   # D. Write Post-Mortem in AGENT_PLAN.md
   cat >> .oodatcaa/work/AGENT_PLAN.md <<EOF
   
   ## Post-Mortem: Version 1.0 Failure
   
   **Date:** $(date -Iseconds)
   **Root Cause:** Approach X fundamentally flawed (reason)
   **Version 2.0 Changes:** New approach Y (details)
   **Lessons Learned:** (insights)
   EOF
   
   # E. Reset task status
   jq '.tasks |= map(if .id == "P005-B01" then .status = "ready" | .adaptation_count = 0 | .plan_version = "2.0" else . end)' SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json SPRINT_QUEUE.json
   ```

3. **Log Rollback:**
   ```markdown
   ## P005-B01: Start-Over Gate Triggered
   
   **Agent:** Refiner (agent-refiner-A)
   **Date:** 2025-10-04T15:00:00Z
   **Reason:** 2 adaptation attempts failed, fundamental design flaw
   
   **Root Cause:** Approach in Version 1.0 used X, but Y is required
   **Rollback:** Reset to baseline tag pre/P005-B01-2025-10-04T08-00-00
   **Plan Update:** AGENT_PLAN.md Version 2.0 (new approach Y)
   **Post-Mortem:** Added to AGENT_PLAN.md
   
   **Status:** ready (fresh start with revised plan)
   **Next:** Builder will re-implement using Version 2.0 plan
   ```

4. **Builder Re-implementation:**
   - Read AGENT_PLAN.md Version 2.0
   - Start fresh from baseline tag
   - Implement new approach

**Real-World Note:** No Start-Over gates triggered in Sprint 1 (all 4 adaptations resolved with quick fixes)

---

## Best Practices

### 1. Atomic File Operations

**Always use temp file + atomic rename pattern:**

```bash
# ✅ GOOD: Atomic
jq '.tasks |= map(...)' SPRINT_QUEUE.json > /tmp/queue_tmp.json
mv /tmp/queue_tmp.json SPRINT_QUEUE.json

# ❌ BAD: Non-atomic (can corrupt file if interrupted)
jq '.tasks |= map(...)' SPRINT_QUEUE.json > SPRINT_QUEUE.json
```

**Rationale:** Atomic rename ensures file is never in partially-written state, preventing JSON corruption.

---

### 2. Heartbeat Discipline

**Always send heartbeats for long-running tasks:**

```bash
# Every ~10 minutes during work
jq '.last_heartbeat = "'$(date -Iseconds)'"' .leases/P005-B01.json > /tmp/lease_tmp.json
mv /tmp/lease_tmp.json .leases/P005-B01.json
```

**Rationale:** Prevents Negotiator from treating active work as stale lease (causing takeover).

---

### 3. Always Release Leases

**Use trap to ensure lease release even on error:**

```bash
# At start of script
trap 'rm -f .leases/P005-B01.json; exit' EXIT INT TERM

# Work happens here...

# Normal exit will trigger trap, releasing lease
```

**Rationale:** Prevents permanent lease locks if script crashes or is interrupted.

---

### 4. Log Before Status Change

**Always log action before updating SPRINT_QUEUE.json:**

```bash
# 1. Log action
echo "$(date -Iseconds) - Builder: P005-B01 complete, status → awaiting_test" >> .oodatcaa/work/AGENT_LOG.md

# 2. Update status
jq '.tasks |= map(if .id == "P005-B01" then .status = "awaiting_test" else . end)' SPRINT_QUEUE.json > /tmp/queue_tmp.json
mv /tmp/queue_tmp.json SPRINT_QUEUE.json
```

**Rationale:** If status update fails, log entry exists for debugging. Ensures auditability.

---

### 5. Validate JSON After Write

**Always verify JSON syntax after modification:**

```bash
jq '.tasks |= map(...)' SPRINT_QUEUE.json > /tmp/queue_tmp.json

# Validate before atomic rename
if jq empty /tmp/queue_tmp.json 2>/dev/null; then
  mv /tmp/queue_tmp.json SPRINT_QUEUE.json
else
  echo "ERROR: Invalid JSON generated, aborting"
  exit 1
fi
```

**Rationale:** Catches jq errors before corrupting SPRINT_QUEUE.json.

---

### 6. Create Completion Reports

**Every agent must create completion report:**

```bash
# At end of agent work
cat > .oodatcaa/work/reports/P005/builder_P005-B01.md <<EOF
# Builder Completion Report: P005-B01

**Task:** P005-B01 - Agent Audit + Interaction + Evidence
**Agent:** agent-builder-cursor
**Status:** ready → awaiting_test
**Duration:** 4 hours

## Deliverables
...

## Handoff Notes for Tester
...
EOF

# Also append to AGENT_REPORTS.md
cat >> .oodatcaa/work/AGENT_REPORTS.md <<EOF

## P005-B01: Agent Audit Complete ✅
**Agent:** Builder
**Completed:** $(date -Iseconds)
**Report:** .oodatcaa/work/reports/P005/builder_P005-B01.md
EOF
```

**Rationale:** Provides comprehensive record, enables next agent to understand context, supports sprint retrospectives.

---

### 7. Use Descriptive Commit Messages

**Follow commit message conventions:**

```bash
git commit -m "[impl] P005-B01: Add AGENT_ROLES_MATRIX.md (11 agents documented)"
git commit -m "[test] P005-B01: Add validation tests for agent matrix"
git commit -m "[tracking] P005-B01: Update status to awaiting_test"
git commit -m "[refactor] P005-B01: Simplify workflow pattern descriptions"
```

**Rationale:** Clear commit history, easy to understand changes, supports rollback if needed.

---

### 8. Cross-Reference Aggressively

**Always link related files:**

```markdown
**Related Files:**
- [AGENT_PLAN.md](.oodatcaa/work/AGENT_PLAN.md) - Implementation plan
- [TEST_PLAN.md](.oodatcaa/work/TEST_PLAN.md) - Acceptance criteria
- [Builder Report](.oodatcaa/work/reports/P005/builder_P005-B01.md) - Implementation details
- [Sprint 1 Log](.oodatcaa/work/archive/sprint_1/SPRINT_LOG_final.md) - Historical evidence
```

**Rationale:** Enables agents to find context quickly, supports comprehensive understanding.

---

### 9. Status Transitions Must Be Logged

**Every status change must have corresponding AGENT_LOG.md entry:**

```bash
# Bad: Status change without log
jq '.tasks |= map(if .id == "P005-B01" then .status = "done" else . end)' SPRINT_QUEUE.json > /tmp/queue_tmp.json
mv /tmp/queue_tmp.json SPRINT_QUEUE.json

# Good: Log + status change
echo "$(date -Iseconds) - Integrator: P005-B01 merged (PR #123, tag pre/P005-B01-*), status → done" >> .oodatcaa/work/AGENT_LOG.md
jq '.tasks |= map(if .id == "P005-B01" then .status = "done" else . end)' SPRINT_QUEUE.json > /tmp/queue_tmp.json
mv /tmp/queue_tmp.json SPRINT_QUEUE.json
```

**Rationale:** Audit trail, debugging capability, sprint retrospectives rely on comprehensive logs.

---

### 10. Prefer Quick Fixes Over Rollbacks

**Refiner decision matrix:**

```bash
if [[ "$FAILURE_TYPE" == "lint" ]] || [[ "$FAILURE_TYPE" == "format" ]] || [[ "$FAILURE_TYPE" == "minor_test" ]]; then
  DECISION="quick_fix"
elif [[ "$ADAPTATION_COUNT" -ge 2 ]]; then
  DECISION="rollback"  # Start-Over gate
elif [[ "$FAILURE_IMPACT" == "fundamental" ]]; then
  DECISION="rollback"
else
  DECISION="quick_fix"
fi
```

**Rationale:** Quick fixes faster (30min vs 2hr rollback), Sprint 1 evidence shows 100% quick fix success rate.

---

## Communication Protocols

Standardized protocols for agent coordination, decision transparency, and conflict resolution based on Sprint 1/2 evidence and gap analysis (P005-B02).

---

### Protocol 1: Structured Message Format

**Purpose:** Standardize inter-agent messages for parsing, tracing, and automation.

**When to Use:**
- Builder → Tester handoff (task complete, awaiting validation)
- Tester → Refiner escalation (test failure requiring adaptation)
- Monitor → Negotiator alert (anomaly detected)
- Any agent → Any agent query/response

**Message Template:**

```markdown
## Message: <From Agent> → <To Agent> <Type>

**Message ID:** MSG-<UUID>  
**Timestamp:** <ISO8601>  
**From:** <agent_role> (<agent_instance>)  
**To:** <agent_role> (<agent_instance or "any">)  
**Task:** <task_id>  
**Type:** handoff | alert | decision | query | response | status_update  
**Priority:** low | normal | high | urgent

**Content:**
- Summary: <one-line summary>
- Details: <additional context>
- [Type-specific fields]

**Action Required:** <what recipient should do>

**Thread:** THREAD-<task_id>
```

**Message Types:**

1. **handoff:** Agent completed work, passing to next agent
   - Required fields: summary, branch, status_from, status_to, gate_results
   - Example: Builder → Tester after implementation complete

2. **alert:** Anomaly or issue requiring attention
   - Required fields: alert_type, severity, details, recommended_action
   - Example: Monitor → Negotiator when task exceeds 150% estimated time

3. **decision:** Agent made a decision, documenting for transparency
   - Required fields: decision, rationale, alternatives_considered, confidence
   - Example: Refiner → Builder quick fix decision

4. **query:** Agent requesting information from another agent
   - Required fields: question, context, urgency
   - Example: Builder → Planner asking for design clarification

5. **response:** Reply to query or handoff
   - Required fields: response_to (message_id), answer/status
   - Example: Tester → Builder test results

6. **status_update:** Progress update during long-running task
   - Required fields: progress_pct, duration_elapsed, duration_remaining, blockers
   - Example: Builder mid-implementation progress report

**Storage:**
- Primary: AGENT_LOG.md (human-readable markdown format)
- Optional: `.messages/<task_id>.jsonl` (machine-readable JSON for automation)

**Benefits:**
- Programmatic message parsing enables automation (Monitor agent can parse alerts)
- Traceability via thread_id links related messages across agents
- Priority-based processing (urgent alerts handled before normal handoffs)
- Audit trail for retrospectives and debugging

**JSON Schema (for .messages/*.jsonl):**

```json
{
  "message_id": "MSG-<UUID>",
  "timestamp": "2025-10-04T10:30:00Z",
  "from_agent": "builder",
  "from_instance": "agent-builder-A",
  "to_agent": "tester",
  "to_instance": null,
  "task_id": "P005-B01",
  "message_type": "handoff",
  "priority": "normal",
  "content": { ... },
  "decision_required": false,
  "response_expected": true,
  "thread_id": "THREAD-P005-B01"
}
```

**Implementation Status:** Defined in Sprint 2 (P005-B02), implement in Sprint 3

---

### Protocol 2: Decision Transparency Template

**Purpose:** Standardize decision documentation for auditability, learning, and confidence calibration.

**When to Use:**
- Refiner: Quick fix vs Rollback decision
- Planner: Alternative selection (design approach)
- Negotiator: Priority change, agent assignment, conflict resolution
- Sprint Planner: Sprint goal definition, objective completion assessment

**Decision Template:**

```markdown
## Decision: <Decision Type> (<Task ID>)

**Decision ID:** DEC-<UUID>  
**Timestamp:** <ISO8601>  
**Agent:** <agent_role> (<agent_instance>)  
**Task:** <task_id>  
**Type:** adaptation_approach | alternative_selection | priority_change | conflict_resolution

**Decision:** <chosen option>

**Rationale:**  
<Why this decision? 2-3 sentences explaining reasoning>

**Alternatives Considered:**
1. **<Option 1>**
   - Pros: <benefits>
   - Cons: <drawbacks>
   - Rejected: <reason>

2. **<Option 2>**
   - Pros: <benefits>
   - Cons: <drawbacks>
   - Rejected: <reason>

[Minimum 2 alternatives required]

**Evidence:**
- <Citation 1>
- <Citation 2>
- <Citation 3>

[Minimum 2 evidence items required]

**Confidence:** low | medium | high

**Outcome:** [To be filled retrospectively]  
<After decision plays out, document outcome: success, failure, or mixed. Include metrics/observations.>
```

**Decision Types:**

| Decision Type | Agent | Typical Choices | Evidence Sources |
|---------------|-------|-----------------|------------------|
| **adaptation_approach** | Refiner | quick_fix, rollback, defer | Tester report, failure analysis, time estimates |
| **alternative_selection** | Planner | Approach A/B/C/D | Design patterns, performance, complexity, maintainability |
| **priority_change** | Negotiator | Increase/decrease priority | Sprint goals, dependencies, blockers |
| **conflict_resolution** | Negotiator | Agent A/B position, compromise | TEST_PLAN.md, OBJECTIVE.md, evidence from both sides |

**Examples:**

**Example 1: Refiner Adaptation Decision (W004-B01)**

```markdown
## Decision: Adaptation Approach (W004-B01)

**Decision ID:** DEC-w004-001  
**Timestamp:** 2025-09-20T09:45:00Z  
**Agent:** Refiner (agent-refiner-A)  
**Task:** W004-B01  
**Type:** adaptation_approach

**Decision:** Quick Fix (add LRU cache)

**Rationale:**  
Performance issue isolated to query caching layer. Adding LRU cache resolves issue without architectural changes. Estimated fix time: 30 minutes.

**Alternatives Considered:**
1. **Rollback to baseline**
   - Pros: Clean slate, rethink approach
   - Cons: Wastes 90 min of work, no fundamental flaw identified
   - Rejected: Issue too narrow for rollback

2. **Defer to next sprint**
   - Pros: Avoid immediate work, wait for more data
   - Cons: Blocks sprint progress, issue clear enough to fix now
   - Rejected: Clear fix available, no reason to defer

**Evidence:**
- Tester report: p95 latency 180ms (target: 150ms)
- Profiling shows 80% time in repeated query execution
- LRU cache standard pattern for this scenario

**Confidence:** High

**Outcome:** Success  
Quick fix applied, p95 latency reduced to 120ms, AC5 passed on re-test. Fix time: 28 minutes (within estimate).
```

**Example 2: Planner Alternative Selection (P003)**

```markdown
## Decision: Dashboard Implementation Approach (P003)

**Decision ID:** DEC-p003-001  
**Timestamp:** 2025-10-02T14:15:00Z  
**Agent:** Planner (agent-planner-A)  
**Task:** P003  
**Type:** alternative_selection

**Decision:** Bash script with jq JSON processing

**Rationale:**  
Bash + jq aligns with existing script pattern (P002 log rotation). Provides real-time status without requiring daemon infrastructure. Simpler than Python for file parsing tasks.

**Alternatives Considered:**
1. **Python script**
   - Pros: Better JSON handling, easier testing, type safety
   - Cons: Requires venv, adds dependency complexity
   - Rejected: Overkill for simple file parsing

2. **Python daemon (integrate with P001)**
   - Pros: Continuous monitoring, push notifications
   - Cons: P001 incomplete, adds scope, blocks P003 on P001
   - Rejected: P003 needs delivery before P001 complete

3. **Web dashboard (Flask/FastAPI)**
   - Pros: Rich UI, real-time updates
   - Cons: Significant complexity, not sprint-scoped
   - Rejected: Over-engineering for internal tool

**Evidence:**
- P002: Bash log rotation successful (400 lines, all gates passed)
- SPRINT_QUEUE.json: JSON structure well-suited for jq
- Project patterns: 5 existing bash scripts, consistent style

**Confidence:** High

**Outcome:** Success  
P003 completed in 90% of estimated time (parallel subtasks). Dashboard generates accurate SPRINT_STATUS.json, bash + jq combination effective. Confirmed: appropriate choice for this use case.
```

**Storage:**
- Primary: AGENT_LOG.md (human-readable markdown)
- Optional: `.decisions/<task_id>.jsonl` (machine-readable JSON for pattern analysis)

**Benefits:**
- **Transparency:** All decisions documented with rationale
- **Learning:** Pattern analysis identifies high-confidence decisions vs low-confidence
- **Calibration:** Compare confidence levels to outcomes, improve decision quality
- **Auditability:** Retrospectives can review decision quality

**Implementation Status:** Defined in Sprint 2 (P005-B02), implement in Sprint 3

---

### Protocol 3: Status Reporting Standard

**Purpose:** Consistent status updates for metrics aggregation, progress visibility, and anomaly detection.

**When to Use:**
- Long-running tasks (>60 minutes): Progress update every 30 minutes
- Completion report: Always (all agents)
- Blocked status: Immediately when blocker encountered
- Adaptation loop: Before and after adaptation

**Status Report Template:**

```markdown
## Status Update: <Task ID> <Action>

**Timestamp:** <ISO8601>  
**Agent:** <agent_role> (<agent_instance>)  
**Task:** <task_id>  
**Action:** <current_action>  
**Status:** in_progress | complete | blocked | needs_adapt

**Duration:**
- Elapsed: <time_spent>
- Remaining: <estimated_remaining> (estimated)

**Progress:**
- ✅ <completed_step_1>
- 🔄 <in_progress_step>
- ⏳ <pending_step_1>
- ⏳ <pending_step_2>

**Metrics:**
- <metric_1>: <value>
- <metric_2>: <value>

**Blockers:** <None | blocker description>

**Next Steps:** <planned actions>
```

**Status Values:**

| Status | Meaning | Required Fields | Next Agent |
|--------|---------|-----------------|------------|
| **in_progress** | Task actively being worked | progress_pct, duration_elapsed, duration_remaining | Same agent (update) |
| **complete** | Task finished successfully | outcome (success), final_metrics | Next agent in flow |
| **blocked** | Cannot proceed, waiting on external | blocker description, expected_resolution_time | Negotiator (escalation) |
| **needs_adapt** | Tests failed, adaptation required | failure_summary, gate_failures | Refiner |

**Metrics by Agent:**

| Agent | Key Metrics | Example Values |
|-------|------------|----------------|
| **Builder** | lines_written, files_created, gates_passed | 1500 lines, 3 files, 4/5 gates pass |
| **Tester** | acs_tested, acs_passed, coverage | 8 ACs tested, 7 passed, 88% coverage |
| **Integrator** | commits_merged, prs_closed, conflicts | 2 commits, 1 PR, 0 conflicts |
| **Refiner** | adaptations_analyzed, fix_time_estimated | 1 adaptation, 30 min estimate |

**Example: Builder Progress Update (Long-Running Task)**

```markdown
## Status Update: P005-B01 Implementation

**Timestamp:** 2025-10-04T10:15:00Z  
**Agent:** Builder (agent-builder-A)  
**Task:** P005-B01  
**Action:** Implementation  
**Status:** in_progress (60% complete)

**Duration:**
- Elapsed: 50 minutes
- Remaining: ~35 minutes (estimated)

**Progress:**
- ✅ AGENT_ROLES_MATRIX.md complete (810 lines, 11 agents)
- 🔄 AGENT_INTERACTION_GUIDE.md in progress (50% done, 4 workflow patterns)
- ⏳ AGENT_GAP_ANALYSIS.md pending (evidence section)

**Metrics:**
- Files created: 2/3
- Lines written: 1,500
- Quality gates passed: 2/5 (markdown, cross-ref pass; completeness, accuracy, integration pending)

**Blockers:** None

**Next Steps:** Complete AGENT_INTERACTION_GUIDE.md (20 min), then start AGENT_GAP_ANALYSIS.md evidence section (15 min).
```

**Example: Tester Completion Report**

```markdown
## Status Update: P005-T01 Validation Complete

**Timestamp:** 2025-10-04T12:00:00Z  
**Agent:** Tester (agent-tester-A)  
**Task:** P005-T01  
**Action:** Validation  
**Status:** complete (success)

**Duration:**
- Elapsed: 45 minutes
- Estimated: 45 minutes (100% accurate)

**Progress:**
- ✅ AC1: Agent capability matrix complete (11 agents, 7 attributes each)
- ✅ AC2: Agent interaction guide (4 workflow patterns, 15+ examples)
- ✅ AC3: Sprint 1/2 evidence analysis (116 citations, 7 lessons)
- ✅ AC4: Descriptions accurate (verified against prompts)
- ✅ AC5: Cross-references valid (20+ links checked)

**Metrics:**
- ACs tested: 5/5
- ACs passed: 5/5 (100%)
- Validation time: 9 min/AC average

**Blockers:** None

**Next Steps:** Handoff to Integrator for PR creation and merge.
```

**Storage:**
- Primary: AGENT_LOG.md (all status updates)
- Optional: `.status/<task_id>.jsonl` (machine-readable for monitoring)

**Benefits:**
- **Visibility:** Progress updates during long tasks (Builder 90-minute tasks)
- **Early Detection:** Monitor agent can detect delays (elapsed > 150% estimated)
- **Metrics Aggregation:** Average duration per agent, gate pass rates, adaptation rate
- **Retrospectives:** Analyze which agents consistently over/under-estimate

**Implementation Status:** Defined in Sprint 2 (P005-B02), gradual adoption Sprint 3+

---

### Protocol 4: Conflict Resolution Process

**Purpose:** Define 5-step escalation process for agent disagreements, preventing deadlocks and ensuring evidence-based resolution.

**When to Use:**
- Builder disagrees with Tester rejection
- Refiner chooses rollback, Builder wants to retry
- Negotiator assigns task, agent believes wrong agent type
- Planner and Refiner disagree on adaptation approach

**5-Step Conflict Resolution Protocol:**

**Step 1: Direct Communication (15 minutes)**
- Agents attempt to resolve disagreement directly
- Log discussion in AGENT_LOG.md (message exchange using Protocol 1 format)
- Both agents present their positions
- Look for misunderstanding or missing information

**Exit Criteria:**
- Agreement reached → Conflict resolved
- No agreement → Escalate to Step 2

---

**Step 2: Evidence Review (15 minutes)**
- Both agents gather and present evidence
- Review authoritative sources:
  - TEST_PLAN.md (acceptance criteria)
  - AGENT_PLAN.md (design specifications)
  - OBJECTIVE.md (project goals)
  - Agent prompts (role boundaries)
- Check for interpretation differences or missing context

**Exit Criteria:**
- Evidence clearly supports one position → Conflict resolved
- Evidence ambiguous or contradictory → Escalate to Step 3

---

**Step 3: Third-Party Review (30 minutes)**
- Escalate to relevant agent based on conflict type:

| Conflict Type | Third-Party Reviewer | Rationale |
|---------------|---------------------|-----------|
| **Planning conflicts** | Sprint Planner | Ensures sprint goal alignment |
| **Technical conflicts** | Planner (or Refiner if adaptation-related) | Design expertise |
| **Process conflicts** | Negotiator | OODATCAA protocol authority |
| **Acceptance criteria disputes** | Tester | Quality assurance expertise |

- Third party reviews evidence from both sides
- Provides non-binding recommendation
- Documents analysis in AGENT_LOG.md

**Exit Criteria:**
- Both agents accept recommendation → Conflict resolved
- Recommendation rejected by one/both agents → Escalate to Step 4

---

**Step 4: Negotiator Decision (30 minutes)**
- Escalate to Negotiator (if not already reviewer)
- Negotiator makes **binding decision** based on:
  1. **Objective alignment:** Which position better advances OBJECTIVE.md?
  2. **Sprint goal alignment:** Which completes sprint exit criteria faster?
  3. **Evidence quality:** Which position has stronger supporting data?
  4. **System health:** What's best for overall sprint progress?
- Decision logged in `.oodatcaa/work/SPRINT_DISCUSS.md` with full rationale
- Includes decision template from Protocol 2 (alternatives, evidence, confidence)

**Exit Criteria:**
- Negotiator makes decision → Conflict resolved (binding)
- Negotiator cannot decide (rare) → Escalate to Step 5

---

**Step 5: Human Escalation (Variable)**
- **RARE:** Only if Negotiator cannot make decision (e.g., requires policy change, outside OODATCAA scope)
- Create `.oodatcaa/work/ESCALATION.md` with:
  - Conflict description
  - Agent positions (both sides)
  - Evidence summary
  - Third-party review outcome
  - Negotiator analysis
  - Negotiator recommendation (but unable to decide)
- Human reviews and makes final decision
- Decision recorded in ESCALATION.md and SPRINT_LOG.md

**Exit Criteria:**
- Human makes decision → Conflict resolved (final)

---

**Conflict Logging Format:**

```markdown
## Conflict Resolution: <Task ID>

**Conflict ID:** CONFLICT-<UUID>  
**Timestamp:** <ISO8601>  
**Participants:** <Agent 1> vs <Agent 2>  
**Task:** <task_id>  
**Issue:** <brief description of disagreement>

### Step 1: Direct Communication
- **<Agent 1> Position:** <position summary>
- **<Agent 2> Position:** <position summary>
- **Outcome:** <Resolved | Escalate to Step 2>

[If escalated:]

### Step 2: Evidence Review
- **Authoritative Source(s):** <TEST_PLAN.md AC3, OBJECTIVE.md, etc.>
- **Evidence:** <what evidence says>
- **Outcome:** <Resolved | Escalate to Step 3>

[If escalated:]

### Step 3: Third-Party Review
- **Reviewer:** <agent_role>
- **Analysis:** <reviewer's assessment>
- **Recommendation:** <non-binding suggestion>
- **Outcome:** <Resolved | Escalate to Step 4>

[If escalated:]

### Step 4: Negotiator Decision
- **Decision:** <chosen position or compromise>
- **Rationale:** <why this decision?>
- **Alternatives Considered:** <list>
- **Evidence:** <supporting data>
- **Confidence:** <high/medium/low>
- **Outcome:** Resolved (binding)

[If escalated:]

### Step 5: Human Escalation
- **Escalation Reason:** <why Negotiator couldn't decide>
- **Human Decision:** <final decision>
- **Rationale:** <explanation>
- **Outcome:** Resolved (final)

---

### Resolution Summary
- **Decision:** <final outcome>
- **Action:** <what happens next>
- **Status:** Resolved at Step <N>
- **Time to Resolution:** <duration>
```

**Example: Builder vs Tester Conflict (Hypothetical)**

```markdown
## Conflict Resolution: P005-B01

**Conflict ID:** CONFLICT-p005-001  
**Timestamp:** 2025-10-04T11:00:00Z  
**Participants:** Builder (agent-builder-A) vs Tester (agent-tester-A)  
**Task:** P005-B01  
**Issue:** Disagreement on AC2 acceptance (Tester rejected, Builder disputes)

### Step 1: Direct Communication
- **Builder Position:** AC2 requires "4+ workflow patterns". Implemented 4 patterns (Primary Dev, Adaptation, Sprint Lifecycle, Completion). Criteria met.
- **Tester Position:** AC2 requires "4+ workflow patterns with examples". Only 3 patterns have examples. Completion pattern missing examples. Criteria NOT met.
- **Outcome:** No resolution, escalate to Step 2

### Step 2: Evidence Review
- **Authoritative Source:** TEST_PLAN.md AC2
- **Evidence:** "Agent interaction guide with 4+ workflow patterns **with examples** from Sprint 1/2"
- **Analysis:** "with examples" is part of AC2 requirement. Tester interpretation correct.
- **Outcome:** Builder acknowledges, will add examples to Completion pattern

### Resolution Summary
- **Decision:** Tester rejection valid
- **Action:** Builder adds examples to Completion pattern (15 minutes)
- **Status:** Resolved at Step 2 (no escalation needed)
- **Time to Resolution:** 20 minutes
```

**Conflict Statistics (Sprint 1/2):**

| Sprint | Conflicts | Step 1 Resolution | Step 2 Resolution | Step 3 Resolution | Step 4+ |
|--------|-----------|------------------|-------------------|-------------------|---------|
| Sprint 1 | 0 | 0 | 0 | 0 | 0 |
| Sprint 2 | 0 | 0 | 0 | 0 | 0 |
| **Total** | **0** | **0** | **0** | **0** | **0** |

**Pattern:** No conflicts in first 2 sprints. Protocol defined preventatively for future scalability.

**Benefits:**
- **Clear escalation path:** Prevents deadlocks, always moves forward
- **Evidence-based:** Not arbitrary, decisions grounded in authoritative sources
- **Negotiator authority:** System-level decision-making when needed
- **Human safety valve:** Rare but available for policy/scope issues
- **Audit trail:** Full conflict history logged

**Implementation Status:** Defined in Sprint 2 (P005-B02), ready to use if conflicts arise

---

## Communication Protocol Summary

| Protocol | Purpose | Priority | Implementation Status | Adoption Timeline |
|----------|---------|----------|----------------------|-------------------|
| **Protocol 1: Structured Message Format** | Parsing, tracing, automation | High | Defined (P005-B02) | Sprint 3 |
| **Protocol 2: Decision Transparency** | Auditability, learning | High | Defined (P005-B02) | Sprint 3 |
| **Protocol 3: Status Reporting** | Metrics, monitoring | Medium | Defined (P005-B02) | Sprint 3+ (gradual) |
| **Protocol 4: Conflict Resolution** | Prevent deadlocks | High | Defined (P005-B02) | Ready (use as needed) |

**Total Implementation Effort:** ~3.5 hours (all protocols, Sprint 3)

**Phasing Strategy:**
- **Sprint 2 (Current):** Define all protocols (documentation complete ✅)
- **Sprint 3:** Implement Protocols 1 & 2 (high priority, structured messages + decision templates)
- **Sprint 4:** Implement Protocol 3 (medium priority, status reporting standardization)
- **Ongoing:** Use Protocol 4 as needed (already ready, no implementation required)

**Detailed Schema Documentation:**  
For full JSON schemas and additional examples, see [`.oodatcaa/work/AGENT_GAP_ANALYSIS.md`](.oodatcaa/work/AGENT_GAP_ANALYSIS.md) Communication Protocol Design section.

---

## Cross-References

**Agent Prompts:** [`.oodatcaa/prompts/`](.oodatcaa/prompts/)  
**Agent Roles Matrix:** [`.oodatcaa/AGENT_ROLES_MATRIX.md`](.oodatcaa/AGENT_ROLES_MATRIX.md)  
**Agent Gap Analysis:** [`.oodatcaa/work/AGENT_GAP_ANALYSIS.md`](.oodatcaa/work/AGENT_GAP_ANALYSIS.md)  
**OODATCAA Loop Guide:** [`.oodatcaa/OODATCAA_LOOP_GUIDE.md`](.oodatcaa/OODATCAA_LOOP_GUIDE.md)

**Sprint Evidence:**
- Sprint 1 Reports: `.oodatcaa/work/reports/W001/` through `.oodatcaa/work/reports/W008/`
- Sprint 2 Reports: `.oodatcaa/work/reports/P001/` through `.oodatcaa/work/reports/P007/`
- Sprint Logs: `.oodatcaa/work/SPRINT_LOG.md`
- Agent Logs: `.oodatcaa/work/AGENT_LOG.md`

---

**Guide Version:** 2.0 (Communication Protocols Added)  
**Last Updated:** 2025-10-04  
**Next Review:** End of Sprint 2  
**Maintainer:** Builder (P005-B02)

