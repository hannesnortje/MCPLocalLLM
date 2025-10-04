# Background Agent Daemon System

**Status:** Production Ready  
**Version:** 1.0  
**Last Updated:** 2025-10-04

---

## Overview

The Background Agent Daemon System enables OODATCAA agents to run autonomously as background processes, automatically claiming and executing work from the sprint queue without manual intervention.

### Key Features

- **Autonomous Operation:** Agents poll the queue and claim work automatically
- **WIP Enforcement:** Respects work-in-progress limits per agent role
- **Lease Management:** Atomic task claiming prevents race conditions
- **Graceful Shutdown:** Clean shutdown handling (SIGTERM/SIGINT)
- **Systemd Integration:** Production-grade process management (Linux)
- **Fallback Mode:** CLI scripts for environments without systemd
- **State-Change Logging:** Efficient logging (only state changes, not polls)

---

## Quick Start

### Start All Agents (Systemd)

```bash
make agents-start
```

### Start Specific Agent

```bash
# Using systemd (Linux)
systemctl --user start agent-builder

# Using CLI (any platform)
bash scripts/agents-daemon-cli.sh start builder
```

### Check Status

```bash
make agents-status

# Or individual agent
systemctl --user status agent-builder
```

### Stop All Agents

```bash
make agents-stop
```

---

## Installation

### Prerequisites

- Python 3.11+
- Linux with systemd (recommended) OR any platform for CLI mode
- Project dependencies installed (`pip install -e ".[dev]"`)

### Systemd Installation (Linux)

```bash
cd systemd/
bash install-services.sh
```

This installs 5 user services (no root required):
- `agent-planner.service`
- `agent-builder.service`
- `agent-tester.service`
- `agent-refiner.service`
- `agent-integrator.service`

Services are installed to `~/.config/systemd/user/`

### CLI Mode (Cross-Platform)

No installation needed. Use `scripts/agents-daemon-cli.sh` directly:

```bash
bash scripts/agents-daemon-cli.sh start builder
bash scripts/agents-daemon-cli.sh stop builder
bash scripts/agents-daemon-cli.sh status builder
```

---

## Architecture

### Components

1. **agent-daemon.py** - Core daemon script
   - Queue polling (configurable interval, default 60s)
   - Atomic lease acquisition (fcntl.flock)
   - WIP limit checking
   - Graceful shutdown handling
   - Heartbeat updates

2. **agents-daemon-cli.sh** - CLI wrapper
   - PID-based process management
   - Start/stop/restart/status commands
   - Colored output for UX
   - Graceful shutdown with timeout

3. **Systemd Services** - Process management (Linux)
   - Auto-restart on failure
   - Journal integration
   - User services (no root)
   - Graceful shutdown

4. **Makefile Commands** - Convenience wrappers
   - `make agents-start` - Start all agents
   - `make agents-stop` - Stop all agents
   - `make agents-restart` - Restart all agents
   - `make agents-status` - Check status
   - Auto-detects systemd availability

### How It Works

```
┌─────────────────┐
│  Agent Daemon   │
│   (background)  │
└────────┬────────┘
         │
         ├─ Poll: Read SPRINT_QUEUE.json every 60s
         │
         ├─ Check: WIP limit < max?
         │
         ├─ Find: Ready task with satisfied dependencies?
         │
         ├─ Claim: Atomic lease acquisition (fcntl.flock)
         │
         ├─ Execute: Run agent prompt (TODO: LLM integration)
         │
         ├─ Update: Heartbeat every 60s
         │
         └─ Release: Clean lease on completion/error
```

---

## Configuration

### Daemon Options

```bash
python3 scripts/agent-daemon.py \
    --role builder \
    --interval 60 \
    --once  # Single run (for testing)
```

**Parameters:**
- `--role`: Agent role (planner, builder, tester, refiner, integrator)
- `--interval`: Poll interval in seconds (default: 60)
- `--once`: Run single iteration and exit (testing mode)

### WIP Limits

Configured in `.oodatcaa/work/SPRINT_QUEUE.json`:

```json
{
  "wip_limits": {
    "planner": 1,
    "builder": 3,
    "tester": 2,
    "refiner": 1,
    "integrator": 1
  }
}
```

---

## Usage Examples

### Development Testing

```bash
# Test single iteration (doesn't daemonize)
python3 scripts/agent-daemon.py --role builder --once

# Check logs
tail -f .agent-daemon-logs/builder.log
```

### Production Operation (Systemd)

```bash
# Start all agents
systemctl --user start agent-planner agent-builder agent-tester agent-refiner agent-integrator

# Check status
systemctl --user status agent-builder

# View logs
journalctl --user -u agent-builder -f

# Restart specific agent
systemctl --user restart agent-tester

# Stop all
systemctl --user stop agent-*
```

### Production Operation (CLI)

