# AGENT_PLAN: P003 - Enhanced Sprint Management System

**Plan Version:** 1.0  
**Task ID:** P003  
**Objective:** SPRINT-2025-002 (OODATCAA Process Improvement)  
**Sprint:** 2  
**Complexity:** Medium  
**Planner:** agent-planner-A  
**Created:** 2025-10-03T15:30:00+02:00

---

## Traceability

**Objective Link:** `.oodatcaa/objectives/SPRINT_2_OBJECTIVE.md` → Sprint Management Improvements  
**Epic:** Sprint 2 - OODATCAA Process Improvement  
**Success Criteria Addressed:**
- Sprint ID System: Clear, unambiguous sprint identifiers (Format: SPRINT-YYYY-NNN)
- Sprint Dashboard: Visual progress tracking (`make sprint-status`)
- Sprint Transitions: Automated sprint lifecycle (`make sprint-complete`, `make sprint-new`)

---

## Problem Statement

**Current State:**
- Sprint 1 completed successfully but revealed sprint management gaps
- Sprint transitions are manual with unclear numbering
- No automated way to visualize sprint progress
- Sprint completion requires manual log archiving and state updates
- Sprint initiation is ad-hoc without standardized process

**Evidence:**
- SPRINT_QUEUE.json shows sprint 2 status but no standardized tracking
- SPRINT_LOG.md has sprint completion markers but no automated lifecycle
- No sprint dashboard or status visualization exists
- Sprint transitions performed manually by agents (error-prone)

**Impact:**
- Increased cognitive load for Negotiator agent
- Risk of incomplete sprint transitions
- Difficulty tracking sprint health and progress
- Inconsistent sprint metadata and documentation

**Goal:**
Build a comprehensive sprint management system that automates transitions, provides visibility, and maintains consistent sprint metadata across the project lifecycle.

---

## Constraints & Interfaces

### Technical Constraints
- **Shell Scripts:** Bash 4+ for maximum compatibility
- **JSON Parsing:** Use `jq` for reliable SPRINT_QUEUE.json manipulation
- **Makefile Integration:** Commands must integrate with existing Makefile targets
- **Cross-Platform:** Scripts should work on Linux/macOS (current: Linux 6.14.0)
- **Non-Interactive:** All operations must be automatable (no user prompts)

### Interfaces
**Input:**
- `.oodatcaa/work/SPRINT_QUEUE.json` - Current sprint state
- `.oodatcaa/work/SPRINT_LOG.md` - Sprint history
- `.oodatcaa/work/SPRINT_PLAN.md` - Sprint assignments
- `.oodatcaa/objectives/SPRINT_GOAL.md` - Sprint goals
- `.oodatcaa/objectives/SPRINT_2_OBJECTIVE.md` - Current objective

**Output:**
- `scripts/sprint-dashboard.sh` - Status visualization script
- `scripts/sprint-complete.sh` - Sprint finalization script  
- `scripts/sprint-new.sh` - Sprint initialization script
- `Makefile` - Updated with new targets
- `.oodatcaa/work/SPRINT_STATUS.json` - Real-time sprint metrics

### Existing Infrastructure
- Log rotation system (P002-B01) - Sprint-aware archiving
- OODATCAA documentation (P004) - Process documentation
- Makefile - Existing quality gates and commands
- SPRINT_QUEUE.json - Task tracking system

### Risks
1. **JSON Corruption:** Improper jq usage could corrupt SPRINT_QUEUE.json
   - Mitigation: Atomic writes with temp files, validation before commit
2. **Incomplete Transitions:** Partial sprint completion could leave inconsistent state
   - Mitigation: Transaction-like behavior, rollback on errors
3. **Breaking Changes:** New sprint ID format might break existing scripts
   - Mitigation: Backward compatibility checks, migration path
4. **Concurrency:** Multiple agents might trigger transitions simultaneously
   - Mitigation: Lock files during transitions

---

## Definition of Done (DoD)

### Functional Requirements
1. **Sprint ID System:**
   - All sprints identified with SPRINT-YYYY-NNN format
   - Sprint metadata consistent across all OODATCAA files
   - Backward compatible with existing sprint references (sprint 1, sprint 2)

