#!/usr/bin/env bash
#
# Agent Daemon CLI - Command-line interface for managing agent daemons
#
# Usage:
#   ./scripts/agents-daemon-cli.sh start     # Start all agent daemons
#   ./scripts/agents-daemon-cli.sh stop      # Stop all agent daemons
#   ./scripts/agents-daemon-cli.sh restart   # Restart all agent daemons
#   ./scripts/agents-daemon-cli.sh status    # Show status of all agents
#

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_DIR="${PROJECT_ROOT}/.agent-daemon-pids"
LOG_DIR="${PROJECT_ROOT}/.agent-daemon-logs"

ROLES=("planner" "builder" "tester" "refiner" "integrator")

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Ensure directories exist
mkdir -p "${PID_DIR}" "${LOG_DIR}"

start_daemon() {
    local role=$1
    local pid_file="${PID_DIR}/${role}.pid"
    local log_file="${LOG_DIR}/${role}.log"
    
    # Check if already running
    if [ -f "${pid_file}" ]; then
        local pid=$(cat "${pid_file}")
        if kill -0 "${pid}" 2>/dev/null; then
            echo -e "${YELLOW}⚠${NC}  ${role} daemon already running (PID: ${pid})"
            return 0
        else
            # Stale PID file
            rm -f "${pid_file}"
        fi
    fi
    
    # Start daemon in background
    echo -e "${GREEN}▶${NC}  Starting ${role} daemon..."
    nohup python3 "${PROJECT_ROOT}/scripts/agent-daemon.py" \
        --role "${role}" \
        --interval 60 \
        --owner "agent-daemon-${role}" \
        >> "${log_file}" 2>&1 &
    
    local pid=$!
    echo "${pid}" > "${pid_file}"
    
    # Verify it started
    sleep 1
    if kill -0 "${pid}" 2>/dev/null; then
        echo -e "${GREEN}✓${NC}  ${role} daemon started (PID: ${pid})"
    else
        echo -e "${RED}✗${NC}  ${role} daemon failed to start"
        rm -f "${pid_file}"
        return 1
    fi
}

stop_daemon() {
    local role=$1
    local pid_file="${PID_DIR}/${role}.pid"
    
    if [ ! -f "${pid_file}" ]; then
        echo -e "${YELLOW}⚠${NC}  ${role} daemon not running"
        return 0
    fi
    
    local pid=$(cat "${pid_file}")
    
    if ! kill -0 "${pid}" 2>/dev/null; then
        echo -e "${YELLOW}⚠${NC}  ${role} daemon not running (stale PID file)"
        rm -f "${pid_file}"
        return 0
    fi
    
    # Send SIGTERM for graceful shutdown
    echo -e "${YELLOW}■${NC}  Stopping ${role} daemon (PID: ${pid})..."
    kill -TERM "${pid}" 2>/dev/null || true
    
    # Wait up to 10 seconds for graceful shutdown
    local count=0
    while kill -0 "${pid}" 2>/dev/null && [ $count -lt 10 ]; do
        sleep 1
        ((count++))
    done
    
    # Force kill if still running
    if kill -0 "${pid}" 2>/dev/null; then
        echo -e "${YELLOW}!${NC}  Forcing ${role} daemon to stop..."
        kill -9 "${pid}" 2>/dev/null || true
        sleep 1
    fi
    
    rm -f "${pid_file}"
    echo -e "${GREEN}✓${NC}  ${role} daemon stopped"
}

status_daemon() {
    local role=$1
    local pid_file="${PID_DIR}/${role}.pid"
    
    if [ ! -f "${pid_file}" ]; then
        echo -e "${RED}●${NC} ${role}: stopped"
        return 1
    fi
    
    local pid=$(cat "${pid_file}")
    
    if kill -0 "${pid}" 2>/dev/null; then
        echo -e "${GREEN}●${NC} ${role}: running (PID: ${pid})"
        return 0
    else
        echo -e "${RED}●${NC} ${role}: stopped (stale PID file)"
        rm -f "${pid_file}"
        return 1
    fi
}

cmd_start() {
    echo "Starting agent daemons..."
    echo
    
    local failed=0
    for role in "${ROLES[@]}"; do
        start_daemon "${role}" || ((failed++))
    done
    
    echo
    if [ $failed -eq 0 ]; then
        echo -e "${GREEN}✅ All agent daemons started successfully${NC}"
    else
        echo -e "${RED}❌ ${failed} agent daemon(s) failed to start${NC}"
        return 1
    fi
}

cmd_stop() {
    echo "Stopping agent daemons..."
    echo
    
    for role in "${ROLES[@]}"; do
        stop_daemon "${role}"
    done
    
    echo
    echo -e "${GREEN}✅ All agent daemons stopped${NC}"
}

cmd_restart() {
    echo "Restarting agent daemons..."
    echo
    
    cmd_stop
    sleep 2
    cmd_start
}

cmd_status() {
    echo "Agent daemon status:"
    echo
    
    local running=0
    local stopped=0
    
    for role in "${ROLES[@]}"; do
        if status_daemon "${role}"; then
            ((running++))
        else
            ((stopped++))
        fi
    done
    
    echo
    echo "Running: ${running}/${#ROLES[@]}"
    echo "Stopped: ${stopped}/${#ROLES[@]}"
}

usage() {
    echo "Usage: $0 {start|stop|restart|status}"
    echo
    echo "Commands:"
    echo "  start    - Start all agent daemons"
    echo "  stop     - Stop all agent daemons"
    echo "  restart  - Restart all agent daemons"
    echo "  status   - Show status of all agent daemons"
    exit 1
}

main() {
    if [ $# -eq 0 ]; then
        usage
    fi
    
    local command=$1
    
    case "${command}" in
        start)
            cmd_start
            ;;
        stop)
            cmd_stop
            ;;
        restart)
            cmd_restart
            ;;
        status)
            cmd_status
            ;;
        *)
            echo "Unknown command: ${command}"
            usage
            ;;
    esac
}

main "$@"

