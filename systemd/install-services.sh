#!/usr/bin/env bash
#
# Install OODATCAA agent daemon systemd services
#
# This script installs systemd user services (no root required) for all agent roles.
# Services are installed to ~/.config/systemd/user/
#

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"
SERVICE_FILES=("agent-planner.service" "agent-builder.service" "agent-tester.service" "agent-refiner.service" "agent-integrator.service")

echo "Installing OODATCAA Agent Daemon Services"
echo "=========================================="
echo

# Create systemd user directory if it doesn't exist
mkdir -p "${SYSTEMD_USER_DIR}"

# Install service files
echo "Installing service files..."
for service in "${SERVICE_FILES[@]}"; do
    src="${PROJECT_ROOT}/systemd/${service}"
    dst="${SYSTEMD_USER_DIR}/${service}"
    
    if [ ! -f "${src}" ]; then
        echo "ERROR: Service file not found: ${src}"
        exit 1
    fi
    
    # Update WorkingDirectory and ExecStart paths with actual project root
    sed "s|%h/storage/Code/MCPLocalLLM|${PROJECT_ROOT}|g" "${src}" > "${dst}"
    
    echo "  ✓ Installed ${service}"
done

echo
echo "Reloading systemd user daemon..."
systemctl --user daemon-reload

echo
echo "Installation complete!"
echo
echo "To start all agents:"
echo "  systemctl --user start agent-planner agent-builder agent-tester agent-refiner agent-integrator"
echo
echo "To enable agents on login:"
echo "  systemctl --user enable agent-planner agent-builder agent-tester agent-refiner agent-integrator"
echo
echo "To check status:"
echo "  systemctl --user status agent-*"
echo
echo "To view logs:"
echo "  journalctl --user -u agent-planner -f"
echo