2. **Sprint Dashboard:**
   - `make sprint-status` command functional
   - Displays: Sprint ID, progress %, task counts, exit criteria status
   - Color-coded output for quick health assessment
   - Shows WIP limits and utilization

3. **Sprint Transitions:**
   - `make sprint-complete` finalizes current sprint:
     - Archives all logs automatically
     - Updates sprint status to "completed"
     - Generates sprint retrospective template
     - Tags sprint completion in git (e.g., sprint-2-complete)
   - `make sprint-new` initializes next sprint:
     - Creates new sprint directories
     - Resets active logs
     - Updates sprint number in SPRINT_QUEUE.json
     - Creates sprint planning templates

### Non-Functional Requirements
- **Performance:** All commands complete in < 5 seconds
- **Reliability:** No data loss during transitions (atomic operations)
- **Usability:** Clear, informative output with progress indicators
- **Maintainability:** Well-documented scripts with error handling

### Acceptance Criteria (Detailed in TEST_PLAN.md)
- AC1: Sprint ID system functional
- AC2: `make sprint-status` displays accurate information
- AC3: `make sprint-complete` finalizes sprint correctly
- AC4: `make sprint-new` initializes next sprint
- AC5: All quality gates pass
- AC6: Documentation complete
- AC7: Zero regressions in existing functionality
- AC8: Sprint transitions are atomic (no partial states)
- AC9: Sprint metadata consistent across all files
- AC10: Performance targets met (< 5s per command)

---

## Alternatives Considered

### Alternative 1: Python-Based Sprint Management
**Approach:**
- Implement sprint management in Python using existing project structure
- Create `src/sprint_management/` module with OOP design
- Use Python's JSON library for manipulation

**Pros:**
- Type safety with mypy
- Better error handling and testing
- Integration with existing Python tooling
- More sophisticated data validation

**Cons:**
- Adds complexity to project structure
- Requires additional dependencies
- Heavier weight for simple shell operations
- Less transparent for debugging

**Verdict:** ❌ **Rejected** - Overkill for straightforward file manipulation. Shell scripts are more appropriate for DevOps automation tasks.

---

### Alternative 2: Makefile-Only Implementation
**Approach:**
- Implement all logic directly in Makefile targets
- No separate shell scripts, everything inline
- Use Make's variable system for state management

**Pros:**
- Single source of truth (Makefile)
- No separate script files to maintain
- Familiar Make syntax

**Cons:**
- Make syntax is arcane for complex logic
- Poor error handling capabilities
- Difficult to test in isolation
- Hard to read and maintain for complex operations
- No real transaction support

**Verdict:** ❌ **Rejected** - Makefile is great for orchestration but poor for complex business logic. Separate scripts are more maintainable.

---

### Alternative 3: Hybrid Bash Scripts + Make Orchestration (CHOSEN)
**Approach:**
- Implement core logic in well-structured bash scripts
- Use Makefile as thin orchestration layer
- Scripts are independently testable and reusable
- Follow existing pattern from P002 (log rotation)

**Pros:**
- ✅ Separation of concerns (orchestration vs logic)
- ✅ Scripts can be called directly or via Make
- ✅ Consistent with existing P002 pattern
- ✅ Easy to test and debug
- ✅ Good error handling in bash
- ✅ Transparent execution (scripts show progress)

**Cons:**
- Requires bash 4+ (acceptable given deployment environment)
- More files to maintain (mitigated by good structure)

**Verdict:** ✅ **CHOSEN** - Best balance of simplicity, maintainability, and consistency with existing codebase patterns.

---

## Implementation Plan

### Step-by-Step Breakdown

#### **Step 1: Sprint Dashboard Script (60 min)**
**Goal:** Create `scripts/sprint-dashboard.sh` - Visualize current sprint status

**Tasks:**
1. Parse SPRINT_QUEUE.json for current sprint state
2. Calculate progress metrics:
   - Total tasks, completed, in-progress, blocked
   - Sprint completion percentage
   - Exit criteria progress
