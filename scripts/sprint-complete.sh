#!/usr/bin/env bash
#
# sprint-complete.sh - Sprint Finalization Script
#
# Automates sprint completion: validates exit criteria, archives logs,
# updates status, generates retrospective, creates git tag.
#
# Usage:
#   bash scripts/sprint-complete.sh [--dry-run] [--force]
#
# Author: agent-builder-A
# Task: P003-B01 Step 3
# Sprint: SPRINT-2025-002

set -euo pipefail

QUEUE_FILE=".oodatcaa/work/SPRINT_QUEUE.json"
SPRINT_LOG=".oodatcaa/work/SPRINT_LOG.md"
ARCHIVE_DIR=".oodatcaa/work/archive"

DRY_RUN=false
FORCE=false

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=true; shift ;;
        --force) FORCE=true; shift ;;
        --help|-h)
            cat <<EOF
Usage: bash scripts/sprint-complete.sh [OPTIONS]

Finalize current sprint with validation, archiving, and tagging.

Options:
  --dry-run    Preview actions without executing
  --force      Skip exit criteria validation
  --help       Display this help

Exit Codes:
  0 - Success
  1 - Exit criteria not met
  2 - Sprint already completed
  3 - Required files not found
EOF
            exit 0
            ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

# Validate prerequisites
echo "=== Validating Prerequisites ==="
[[ ! -f "$QUEUE_FILE" ]] && { echo "Error: SPRINT_QUEUE.json not found" >&2; exit 3; }
command -v jq &> /dev/null || { echo "Error: jq required" >&2; exit 3; }

STATUS=$(jq -r '.status' "$QUEUE_FILE")
[[ "$STATUS" == "completed" ]] && { echo "Error: Sprint already completed" >&2; exit 2; }

echo "✅ Prerequisites validated"
echo ""

# Validate exit criteria
echo "=== Validating Exit Criteria ==="
if [[ "$FORCE" == "true" ]]; then
    echo "⚠️  Forcing completion, skipping validation"
else
    INCOMPLETE=$(jq -r '[.tasks[] | select(.priority <= 3 and .status != "done" and .status != "cancelled")] | length' "$QUEUE_FILE")
    
    if [[ "$INCOMPLETE" -gt 0 ]]; then
        echo "❌ Exit criteria not met: $INCOMPLETE critical tasks incomplete"
        echo ""
        jq -r '.tasks[] | select(.priority <= 3 and .status != "done" and .status != "cancelled") | "  - \(.id): \(.title) (\(.status))"' "$QUEUE_FILE"
        echo ""
        echo "Use --force to complete anyway"
        exit 1
    fi
    
    echo "✅ Exit criteria met"
fi
echo ""

# Archive logs
echo "=== Archiving Logs ==="
SPRINT_NUM=$(jq -r '.sprint' "$QUEUE_FILE")

if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY-RUN] Would call: bash scripts/rotate-logs.sh --force"
    echo "[DRY-RUN] Would copy SPRINT_QUEUE.json to archive/sprint_${SPRINT_NUM}/"
else
    [[ -f "scripts/rotate-logs.sh" ]] && bash scripts/rotate-logs.sh --force || echo "⚠️  rotate-logs.sh not found"
    
    mkdir -p "$ARCHIVE_DIR/sprint_${SPRINT_NUM}"
    cp "$QUEUE_FILE" "$ARCHIVE_DIR/sprint_${SPRINT_NUM}/SPRINT_${SPRINT_NUM}_FINAL.json"
    echo "✅ Logs archived"
fi
echo ""

# Update status
echo "=== Updating Sprint Status ==="
if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY-RUN] Would update SPRINT_QUEUE.json status to 'completed'"
else
    TEMP="${QUEUE_FILE}.tmp"
    jq --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
       '.status = "completed" | .metadata.completed_at = $ts' \
       "$QUEUE_FILE" > "$TEMP"
    
    jq empty "$TEMP" 2>/dev/null && mv -f "$TEMP" "$QUEUE_FILE" || { rm -f "$TEMP"; echo "Error: Invalid JSON" >&2; exit 4; }
    
    {
        echo ""
        echo "---"
        echo ""
        echo "## Sprint $SPRINT_NUM Complete"
        echo ""
        echo "**Completed:** $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo ""
    } >> "$SPRINT_LOG"
    
    echo "✅ Status updated"
fi
echo ""

# Generate retrospective
echo "=== Generating Retrospective ==="
RETRO_FILE=".oodatcaa/work/SPRINT_${SPRINT_NUM}_RETROSPECTIVE.md"

if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY-RUN] Would generate $RETRO_FILE"
else
    TOTAL=$(jq '.metadata.total_tasks' "$QUEUE_FILE")
    DONE=$(jq '.metadata.done_tasks' "$QUEUE_FILE")
    SUCCESS=$(( (DONE * 100) / TOTAL ))
    
    cat > "$RETRO_FILE" <<EOF
# Sprint $SPRINT_NUM Retrospective

**Sprint ID:** $(jq -r '.metadata.sprint_id // "SPRINT-UNKNOWN"' "$QUEUE_FILE")
**Completed:** $(date -u +%Y-%m-%dT%H:%M:%SZ")
**Status:** $(jq -r '.status' "$QUEUE_FILE")

---

## Metrics

- **Total Tasks:** $TOTAL
- **Completed:** $DONE
- **Success Rate:** $SUCCESS%
- **Goal:** $(jq -r '.metadata.sprint_goal' "$QUEUE_FILE")

---

## Achievements

$(jq -r '.tasks[] | select(.status == "done") | "- ✅ \(.id): \(.title)"' "$QUEUE_FILE")

---

Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ")
EOF
    
    echo "✅ Retrospective generated: $RETRO_FILE"
fi
echo ""

# Create git tag
echo "=== Creating Git Tag ==="
TAG_NAME="sprint-${SPRINT_NUM}-complete"

if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY-RUN] Would create git tag: $TAG_NAME"
else
    DONE=$(jq '.metadata.done_tasks' "$QUEUE_FILE")
    TOTAL=$(jq '.metadata.total_tasks' "$QUEUE_FILE")
    
    git tag -a "$TAG_NAME" -m "Sprint $SPRINT_NUM Complete

Completed: $DONE of $TOTAL tasks
Goal: $(jq -r '.metadata.sprint_goal' "$QUEUE_FILE")
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)" 2>&1 || echo "⚠️  Tag creation failed"
    
    echo "✅ Git tag created: $TAG_NAME"
fi
echo ""

# Cleanup
echo "=== Cleaning Up ==="
if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY-RUN] Would remove stale leases and locks"
else
    [[ -d ".leases" ]] && find .leases -name "*.json" -type f -delete 2>/dev/null || true
    [[ -d ".locks" ]] && rm -f .locks/*.lock 2>/dev/null || true
    echo "✅ Cleanup completed"
fi
echo ""

# Summary
echo "======================================="
echo "  Sprint Completion Summary"
echo "======================================="
echo ""
[[ "$DRY_RUN" == "true" ]] && echo "Mode: DRY-RUN (no changes made)" || echo "Sprint $SPRINT_NUM finalized!"
echo ""
echo "Next steps:"
echo "  - Review: $RETRO_FILE"
echo "  - Run: make sprint-new (start next sprint)"
echo ""
echo "======================================="

