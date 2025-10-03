#!/usr/bin/env bash
#
# sprint-new.sh - Sprint Initialization Script
#
# Initializes a new sprint: increments sprint number, creates directories,
# resets logs, and prepares for Sprint Planner.
#
# Usage:
#   bash scripts/sprint-new.sh [--force]
#
# Author: agent-builder-A
# Task: P003-B02 Step 4
# Sprint: SPRINT-2025-002

set -euo pipefail

QUEUE_FILE=".oodatcaa/work/SPRINT_QUEUE.json"
AGENT_LOG=".oodatcaa/work/AGENT_LOG.md"
SPRINT_LOG=".oodatcaa/work/SPRINT_LOG.md"
SPRINT_PLAN=".oodatcaa/work/SPRINT_PLAN.md"
SPRINT_GOAL=".oodatcaa/objectives/SPRINT_GOAL.md"
ARCHIVE_DIR=".oodatcaa/work/archive"
REPORTS_DIR=".oodatcaa/work/reports"

FORCE=false

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --force) FORCE=true; shift ;;
        --help|-h)
            cat <<EOF
Usage: bash scripts/sprint-new.sh [--force]

Initialize a new sprint with fresh logs and directories.

Options:
  --force    Skip validation and confirmation prompts
  --help     Display this help

Requirements:
  - Current sprint must be "completed"
  - No active tasks
  - No active leases

Exit Codes:
  0 - Success
  1 - Current sprint not completed
  2 - Active work detected
  3 - Required files not found
EOF
            exit 0
            ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

echo "=== Sprint Initialization ==="
echo ""

# Validate prerequisites
if [[ ! -f "$QUEUE_FILE" ]]; then
    echo "Error: SPRINT_QUEUE.json not found" >&2
    exit 3
fi

command -v jq &> /dev/null || { echo "Error: jq required" >&2; exit 3; }

# Check current sprint status
CURRENT_STATUS=$(jq -r '.status' "$QUEUE_FILE")
CURRENT_SPRINT=$(jq -r '.sprint' "$QUEUE_FILE")

if [[ "$CURRENT_STATUS" != "completed" && "$FORCE" != "true" ]]; then
    echo "❌ Current sprint (Sprint $CURRENT_SPRINT) is not completed" >&2
    echo "Status: $CURRENT_STATUS" >&2
    echo "" >&2
    echo "Use --force to initialize anyway" >&2
    exit 1
fi

# Check for active tasks
ACTIVE_TASKS=$(jq '[.tasks[] | select(.status | IN("in_progress", "awaiting_test", "testing", "adapting", "integrating"))] | length' "$QUEUE_FILE")

if [[ "$ACTIVE_TASKS" -gt 0 && "$FORCE" != "true" ]]; then
    echo "❌ Active tasks detected: $ACTIVE_TASKS task(s)" >&2
    echo "" >&2
    jq -r '.tasks[] | select(.status | IN("in_progress", "awaiting_test", "testing", "adapting", "integrating")) | "  - \(.id): \(.status)"' "$QUEUE_FILE" >&2
    echo "" >&2
    echo "Complete all tasks before starting new sprint" >&2
    exit 2
fi

# Check for active leases
if [[ -d ".leases" ]]; then
    ACTIVE_LEASES=$(find .leases -name "*.json" -type f 2>/dev/null | wc -l)
    if [[ "$ACTIVE_LEASES" -gt 0 && "$FORCE" != "true" ]]; then
        echo "⚠️  Warning: $ACTIVE_LEASES active lease(s) detected" >&2
        echo "These will be removed during initialization" >&2
    fi
fi

echo "✅ Validation passed"
echo ""

# Calculate new sprint number
NEW_SPRINT=$((CURRENT_SPRINT + 1))
YEAR=$(date +%Y)
SPRINT_ID=$(printf "SPRINT-%s-%03d" "$YEAR" "$NEW_SPRINT")

echo "Sprint Transition:"
echo "  Current: Sprint $CURRENT_SPRINT"
echo "  New:     Sprint $NEW_SPRINT ($SPRINT_ID)"
echo ""

# Confirmation (unless --force)
if [[ "$FORCE" != "true" ]]; then
    read -p "Initialize Sprint $NEW_SPRINT? (y/N) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted" >&2
        exit 0
    fi
fi

# Create directories
echo "=== Creating Directories ==="
mkdir -p "$ARCHIVE_DIR/sprint_$NEW_SPRINT"
mkdir -p "$REPORTS_DIR/sprint_$NEW_SPRINT"
echo "✅ Directories created"
echo ""

# Initialize SPRINT_QUEUE.json
echo "=== Initializing SPRINT_QUEUE.json ==="
TEMP="${QUEUE_FILE}.tmp"

