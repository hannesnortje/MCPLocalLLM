"""
Unit tests for agent daemon functionality.

Tests cover core daemon logic including queue reading, WIP enforcement,
lease management, and task claiming.
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

import pytest


# Import daemon functions (they're in a script, so we'll need to handle imports)
@pytest.fixture
def mock_queue_data():
    """Sample queue data for testing."""
    return {
        "sprint": 2,
        "sprint_id": "SPRINT-2025-002",
        "wip_limits": {
            "planner": 1,
            "builder": 3,
            "tester": 2,
            "refiner": 1,
            "integrator": 1,
        },
        "tasks": [
            {
                "id": "P001-B03",
                "title": "Test Task",
                "type": "Build",
                "status": "ready",
                "agent": None,
                "lease": None,
                "dependencies": [],
            },
            {
                "id": "P001-B04",
                "title": "In Progress Task",
                "type": "Build",
                "status": "in_progress",
                "agent": "builder",
                "lease": {"task_id": "P001-B04"},
                "dependencies": [],
            },
        ],
    }


@pytest.fixture
def temp_project_root(tmp_path):
    """Create temporary project structure for testing."""
    # Create necessary directories
    (tmp_path / ".oodatcaa/work").mkdir(parents=True)
    (tmp_path / ".leases").mkdir(parents=True)
    (tmp_path / ".locks").mkdir(parents=True)
    (tmp_path / ".oodatcaa/prompts").mkdir(parents=True)
    
    # Create empty queue file
    queue_file = tmp_path / ".oodatcaa/work/SPRINT_QUEUE.json"
    queue_file.write_text("{}")
    
    return tmp_path


class TestDaemonFunctions:
    """Test daemon utility functions."""
    
    def test_get_wip_count(self, mock_queue_data):
        """Test WIP counting for a specific role."""
        # Import the function (adjust path as needed)
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from agent_daemon import get_wip_count
        
        count = get_wip_count(mock_queue_data, "builder")
        assert count == 1  # One builder task in progress
        
        count = get_wip_count(mock_queue_data, "tester")
        assert count == 0  # No tester tasks in progress
    
    def test_get_wip_limit(self, mock_queue_data):
        """Test WIP limit retrieval."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from agent_daemon import get_wip_limit
        
        limit = get_wip_limit(mock_queue_data, "builder")
        assert limit == 3
        
        limit = get_wip_limit(mock_queue_data, "planner")
        assert limit == 1
        
        # Test default limit for unknown role
        limit = get_wip_limit(mock_queue_data, "unknown")
        assert limit == 1
    
    def test_read_queue_success(self, temp_project_root, mock_queue_data):
        """Test successful queue file reading."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        
        # Write valid queue data
        queue_file = temp_project_root / ".oodatcaa/work/SPRINT_QUEUE.json"
        queue_file.write_text(json.dumps(mock_queue_data))
        
        # Mock PROJECT_ROOT
        with patch("agent_daemon.QUEUE_FILE", queue_file):
            from agent_daemon import read_queue
            data = read_queue()
            assert data is not None
            assert data["sprint"] == 2
            assert "tasks" in data
    
    def test_read_queue_invalid_json(self, temp_project_root):
        """Test queue reading with invalid JSON."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        
        # Write invalid JSON
        queue_file = temp_project_root / ".oodatcaa/work/SPRINT_QUEUE.json"
        queue_file.write_text("{invalid json")
        
        with patch("agent_daemon.QUEUE_FILE", queue_file):
            from agent_daemon import read_queue
            data = read_queue()
            assert data is None
    
    def test_read_queue_missing_file(self, temp_project_root):
        """Test queue reading when file doesn't exist."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        
        nonexistent = temp_project_root / "nonexistent.json"
        
        with patch("agent_daemon.QUEUE_FILE", nonexistent):
            from agent_daemon import read_queue
            data = read_queue()
            assert data is None


class TestLeaseManagement:
    """Test lease management functions."""
    
    def test_check_lease_exists(self, temp_project_root):
        """Test lease file existence checking."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        
        leases_dir = temp_project_root / ".leases"
        
        # Create a lease file
        lease_file = leases_dir / "P001-B03.json"
        lease_file.write_text('{"task_id": "P001-B03"}')
        
        with patch("agent_daemon.LEASES_DIR", leases_dir):
            from agent_daemon import check_lease_exists
            assert check_lease_exists("P001-B03") is True
            assert check_lease_exists("P001-B04") is False


class TestWIPEnforcement:
    """Test WIP limit enforcement."""
    
    def test_wip_enforcement_blocks_when_at_limit(self, mock_queue_data):
        """Test that WIP limit prevents new work when at capacity."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from agent_daemon import get_wip_count, get_wip_limit
        
        # Simulate tester role (limit = 2)
        mock_queue_data["tasks"].extend([
            {
                "id": "P001-T01",
                "type": "Test",
                "status": "in_progress",
                "agent": "tester",
            },
            {
                "id": "P001-T02",
                "type": "Test",
                "status": "in_progress",
                "agent": "tester",
            },
        ])
        
        wip_count = get_wip_count(mock_queue_data, "tester")
        wip_limit = get_wip_limit(mock_queue_data, "tester")
        
        assert wip_count == 2
        assert wip_limit == 2
        assert wip_count >= wip_limit  # Should block new work
    
    def test_wip_enforcement_allows_when_below_limit(self, mock_queue_data):
        """Test that WIP limit allows new work when below capacity."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        from agent_daemon import get_wip_count, get_wip_limit
        
        wip_count = get_wip_count(mock_queue_data, "builder")
        wip_limit = get_wip_limit(mock_queue_data, "builder")
        
        assert wip_count == 1
        assert wip_limit == 3
        assert wip_count < wip_limit  # Should allow new work


class TestGracefulShutdown:
    """Test graceful shutdown handling."""
    
    def test_signal_handler_sets_shutdown_flag(self):
        """Test that signal handler sets the shutdown flag."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        import agent_daemon
        
        # Reset shutdown flag
        agent_daemon.shutdown_requested = False
        
        # Simulate SIGTERM
        agent_daemon.signal_handler(15, None)
        
        assert agent_daemon.shutdown_requested is True


class TestDirectoryCreation:
    """Test directory initialization."""
    
    def test_ensure_directories_creates_missing_dirs(self, temp_project_root):
        """Test that ensure_directories creates required directories."""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        
        leases_dir = temp_project_root / ".leases-test"
        locks_dir = temp_project_root / ".locks-test"
        
        assert not leases_dir.exists()
        assert not locks_dir.exists()
        
        with patch("agent_daemon.LEASES_DIR", leases_dir), \
             patch("agent_daemon.LOCKS_DIR", locks_dir):
            from agent_daemon import ensure_directories
            ensure_directories()
            
            assert leases_dir.exists()
            assert locks_dir.exists()

