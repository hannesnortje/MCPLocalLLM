"""
Pytest fixtures for MCP integration tests.

Provides shared test fixtures for:
- Qdrant availability checking
- MCP server initialization
- Test collection management
- Automatic cleanup
"""

import logging
import sys
import uuid
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest

# Clear any cached mcp modules to avoid conflict with protocol library
for key in list(sys.modules.keys()):
    if key.startswith("mcp") and not key.startswith("mcp."):
        # Don't remove the protocol library, just top-level mcp if it exists
        pass
    elif key.startswith("mcp.") and "site-packages" not in str(
        getattr(sys.modules[key], "__file__", "")
    ):
        # Remove our local mcp modules if they were cached
        del sys.modules[key]

# Add src directory to path to import local mcp module (not the protocol library)
src_path = Path(__file__).absolute().parent.parent.parent / "src"
src_str = str(src_path)
#  Remove src if it's already in sys.path (from editable install)
while src_str in sys.path:
    sys.path.remove(src_str)
# Insert at the very beginning to override site-packages mcp
sys.path.insert(0, src_str)

# Configure logging for tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def qdrant_available() -> bool:
    """
    Check if Qdrant is running and available for tests.

    Returns:
        bool: True if Qdrant is accessible, False otherwise
    """
    try:
        from qdrant_client import QdrantClient

        client = QdrantClient(host="localhost", port=6333, timeout=5)
        # Try to get health status
        client.get_collections()
        logger.info("✅ Qdrant is available for testing")
        return True
    except Exception as e:
        logger.warning(f"⚠️ Qdrant not available: {e}")
        return False


@pytest.fixture
def test_collection_name() -> str:
    """
    Generate a unique test collection name for isolation.

    Returns:
        str: Unique collection name with test prefix
    """
    return f"test_collection_{uuid.uuid4().hex[:8]}"


@pytest.fixture
async def mcp_server(qdrant_available: bool) -> Generator[Any, None, None]:
    """
    Initialize a MemoryMCPServer instance for testing.

    Args:
        qdrant_available: Whether Qdrant is available

    Yields:
        MemoryMCPServer: Initialized MCP server instance

    Note:
        Tests will be skipped if Qdrant is not available
    """
    if not qdrant_available:
        pytest.skip("Qdrant is not available - skipping MCP server tests")

    from mcp.mcp_server import MemoryMCPServer

    # Initialize server
    server = MemoryMCPServer(server_mode="full")

    yield server

    # Cleanup: server cleanup happens automatically on destruction
    logger.info("Test server cleanup complete")


@pytest.fixture
async def cleanup_test_collections(qdrant_available: bool) -> Generator[list[str], None, None]:
    """
    Track and cleanup test collections after tests.

    Args:
        qdrant_available: Whether Qdrant is available

    Yields:
        list[str]: List to track collection names for cleanup
    """
    if not qdrant_available:
        pytest.skip("Qdrant is not available - skipping collection cleanup")

    collections_to_cleanup = []

    yield collections_to_cleanup

    # Cleanup all test collections
    if collections_to_cleanup:
        try:
            from qdrant_client import QdrantClient

            client = QdrantClient(host="localhost", port=6333)
            for collection_name in collections_to_cleanup:
                try:
                    client.delete_collection(collection_name)
                    logger.info(f"Cleaned up test collection: {collection_name}")
                except Exception as e:
                    logger.warning(f"Failed to cleanup collection {collection_name}: {e}")
        except Exception as e:
            logger.error(f"Failed to initialize Qdrant client for cleanup: {e}")


# Pytest markers for integration tests
def pytest_configure(config: Any) -> None:
    """Register custom pytest markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test (requires Qdrant)"
    )
