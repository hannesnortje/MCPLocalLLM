#!/usr/bin/env bash
#
# sprint-dashboard.sh - Sprint Status Dashboard
#
# Displays real-time sprint progress, task counts, WIP utilization,
# exit criteria status, and recent activity for OODATCAA agents.
#
# Usage:
#   bash scripts/sprint-dashboard.sh
#   make sprint-status
#
# Author: agent-builder-A
# Task: P003-B01 Step 1
# Sprint: SPRINT-2025-002

set -euo pipefail

QUEUE_FILE=".oodatcaa/work/SPRINT_QUEUE.json"
STATUS_FILE=".oodatcaa/work/SPRINT_STATUS.json"

# Colors
if [[ -t 1 ]]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    BLUE='\033[0;34m'
    BOLD='\033[1m'
    RESET='\033[0m'
else
    GREEN='' YELLOW='' RED='' BLUE='' BOLD='' RESET=''
fi

# Check dependencies
if ! command -v jq &> /dev/null; then
    echo "Error: jq required. Install: sudo apt-get install jq" >&2
    exit 3
fi

if [[ ! -f "$QUEUE_FILE" ]]; then
    echo "Error: SPRINT_QUEUE.json not found" >&2
    exit 1
fi

if ! jq empty "$QUEUE_FILE" 2>/dev/null; then
    echo "Error: Invalid JSON in $QUEUE_FILE" >&2
    exit 2
fi

# Extract sprint data
SPRINT_ID=$(jq -r '.metadata.sprint_id // "SPRINT-UNKNOWN"' "$QUEUE_FILE")
SPRINT_NUM=$(jq -r '.sprint // "unknown"' "$QUEUE_FILE")
SPRINT_STATUS=$(jq -r '.status // "unknown"' "$QUEUE_FILE")
SPRINT_GOAL=$(jq -r '.metadata.sprint_goal // "No goal set"' "$QUEUE_FILE")

TOTAL_TASKS=$(jq '.metadata.total_tasks // 0' "$QUEUE_FILE")
DONE_TASKS=$(jq '.metadata.done_tasks // 0' "$QUEUE_FILE")
IN_PROGRESS=$(jq '.metadata.in_progress_tasks // 0' "$QUEUE_FILE")
READY_TASKS=$(jq '.metadata.ready_tasks // 0' "$QUEUE_FILE")
BLOCKED=$(jq '.metadata.blocked_tasks // 0' "$QUEUE_FILE")
NEEDS_PLAN=$(jq '.metadata.needs_plan_tasks // 0' "$QUEUE_FILE")
PLANNING=$(jq '.metadata.planning_tasks // 0' "$QUEUE_FILE")
AWAITING_TEST=$(jq '.metadata.awaiting_test_tasks // 0' "$QUEUE_FILE")

PROGRESS_PCT=0
if (( TOTAL_TASKS > 0 )); then
    PROGRESS_PCT=$(( (DONE_TASKS * 100) / TOTAL_TASKS ))
fi

# Display header
echo "======================================="
echo -e "  ${BOLD}Sprint Status: $SPRINT_ID${RESET}"
echo "======================================="
echo ""
echo "Sprint: $SPRINT_GOAL"

STATUS_COLOR="$YELLOW"
[[ "$SPRINT_STATUS" == "completed" ]] && STATUS_COLOR="$GREEN"
[[ "$SPRINT_STATUS" == "failed" ]] && STATUS_COLOR="$RED"
echo -e "Status: ${STATUS_COLOR}${SPRINT_STATUS}${RESET}"

PROGRESS_COLOR="$RED"
(( PROGRESS_PCT >= 50 )) && PROGRESS_COLOR="$YELLOW"
(( PROGRESS_PCT >= 80 )) && PROGRESS_COLOR="$GREEN"
echo -e "Progress: ${PROGRESS_COLOR}${PROGRESS_PCT}% complete${RESET} (${DONE_TASKS} of ${TOTAL_TASKS} tasks)"
echo ""

# Tasks
echo "Tasks:"
echo -e "  ${GREEN}✅ Done:          ${DONE_TASKS} tasks${RESET}"
echo -e "  ${BLUE}🔄 In Progress:   ${IN_PROGRESS} task(s)${RESET}"
echo -e "  ${YELLOW}⏳ Ready:         ${READY_TASKS} task(s)${RESET}"
echo -e "  ${RED}🚫 Blocked:       ${BLOCKED} task(s)${RESET}"
echo -e "  📋 Needs Plan:    ${NEEDS_PLAN} task(s)"
echo -e "  🔍 Planning:      ${PLANNING} task(s)"
echo -e "  ⏸️  Awaiting Test: ${AWAITING_TEST} task(s)"
echo ""