```bash
# Start all agents
for role in planner builder tester refiner integrator; do
    bash scripts/agents-daemon-cli.sh start $role
done

# Check status
bash scripts/agents-daemon-cli.sh status builder

# Stop all
for role in planner builder tester refiner integrator; do
    bash scripts/agents-daemon-cli.sh stop $role
done
```

---

## Monitoring

### Logs

**Systemd Mode:**
```bash
journalctl --user -u agent-builder -f
```

**CLI Mode:**
```bash
tail -f .agent-daemon-logs/builder.log
```

### Log Events

Daemons log only state changes (not routine polls):
- Task claimed
- Lease acquired/released
- WIP limit reached
- Errors
- Shutdown initiated

### Health Checks

```bash
# Check if daemon is running
systemctl --user is-active agent-builder

# Or with CLI
bash scripts/agents-daemon-cli.sh status builder

# Check recent activity
tail -20 .agent-daemon-logs/builder.log
```

---

## Troubleshooting

### Agent Not Claiming Work

**Check WIP Limit:**
```bash
# View current WIP
jq '.tasks[] | select(.agent == "builder" and .status == "in_progress") | .id' .oodatcaa/work/SPRINT_QUEUE.json | wc -l

# Compare to limit
jq '.wip_limits.builder' .oodatcaa/work/SPRINT_QUEUE.json
```

**Check Lease Files:**
```bash
ls -la .leases/
# Remove stale leases if needed (daemon stopped uncleanly)
```

**Check Queue:**
```bash
# Are there ready tasks with satisfied dependencies?
jq '.tasks[] | select(.type == "Build" and .status == "ready" and (.lease == null or .lease == ""))' .oodatcaa/work/SPRINT_QUEUE.json
```

### Daemon Won't Start

**Check Dependencies:**
```bash
python3 -c "import fcntl, json, logging"  # Should not error
```

**Check Permissions:**
```bash
ls -ld .oodatcaa/work .leases .locks
# All should be writable
```

**Check Logs:**
```bash
tail -50 .agent-daemon-logs/builder.log
```

### Stale Leases

If daemon crashes, leases may remain:

```bash
# List leases
ls -la .leases/

# Remove specific lease
rm .leases/P001-B03.json

# Remove all leases (caution!)
rm .leases/*.json
```

### Systemd Service Issues

**Service Won't Enable:**
```bash
systemctl --user daemon-reload
systemctl --user enable agent-builder
```

**Path Issues:**
- Edit `~/.config/systemd/user/agent-builder.service`
- Verify `WorkingDirectory` points to correct project root
- Run `systemctl --user daemon-reload`

---

## Limitations & Future Work

### Current Limitations

1. **Autonomous Execution Placeholder:**
   - Daemon claims tasks but doesn't yet execute agent prompts automatically
   - Requires LLM API integration for full autonomy
   - Currently logs warning: "Autonomous execution not yet implemented"

2. **Platform Support:**
   - Systemd mode requires Linux
   - macOS users must use CLI mode
   - Windows support untested

3. **Error Recovery:**
   - Task failures require manual intervention
   - No automatic retry logic yet

### Planned Enhancements

- **Phase 2:** LLM API integration for autonomous prompt execution
- **Phase 3:** Advanced error recovery (retry logic, exponential backoff)
- **Phase 4:** Cross-platform daemon management (launchd for macOS, Windows Service)
- **Phase 5:** Monitoring dashboard (real-time agent status, metrics)

---

## Testing

### Unit Tests

```bash
pytest tests/test_agent_daemon.py -v
```

Tests cover:
- Queue reading and parsing
- WIP limit enforcement
- Lease management
- Graceful shutdown
- Directory initialization

### Integration Testing

```bash
# Terminal 1: Start daemon in test mode
python3 scripts/agent-daemon.py --role builder --once

# Terminal 2: Watch queue
watch -n 2 'jq ".tasks[] | select(.status == \"in_progress\")" .oodatcaa/work/SPRINT_QUEUE.json'

# Verify task is claimed and lease created
ls -la .leases/
```

---

## Security

- **User Services:** Systemd services run as user (no root)
- **File Permissions:** Leases and locks use standard Unix permissions
- **Atomic Operations:** fcntl.flock prevents race conditions
- **No Network:** Daemon operates entirely on local filesystem

---

## Performance

- **Poll Interval:** 60s default (configurable)
- **CPU Usage:** Minimal (only active during polls)
- **Memory:** ~50MB per daemon
- **Disk I/O:** Low (state-change logging only)

---

## References

- **Core Daemon:** `scripts/agent-daemon.py`
- **CLI Wrapper:** `scripts/agents-daemon-cli.sh`
- **Systemd Services:** `systemd/*.service`
- **Installation:** `systemd/install-services.sh`
- **Tests:** `tests/test_agent_daemon.py`
- **Sprint Task:** P001 (Background Agent Daemon System)

---

**For questions or issues, refer to CONTRIBUTING.md or open an issue.**

