"""
Integration tests for MCP server initialization.

Tests that verify the MemoryMCPServer can be created and initialized
successfully with all required components.
"""

import sys
from pathlib import Path

import pytest

# Add src to path (conftest.py should handle this, but we ensure it here too)
src_path = Path(__file__).absolute().parent.parent.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from mcp.mcp_server import MemoryMCPServer  # noqa: E402


@pytest.mark.integration
@pytest.mark.asyncio
async def test_server_can_initialize(mcp_server: MemoryMCPServer) -> None:
    """
    Test that MemoryMCPServer instance can be created successfully.

    Validates:
    - Server initializes without errors
    - Server instance is not None
    - Server has expected mode attribute
    """
    assert mcp_server is not None, "MCP server should be initialized"
    assert hasattr(mcp_server, "server_mode"), "Server should have server_mode attribute"
    assert mcp_server.server_mode == "full", "Server should be in 'full' mode"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_memory_manager_available(mcp_server: MemoryMCPServer) -> None:
    """
    Test that memory manager is properly initialized and available.

    Validates:
    - memory_manager attribute exists
    - memory_manager is not None
    - memory_manager has expected client attribute
    """
    assert hasattr(mcp_server, "memory_manager"), "Server should have memory_manager attribute"
    assert mcp_server.memory_manager is not None, "Memory manager should be initialized"
    assert hasattr(mcp_server.memory_manager, "client"), "Memory manager should have Qdrant client"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_health_check(mcp_server: MemoryMCPServer) -> None:
    """
    Test that system health check returns valid status information.

    Validates:
    - get_system_health() returns a dictionary
    - Health response contains expected keys
    - Health status indicates system is operational
    """
    health = mcp_server.get_system_health()

    assert isinstance(health, dict), "Health check should return a dictionary"
    assert "status" in health, "Health response should contain 'status' key"
    assert "timestamp" in health, "Health response should contain 'timestamp' key"

    # Check that status indicates system is working
    status = health.get("status")
    assert status in [
        "healthy",
        "degraded",
        "operational",
    ], f"Health status should be valid, got: {status}"


@pytest.mark.integration
@pytest.mark.asyncio
async def test_available_tools(mcp_server: MemoryMCPServer) -> None:
    """
    Test that server can list available memory management tools.

    Validates:
    - get_available_tools() returns a list
    - Tool list is not empty (at least basic memory tools exist)
    - Each tool has required fields (name, description, inputSchema)
    """
    tools = mcp_server.get_available_tools()

    assert isinstance(tools, list), "Available tools should return a list"
    assert len(tools) > 0, "Server should have at least some memory tools available"

    # Verify tool structure
    for tool in tools:
        assert "name" in tool, f"Tool should have 'name' field: {tool}"
        assert "description" in tool, f"Tool should have 'description' field: {tool}"
        assert "inputSchema" in tool, f"Tool should have 'inputSchema' field: {tool}"
