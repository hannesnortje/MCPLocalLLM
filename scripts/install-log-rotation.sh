#!/usr/bin/env bash
#
# Install Log Rotation Scheduling
#
# Sets up automatic log rotation via cron or systemd timer.
# Runs hourly check for logs exceeding threshold.
#
# Usage:
#   ./scripts/install-log-rotation.sh              # Install with auto-detection
#   ./scripts/install-log-rotation.sh --cron       # Force cron installation
#   ./scripts/install-log-rotation.sh --systemd    # Force systemd installation
#   ./scripts/install-log-rotation.sh --uninstall  # Remove scheduling
#

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ROTATION_SCRIPT="${PROJECT_ROOT}/scripts/rotate-logs.sh"
INDEX_SCRIPT="${PROJECT_ROOT}/scripts/generate-archive-index.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

MODE=""
ACTION="install"

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --cron)
            MODE="cron"
            shift
            ;;
        --systemd)
            MODE="systemd"
            shift
            ;;
        --uninstall)
            ACTION="uninstall"
            shift
            ;;
        --help|-h)
            cat << EOF
Usage: $(basename "$0") [OPTIONS]

Install automatic log rotation scheduling.

Options:
    --cron       Force cron installation
    --systemd    Force systemd timer installation
    --uninstall  Remove log rotation scheduling
    --help       Show this help message

Examples:
    $(basename "$0")              # Auto-detect best method
    $(basename "$0") --cron       # Install as cron job
    $(basename "$0") --systemd    # Install as systemd timer
    $(basename "$0") --uninstall  # Remove scheduling

EOF
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Check if systemd is available
has_systemd() {
    command -v systemctl >/dev/null 2>&1 && systemctl --user status >/dev/null 2>&1
}

# Check if cron is available
has_cron() {
    command -v crontab >/dev/null 2>&1
}

# Auto-detect best method
if [ -z "$MODE" ]; then
    if has_systemd; then
        MODE="systemd"
        echo -e "${BLUE}→${NC} Auto-detected: systemd available"
    elif has_cron; then
        MODE="cron"
        echo -e "${BLUE}→${NC} Auto-detected: cron available"
    else
        echo -e "${RED}✗${NC} Neither systemd nor cron available!"
        echo "Manual scheduling required. Add to your preferred scheduler:"
        echo "  Command: bash ${ROTATION_SCRIPT} && bash ${INDEX_SCRIPT}"
        echo "  Schedule: Hourly"
        exit 1
    fi
fi

# Install cron job
install_cron() {
    echo -e "${BLUE}→${NC} Installing cron job..."
    
    # Create cron entry
    local cron_entry="0 * * * * cd ${PROJECT_ROOT} && bash ${ROTATION_SCRIPT} && bash ${INDEX_SCRIPT} >> ${PROJECT_ROOT}/.log-rotation.log 2>&1"
    
    # Check if entry already exists
    if crontab -l 2>/dev/null | grep -F "$ROTATION_SCRIPT" >/dev/null; then
        echo -e "${YELLOW}⚠${NC}  Cron job already installed"
        return 0
    fi
    
    # Add to crontab
    (crontab -l 2>/dev/null; echo "$cron_entry") | crontab -
    
    echo -e "${GREEN}✓${NC} Cron job installed"
    echo "     Schedule: Hourly (at minute 0)"
    echo "     Log: ${PROJECT_ROOT}/.log-rotation.log"
    
    # Verify installation
    echo
    echo "Cron entry:"
    crontab -l | grep "$ROTATION_SCRIPT"
}

# Uninstall cron job
uninstall_cron() {
    echo -e "${BLUE}→${NC} Removing cron job..."
    
    if ! crontab -l 2>/dev/null | grep -F "$ROTATION_SCRIPT" >/dev/null; then
        echo -e "${YELLOW}⚠${NC}  No cron job found"
        return 0
    fi
    
    # Remove from crontab
    crontab -l 2>/dev/null | grep -v "$ROTATION_SCRIPT" | crontab -
    
    echo -e "${GREEN}✓${NC} Cron job removed"
}

# Install systemd timer
install_systemd() {
    echo -e "${BLUE}→${NC} Installing systemd timer..."
    
    local systemd_dir="${HOME}/.config/systemd/user"
    local service_file="${systemd_dir}/log-rotation.service"
    local timer_file="${systemd_dir}/log-rotation.timer"
    
    mkdir -p "$systemd_dir"
    
    # Create service file
    cat > "$service_file" << EOF
[Unit]
Description=OODATCAA Log Rotation Service
After=network.target

[Service]
Type=oneshot
WorkingDirectory=${PROJECT_ROOT}
ExecStart=/bin/bash ${ROTATION_SCRIPT}
ExecStartPost=/bin/bash ${INDEX_SCRIPT}
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
EOF
    
    # Create timer file
    cat > "$timer_file" << EOF
[Unit]
Description=OODATCAA Log Rotation Timer
Requires=log-rotation.service

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
EOF
    
    # Reload systemd
    systemctl --user daemon-reload
    
    # Enable and start timer
    systemctl --user enable log-rotation.timer
    systemctl --user start log-rotation.timer
    
    echo -e "${GREEN}✓${NC} Systemd timer installed"
    echo "     Service: log-rotation.service"
    echo "     Timer:   log-rotation.timer"
    echo "     Schedule: Hourly"
    
    # Show status
    echo
    echo "Timer status:"
    systemctl --user status log-rotation.timer --no-pager || true
}

# Uninstall systemd timer
uninstall_systemd() {
    echo -e "${BLUE}→${NC} Removing systemd timer..."
    
    # Stop and disable timer
    systemctl --user stop log-rotation.timer 2>/dev/null || true
    systemctl --user disable log-rotation.timer 2>/dev/null || true
    
    # Remove files
    local systemd_dir="${HOME}/.config/systemd/user"
    rm -f "${systemd_dir}/log-rotation.service"
    rm -f "${systemd_dir}/log-rotation.timer"
    
    # Reload systemd
    systemctl --user daemon-reload
    
    echo -e "${GREEN}✓${NC} Systemd timer removed"
}

# Main execution
main() {
    echo "OODATCAA Log Rotation Installation"
    echo "==================================="
    echo
    
    if [ "$ACTION" = "uninstall" ]; then
        echo "Uninstalling log rotation scheduling..."
        echo
        
        if [ "$MODE" = "cron" ]; then
            uninstall_cron
        elif [ "$MODE" = "systemd" ]; then
            uninstall_systemd
        fi
        
        echo
        echo -e "${GREEN}✅ Log rotation scheduling removed${NC}"
        exit 0
    fi
    
    # Install
    echo "Installing automatic log rotation..."
    echo "  Method: ${MODE}"
    echo "  Script: ${ROTATION_SCRIPT}"
    echo
    
    if [ "$MODE" = "cron" ]; then
        install_cron
    elif [ "$MODE" = "systemd" ]; then
        install_systemd
    fi
    
    echo
    echo -e "${GREEN}✅ Log rotation installed successfully!${NC}"
    echo
    echo "Next steps:"
    echo "  1. Logs will be checked hourly"
    echo "  2. Rotation happens automatically when > 1000 lines"
    echo "  3. Manual rotation: bash ${ROTATION_SCRIPT}"
    echo "  4. View logs: tail -f .log-rotation.log (cron) or journalctl --user -u log-rotation (systemd)"
    echo
    echo "To test immediately:"
    echo "  bash ${ROTATION_SCRIPT} --dry-run"
}

main