3. Parse SPRINT_GOAL.md for sprint objectives
4. Format output with color coding:
   - Green: ✅ Complete
   - Yellow: 🔄 In Progress  
   - Red: ❌ Blocked/Failed
5. Display WIP limits and utilization
6. Show time estimates vs actuals (if available)

**Output Example:**
```
=======================================
  Sprint Status: SPRINT-2025-002
=======================================

Sprint: OODATCAA Process Improvement
Status: in_progress
Progress: 18% complete (4 of 22 tasks)

Tasks:
  ✅ Done:       2 tasks
  🔄 In Progress: 1 task
  ⏳ Ready:      2 tasks
  🚫 Blocked:    7 tasks
  📋 Needs Plan: 4 tasks

WIP Utilization:
  Planner:    0/1 (0%)
  Builder:    1/3 (33%)
  Tester:     0/2 (0%)
  Refiner:    0/1 (0%)
  Integrator: 0/1 (0%)

Exit Criteria:
  ✅ Background Agent System Operational
  🔄 Automatic Log Rotation Working (50%)
  ❌ Sprint Management Enhanced
  🔄 OODATCAA Loop Documented (75%)
  ❌ Agent Role Completeness
  ❌ Process Documentation Complete
  ❌ Quality Gates Maintained

Recent Activity:
  - P002-B01 INTEGRATED (Automatic Log Rotation)
  - P004-B01 COMPLETE (OODATCAA Docs Foundation)
  - P002-B02 in progress (Testing + Docs)

Next Actions:
  - P004-B03 ready for integrator
  - P003 needs planning
=======================================
```

**Exit Gate:** Script runs without errors, displays accurate information

---

#### **Step 2: Sprint Status JSON Generator (45 min)**
**Goal:** Create `.oodatcaa/work/SPRINT_STATUS.json` - Machine-readable sprint metrics

**Tasks:**
1. Extract all relevant metrics from SPRINT_QUEUE.json
2. Calculate derived metrics:
   - Progress percentage
   - Velocity (tasks/day)
   - Estimated completion date
   - Blocker analysis
3. Generate JSON with consistent schema
4. Include timestamp for staleness detection
5. Document JSON schema in comments

**Output Schema:**
```json
{
  "sprint_id": "SPRINT-2025-002",
  "sprint_number": 2,
  "status": "in_progress",
  "started": "2025-10-03",
  "target_completion": "2025-10-10",
  "progress": {
    "total_tasks": 22,
    "completed": 2,
    "in_progress": 1,
    "ready": 2,
    "blocked": 7,
    "needs_plan": 4,
    "percentage": 18
  },
  "wip": {
    "planner": {"current": 0, "limit": 1},
    "builder": {"current": 1, "limit": 3},
    "tester": {"current": 0, "limit": 2},
    "refiner": {"current": 0, "limit": 1},
    "integrator": {"current": 0, "limit": 1}
  },
  "exit_criteria": [
    {"name": "Background Agent System", "status": "complete", "progress": 100},
    {"name": "Automatic Log Rotation", "status": "in_progress", "progress": 50}
  ],
  "velocity": {
    "tasks_per_day": 1.5,
    "estimated_days_remaining": 10
  },
  "generated_at": "2025-10-03T15:30:00+02:00"
}
```

**Exit Gate:** JSON validates, contains all required fields, integrates with dashboard script

---

#### **Step 3: Sprint Completion Script (90 min)**
**Goal:** Create `scripts/sprint-complete.sh` - Automate sprint finalization

**Tasks:**
1. Validate sprint can be completed (check exit criteria)
2. **Archive Phase:**
   - Call `scripts/rotate-logs.sh --force` to archive all logs
   - Copy SPRINT_QUEUE.json to archive as SPRINT_N_FINAL.json
   - Copy SPRINT_PLAN.md to archive as SPRINT_N_FINAL.md
3. **Status Update Phase:**
   - Update SPRINT_QUEUE.json status to "completed"
   - Update SPRINT_GOAL.md with completion timestamp
   - Add completion entry to SPRINT_LOG.md
