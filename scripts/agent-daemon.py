#!/usr/bin/env python3
"""
Agent Daemon - Background process for autonomous agent work claiming.

This daemon enables agents to run continuously, automatically claiming work from
the sprint queue without manual intervention. Supports WIP limits, lease management,
and graceful error handling.

Usage:
    python3 scripts/agent-daemon.py --role builder --interval 60
    python3 scripts/agent-daemon.py --role planner --once  # Single run
"""

import argparse
import datetime
import fcntl
import json
import logging
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
QUEUE_FILE = PROJECT_ROOT / ".oodatcaa/work/SPRINT_QUEUE.json"
LEASES_DIR = PROJECT_ROOT / ".leases"
PROMPTS_DIR = PROJECT_ROOT / ".oodatcaa/prompts"
AGENT_LOG = PROJECT_ROOT / ".oodatcaa/work/AGENT_LOG.md"
LOCKS_DIR = PROJECT_ROOT / ".locks"

# Graceful shutdown flag
shutdown_requested = False


def signal_handler(signum: int, frame: Any) -> None:
    """Handle SIGTERM/SIGINT for graceful shutdown."""
    global shutdown_requested
    sig_name = signal.Signals(signum).name
    logging.info(f"Received {sig_name}, initiating graceful shutdown...")
    shutdown_requested = True


def setup_logging(role: str) -> None:
    """Configure logging to write only state changes, not routine polls."""
    log_dir = PROJECT_ROOT / ".agent-daemon-logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"{role}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )


def ensure_directories() -> None:
    """Ensure required directories exist."""
    LEASES_DIR.mkdir(parents=True, exist_ok=True)
    LOCKS_DIR.mkdir(parents=True, exist_ok=True)


def read_queue() -> Optional[Dict[str, Any]]:
    """Read and parse the sprint queue JSON file."""
    try:
        if not QUEUE_FILE.exists():
            logging.error(f"Queue file not found: {QUEUE_FILE}")
            return None
        
        with open(QUEUE_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in queue file: {e}")
        return None
    except Exception as e:
        logging.error(f"Error reading queue file: {e}")
        return None


def get_wip_count(queue_data: Dict[str, Any], role: str) -> int:
    """Count current in-progress tasks for a specific role."""
    count = 0
    for task in queue_data.get("tasks", []):
        if task.get("agent") == role and task.get("status") == "in_progress":
            count += 1
    return count


def get_wip_limit(queue_data: Dict[str, Any], role: str) -> int:
    """Get WIP limit for a specific role from queue metadata."""
    return queue_data.get("wip_limits", {}).get(role, 1)


def check_lease_exists(task_id: str) -> bool:
    """Check if a valid lease file exists for the task."""
    lease_file = LEASES_DIR / f"{task_id}.json"
    return lease_file.exists()


def is_lease_stale(lease_data: Dict[str, Any]) -> bool:
    """Check if a lease is stale (heartbeat + TTL expired)."""
    try:
        last_heartbeat = datetime.datetime.fromisoformat(
            lease_data["heartbeat_at"].replace("+00:00", "+00:00")
        )
        ttl_seconds = lease_data.get("ttl_seconds", 5400)
        now = datetime.datetime.now(datetime.timezone.utc)
        
        return (now - last_heartbeat).total_seconds() > ttl_seconds
    except Exception as e:
        logging.error(f"Error checking lease staleness: {e}")
        return True  # Treat as stale if we can't parse


def find_ready_task(queue_data: Dict[str, Any], role: str, ignore_wip: bool = False) -> Optional[Dict[str, Any]]:
    """
    Find the first task ready for this agent role.
    
    Task is ready if:
    - Status matches role's expected status (needs_plan for planner, ready for builder, etc.)
    - Dependencies are satisfied
    - No active lease exists
    - WIP limit not exceeded (unless ignore_wip=True)
    """
    # Map roles to expected task statuses
    role_status_map = {
        "planner": "needs_plan",
        "builder": "ready",
        "tester": "awaiting_test",
        "refiner": "needs_adapt",
        "integrator": "ready_for_integrator"
    }
    
    expected_status = role_status_map.get(role)
    if not expected_status:
        logging.error(f"Unknown role: {role}")
        return None
    
    # Check WIP limit
    if not ignore_wip:
        current_wip = get_wip_count(queue_data, role)
        wip_limit = get_wip_limit(queue_data, role)
        
        if current_wip >= wip_limit:
            logging.debug(f"WIP limit reached for {role}: {current_wip}/{wip_limit}")
            return None
    
    # Find first matching task
    for task in queue_data.get("tasks", []):
        if task.get("status") != expected_status:
            continue
        
        # Check dependencies
        deps = task.get("dependencies", [])
        if deps:
            # Verify all dependencies are complete
            deps_satisfied = all(
                any(t.get("id") == dep and t.get("status") in ["done", "completed"]
                    for t in queue_data.get("tasks", []))
                for dep in deps
            )
            if not deps_satisfied:
                continue
        
        # Check for active lease
        task_id = task.get("id")
        if check_lease_exists(task_id):
            lease_file = LEASES_DIR / f"{task_id}.json"
            try:
                with open(lease_file, 'r') as f:
                    lease_data = json.load(f)
                if not is_lease_stale(lease_data):
                    continue  # Active lease exists, skip this task
                else:
                    logging.warning(f"Stale lease detected for {task_id}, will take over")
            except Exception:
                pass  # Treat unreadable lease as stale
        
        return task
    
    return None


def acquire_lease(task_id: str, role: str, owner: str) -> bool:
    """
    Atomically acquire a lease for a task.
    
    Uses file locking (fcntl.flock) to prevent race conditions.
    """
    lease_file = LEASES_DIR / f"{task_id}.json"
    lock_file = LOCKS_DIR / f"{task_id}.lock"
    
    try:
        # Atomic lock acquisition
        with open(lock_file, 'w') as lock_fd:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
            
            # Check if lease already exists (double-check after acquiring lock)
            if lease_file.exists():
                with open(lease_file, 'r') as f:
                    existing_lease = json.load(f)
                if not is_lease_stale(existing_lease):
                    logging.debug(f"Lease already exists for {task_id}")
                    fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)
                    return False
            
            # Create lease
            now = datetime.datetime.now(datetime.timezone.utc).isoformat()
            lease_data = {
                "task_id": task_id,
                "role": role,
                "owner": owner,
                "started_at": now,
                "ttl_seconds": 5400,  # 90 minutes
                "heartbeat_at": now
            }
            
            with open(lease_file, 'w') as f:
                json.dump(lease_data, f, indent=2)
            
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)
            logging.info(f"✅ Acquired lease for {task_id}")
            return True
            
    except Exception as e:
        logging.error(f"Error acquiring lease for {task_id}: {e}")
        return False
    finally:
        # Clean up lock file
        if lock_file.exists():
            try:
                lock_file.unlink()
            except Exception:
                pass