cat > "$TEMP" <<EOF
{
  "sprint": $NEW_SPRINT,
  "status": "planning",
  "sprint_id": "$SPRINT_ID",
  "wip_limits": {
    "planner": 1,
    "builder": 3,
    "tester": 2,
    "refiner": 1,
    "integrator": 1
  },
  "tasks": [],
  "metadata": {
    "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "updated": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
    "sprint_id": "$SPRINT_ID",
    "sprint_goal": "To be defined by Sprint Planner",
    "sprint_status": "planning",
    "total_tasks": 0,
    "story_tasks": 0,
    "builder_tasks": 0,
    "tester_tasks": 0,
    "completed_tasks": 0,
    "ready_tasks": 0,
    "blocked_tasks": 0,
    "in_progress_tasks": 0,
    "planning_tasks": 0,
    "planning_complete_tasks": 0,
    "needs_plan_tasks": 0,
    "awaiting_test_tasks": 0,
    "done_tasks": 0,
    "sprint_${NEW_SPRINT}_start": "$(date +%Y-%m-%d)",
    "previous_sprint": {
      "sprint": $CURRENT_SPRINT,
      "status": "$CURRENT_STATUS",
      "completion_date": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    }
  }
}
EOF

jq empty "$TEMP" 2>/dev/null && mv -f "$TEMP" "$QUEUE_FILE" || { rm -f "$TEMP"; echo "Error: Invalid JSON" >&2; exit 4; }
echo "✅ SPRINT_QUEUE.json initialized"
echo ""

# Reset logs
echo "=== Resetting Logs ==="

cat > "$AGENT_LOG" <<EOF
# OODATCAA Agent Log

**Sprint:** $NEW_SPRINT  
**Sprint ID:** $SPRINT_ID  
**Started:** $(date +%Y-%m-%d)  
**Status:** Planning

This log tracks all agent actions during the sprint lifecycle.

---

## $(date -u +%Y-%m-%dT%H:%M:%SZ) - Sprint $NEW_SPRINT Initialized

**ACTION:** Sprint initialization complete  
**PREVIOUS:** Sprint $CURRENT_SPRINT ($CURRENT_STATUS)  
**NEW:** Sprint $NEW_SPRINT ($SPRINT_ID)

Sprint $NEW_SPRINT ready for planning.

---
EOF
echo "✅ AGENT_LOG.md reset"

cat > "$SPRINT_LOG" <<EOF
# Sprint Log

**Sprint:** $NEW_SPRINT  
**Sprint ID:** $SPRINT_ID  
**Started:** $(date +%Y-%m-%d)  
**Status:** Planning

---

## Sprint $NEW_SPRINT Initialized

**Date:** $(date -u +%Y-%m-%dT%H:%M:%SZ)  
**Previous Sprint:** Sprint $CURRENT_SPRINT  
**Status:** Ready for Sprint Planner

---
EOF
echo "✅ SPRINT_LOG.md reset"

cat > "$SPRINT_PLAN" <<EOF
# Sprint Plan

**Sprint:** $NEW_SPRINT  
**Sprint ID:** $SPRINT_ID  
**Status:** Awaiting Sprint Planner

This file will be populated by the Sprint Planner agent.

---
EOF
echo "✅ SPRINT_PLAN.md reset"
echo ""

# Update SPRINT_GOAL.md
echo "=== Updating SPRINT_GOAL.md ==="
if [[ -f "$SPRINT_GOAL" ]]; then
    cat >> "$SPRINT_GOAL" <<EOF

---

## Sprint $NEW_SPRINT

**Status:** needs_planning  
**Sprint ID:** $SPRINT_ID  
**Started:** $(date +%Y-%m-%d)

Sprint goal to be defined by Sprint Planner.

---
EOF
    echo "✅ SPRINT_GOAL.md updated"
else
    echo "⚠️  SPRINT_GOAL.md not found, skipping"
fi
echo ""

# Cleanup
echo "=== Cleanup ==="
if [[ -d ".leases" ]]; then
    find .leases -name "*.json" -type f -delete 2>/dev/null || true
    echo "✅ Stale leases removed"
fi

if [[ -d ".locks" ]]; then
    rm -f .locks/*.lock 2>/dev/null || true
    echo "✅ Temporary locks cleared"
fi
echo ""

# Summary
echo "======================================="
echo "  Sprint $NEW_SPRINT Initialized"
echo "======================================="
echo ""
echo "Sprint ID: $SPRINT_ID"
echo "Status: Planning"
echo ""
echo "Next steps:"
echo "  1. Run Sprint Planner to define sprint goal"
echo "  2. Populate SPRINT_QUEUE.json with tasks"
echo "  3. Begin sprint execution"
echo ""
echo "Files initialized:"
echo "  • SPRINT_QUEUE.json"
echo "  • AGENT_LOG.md"
echo "  • SPRINT_LOG.md"
echo "  • SPRINT_PLAN.md"
echo ""
echo "======================================="