4. **Retrospective Generation:**
   - Create `.oodatcaa/work/SPRINT_N_RETROSPECTIVE.md` template
   - Include: achievements, challenges, metrics, lessons learned
   - Auto-fill with data from SPRINT_STATUS.json
5. **Git Tagging:**
   - Create annotated tag: `sprint-N-complete`
   - Include sprint summary in tag annotation
6. **Cleanup:**
   - Remove stale leases (all expired during sprint)
   - Clear temporary locks

**Safety Features:**
- Dry-run mode (`--dry-run`) to preview actions
- Atomic operations (temp files + atomic renames)
- Rollback capability if errors occur
- Validation checks before each phase
- Backup critical files before modification

**Exit Gate:** Sprint transitions to "completed" state, all artifacts archived, git tag created

---

#### **Step 4: Sprint Initialization Script (75 min)**
**Goal:** Create `scripts/sprint-new.sh` - Automate next sprint setup

**Tasks:**
1. **Validation Phase:**
   - Verify current sprint is "completed"
   - Check no active tasks remain
   - Ensure no active agent leases
2. **Sprint Number Increment:**
   - Parse current sprint number
   - Generate new sprint ID (SPRINT-YYYY-NNN)
   - Update all relevant files with new sprint number
3. **Directory Setup:**
   - Create `.oodatcaa/work/archive/sprint_N/` (if not exists)
   - Create `.oodatcaa/work/reports/sprint_N/` (if not exists)
4. **File Initialization:**
   - Reset AGENT_LOG.md with sprint header
   - Reset SPRINT_LOG.md with sprint header
   - Reset SPRINT_PLAN.md with sprint header
   - Create new SPRINT_QUEUE.json with empty tasks array
5. **Sprint Goal Setup:**
   - Update SPRINT_GOAL.md status to "needs_planning"
   - Trigger Sprint Planner (or document manual step)
6. **Documentation:**
   - Update ROTATION_STATS.md with sprint transition marker
   - Create sprint planning checklist

**Safety Features:**
- Pre-flight checks (no active work)
- Confirmation prompt (unless --force flag)
- Preserve sprint 1 artifacts
- Comprehensive logging

**Exit Gate:** New sprint initialized, all files reset, ready for Sprint Planner

---

#### **Step 5: Makefile Integration (30 min)**
**Goal:** Add sprint management commands to Makefile

**Tasks:**
1. Add target: `sprint-status`
   - Calls `scripts/sprint-dashboard.sh`
   - No parameters needed
2. Add target: `sprint-complete`
   - Calls `scripts/sprint-complete.sh`
   - Optional: `FORCE=1` to skip checks
3. Add target: `sprint-new`
   - Calls `scripts/sprint-new.sh`
   - Requires sprint-complete first
4. Add .PHONY declarations for all new targets
5. Update Makefile documentation (comments)

**New Makefile Targets:**
```makefile
# Sprint Management
sprint-status:
	bash scripts/sprint-dashboard.sh

sprint-complete:
	bash scripts/sprint-complete.sh $(if $(FORCE),--force,)

sprint-new:
	bash scripts/sprint-new.sh

.PHONY: sprint-status sprint-complete sprint-new
```

**Exit Gate:** All make targets work, integrate with existing quality gates

---

#### **Step 6: Sprint ID Consistency Update (45 min)**
**Goal:** Ensure sprint ID format consistency across all files

**Tasks:**
1. Update SPRINT_QUEUE.json:
   - Add `sprint_id` field to metadata
   - Ensure consistent with `sprint` field
2. Update SPRINT_GOAL.md:
   - Add sprint ID to each sprint section
3. Update template files:
   - `.oodatcaa/templates/*` (if any)
4. Document sprint ID format in README
5. Create migration guide for sprint 1 → sprint 2 format

**Validation:**
- Grep all OODATCAA files for sprint references
- Ensure consistent format (SPRINT-YYYY-NNN)
- No orphaned sprint 1 references

**Exit Gate:** All files use consistent sprint ID format

---

#### **Step 7: Documentation & Quality Gates (45 min)**
**Goal:** Complete documentation and verify quality

