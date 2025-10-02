"""
System management tool definitions for MCP Memory Server.

This module contains tool definitions for system operations,
status checking, and administrative functions.
Extracted from monolithic tool_definitions.py for better maintainability.
"""

from typing import Any


class SystemTools:
    """System management and administrative tools."""

    @staticmethod
    def get_tools() -> list[dict[str, Any]]:
        """Get system monitoring tool definitions."""
        return [
            {
                "name": "system_health",
                "description": (
                    "Check system health and get diagnostic information " "about all components"
                ),
                "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
            }
        ]