def update_heartbeat(task_id: str) -> None:
    """Update the heartbeat timestamp in the lease file."""
    lease_file = LEASES_DIR / f"{task_id}.json"
    
    try:
        if not lease_file.exists():
            return
        
        with open(lease_file, 'r') as f:
            lease_data = json.load(f)
        
        lease_data["heartbeat_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        with open(lease_file, 'w') as f:
            json.dump(lease_data, f, indent=2)
        
        logging.debug(f"Heartbeat updated for {task_id}")
    except Exception as e:
        logging.error(f"Error updating heartbeat for {task_id}: {e}")


def release_lease(task_id: str) -> None:
    """Release a lease by deleting the lease file."""
    lease_file = LEASES_DIR / f"{task_id}.json"
    
    try:
        if lease_file.exists():
            lease_file.unlink()
            logging.info(f"✅ Released lease for {task_id}")
    except Exception as e:
        logging.error(f"Error releasing lease for {task_id}: {e}")


def update_queue_status(task_id: str, status: str, agent: str = None) -> bool:
    """Update task status in the queue file."""
    try:
        queue_data = read_queue()
        if not queue_data:
            return False
        
        task_found = False
        for task in queue_data.get("tasks", []):
            if task.get("id") == task_id:
                task["status"] = status
                if agent:
                    task["agent"] = agent
                task_found = True
                break
        
        if not task_found:
            logging.error(f"Task {task_id} not found in queue")
            return False
        
        # Write updated queue
        with open(QUEUE_FILE, 'w') as f:
            json.dump(queue_data, f, indent=2)
        
        logging.info(f"Updated {task_id} status to '{status}'")
        return True
        
    except Exception as e:
        logging.error(f"Error updating queue status: {e}")
        return False


def execute_agent_prompt(role: str, task_id: str) -> bool:
    """
    Execute the agent prompt for the given role.
    
    This invokes Cursor/Claude with the appropriate prompt file.
    For autonomous operation, this would need integration with an LLM API.
    
    For now, this is a placeholder that logs the action.
    """
    prompt_file = PROMPTS_DIR / f"{role}.md"
    
    if not prompt_file.exists():
        logging.error(f"Prompt file not found: {prompt_file}")
        return False
    
    logging.info(f"🔨 Executing {role} prompt for {task_id}")
    logging.info(f"Prompt file: {prompt_file}")
    
    # TODO: Implement actual LLM integration
    # For now, this is a placeholder that simulates work
    # In production, this would call an LLM API or spawn a Cursor session
    
    logging.warning("⚠️  Autonomous execution not yet implemented")
    logging.warning("⚠️  Manual agent invocation still required")
    logging.warning(f"⚠️  Human must run: Load {prompt_file} and execute")
    
    return False  # Return False since we can't actually execute yet


def poll_and_claim(role: str, owner: str, ignore_wip: bool = False) -> Optional[str]:
    """
    Poll the queue and claim an available task.
    
    Returns task_id if a task was claimed, None otherwise.
    """
    queue_data = read_queue()
    if not queue_data:
        return None
    
    # Find ready task
    task = find_ready_task(queue_data, role, ignore_wip)
    if not task:
        logging.debug(f"No ready tasks for {role}")
        return None
    
    task_id = task.get("id")
    task_title = task.get("title", "Unknown")
    
    # Acquire lease
    if not acquire_lease(task_id, role, owner):
        logging.debug(f"Could not acquire lease for {task_id}")
        return None
    
    # Update queue status
    status_map = {
        "needs_plan": "planning",
        "ready": "in_progress",
        "awaiting_test": "testing",
        "needs_adapt": "adapting",
        "ready_for_integrator": "integrating"
    }
    new_status = status_map.get(task.get("status"), "in_progress")
    
    if not update_queue_status(task_id, new_status, role):
        release_lease(task_id)
        return None
    
    logging.info(f"✅ Claimed task: {task_id} - {task_title}")
    
    # Execute agent prompt (placeholder for now)
    execute_agent_prompt(role, task_id)
    
    return task_id


def daemon_loop(role: str, owner: str, interval: int, ignore_wip: bool = False) -> None:
    """
    Main daemon loop - polls queue at regular intervals.
    
    Only logs state changes (task claims, errors), not routine polls.
    """
    logging.info(f"Starting {role} daemon (interval: {interval}s, owner: {owner})")
    
    active_task: Optional[str] = None
    last_heartbeat = time.time()
    
    while not shutdown_requested:
        try:
            # Update heartbeat if we have an active task
            if active_task:
                if time.time() - last_heartbeat >= 60:
                    update_heartbeat(active_task)
                    last_heartbeat = time.time()
            
            # Try to claim work if we don't have an active task
            if not active_task:
                claimed_task = poll_and_claim(role, owner, ignore_wip)
                if claimed_task:
                    active_task = claimed_task
                    last_heartbeat = time.time()
            
            # Sleep for interval (check shutdown every second for responsiveness)
            for _ in range(interval):
                if shutdown_requested:
                    break
                time.sleep(1)
                
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt received")
            break
        except Exception as e:
            logging.error(f"Error in daemon loop: {e}")
            # Continue after error (resilient)
            time.sleep(interval)
    
    # Cleanup on shutdown
    if active_task:
        logging.info(f"Releasing active task lease: {active_task}")
        release_lease(active_task)
    
    logging.info(f"Daemon shutdown complete for {role}")


def main() -> None:
    """Main entry point for agent daemon."""
    parser = argparse.ArgumentParser(
        description="Agent daemon for autonomous work claiming"
    )
    parser.add_argument(
        "--role",
        required=True,
        choices=["planner", "builder", "tester", "refiner", "integrator"],
        help="Agent role (determines which tasks to claim)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Polling interval in seconds (default: 60)"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run once and exit (for testing)"
    )
    parser.add_argument(
        "--ignore-wip",
        action="store_true",
        help="Ignore WIP limits (for testing)"
    )
    parser.add_argument(
        "--owner",
        default="agent-daemon",
        help="Owner identifier for lease (default: agent-daemon)"
    )
    
    args = parser.parse_args()
    
    # Setup
    setup_logging(args.role)
    ensure_directories()
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Run once or daemon mode
    if args.once:
        logging.info(f"Running {args.role} daemon once (--once mode)")
        poll_and_claim(args.role, args.owner, args.ignore_wip)
    else:
        daemon_loop(args.role, args.owner, args.interval, args.ignore_wip)


if __name__ == "__main__":
    main()