# WIP Utilization
echo "WIP Utilization:"
for role in planner builder tester refiner integrator; do
    LIMIT=$(jq -r ".wip_limits.${role} // 1" "$QUEUE_FILE")
    CURRENT=$(jq "[.tasks[] | select(.agent == \"${role}\" and (.status | IN(\"in_progress\", \"planning\", \"testing\", \"adapting\", \"integrating\")))] | length" "$QUEUE_FILE")
    
    UTIL_PCT=0
    (( LIMIT > 0 )) && UTIL_PCT=$(( (CURRENT * 100) / LIMIT ))
    
    WIP_COLOR="$GREEN"
    (( UTIL_PCT >= 67 )) && WIP_COLOR="$YELLOW"
    (( UTIL_PCT >= 100 )) && WIP_COLOR="$RED"
    
    printf "  %-12s ${WIP_COLOR}%d/%d (%d%%)${RESET}\n" "${role^}:" "$CURRENT" "$LIMIT" "$UTIL_PCT"
done
echo ""

# Exit Criteria
echo "Exit Criteria:"
CRITERIA_JSON=$(jq '[.tasks[] | select(.objective_link != null) | {title: .objective_link, status}] | unique_by(.title)' "$QUEUE_FILE" 2>/dev/null)

if [[ "$CRITERIA_JSON" == "[]" ]]; then
    echo "  No exit criteria defined"
else
    COUNT=$(echo "$CRITERIA_JSON" | jq 'length')
    for ((i=0; i<COUNT; i++)); do
        TITLE=$(echo "$CRITERIA_JSON" | jq -r ".[$i].title")
        STATUS=$(echo "$CRITERIA_JSON" | jq -r ".[$i].status")
        
        case "$STATUS" in
            "done") SYMBOL="✅"; COLOR="$GREEN"; PROG="100%" ;;
            "in_progress"|"awaiting_test"|"ready") SYMBOL="🔄"; COLOR="$YELLOW"; PROG="50%" ;;
            "planning_complete"|"planning") SYMBOL="🔄"; COLOR="$BLUE"; PROG="25%" ;;
            *) SYMBOL="❌"; COLOR="$RED"; PROG="0%" ;;
        esac
        
        echo -e "  ${COLOR}${SYMBOL} ${TITLE} (${PROG})${RESET}"
    done
fi
echo ""

# Recent Activity
echo "Recent Activity:"
jq -r '[.tasks[] | select(.status | IN("done", "in_progress", "awaiting_test"))] | sort_by(.completed // .started // "") | reverse | .[0:3] | .[] | "  - \(.id) \(.status | ascii_upcase) (\(.title))"' "$QUEUE_FILE" 2>/dev/null || echo "  No recent activity"
echo ""

# Next Actions
echo "Next Actions:"
jq -r '[.tasks[] | select(.status == "ready")] | sort_by(.priority) | .[0:3] | .[] | "  - \(.id) ready for \(.type | ascii_downcase) (\(.title))"' "$QUEUE_FILE" 2>/dev/null || echo "  No tasks currently ready"
echo ""

echo "======================================="

# Generate STATUS JSON
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
cat > "$STATUS_FILE" <<EOF
{
  "sprint_id": "${SPRINT_ID}",
  "sprint_number": ${SPRINT_NUM},
  "status": "${SPRINT_STATUS}",
  "generated_at": "${TIMESTAMP}",
  "progress": {
    "total_tasks": ${TOTAL_TASKS},
    "completed": ${DONE_TASKS},
    "in_progress": ${IN_PROGRESS},
    "ready": ${READY_TASKS},
    "blocked": ${BLOCKED},
    "needs_plan": ${NEEDS_PLAN},
    "planning": ${PLANNING},
    "awaiting_test": ${AWAITING_TEST},
    "percentage": ${PROGRESS_PCT}
  },
  "wip": $(jq -c '{
    planner: {current: [.tasks[] | select(.agent == "planner" and (.status | IN("in_progress", "planning")))] | length, limit: .wip_limits.planner},
    builder: {current: [.tasks[] | select(.agent == "builder" and (.status | IN("in_progress", "awaiting_test")))] | length, limit: .wip_limits.builder},
    tester: {current: [.tasks[] | select(.agent == "tester" and (.status | IN("in_progress", "testing")))] | length, limit: .wip_limits.tester},
    refiner: {current: [.tasks[] | select(.agent == "refiner" and (.status | IN("in_progress", "adapting")))] | length, limit: .wip_limits.refiner},
    integrator: {current: [.tasks[] | select(.agent == "integrator" and (.status | IN("in_progress", "integrating")))] | length, limit: .wip_limits.integrator}
  }' "$QUEUE_FILE"),
  "exit_criteria": $(jq -c '[.tasks[] | select(.objective_link != null) | {name: .objective_link, status, progress: (if .status == "done" then 100 elif (.status | IN("in_progress", "awaiting_test", "ready")) then 50 elif (.status | IN("planning", "planning_complete")) then 25 else 0 end)}] | unique_by(.name)' "$QUEUE_FILE")
}
EOF

