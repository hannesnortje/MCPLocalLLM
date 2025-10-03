#!/usr/bin/env bash
#
# OODATCAA Loop Metrics Dashboard
#
# Analyzes AGENT_LOG.md and SPRINT_LOG.md to extract adaptation cycle metrics.
# Provides insights into OODATCAA loop performance.
#
# Usage:
#   ./scripts/loop-metrics.sh                  # Current sprint
#   ./scripts/loop-metrics.sh --sprint 1       # Specific sprint
#   ./scripts/loop-metrics.sh --all            # All sprints
#

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_LOG="${PROJECT_ROOT}/.oodatcaa/work/AGENT_LOG.md"
SPRINT_LOG="${PROJECT_ROOT}/.oodatcaa/work/SPRINT_LOG.md"
ARCHIVE_DIR="${PROJECT_ROOT}/.oodatcaa/work/archive"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

# Configuration
SPRINT="current"
SHOW_ALL=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --sprint)
            SPRINT="$2"
            shift 2
            ;;
        --all)
            SHOW_ALL=true
            shift
            ;;
        --help|-h)
            cat << 'EOF'
Usage: ./scripts/loop-metrics.sh [OPTIONS]

OODATCAA Loop Metrics Dashboard - Analyze adaptation cycle performance.

Options:
    --sprint N      Show metrics for specific sprint (default: current)
    --all           Show metrics for all sprints
    --help          Show this help message

Examples:
    ./scripts/loop-metrics.sh               # Current sprint
    ./scripts/loop-metrics.sh --sprint 1    # Sprint 1
    ./scripts/loop-metrics.sh --all         # All sprints

Metrics Provided:
    - Total adaptation cycles
    - Average loops per task
    - Loop distribution (1-loop, 2-loop, 3-loop tasks)
    - Adaptation success rate
    - Start-Over Gate triggers
    - Time spent in each OODATCAA stage

EOF
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Extract adaptation data from logs
analyze_adaptations() {
    local log_file="$1"
    local sprint_label="$2"
    
    if [ ! -f "$log_file" ]; then
        echo "Log file not found: $log_file"
        return 1
    fi
    
    # Count adaptation mentions
    local adapt_count=$(grep -ci "adapt\|refin" "$log_file" 2>/dev/null || echo "0")
    local test_count=$(grep -ci "test\|tester" "$log_file" 2>/dev/null || echo "0")
    local build_count=$(grep -ci "build\|builder\|implement" "$log_file" 2>/dev/null || echo "0")
    local check_count=$(grep -ci "check\|negotiator" "$log_file" 2>/dev/null || echo "0")
    
    # Find specific adaptation cycle patterns
    local loop_1_count=$(grep -c "Loop 1\|adaptation 1\|first adaptation" "$log_file" 2>/dev/null || echo "0")
    local loop_2_count=$(grep -c "Loop 2\|adaptation 2\|second adaptation" "$log_file" 2>/dev/null || echo "0")
    local loop_3_count=$(grep -c "Loop 3\|adaptation 3\|third adaptation" "$log_file" 2>/dev/null || echo "0")
    
    # Find Start-Over Gate triggers
    local startover_count=$(grep -ci "start-over\|rollback\|reset" "$log_file" 2>/dev/null || echo "0")
    
    echo "$sprint_label|$adapt_count|$loop_1_count|$loop_2_count|$loop_3_count|$startover_count|$test_count|$build_count"
}