**Tasks:**
1. **Script Documentation:**
   - Add comprehensive header comments to all scripts
   - Document all functions and exit codes
   - Add usage examples
2. **README Updates:**
   - Add "Sprint Management" section
   - Document all new Makefile targets
   - Provide workflow examples
3. **Testing Documentation:**
   - Create test cases for each script
   - Document expected inputs/outputs
   - Add troubleshooting guide
4. **Quality Gates:**
   - Run `make gates` (black, ruff, mypy)
   - Run `make test` (existing tests)
   - Run `make audit` (security scan)
   - Verify no regressions

**Documentation Structure:**
```
docs/
  SPRINT_MANAGEMENT.md
    - Overview
    - Commands Reference
    - Workflow Examples
    - Troubleshooting
```

**Exit Gate:** All quality gates pass, documentation complete

---

## Task Breakdown for SPRINT_QUEUE.json

### P003-B01: Steps 1-3 - Dashboard + Status JSON + Completion Script
**Complexity:** Large  
**Estimated Time:** 195 minutes (~3.25 hours)  
**Steps:** 1, 2, 3  
**Dependencies:** None  
**Deliverables:**
- `scripts/sprint-dashboard.sh` (executable, tested)
- `.oodatcaa/work/SPRINT_STATUS.json` (schema documented)
- `scripts/sprint-complete.sh` (executable, tested with --dry-run)

**Branch:** `feat/P003-step-01-sprint-dashboard`

---

### P003-B02: Steps 4-6 - Initialization Script + Makefile + Sprint ID Consistency
**Complexity:** Medium  
**Estimated Time:** 150 minutes (~2.5 hours)  
**Steps:** 4, 5, 6  
**Dependencies:** P003-B01  
**Deliverables:**
- `scripts/sprint-new.sh` (executable, tested)
- Makefile updated with new targets
- Sprint ID consistency across all files

**Branch:** `feat/P003-step-02-sprint-init`

---

### P003-B03: Step 7 - Documentation + Quality Gates + Integration
**Complexity:** Small  
**Estimated Time:** 45 minutes  
**Steps:** 7  
**Dependencies:** P003-B02  
**Deliverables:**
- `docs/SPRINT_MANAGEMENT.md` (complete)
- README updated
- All quality gates pass
- Branch ready for integration

**Branch:** `feat/P003-step-03-docs-quality`

---

### P003-T01: Testing - Verify All 10 ACs
**Complexity:** Medium  
**Estimated Time:** 45 minutes  
**Dependencies:** P003-B03  
**Deliverables:**
- All 10 acceptance criteria verified
- Sprint transition tested end-to-end
- No regressions confirmed
- Performance validated (< 5s per command)

---

## Exit Criteria Summary

This task is complete when:
1. ✅ Sprint ID system operational (SPRINT-YYYY-NNN format)
2. ✅ `make sprint-status` displays accurate sprint information
3. ✅ `make sprint-complete` finalizes sprint with full archival
4. ✅ `make sprint-new` initializes next sprint correctly
5. ✅ All sprint transitions are atomic (no partial states)
6. ✅ Sprint metadata consistent across all OODATCAA files
7. ✅ Documentation complete (README + SPRINT_MANAGEMENT.md)
8. ✅ All quality gates pass (black, ruff, mypy, pytest)
9. ✅ Zero regressions in existing functionality
10. ✅ Performance targets met (< 5s per command)

**Unblocks:** P006 (Process Documentation), P007 (Integration Testing)

---

## Notes

- **Pattern Consistency:** Follows P002 (log rotation) bash script patterns
- **Backward Compatibility:** Sprint 1 references preserved, new system additive
- **Safety First:** All destructive operations have dry-run mode and confirmation
- **Agent Coordination:** Scripts designed to be called by Negotiator or manually
- **Future Enhancement:** Could add sprint analytics, burndown charts, velocity tracking

---

**Plan Status:** ✅ Complete  
**Ready for:** Builder (P003-B01)  
**Estimated Total Time:** 390 minutes (~6.5 hours across 3 builder tasks)
