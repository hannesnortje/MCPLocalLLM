# OODATCAA Troubleshooting Guide

**Version:** 1.0  
**Last Updated:** 2025-10-04  
**Status:** Production Ready

---

## Table of Contents

- [How to Use This Guide](#how-to-use-this-guide)
- [Agent Issues](#agent-issues)
- [System Issues](#system-issues)
- [Process Issues](#process-issues)
- [Quick Diagnostics](#quick-diagnostics)

---

## How to Use This Guide

**Issue Format:**
- **Symptoms:** What you observe
- **Diagnosis:** How to investigate
- **Solution:** Steps to resolve
- **Prevention:** How to avoid recurring

**Severity Levels:**
- 🟢 **Low:** Minor inconvenience, workarounds available
- 🟡 **Medium:** Impacts productivity, needs resolution
- 🔴 **High:** Blocks work, requires immediate action
- 🚨 **Critical:** System failure, emergency procedures needed

---

## Agent Issues

### Issue 1: Agent Won't Claim Work 🟡

**Symptoms:**
- Background agent running but no tasks claimed
- Daemon logs show polling but no activity
- Tasks remain in `ready` status

**Diagnosis:**
```bash
# Check WIP limits
jq '{wip_limits, in_progress: [.tasks[] | select(.status == "in_progress") | {id, agent}]}' .oodatcaa/work/SPRINT_QUEUE.json

# Check if tasks truly ready
jq '.tasks[] | select(.status == "ready" and (.lease == null or .lease == "")) | {id, dependencies}' .oodatcaa/work/SPRINT_QUEUE.json

# Check daemon logs
tail -50 .agent-daemon-logs/builder.log
```

**Solution:**
1. **If WIP at limit:**
   ```bash
   # Release stale leases (see Issue 5)
   ```

2. **If dependencies not met:**
   ```bash
   # Check dependency status
   jq '.tasks[] | select(.id == "<dep-id>") | {id, status}' .oodatcaa/work/SPRINT_QUEUE.json
   
   # Complete or unblock dependencies
   ```

3. **If JSON corrupted:**
   ```bash
   jq empty .oodatcaa/work/SPRINT_QUEUE.json || \
   cp .oodatcaa/work/SPRINT_QUEUE.json.backup .oodatcaa/work/SPRINT_QUEUE.json
   ```

4. **If agent role mismatch:**
   ```bash
   # Verify task.agent matches daemon role
   jq '.tasks[] | select(.status == "ready") | {id, agent}' .oodatcaa/work/SPRINT_QUEUE.json
   ```

**Prevention:**
- Regular WIP monitoring (`make sprint-dashboard`)
- Automated lease cleanup (TTL enforcement)
- JSON validation in CI/CD
- Clear dependency management

**See Also:** [RUNBOOK: Scenario 9 - WIP Limits](RUNBOOK.md#scenario-9-checking-agent-wip-limits)

---

### Issue 2: Agent Crashes During Execution 🔴

**Symptoms:**
- Agent process terminates unexpectedly
- Task stuck in `in_progress`
- Lease exists but no heartbeat

**Diagnosis:**
```bash
# Check recent crash logs
tail -100 .agent-daemon-logs/<role>.log | grep -i "error\|exception\|traceback"

# Check system logs (if systemd)
journalctl --user -u agent-<role> -n 100

# Check for core dumps
ls -lh core* 2>/dev/null

# Check system resources
df -h .
free -h
```

**Solution:**
1. **Release stuck task:**
   ```bash
   # Remove lease
   rm .leases/<task-id>.json
   
   # Reset task
   jq '.tasks |= map(if .id == "<task-id>" then .status = "ready" | .lease = null else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

2. **Fix underlying cause:**
   - **Out of memory:** Increase system RAM or reduce WIP
   - **Disk full:** Clean up old archives, logs
   - **Python error:** Install missing dependencies, fix code
   - **Network timeout:** Check API endpoints, increase timeouts

3. **Restart agent:**
   ```bash
   make agents-restart
   ```

**Prevention:**
- Monitor system resources
- Set appropriate WIP limits for system capacity
- Implement heartbeat monitoring
- Add agent health checks
- Log rotation to prevent disk issues

**See Also:** [RUNBOOK: Scenario 19 - Debugging Agent Failures](RUNBOOK.md#scenario-19-debugging-agent-failures)

---

### Issue 3: Agent Produces Invalid Output 🟡

**Symptoms:**
- Test failures on valid code
- Malformed JSON in queue updates
- Incomplete deliverables

**Diagnosis:**
```bash
# Check agent report
cat .oodatcaa/work/reports/<story>/<agent>_<task>.md

# Check branch commits
git log feat/<task-id>... --oneline

# Check for partial work
git diff main...feat/<task-id> --stat

# Validate JSON changes
git show feat/<task-id>:.oodatcaa/work/SPRINT_QUEUE.json | jq empty
```

**Solution:**
1. **If prompt misunderstood:**
   - Review agent prompt clarity
   - Add examples to prompt
   - Refine acceptance criteria

2. **If partial completion:**
   ```bash
   # Call refiner
   # Update task status to needs_adapt
   jq '.tasks |= map(if .id == "<task-id>" then .status = "needs_adapt" else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

3. **If JSON errors:**
   ```bash
   # Fix JSON manually
   nano .oodatcaa/work/SPRINT_QUEUE.json
   jq empty .oodatcaa/work/SPRINT_QUEUE.json  # Validate
   ```

**Prevention:**
- Clear acceptance criteria in plans
- Examples in agent prompts
- Quality gates before status updates
- Automated JSON validation
- Agent output templates

**See Also:** [RUNBOOK: Scenario 13 - Updating Agent Prompts](RUNBOOK.md#scenario-13-updating-agent-prompts)

---

### Issue 4: Agent Ignores Instructions 🟡

**Symptoms:**
- Agent does work not in plan
- Skips required steps
- Delivers wrong artifacts

**Diagnosis:**
```bash
# Compare delivered vs planned
cat .oodatcaa/work/AGENT_PLAN.md | grep "Step <N>"
cat .oodatcaa/work/reports/<story>/<agent>_<task>.md | grep "Deliverables"

# Check if plan overwritten
head -20 .oodatcaa/work/AGENT_PLAN.md

# Check agent logs for plan reading
grep "READ PLAN" .oodatcaa/work/AGENT_LOG.md | tail -10
```

**Solution:**
1. **If plan missing/overwritten:**
   ```bash
   # Restore plan from git
   git log --all --oneline -- .oodatcaa/work/AGENT_PLAN.md
   git show <commit>:.oodatcaa/work/AGENT_PLAN.md > .oodatcaa/work/AGENT_PLAN.md
   
   # OR call planner to recreate
   ```

2. **If agent context limited:**
   - Ensure agent loaded current plan
   - Check if agent has access to files
   - Verify agent context window not exceeded

3. **If prompt ambiguous:**
   - Clarify builder protocol
   - Add explicit step-by-step guidance
   - Include verification checkpoints

**Prevention:**
- Don't overwrite AGENT_PLAN.md for new stories
- Use plan versioning or separate files
- Explicit plan loading in agent protocol
- Verification: agent must confirm plan read

**See Also:** [RUNBOOK: Scenario 7 - Running Agent Manually](RUNBOOK.md#scenario-7-running-agent-manually)

---

### Issue 5: Stale Lease Blocks Task 🟡

**Symptoms:**
- Task marked `in_progress` but no activity
- Lease file exists for crashed agent
- WIP at limit due to ghost tasks

**Diagnosis:**
```bash
# List all leases
ls -lh .leases/

# Check lease age
stat .leases/<task-id>.json

# Check lease details
cat .leases/<task-id>.json | jq '{acquired, ttl, last_heartbeat}'

# Check if agent still running
ps aux | grep agent-daemon | grep <role>

# Check recent agent activity
grep "<task-id>" .oodatcaa/work/AGENT_LOG.md | tail -20
```

**Solution:**
1. **If lease expired (age > TTL):**
   ```bash
   rm .leases/<task-id>.json
   
   jq '.tasks |= map(if .id == "<task-id>" then .status = "ready" | .lease = null else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

2. **If agent still active:**
   - Check agent logs for progress
   - If stalled, stop agent gracefully
   - Release lease after stop

3. **Clear all stale leases:**
   ```bash
   # CAUTION: Only if no agents running
   make agents-stop
   rm .leases/*.json
   
   jq '.tasks |= map(if .status == "in_progress" then .status = "ready" | .lease = null else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

**Prevention:**
- Graceful agent shutdown (SIGTERM not SIGKILL)
- Automated lease expiry checks
- Health monitoring for agents
- Lower TTL values for faster recovery

**See Also:** [RUNBOOK: Scenario 10 - Managing Task Leases](RUNBOOK.md#scenario-10-managing-task-leases)

---

### Issue 6: Multiple Agents Claim Same Task 🔴

**Symptoms:**
- Race condition: Two agents working on same task
- Conflicting branches for same task
- Duplicate lease files

**Diagnosis:**
```bash
# Check for duplicate leases
ls -lh .leases/ | grep <task-id>

# Check SPRINT_QUEUE for task
jq '.tasks[] | select(.id == "<task-id>")' .oodatcaa/work/SPRINT_QUEUE.json

# Check git branches
git branch -a | grep <task-id>

# Check agent logs for timing
grep "<task-id>" .oodatcaa/work/AGENT_LOG.md | grep "LEASE"
```

**Solution:**
1. **Stop all agents immediately:**
   ```bash
   make agents-stop
   ```

2. **Identify which agent has valid work:**
   ```bash
   # Check both branches
   git log feat/<task-id>-agent1 --oneline
   git log feat/<task-id>-agent2 --oneline
   
   # Compare work quality
   git diff feat/<task-id>-agent1...main
   git diff feat/<task-id>-agent2...main
   ```

3. **Keep best work, discard duplicate:**
   ```bash
   # Delete redundant branch
   git branch -D feat/<task-id>-agent2
   git push origin :feat/<task-id>-agent2
   
   # Clean up leases
   rm .leases/<task-id>*.json
   
   # Update queue with valid lease
   ```

4. **Fix race condition cause:**
   - Verify fcntl.flock working correctly
   - Check NFS/networked filesystem issues (use local disk for .leases)
   - Review daemon lease acquisition logic

**Prevention:**
- Use local filesystem for .leases (not NFS)
- Atomic lease acquisition with fcntl.flock
- Lease ownership validation before work
- Lower poll intervals increase race risk - keep at 60s minimum

**See Also:** [BACKGROUND_AGENTS.md - Lease Management](../docs/BACKGROUND_AGENTS.md#lease-management)

---

### Issue 7: Agent Protocol Out of Date 🟡

**Symptoms:**
- Agent doesn't follow new procedures
- Missing steps in execution
- Outdated behavior after prompt update

**Diagnosis:**
```bash
# Check prompt version
grep "Version:" .oodatcaa/prompts/<agent>.md

# Check when last updated
git log -1 --format="%ai" -- .oodatcaa/prompts/<agent>.md

# Check if agents restarted since update
journalctl --user -u agent-<role> --since "$(git log -1 --format='%ai' -- .oodatcaa/prompts/<agent>.md)"
```

**Solution:**
1. **Restart agents to load new prompts:**
   ```bash
   make agents-restart
   ```

2. **For manual execution:**
   - Reload prompt in IDE
   - Clear context/cache
   - Re-run from fresh state

3. **Verify prompt loaded:**
   ```bash
   # Check agent logs for protocol version
   grep "BUILDER PROTOCOL" .oodatcaa/work/AGENT_LOG.md | tail -5
   ```

**Prevention:**
- Version prompts explicitly
- Automated agent restart on prompt changes
- Prompt checksum validation
- Agent reports must include protocol version

**See Also:** [RUNBOOK: Scenario 13 - Updating Agent Prompts](RUNBOOK.md#scenario-13-updating-agent-prompts)

---

### Issue 8: Integrator Can't Merge Branch 🟡

**Symptoms:**
- Merge conflicts
- Branch behind main
- CI/CD failures blocking merge

**Diagnosis:**
```bash
# Check branch status
git checkout feat/<task-id>
git fetch origin
git status

# Check for conflicts
git merge origin/main --no-commit --no-ff

# Check CI status
git log feat/<task-id> --oneline
```

**Solution:**
1. **If branch behind main:**
   ```bash
   git checkout feat/<task-id>
   git rebase origin/main
   # Resolve conflicts if any
   git push --force-with-lease origin feat/<task-id>
   ```

2. **If conflicts exist:**
   ```bash
   git merge origin/main
   # Manually resolve conflicts
   git add .
   git commit -m "[merge] Resolve conflicts with main"
   git push origin feat/<task-id>
   ```

3. **If CI failing:**
   ```bash
   # Run local quality gates
   make test
   
   # Fix issues
   git add .
   git commit -m "[fix] Address CI failures"
   git push origin feat/<task-id>
   ```

4. **If unsolvable, call refiner:**
   ```bash
   jq '.tasks |= map(if .id == "<task-id>" then .status = "needs_adapt" else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

**Prevention:**
- Regular rebasing on long-lived branches
- Smaller task scopes (faster integration)
- Pre-merge quality gates
- Branch protection rules

**See Also:** [BRANCH_PROTECTION.md](../docs/BRANCH_PROTECTION.md)

---

### Issue 9: Tester Reports False Failures 🟡

**Symptoms:**
- Tests fail but code is correct
- Flaky test results
- Environment-specific failures

**Diagnosis:**
```bash
# Check test report
cat .oodatcaa/work/reports/<story>/tester_<task>.md

# Review test execution logs
grep "pytest\|test" .oodatcaa/work/AGENT_LOG.md | tail -50

# Re-run tests locally
pytest tests/ -v

# Check for environment differences
cat .oodatcaa/work/reports/<story>/tester_<task>.md | grep "Environment\|Python\|Dependencies"
```

**Solution:**
1. **If environment issue:**
   ```bash
   # Ensure dev dependencies installed
   pip install -e ".[dev]"
   
   # Verify Python version
   python3 --version  # Should be 3.11+
   ```

2. **If flaky tests:**
   ```bash
   # Run multiple times
   for i in {1..5}; do pytest tests/test_<module>.py; done
   
   # Identify flaky test
   # Fix timing issues, race conditions
   ```

3. **If tester misinterpreted AC:**
   - Review acceptance criteria with planner
   - Update TEST_PLAN.md if needed
   - Retest with corrected criteria

4. **If false positive, mark for integration:**
   ```bash
   jq '.tasks |= map(if .id == "<task-id>" then .status = "ready_for_integrator" else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

**Prevention:**
- Deterministic tests (no random, timing dependencies)
- Clear acceptance criteria
- Environment standardization
- Test environment documentation

**See Also:** [RUNBOOK: Scenario 4 - Viewing Agent Activity](RUNBOOK.md#scenario-4-viewing-agent-activity)

---

### Issue 10: Planner Creates Infeasible Plans 🟡

**Symptoms:**
- Estimates vastly wrong
- Dependencies circular or missing
- Plan steps don't match task scope

**Diagnosis:**
```bash
# Review plan
cat .oodatcaa/work/AGENT_PLAN.md

# Check estimates vs actuals
jq '.tasks[] | select(.parent == "<story>") | {id, estimated_time, actual_time}' .oodatcaa/work/SPRINT_QUEUE.json

# Check dependencies
jq '.tasks[] | select(.parent == "<story>") | {id, dependencies}' .oodatcaa/work/SPRINT_QUEUE.json
```

**Solution:**
1. **If circular dependencies:**
   ```bash
   # Manually fix in SPRINT_QUEUE.json
   nano .oodatcaa/work/SPRINT_QUEUE.json
   # Remove circular dep, update dependencies array
   ```

2. **If estimates way off:**
   - Update task complexity
   - Adjust estimated_time in queue
   - Provide feedback to planner for future

3. **If plan doesn't match scope:**
   - Call planner to revise plan
   - Update AGENT_PLAN.md
   - May need to cancel and re-plan task

4. **If tasks can't proceed:**
   ```bash
   # Block infeasible tasks
   jq '.tasks |= map(if .parent == "<story>" then .status = "blocked" | .blocked_reason = "Plan revision needed" else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   
   # Call negotiator to re-plan
   ```

**Prevention:**
- Planner reviews similar past tasks for estimation
- Clear story requirements before planning
- Dependencies validation in planner protocol
- Historical data for estimate improvement

**See Also:** [RUNBOOK: Scenario 3 - Checking Sprint Status](RUNBOOK.md#scenario-3-checking-sprint-status)

---

## System Issues

### Issue 11: SPRINT_QUEUE.json Corrupted 🔴

**Symptoms:**
- `jq` parsing errors
- Agents can't read queue
- System halted

**Diagnosis:**
```bash
# Validate JSON
jq empty .oodatcaa/work/SPRINT_QUEUE.json

# Check file size (should be >5KB typically)
ls -lh .oodatcaa/work/SPRINT_QUEUE.json

# Check last modification
stat .oodatcaa/work/SPRINT_QUEUE.json

# Check git status
git status .oodatcaa/work/SPRINT_QUEUE.json
```

**Solution:**
1. **Restore from backup:**
   ```bash
   cp .oodatcaa/work/SPRINT_QUEUE.json.backup .oodatcaa/work/SPRINT_QUEUE.json
   ```

2. **Restore from git:**
   ```bash
   git checkout HEAD -- .oodatcaa/work/SPRINT_QUEUE.json
   ```

3. **Restore from recent commit:**
   ```bash
   git log --oneline -- .oodatcaa/work/SPRINT_QUEUE.json | head -5
   git show <commit>:.oodatcaa/work/SPRINT_QUEUE.json > .oodatcaa/work/SPRINT_QUEUE.json
   ```

4. **Reconstruct from agent reports (last resort):**
   ```bash
   # Manually rebuild queue from reports and logs
   # Use previous commit as template
   # Update task statuses from AGENT_LOG.md
   ```

**Prevention:**
- Automated backups before queue updates
- Git commit after each change
- JSON validation before write
- Atomic writes (write to temp, then rename)
- Regular git pushes

**See Also:** [RUNBOOK: Scenario 16 - System Recovery](RUNBOOK.md#scenario-16-recovering-from-system-failure)

---

### Issue 12: Git Conflicts in Work Files 🟡

**Symptoms:**
- Merge conflicts in `.oodatcaa/work/`
- Git pull fails
- Diverged branches

**Diagnosis:**
```bash
git status
git log --oneline --graph origin/main...main
git diff origin/main...main -- .oodatcaa/work/
```

**Solution:**
1. **For SPRINT_QUEUE.json conflicts:**
   ```bash
   # Take remote version (if local not pushed)
   git checkout --theirs .oodatcaa/work/SPRINT_QUEUE.json
   
   # OR take local version
   git checkout --ours .oodatcaa/work/SPRINT_QUEUE.json
   
   # OR merge manually (preserve both sets of changes)
   nano .oodatcaa/work/SPRINT_QUEUE.json
   # Validate JSON
   jq empty .oodatcaa/work/SPRINT_QUEUE.json
   ```

2. **For log files (AGENT_LOG.md, SPRINT_LOG.md):**
   ```bash
   # Take both versions (logs are append-only)
   git show :1:.oodatcaa/work/AGENT_LOG.md > /tmp/base.md
   git show :2:.oodatcaa/work/AGENT_LOG.md > /tmp/ours.md
   git show :3:.oodatcaa/work/AGENT_LOG.md > /tmp/theirs.md
   
   # Merge manually (take both entries chronologically)
   # Or accept one version if sync failed
   ```

3. **Complete merge:**
   ```bash
   git add .oodatcaa/work/
   git commit -m "[merge] Resolve work file conflicts"
   git push origin main
   ```

**Prevention:**
- Frequent git pulls before starting work
- Push tracking changes immediately
- Single writer principle (only active agent writes)
- Lock files for critical sections
- Branch-based work (not all on main)

**See Also:** [BRANCH_PROTECTION.md](../docs/BRANCH_PROTECTION.md)

---

### Issue 13: Disk Space Full 🔴

**Symptoms:**
- Write errors
- Agents crash
- Log rotation fails

**Diagnosis:**
```bash
df -h .
du -sh .oodatcaa/work/
du -sh .agent-daemon-logs/
du -sh .git/
```

**Solution:**
1. **Clean up logs:**
   ```bash
   # Compress old archives
   gzip .oodatcaa/work/archive/sprint_1/*.md
   
   # Compress daemon logs
   gzip .agent-daemon-logs/*.log.old
   
   # Rotate logs immediately
   bash scripts/rotate-logs.sh
   ```

2. **Clean git objects:**
   ```bash
   git gc --aggressive --prune=now
   ```

3. **Remove build artifacts:**
   ```bash
   rm -rf dist/ build/ *.egg-info
   find . -type d -name __pycache__ -exec rm -rf {} +
   ```

4. **Archive and remove old sprints:**
   ```bash
   # Archive to external storage
   tar -czf sprint_1_archive.tar.gz .oodatcaa/work/archive/sprint_1/
   # Move to external storage
   # Remove local copy
   rm -rf .oodatcaa/work/archive/sprint_1/
   ```

**Prevention:**
- Regular log rotation
- Automated cleanup scripts
- Disk space monitoring
- Archive old sprints to external storage
- Set up disk space alerts

**See Also:** [RUNBOOK: Scenario 15 - Archiving Logs](RUNBOOK.md#scenario-15-archiving-logs)

---

### Issue 14: High CPU Usage by Agents 🟡

**Symptoms:**
- System slow
- Agent daemons consuming excessive CPU
- Laptop/desktop unresponsive

**Diagnosis:**
```bash
# Check CPU usage
top -p $(pgrep -d',' agent-daemon)

# Check agent activity
ps aux | grep agent-daemon

# Check polling frequency
grep "interval" .agent-daemon-logs/*.log | tail -20

# Check for infinite loops
strace -p $(pgrep agent-daemon | head -1)
```

**Solution:**
1. **If poll interval too low:**
   ```bash
   # Stop agents
   make agents-stop
   
   # Edit daemon command to increase interval
   nano scripts/agent-daemon.py  # Or systemd service file
   # Change default from 60s to 120s
   
   # Restart agents
   make agents-start
   ```

2. **If agent stuck in loop:**
   ```bash
   # Kill problematic agent
   pkill -f "agent-daemon.*<role>"
   
   # Check logs for cause
   tail -100 .agent-daemon-logs/<role>.log
   
   # Fix issue, restart agent
   ```

3. **If too many agents for system:**
   ```bash
   # Reduce WIP limits
   jq '.wip_limits = {planner: 1, builder: 1, tester: 1, refiner: 0, integrator: 0}' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   
   # Run fewer agents
   make agents-stop
   systemctl --user start agent-builder agent-tester
   ```

**Prevention:**
- Appropriate poll intervals (60-120s)
- WIP limits matched to system capacity
- Agent health monitoring
- Resource limits (systemd MemoryMax, CPUQuota)

**See Also:** [BACKGROUND_AGENTS.md - Performance](../docs/BACKGROUND_AGENTS.md#performance)

---

### Issue 15: Permission Denied Errors 🟡

**Symptoms:**
- Agents can't write files
- Lease creation fails
- Log updates blocked

**Diagnosis:**
```bash
# Check permissions
ls -ld .oodatcaa/work .leases .locks
ls -l .oodatcaa/work/SPRINT_QUEUE.json

# Check ownership
ls -l .oodatcaa/work/AGENT_LOG.md | awk '{print $3, $4}'

# Check for read-only mounts
mount | grep $(pwd)
```

**Solution:**
1. **Fix permissions:**
   ```bash
   chmod -R u+w .oodatcaa/work/
   chmod -R u+w .leases/
   chmod -R u+w .locks/
   ```

2. **Fix ownership (if needed):**
   ```bash
   chown -R $USER:$USER .oodatcaa/work/
   ```

3. **If on read-only mount:**
   - Move .leases and .locks to /tmp or home directory
   - Update paths in agent-daemon.py
   - Use symbolic links

**Prevention:**
- Proper setup script permissions
- Run agents as same user who owns files
- Avoid running as root
- Check filesystem mount options

**See Also:** [RUNBOOK: Scenario 12 - Validating Configuration](RUNBOOK.md#scenario-12-validating-configuration)

---

### Issue 16: Missing Dependencies 🟡

**Symptoms:**
- Import errors in agents
- Quality gates fail
- Tools not found (jq, git, pytest)

**Diagnosis:**
```bash
# Check Python imports
python3 -c "import json, fcntl, logging, subprocess"

# Check system tools
which jq git python3 make

# Check Python packages
pip list | grep -E "(pytest|black|ruff|mypy)"

# Run validation
make validate-env
```

**Solution:**
1. **Install system dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install jq git python3 python3-pip make
   
   # macOS
   brew install jq git python3 make
   ```

2. **Install Python dependencies:**
   ```bash
   # Development dependencies
   pip install -e ".[dev]"
   
   # OR minimal dependencies
   pip install pytest black ruff mypy
   ```

3. **Run setup script:**
   ```bash
   ./scripts/setup-dev.sh
   ```

**Prevention:**
- Document all dependencies
- Automated setup scripts
- Dependency version pinning
- CI/CD dependency caching
- Environment validation before starting work

**See Also:** [ONBOARDING.md - Setup](ONBOARDING.md#environment-setup), [RUNBOOK: Scenario 12](RUNBOOK.md#scenario-12-validating-configuration)

---

### Issue 17: Slow System Performance 🟡

**Symptoms:**
- Commands take long to execute
- Dashboard generation slow
- Git operations sluggish

**Diagnosis:**
```bash
# Check disk I/O
iostat 1 5

# Check for large files
find . -type f -size +10M -exec ls -lh {} \;

# Check git repo size
du -sh .git/

# Check log file sizes
du -sh .oodatcaa/work/*.md

# Profile command
time make sprint-dashboard
```

**Solution:**
1. **Optimize git:**
   ```bash
   git gc --aggressive
   git repack -Ad
   ```

2. **Rotate logs:**
   ```bash
   bash scripts/rotate-logs.sh
   ```

3. **Clean up:**
   ```bash
   # Remove old branches
   git branch -d $(git branch --merged | grep -v main)
   
   # Compress archives
   find .oodatcaa/work/archive/ -name "*.md" -exec gzip {} \;
   ```

4. **Optimize jq queries:**
   ```bash
   # Use jq streaming for large files
   jq -c '.tasks[]' .oodatcaa/work/SPRINT_QUEUE.json | grep "ready"
   ```

**Prevention:**
- Regular maintenance (weekly cleanup)
- Log rotation automation
- Git repo pruning
- Monitor file sizes
- Efficient queries (avoid loading entire files if possible)

**See Also:** [RUNBOOK: Scenario 14 - Managing Log Files](RUNBOOK.md#scenario-14-managing-log-files)

---

### Issue 18: Network/API Failures 🟡

**Symptoms:**
- LLM API timeouts
- Git push/pull fails
- External service unavailable

**Diagnosis:**
```bash
# Test network connectivity
ping -c 3 8.8.8.8

# Test git remote
git ls-remote origin

# Check API status (if applicable)
curl -I https://api.example.com/health

# Check for proxy issues
echo $HTTP_PROXY $HTTPS_PROXY
```

**Solution:**
1. **Retry failed operations:**
   ```bash
   # Git operations
   git pull --rebase origin main
   
   # Agent operations (will auto-retry on next poll)
   # OR run manually with retry logic
   ```

2. **Check credentials:**
   ```bash
   # Git credentials
   git config --get-regexp credential
   
   # API keys
   cat .env | grep API_KEY
   ```

3. **Use offline mode:**
   ```bash
   # Manual agent execution without external APIs
   # Use cached/local models if available
   ```

**Prevention:**
- Network monitoring
- Retry logic in critical operations
- Graceful degradation (offline mode)
- Credential management system
- Timeout configuration

**See Also:** [RUNBOOK: Scenario 19 - Debugging Agent Failures](RUNBOOK.md#scenario-19-debugging-agent-failures)

---

### Issue 19: Systemd Service Won't Start 🟡

**Symptoms:**
- `systemctl start` fails
- Service immediately exits
- Service status shows "failed"

**Diagnosis:**
```bash
# Check service status
systemctl --user status agent-builder

# View logs
journalctl --user -u agent-builder -n 50

# Check service file
cat ~/.config/systemd/user/agent-builder.service

# Verify paths
ls -l $(grep ExecStart ~/.config/systemd/user/agent-builder.service | awk '{print $2}')

# Check WorkingDirectory
cd $(grep WorkingDirectory ~/.config/systemd/user/agent-builder.service | awk -F= '{print $2}')
pwd
```

**Solution:**
1. **Fix paths in service file:**
   ```bash
   nano ~/.config/systemd/user/agent-builder.service
   
   # Update WorkingDirectory to correct project path
   # Update ExecStart with absolute paths
   
   systemctl --user daemon-reload
   systemctl --user start agent-builder
   ```

2. **If permissions issue:**
   ```bash
   chmod +x scripts/agent-daemon.py
   chmod +x scripts/agents-daemon-cli.sh
   ```

3. **If Python not found:**
   ```bash
   # Use absolute path to Python
   which python3
   # Update ExecStart with full path
   ```

4. **Reinstall service:**
   ```bash
   cd systemd/
   bash uninstall-services.sh
   bash install-services.sh
   ```

**Prevention:**
- Use absolute paths in service files
- Test service files before installation
- Version control systemd service files
- Document installation process

**See Also:** [BACKGROUND_AGENTS.md - Installation](../docs/BACKGROUND_AGENTS.md#installation)

---

## Process Issues

### Issue 20: Sprint Won't Initialize 🟡

**Symptoms:**
- `make sprint-new` fails
- Previous sprint still active
- Objective file missing

**Diagnosis:**
```bash
# Check current sprint status
make sprint-dashboard

# Check for incomplete tasks
jq '.tasks[] | select(.status != "done" and .status != "cancelled")' .oodatcaa/work/SPRINT_QUEUE.json

# Check objectives
ls -l .oodatcaa/objectives/SPRINT_GOAL.md

# Check git status
git status
```

**Solution:**
1. **Complete previous sprint first:**
   ```bash
   make sprint-complete
   ```

2. **Force sprint initialization (if previous lost/corrupted):**
   ```bash
   # Backup current state
   cp .oodatcaa/work/SPRINT_QUEUE.json .oodatcaa/work/SPRINT_QUEUE.json.backup-old
   
   # Initialize new sprint manually
   jq '.sprint = (.sprint + 1) | .sprint_id = "SPRINT-2025-\(.sprint | tostring | .[6:])" | .tasks = []' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

3. **Create missing objective:**
   ```bash
   nano .oodatcaa/objectives/SPRINT_GOAL.md
   # Add sprint goals, success criteria, exit criteria
   ```

**Prevention:**
- Complete sprints properly before starting new ones
- Don't manually edit sprint numbers
- Maintain objective files
- Use sprint-complete and sprint-new commands

**See Also:** [RUNBOOK: Scenario 1 - Starting a New Sprint](RUNBOOK.md#scenario-1-starting-a-new-sprint)

---

### Issue 21: Sprint Won't Complete 🟡

**Symptoms:**
- `make sprint-complete` fails
- Incomplete tasks blocking
- Archive creation errors

**Diagnosis:**
```bash
# Check task statuses
jq '.tasks | group_by(.status) | map({status: .[0].status, count: length})' .oodatcaa/work/SPRINT_QUEUE.json

# List incomplete tasks
jq '.tasks[] | select(.status != "done" and .status != "cancelled") | {id, title, status}' .oodatcaa/work/SPRINT_QUEUE.json

# Check archive directory
ls -ld .oodatcaa/work/archive/sprint_$(jq '.sprint' .oodatcaa/work/SPRINT_QUEUE.json)/

# Check for write permissions
touch .oodatcaa/work/archive/test && rm .oodatcaa/work/archive/test
```

**Solution:**
1. **Complete or cancel remaining tasks:**
   ```bash
   # Cancel non-essential tasks
   jq '.tasks |= map(if .id == "<task-id>" then .status = "cancelled" else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   
   # OR complete tasks manually
   ```

2. **Force completion (if tasks can't be completed):**
   ```bash
   # Mark all as done (CAUTION)
   jq '.tasks |= map(if .status != "done" and .status != "cancelled" then .status = "cancelled" | .blocked_reason = "Sprint force-completed" else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   
   # Now complete sprint
   make sprint-complete
   ```

3. **Fix archive directory:**
   ```bash
   mkdir -p .oodatcaa/work/archive/sprint_$(jq '.sprint' .oodatcaa/work/SPRINT_QUEUE.json)/
   chmod -R u+w .oodatcaa/work/archive/
   ```

**Prevention:**
- Complete all tasks before sprint-complete
- Clear exit criteria in SPRINT_GOAL.md
- Regular sprint status reviews
- Don't leave sprints open indefinitely

**See Also:** [RUNBOOK: Scenario 2 - Completing a Sprint](RUNBOOK.md#scenario-2-completing-a-sprint)

---

### Issue 22: Dependency Deadlock 🔴

**Symptoms:**
- No tasks can proceed
- All ready tasks blocked by dependencies
- Circular dependency detected

**Diagnosis:**
```bash
# Check dependencies
jq '.tasks[] | {id, status, dependencies}' .oodatcaa/work/SPRINT_QUEUE.json

# Find circular dependencies
# Task A depends on B, B depends on A
jq '.tasks | map({id, deps: .dependencies[]}) | group_by(.deps) | map(select(length > 1))' .oodatcaa/work/SPRINT_QUEUE.json

# Find blocked tasks
jq '.tasks[] | select(.status == "blocked") | {id, blocked_reason, dependencies}' .oodatcaa/work/SPRINT_QUEUE.json
```

**Solution:**
1. **Break circular dependency:**
   ```bash
   # Manually remove one dependency
   jq '.tasks |= map(if .id == "<task-A>" then .dependencies = (.dependencies - ["<task-B>"]) else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

2. **Unblock tasks manually:**
   ```bash
   # If dependency isn't really needed
   jq '.tasks |= map(if .id == "<task-id>" then .status = "ready" | .blocked_reason = null else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

3. **Replan story:**
   ```bash
   # Cancel deadlocked tasks
   # Call planner to create new plan with correct dependencies
   ```

**Prevention:**
- Planner validates dependencies (no cycles)
- Dependency graph visualization
- Regular dependency audits
- Keep dependency chains short

**See Also:** [RUNBOOK: Scenario 3 - Checking Sprint Status](RUNBOOK.md#scenario-3-checking-sprint-status)

---

### Issue 23: Task Stuck in needs_adapt 🟡

**Symptoms:**
- Task marked needs_adapt but no refiner action
- Multiple adaptation cycles
- Unclear how to fix

**Diagnosis:**
```bash
# Check task status
jq '.tasks[] | select(.id == "<task-id>")' .oodatcaa/work/SPRINT_QUEUE.json

# Check tester report
cat .oodatcaa/work/reports/<story>/tester_<task>.md

# Check refiner attempts
find .oodatcaa/work/reports/<story>/ -name "refiner*"

# Check branch state
git log feat/<task-id>... --oneline
```

**Solution:**
1. **Call refiner:**
   ```bash
   # Ensure task accessible by refiner
   # Refiner will analyze and adapt or recommend restart
   ```

2. **If too many adapt cycles (>3):**
   ```bash
   # Trigger Start-Over Gate
   # Delete branch, cancel task, create new task
   git branch -D feat/<task-id>
   
   jq '.tasks |= map(if .id == "<task-id>" then .status = "cancelled" | .blocked_reason = "Start-Over Gate - fundamental issues" else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

3. **Create replacement task:**
   ```bash
   # Call planner to create new task with learnings from failure
   ```

**Prevention:**
- Clear acceptance criteria
- Better initial planning
- Refiner guidelines for when to adapt vs restart
- Limit adaptation cycles (3 max)

**See Also:** [RUNBOOK: Scenario 4 - Viewing Agent Activity](RUNBOOK.md#scenario-4-viewing-agent-activity)

---

### Issue 24: Merge Conflicts After Integration 🔴

**Symptoms:**
- Integration succeeded but broke main
- Tests pass on branch, fail on main
- Conflicts after merge

**Diagnosis:**
```bash
# Check main branch tests
git checkout main
pytest tests/ -v

# Check what was merged
git log --oneline -5

# Check for conflicts
git diff HEAD~1..HEAD

# Review integration report
cat .oodatcaa/work/reports/<story>/integrator_<task>.md
```

**Solution:**
1. **Quick fix on main:**
   ```bash
   # Make minimal fix
   git checkout -b hotfix/<issue>
   # Fix issue
   git commit -m "[hotfix] Fix post-merge issue"
   git checkout main
   git merge hotfix/<issue>
   git branch -d hotfix/<issue>
   ```

2. **Revert merge:**
   ```bash
   git revert -m 1 HEAD
   git push origin main
   
   # Fix on feature branch
   git checkout feat/<task-id>
   # Apply fixes
   # Retest
   # Re-integrate
   ```

3. **Rollback (if critical):**
   ```bash
   # See Issue 17
   ```

**Prevention:**
- Rebase branch before integration
- Test integration locally first
- Protected main branch (require reviews)
- CI/CD gates before merge
- Integration testing

**See Also:** [RUNBOOK: Scenario 17 - Rolling Back Changes](RUNBOOK.md#scenario-17-rolling-back-changes)

---

### Issue 25: Work Duplicated Across Tasks 🟡

**Symptoms:**
- Two tasks implementing same feature
- Conflicting implementations
- Wasted effort

**Diagnosis:**
```bash
# Check task descriptions
jq '.tasks[] | {id, title, status}' .oodatcaa/work/SPRINT_QUEUE.json

# Check branches
git branch -a | grep feat/

# Compare implementations
git diff feat/<task-A>...feat/<task-B>
```

**Solution:**
1. **Identify best implementation:**
   ```bash
   # Review both
   git log feat/<task-A> --oneline
   git log feat/<task-B> --oneline
   
   # Compare quality, completeness
   ```

2. **Cancel redundant task:**
   ```bash
   jq '.tasks |= map(if .id == "<redundant-task>" then .status = "cancelled" | .blocked_reason = "Duplicate of <other-task>" else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   
   # Delete branch
   git branch -D feat/<redundant-task>
   ```

3. **Merge unique aspects:**
   ```bash
   # If both have unique value
   git checkout feat/<task-A>
   git cherry-pick <commits-from-task-B>
   ```

**Prevention:**
- Clear task scopes in planning
- Regular sprint reviews
- Planner checks for overlaps
- Task dependencies (B waits for A)
- Better communication

**See Also:** [RUNBOOK: Scenario 3 - Checking Sprint Status](RUNBOOK.md#scenario-3-checking-sprint-status)

---

### Issue 26: Log Files Too Large to Open 🟡

**Symptoms:**
- AGENT_LOG.md >50MB
- Editor crashes
- Git performance degrades

**Diagnosis:**
```bash
# Check sizes
ls -lh .oodatcaa/work/*.md

# Line counts
wc -l .oodatcaa/work/AGENT_LOG.md
```

**Solution:**
1. **Rotate immediately:**
   ```bash
   bash scripts/rotate-logs.sh
   ```

2. **View with pagination:**
   ```bash
   less .oodatcaa/work/AGENT_LOG.md
   # OR
   tail -1000 .oodatcaa/work/AGENT_LOG.md
   ```

3. **Search without opening:**
   ```bash
   grep "<search-term>" .oodatcaa/work/AGENT_LOG.md | tail -50
   ```

4. **Split manually (if rotation fails):**
   ```bash
   head -5000 .oodatcaa/work/AGENT_LOG.md > .oodatcaa/work/archive/sprint_N/AGENT_LOG_manual_1.md
   tail -n +5001 .oodatcaa/work/AGENT_LOG.md > .oodatcaa/work/AGENT_LOG.md.new
   mv .oodatcaa/work/AGENT_LOG.md.new .oodatcaa/work/AGENT_LOG.md
   ```

**Prevention:**
- Automated log rotation (threshold: 1000 lines)
- Cron job for rotation
- Git LFS for large files (if needed)
- Compress archived logs

**See Also:** [RUNBOOK: Scenario 14 - Managing Log Files](RUNBOOK.md#scenario-14-managing-log-files), [RUNBOOK: Scenario 15 - Archiving Logs](RUNBOOK.md#scenario-15-archiving-logs)

---

### Issue 27: Agent Reports Incomplete 🟡

**Symptoms:**
- Missing sections in reports
- No metrics
- Incomplete handoff notes

**Diagnosis:**
```bash
# Check report structure
cat .oodatcaa/work/reports/<story>/<agent>_<task>.md

# Compare with template
diff .oodatcaa/templates/AGENT_REPORT_TEMPLATE.md .oodatcaa/work/reports/<story>/<agent>_<task>.md

# Check agent logs for completion
grep "<task-id>" .oodatcaa/work/AGENT_LOG.md | grep -i "report\|complete"
```

**Solution:**
1. **If agent didn't finish:**
   - Agent may have crashed/interrupted
   - Check for partial work on branch
   - May need to rerun or call refiner

2. **If report format wrong:**
   - Update agent prompt with report template
   - Call agent again with "create completion report" instruction

3. **Add missing information manually:**
   ```bash
   nano .oodatcaa/work/reports/<story>/<agent>_<task>.md
   # Add metrics, handoff notes from logs/commits
   ```

**Prevention:**
- Strict report template compliance in agent prompts
- Validation step before marking task complete
- Report format examples in prompts
- Automated report structure checking

**See Also:** [RUNBOOK: Scenario 4 - Viewing Agent Activity](RUNBOOK.md#scenario-4-viewing-agent-activity)

---

### Issue 28: Test Coverage Below Threshold 🟡

**Symptoms:**
- Coverage report shows <85%
- CI/CD coverage gate fails
- Quality degradation

**Diagnosis:**
```bash
# Run coverage analysis
pytest --cov=src --cov-report=term-missing

# Check coverage thresholds
grep cov-fail-under pytest.ini

# Identify uncovered code
pytest --cov=src --cov-report=html
open htmlcov/index.html
```

**Solution:**
1. **Add missing tests:**
   ```bash
   # Identify uncovered functions
   pytest --cov=src --cov-report=term-missing | grep "MISS"
   
   # Create tests for those functions
   nano tests/test_<module>.py
   ```

2. **Adjust threshold (if justified):**
   ```bash
   # Only if code is truly untestable (rare)
   nano pytest.ini
   # Adjust --cov-fail-under value
   ```

3. **Call refiner to add tests:**
   ```bash
   jq '.tasks |= map(if .id == "<task-id>" then .status = "needs_adapt" | .blocked_reason = "Coverage below 85%" else . end)' \
      .oodatcaa/work/SPRINT_QUEUE.json > /tmp/queue_tmp.json
   mv /tmp/queue_tmp.json .oodatcaa/work/SPRINT_QUEUE.json
   ```

**Prevention:**
- TDD approach (tests first)
- Coverage requirements in DoD
- Tester validates coverage before passing
- Continuous coverage monitoring

**See Also:** [Project Rules - Coverage Requirements](config/ProjectRules.md)

---

### Issue 29: Documentation Out of Sync 🟡

**Symptoms:**
- Docs describe old behavior
- Examples don't work
- Missing documentation for new features

**Diagnosis:**
```bash
# Check recent code changes
git log --oneline --since="1 week ago" -- src/

# Check doc updates
git log --oneline --since="1 week ago" -- docs/ README.md

# Search for TODOs
grep -r "TODO\|FIXME\|XXX" docs/
```

**Solution:**
1. **Update documentation:**
   ```bash
   # Update affected docs
   nano docs/<relevant-doc>.md
   nano README.md
   
   # Test examples
   # Commit changes
   git add docs/ README.md
   git commit -m "[docs] Update documentation for recent changes"
   ```

2. **Create documentation task:**
   ```bash
   # Add to SPRINT_QUEUE.json
   # Assign to builder or create new story
   ```

3. **Link PRs to doc updates:**
   ```bash
   # Require doc updates in same PR as code changes
   # Update CONTRIBUTING.md with this requirement
   ```

**Prevention:**
- Documentation requirements in DoD
- Update docs with code changes (same PR)
- Regular documentation audits
- Automated doc generation where possible
- Examples in CI/CD tests

**See Also:** [CONTRIBUTING.md](../docs/CONTRIBUTING.md)

---

### Issue 30: Stale Branches Not Cleaned Up 🟡

**Symptoms:**
- Many old feature branches
- Git performance degraded
- Confusion about branch status

**Diagnosis:**
```bash
# List all branches
git branch -a

# Find merged branches
git branch --merged main

# Find old branches
for branch in $(git for-each-ref --format='%(refname:short)' refs/heads/); do
  echo "$branch: $(git log -1 --format=%ai $branch)"
done | sort -k2
```

**Solution:**
1. **Delete merged local branches:**
   ```bash
   git branch -d $(git branch --merged main | grep -v main)
   ```

2. **Delete merged remote branches:**
   ```bash
   git push origin --delete $(git branch -r --merged main | grep origin | grep -v main | sed 's/origin\///')
   ```

3. **Delete specific stale branch:**
   ```bash
   # Local
   git branch -D feat/<old-task>
   
   # Remote
   git push origin :feat/<old-task>
   ```

4. **Prune remote tracking branches:**
   ```bash
   git remote prune origin
   ```

**Prevention:**
- Delete branch after integration
- Automated cleanup (integrator responsibility)
- Branch naming with dates
- Regular maintenance schedule (monthly)
- Git hooks for cleanup

**See Also:** [BRANCH_PROTECTION.md](../docs/BRANCH_PROTECTION.md)

---

## Quick Diagnostics

### Diagnostic Checklist

When encountering any issue, run through this checklist:

**1. System Health**
```bash
make sprint-dashboard
jq empty .oodatcaa/work/SPRINT_QUEUE.json
git status
df -h .
```

**2. Agent Status**
```bash
make agents-status
ls -lh .leases/
tail -50 .oodatcaa/work/AGENT_LOG.md
```

**3. Task Status**
```bash
jq '.tasks[] | select(.status == "in_progress" or .status == "blocked")' .oodatcaa/work/SPRINT_QUEUE.json
```

**4. Recent Activity**
```bash
git log --oneline -10
tail -100 .oodatcaa/work/AGENT_LOG.md
```

**5. Dependencies**
```bash
make validate-env
which jq git python3 make
python3 --version
```

---

## Getting Help

If issues persist after trying solutions in this guide:

1. **Check Logs:**
   - `.oodatcaa/work/AGENT_LOG.md` - Detailed agent activity
   - `.agent-daemon-logs/*.log` - Daemon operation logs
   - `journalctl --user -u agent-*` - System logs (if systemd)

2. **Review Documentation:**
   - [RUNBOOK.md](RUNBOOK.md) - Operational procedures
   - [ONBOARDING.md](ONBOARDING.md) - Setup and basics
   - [ARCHITECTURE.md](ARCHITECTURE.md) - System design
   - [BACKGROUND_AGENTS.md](../docs/BACKGROUND_AGENTS.md) - Daemon documentation

3. **Inspect State Files:**
   - `.oodatcaa/work/SPRINT_QUEUE.json` - Task queue
   - `.oodatcaa/work/SPRINT_STATUS.json` - Sprint metrics
   - `.oodatcaa/work/AGENT_REPORTS.md` - Completion summaries

4. **Seek Assistance:**
   - Check [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for support channels
   - Open issue with diagnostic output
   - Include relevant logs and configuration

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-04  
**Maintained By:** OODATCAA System Team

For operational procedures, see [RUNBOOK.md](RUNBOOK.md). For questions or issues, refer to [CONTRIBUTING.md](../docs/CONTRIBUTING.md).

