#!/usr/bin/env bash
#
# Uninstall OODATCAA agent daemon systemd services
#

set -euo pipefail

SYSTEMD_USER_DIR="${HOME}/.config/systemd/user"
SERVICE_FILES=("agent-planner.service" "agent-builder.service" "agent-tester.service" "agent-refiner.service" "agent-integrator.service")

echo "Uninstalling OODATCAA Agent Daemon Services"
echo "============================================"
echo

# Stop all services
echo "Stopping all agent services..."
for service in "${SERVICE_FILES[@]}"; do
    if systemctl --user is-active --quiet "${service}" 2>/dev/null; then
        systemctl --user stop "${service}"
        echo "  ✓ Stopped ${service}"
    fi
done

echo
echo "Disabling all agent services..."
for service in "${SERVICE_FILES[@]}"; do
    if systemctl --user is-enabled --quiet "${service}" 2>/dev/null; then
        systemctl --user disable "${service}"
        echo "  ✓ Disabled ${service}"
    fi
done

echo
echo "Removing service files..."
for service in "${SERVICE_FILES[@]}"; do
    dst="${SYSTEMD_USER_DIR}/${service}"
    if [ -f "${dst}" ]; then
        rm -f "${dst}"
        echo "  ✓ Removed ${service}"
    fi
done

echo
echo "Reloading systemd user daemon..."
systemctl --user daemon-reload

echo
echo "Uninstallation complete!"
echo