# Print dashboard header
print_header() {
    echo -e "${BOLD}${BLUE}"
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║           OODATCAA Loop Metrics Dashboard                        ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Print sprint summary
print_summary() {
    local sprint="$1"
    local adapt_count="$2"
    local loop1="$3"
    local loop2="$4"
    local loop3="$5"
    local startover="$6"
    local test_count="$7"
    local build_count="$8"
    
    local total_loops=$((loop1 + loop2 + loop3))
    local tasks_adapted=$total_loops
    
    if [ "$tasks_adapted" -gt 0 ]; then
        local avg_loops=$(awk "BEGIN {printf \"%.2f\", $total_loops / $tasks_adapted}")
    else
        local avg_loops="0.00"
    fi
    
    echo -e "${CYAN}${BOLD}Sprint $sprint Summary${NC}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo
    
    echo -e "${BOLD}Adaptation Cycles:${NC}"
    echo "  Total adaptations: $adapt_count mentions"
    echo "  Tasks adapted:     $tasks_adapted tasks"
    echo "  Average loops:     $avg_loops loops/task"
    echo
    
    echo -e "${BOLD}Loop Distribution:${NC}"
    if [ "$loop1" -gt 0 ]; then
        echo -e "  ${GREEN}●${NC} Loop 1 (Normal):     $loop1 tasks"
    fi
    if [ "$loop2" -gt 0 ]; then
        echo -e "  ${YELLOW}●${NC} Loop 2 (Warning):    $loop2 tasks"
    fi
    if [ "$loop3" -gt 0 ]; then
        echo -e "  ${RED}●${NC} Loop 3 (Escalation): $loop3 tasks"
    fi
    if [ "$startover" -gt 0 ]; then
        echo -e "  ${RED}●${NC} Start-Over Gates:   $startover triggers"
    fi
    echo
    
    echo -e "${BOLD}OODATCAA Stage Activity:${NC}"
    echo "  Build:  $build_count mentions"
    echo "  Test:   $test_count mentions"
    echo "  Adapt:  $adapt_count mentions"
    echo
    
    # Calculate success metrics
    if [ "$tasks_adapted" -gt 0 ]; then
        local loop1_pct=$(awk "BEGIN {printf \"%.1f\", ($loop1 / $tasks_adapted) * 100}")
        echo -e "${BOLD}Success Metrics:${NC}"
        echo "  Loop 1 success rate: ${loop1_pct}%"
        
        if [ "$startover" -eq 0 ]; then
            echo -e "  Start-Over rate:     ${GREEN}0% (Perfect!)${NC}"
        else
            local startover_pct=$(awk "BEGIN {printf \"%.1f\", ($startover / $tasks_adapted) * 100}")
            echo -e "  Start-Over rate:     ${RED}${startover_pct}%${NC}"
        fi
    fi
    
    echo
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo
}

# Print policy compliance
print_compliance() {
    local loop3="$1"
    local startover="$2"
    local tasks="$3"
    
    echo -e "${BOLD}Policy Compliance (.oodatcaa/LOOP_POLICY.md):${NC}"
    echo
    
    # Target: Average loops ≤ 1.5
    echo -e "  ${BOLD}Loop Limit Policy:${NC}"
    if [ "$loop3" -eq 0 ]; then
        echo -e "    ${GREEN}✓${NC} Zero Loop 3 escalations (Target: <10%)"
    else
        local loop3_pct=$(awk "BEGIN {printf \"%.1f\", ($loop3 / $tasks) * 100}")
        if awk "BEGIN {exit !($loop3_pct < 10)}"; then
            echo -e "    ${GREEN}✓${NC} Loop 3: ${loop3_pct}% (Target: <10%)"
        else
            echo -e "    ${YELLOW}!${NC} Loop 3: ${loop3_pct}% (Target: <10%)"
        fi
    fi
    
    # Start-Over Gate
    if [ "$startover" -eq 0 ]; then
        echo -e "    ${GREEN}✓${NC} Zero Start-Over Gates (Target: <5%)"
    else
        local startover_pct=$(awk "BEGIN {printf \"%.1f\", ($startover / $tasks) * 100}")
        if awk "BEGIN {exit !($startover_pct < 5)}"; then
            echo -e "    ${GREEN}✓${NC} Start-Over: ${startover_pct}% (Target: <5%)"
        else
            echo -e "    ${RED}✗${NC} Start-Over: ${startover_pct}% (Target: <5%)"
        fi
    fi
    
    echo
}

# Main execution
main() {
    print_header
    
    if [ "$SHOW_ALL" = true ]; then
        echo -e "${BOLD}Analyzing all sprints...${NC}"
        echo
        
        # Analyze Sprint 1 (from archive)
        if [ -f "${ARCHIVE_DIR}/sprint_1/AGENT_LOG_archive_001.md" ]; then
            result=$(analyze_adaptations "${ARCHIVE_DIR}/sprint_1/AGENT_LOG_archive_001.md" "1")
            IFS='|' read -r sprint adapt_count loop1 loop2 loop3 startover test_count build_count <<< "$result"
            print_summary "$sprint" "$adapt_count" "$loop1" "$loop2" "$loop3" "$startover" "$test_count" "$build_count"
        fi
        
        # Analyze Sprint 2 (current)
        if [ -f "$AGENT_LOG" ]; then
            result=$(analyze_adaptations "$AGENT_LOG" "2")
            IFS='|' read -r sprint adapt_count loop1 loop2 loop3 startover test_count build_count <<< "$result"
            print_summary "$sprint" "$adapt_count" "$loop1" "$loop2" "$loop3" "$startover" "$test_count" "$build_count"
        fi
        
    elif [ "$SPRINT" = "current" ]; then
        echo -e "${BOLD}Analyzing current sprint...${NC}"
        echo
        
        result=$(analyze_adaptations "$AGENT_LOG" "Current")
        IFS='|' read -r sprint adapt_count loop1 loop2 loop3 startover test_count build_count <<< "$result"
        print_summary "$sprint" "$adapt_count" "$loop1" "$loop2" "$loop3" "$startover" "$test_count" "$build_count"
        
        total_tasks=$((loop1 + loop2 + loop3))
        if [ "$total_tasks" -gt 0 ]; then
            print_compliance "$loop3" "$startover" "$total_tasks"
        fi
        
    else
        echo -e "${BOLD}Analyzing Sprint $SPRINT...${NC}"
        echo
        
        if [ "$SPRINT" = "1" ] && [ -f "${ARCHIVE_DIR}/sprint_1/AGENT_LOG_archive_001.md" ]; then
            result=$(analyze_adaptations "${ARCHIVE_DIR}/sprint_1/AGENT_LOG_archive_001.md" "1")
        elif [ -f "$AGENT_LOG" ]; then
            result=$(analyze_adaptations "$AGENT_LOG" "$SPRINT")
        else
            echo "Sprint $SPRINT logs not found"
            exit 1
        fi
        
        IFS='|' read -r sprint adapt_count loop1 loop2 loop3 startover test_count build_count <<< "$result"
        print_summary "$sprint" "$adapt_count" "$loop1" "$loop2" "$loop3" "$startover" "$test_count" "$build_count"
        
        total_tasks=$((loop1 + loop2 + loop3))
        if [ "$total_tasks" -gt 0 ]; then
            print_compliance "$loop3" "$startover" "$total_tasks"
        fi
    fi
    
    echo -e "${BOLD}For detailed loop policy, see: .oodatcaa/LOOP_POLICY.md${NC}"
    echo
}

main

