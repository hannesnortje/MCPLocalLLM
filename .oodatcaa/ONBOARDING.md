# OODATCAA Onboarding Guide

**Version:** 1.0  
**Last Updated:** 2025-10-04  
**Target Audience:** New developers and operators

---

## Welcome to OODATCAA! 👋

Welcome to the **OODATCAA** (Observe → Orient → Decide → Act → Test → Check → Adapt → Archive) multi-agent autonomous development system. This guide will get you from zero to running your first sprint in **15 minutes**.

### What is OODATCAA?

OODATCAA is an autonomous development system where AI agents collaboratively:
- **Plan** work into executable tasks
- **Build** code and documentation
- **Test** against acceptance criteria
- **Refine** work until quality standards met
- **Integrate** completed work into main branch
- **Coordinate** through file-based protocols

### What You'll Learn

1. **Quick Start** (15 minutes) - Get system running
2. **Core Concepts** (20 minutes) - Understand the fundamentals
3. **First Sprint** (30 minutes) - Complete your first development cycle
4. **Common Tasks** (reference) - Day-to-day operations
5. **Next Steps** - Deep dive resources

---

## Quick Start (15 Minutes) ⚡

### Prerequisites

Before starting, ensure you have:
- **Python 3.11+** installed
- **Git** configured
- **Terminal** access
- **15 minutes** uninterrupted time

### Step 1: Clone Repository (2 min)

```bash
# Clone the repository
git clone https://github.com/hannesnortje/MCPLocalLLM.git
cd MCPLocalLLM

# Verify you're in the right place
ls .oodatcaa/
# Should show: prompts/ work/ objectives/ config/ etc.
```

**Checkpoint:** ✅ You should see the `.oodatcaa/` directory

---

### Step 2: Run Setup Script (5 min)

```bash
# Run automated setup
./scripts/setup-dev.sh

# This will:
# - Install Python dependencies
# - Set up virtual environment (optional)
# - Install system tools (jq)
# - Create required directories
# - Initialize configuration
```

**If script fails:**
```bash
# Manual setup
pip install -e ".[dev]"  # Or: pip install pytest black ruff mypy

# Install jq (if not present)
# Ubuntu/Debian: sudo apt-get install jq
# macOS: brew install jq
```

**Checkpoint:** ✅ Run `make validate-env` - should show all checks passing

---

### Step 3: Validate Environment (2 min)

```bash
# Validate everything is configured correctly
make validate-env

# Expected output:
# ✅ Python 3.11+
# ✅ Git repository
# ✅ jq installed
# ✅ Configuration files present
# ✅ All systems operational
```

**Checkpoint:** ✅ All validation checks pass

---

### Step 4: Check Sprint Status (2 min)

```bash
# View current sprint dashboard
make sprint-dashboard

# You should see:
# - Current sprint number
# - Task counts and statuses
# - Active agents
# - Ready tasks
```

**Checkpoint:** ✅ Dashboard displays current sprint state

---

### Step 5: Test Agent Execution (4 min)

**Option A: Manual Agent Test (Recommended for Learning)**

```bash
# 1. Check for ready tasks
jq '.tasks[] | select(.status == "ready") | {id, title, agent}' .oodatcaa/work/SPRINT_QUEUE.json | head -20

# 2. Pick a task (example: P006-B01)
# 3. Open Cursor/IDE
# 4. Load builder prompt
cat .oodatcaa/prompts/builder.md

# 5. In Cursor, run:
# "Load @Cursor Rules and @Project Rules. Run .oodatcaa/prompts/builder.md exactly."

# 6. Watch agent work!
```

**Option B: Background Agents (Production Mode)**

```bash
# Start agent daemons
make agents-start

# Check agent status
make agents-status

# Watch agents work
tail -f .oodatcaa/work/AGENT_LOG.md
```

**Checkpoint:** ✅ Agent successfully claims and processes a task

---

### 🎉 Congratulations!

You've successfully set up OODATCAA and run your first agent! You now have a working autonomous development system.

**What just happened:**
1. ✅ Environment configured
2. ✅ Sprint system operational
3. ✅ Agents can claim and execute work
4. ✅ You're ready for autonomous development!

**Next:** Continue to [Core Concepts](#core-concepts-20-minutes) to understand how it all works.

---

## Core Concepts (20 Minutes) 🧠

### The OODATCAA Loop

The system follows an 8-phase development loop:

```
┌─────────────────────────────────────────────────────┐
│                  OODATCAA Loop                       │
│                                                      │
│  Observe → Orient → Decide → Act → Test → Check    │
│     ↑                                         ↓      │
│     └──────── Archive ← Adapt ←──────────────┘      │
└─────────────────────────────────────────────────────┘
```

**Phase Breakdown:**

1. **Observe** (Planner) - Analyze requirements, gather context
2. **Orient** (Planner) - Evaluate alternatives, choose approach
3. **Decide** (Planner) - Create detailed implementation plan
4. **Act** (Builder) - Implement plan, write code/docs
5. **Test** (Tester) - Validate against acceptance criteria
6. **Check** (Tester) - Assess quality, identify issues
7. **Adapt** (Refiner) - Fix issues or trigger Start-Over Gate
8. **Archive** (Integrator) - Merge to main, tag, document

### The 11 Agent Roles

| Agent | Responsibility | Typical Duration |
|-------|---------------|------------------|
| **Planner** | Create implementation plans | 15-45 min |
| **Builder** | Write code/docs | 30-240 min |
| **Tester** | Validate acceptance criteria | 15-60 min |
| **Refiner** | Fix issues, adapt work | 30-90 min |
| **Integrator** | Merge to main, archive | 15-30 min |
| **Sprint Planner** | Plan sprints from objectives | 30-60 min |
| **Negotiator** | Coordinate agents, resolve conflicts | As needed |
| **Project Detector** | Identify project completion | As needed |
| **Sprint Close** | Complete sprints | 15-30 min |
| **Release** | Create releases | 30-60 min |
| **Triage** | Prioritize urgent work | As needed |

### Key Files and Directories

```
.oodatcaa/
├── prompts/             # Agent protocol files (11 agents)
│   ├── builder.md       # Builder agent protocol
│   ├── planner.md       # Planner agent protocol
│   └── ...
├── work/                # Sprint execution files
│   ├── SPRINT_QUEUE.json      # Task queue (THE central file)
│   ├── AGENT_LOG.md           # Detailed agent activity
│   ├── SPRINT_LOG.md          # Sprint-level events
│   ├── AGENT_REPORTS.md       # Executive summaries
│   ├── AGENT_PLAN.md          # Current implementation plan
│   ├── TEST_PLAN.md           # Current test procedures
│   ├── SPRINT_STATUS.json     # Real-time metrics
│   └── reports/               # Completion reports
├── objectives/          # Sprint objectives
│   ├── SPRINT_GOAL.md         # Current sprint goal
│   ├── OBJECTIVE.md           # Project objective
│   └── RELEASE_CHECKLIST.md   # Release criteria
├── config/              # System configuration
│   ├── ProjectRules.md        # Python-specific rules
│   └── UserRules.md           # OODATCAA doctrine
└── scripts/             # Automation scripts
    ├── agent-daemon.py        # Background agent daemon
    ├── agents-daemon-cli.sh   # CLI wrapper
    ├── rotate-logs.sh         # Log rotation
    └── ...

.leases/                 # Active task leases (runtime)
.locks/                  # File locks (runtime)
```

**Most Important Files:**

1. **`.oodatcaa/work/SPRINT_QUEUE.json`** - Task queue, agent assignments, status tracking
2. **`.oodatcaa/work/AGENT_LOG.md`** - Chronological agent activity log
3. **`.oodatcaa/prompts/<agent>.md`** - Agent protocols and instructions
4. **`.oodatcaa/objectives/SPRINT_GOAL.md`** - Current sprint objectives

### Task Lifecycle

```
ready → in_progress → awaiting_test → ready_for_integrator → done
              ↓             ↓
          blocked      needs_adapt
                           ↓
                     (refine or restart)
```

**Status Meanings:**

- **`ready`** - Dependencies met, available for claiming
- **`in_progress`** - Agent actively working
- **`awaiting_test`** - Builder done, needs validation
- **`needs_adapt`** - Issues found, refiner needed
- **`ready_for_integrator`** - All checks passed
- **`done`** - Integrated to main
- **`blocked`** - Waiting on dependencies
- **`cancelled`** - Not needed

### Lease System

**Purpose:** Prevent multiple agents from working on same task (race condition prevention)

**How it works:**
1. Agent polls queue for `ready` tasks
2. Creates lease file: `.leases/<task-id>.json`
3. Updates task status: `ready` → `in_progress`
4. Works on task (heartbeat every 60s)
5. Completes work, releases lease
6. If agent crashes, lease expires after TTL

**Lease File Example:**
```json
{
  "task_id": "P006-B01",
  "agent": "builder",
  "owner": "agent-builder-cursor",
  "acquired": "2025-10-04T16:35:31+02:00",
  "ttl": 7200,
  "last_heartbeat": "2025-10-04T16:45:31+02:00"
}
```

### WIP Limits

**Purpose:** Prevent agents from being overloaded

**Default Limits:**
- Planner: 1 task
- Builder: 3 tasks
- Tester: 2 tasks
- Refiner: 1 task
- Integrator: 1 task

**Configured in:** `.oodatcaa/work/SPRINT_QUEUE.json` → `wip_limits`

### Quality Gates

All code must pass quality gates before integration:

```bash
# Formatting
black --check .

# Linting
ruff check .

# Type checking
mypy .

# Tests
pytest -q

# Coverage
pytest --cov=src --cov-report=term-missing --cov-fail-under=85

# Build
python -m build

# Security
pip-audit
```

**Enforced:** Builder (before commit), Tester (validation), Integrator (final check)

---

## First Sprint Walkthrough (30 Minutes) 🚀

Now that you understand the concepts, let's walk through a complete sprint cycle.

### Sprint Overview

A sprint typically contains:
- **5-10 stories** (P001, P002, etc.)
- **20-40 tasks** (subtasks of stories)
- **Duration:** 1-4 weeks
- **Exit Criteria:** Defined in `SPRINT_GOAL.md`

### Step 1: Review Sprint Objective (5 min)

```bash
# Read the current sprint goal
cat .oodatcaa/objectives/SPRINT_GOAL.md

# Key sections:
# - Sprint Goals (3-5 objectives)
# - Success Criteria (measurable outcomes)
# - Exit Criteria (when sprint is complete)
```

**Example Sprint 2 Goal:**
```markdown
# Sprint 2 Objective: OODATCAA Process Improvement

## Goals
1. Background Agent System Operational
2. Automated log rotation with searchable archives
3. Sprint management dashboard and automation
4. Complete OODATCAA loop documentation
5. Agent role assessment and enhancement

## Success Criteria
- 5/7 infrastructure stories complete
- All agents have clear protocols
- Autonomous operation validated (10+ ops)
- Documentation comprehensive
```

### Step 2: Check Sprint Status (5 min)

```bash
# View dashboard
make sprint-dashboard

# Review task breakdown
jq '.tasks | group_by(.status) | map({status: .[0].status, count: length})' .oodatcaa/work/SPRINT_QUEUE.json

# List ready tasks
jq '.tasks[] | select(.status == "ready") | {id, title, priority, agent}' .oodatcaa/work/SPRINT_QUEUE.json

# Check for blocked tasks
jq '.tasks[] | select(.status == "blocked") | {id, title, blocked_reason}' .oodatcaa/work/SPRINT_QUEUE.json
```

**What to look for:**
- ✅ Tasks with status `ready` (work available)
- ⚠️ Tasks with status `blocked` (dependencies not met)
- 📊 Overall completion percentage
- 🎯 Next priority tasks

### Step 3: Run a Builder Task (10 min)

**Manual Execution (Recommended for Learning):**

1. **Pick a ready task:**
   ```bash
   jq '.tasks[] | select(.type == "Build" and .status == "ready") | {id, title}' .oodatcaa/work/SPRINT_QUEUE.json | head -1
   ```

2. **Review the plan:**
   ```bash
   cat .oodatcaa/work/AGENT_PLAN.md
   # Read steps for this task
   ```

3. **Execute the builder:**
   - Open Cursor
   - Load builder prompt: `.oodatcaa/prompts/builder.md`
   - Run: "Load @Cursor Rules and @Project Rules. Run .oodatcaa/prompts/builder.md exactly."

4. **Watch execution:**
   ```bash
   # In another terminal
   watch -n 5 'tail -50 .oodatcaa/work/AGENT_LOG.md'
   ```

5. **Verify completion:**
   ```bash
   jq '.tasks[] | select(.id == "<task-id>") | {status, lease}' .oodatcaa/work/SPRINT_QUEUE.json
   # Status should be awaiting_test
   ```

**Background Execution (Production):**

```bash
# Start builder daemon
make agents-start

# Watch it work
tail -f .oodatcaa/work/AGENT_LOG.md

# Check progress
make sprint-dashboard
```

### Step 4: Run a Tester Task (5 min)

After builder completes:

1. **Find awaiting_test task:**
   ```bash
   jq '.tasks[] | select(.status == "awaiting_test") | {id, title}' .oodatcaa/work/SPRINT_QUEUE.json
   ```

2. **Review test plan:**
   ```bash
   cat .oodatcaa/work/TEST_PLAN.md
   ```

3. **Execute tester:**
   - Load tester prompt: `.oodatcaa/prompts/tester.md`
   - Run: "Load @Cursor Rules and @Project Rules. Run .oodatcaa/prompts/tester.md exactly."

4. **Check result:**
   ```bash
   jq '.tasks[] | select(.id == "<task-id>") | {status}' .oodatcaa/work/SPRINT_QUEUE.json
   # Should be: ready_for_integrator (pass) or needs_adapt (fail)
   ```

### Step 5: Run an Integrator Task (5 min)

After tester passes:

1. **Find ready_for_integrator task:**
   ```bash
   jq '.tasks[] | select(.status == "ready_for_integrator") | {id, title, branch}' .oodatcaa/work/SPRINT_QUEUE.json
   ```

2. **Execute integrator:**
   - Load integrator prompt: `.oodatcaa/prompts/integrator.md`
   - Run: "Load @Cursor Rules and @Project Rules. Run .oodatcaa/prompts/integrator.md exactly."

3. **Verify integration:**
   ```bash
   git log --oneline -5
   # Should show merge commit
   
   jq '.tasks[] | select(.id == "<task-id>") | {status}' .oodatcaa/work/SPRINT_QUEUE.json
   # Should be: done
   ```

### 🎉 You've Completed a Full Task Cycle!

You just witnessed:
1. ✅ Builder implemented code
2. ✅ Tester validated quality
3. ✅ Integrator merged to main
4. ✅ Task marked as done
5. ✅ Sprint progress updated

**This is autonomous development!**

---

## Common Tasks (Reference) 📚

Quick reference for day-to-day operations.

### Checking Status

```bash
# Sprint dashboard
make sprint-dashboard

# View recent agent activity
tail -50 .oodatcaa/work/AGENT_LOG.md

# Check task status
jq '.tasks[] | select(.id == "<task-id>")' .oodatcaa/work/SPRINT_QUEUE.json

# List all ready tasks
jq '.tasks[] | select(.status == "ready")' .oodatcaa/work/SPRINT_QUEUE.json
```

### Starting/Stopping Agents

```bash
# Start all agents
make agents-start

# Stop all agents
make agents-stop

# Restart agents
make agents-restart

# Check agent status
make agents-status

# Start specific agent (systemd)
systemctl --user start agent-builder

# Start specific agent (CLI)
bash scripts/agents-daemon-cli.sh start builder
```

### Managing Leases

```bash
# List active leases
ls -lh .leases/

# View lease details
cat .leases/<task-id>.json | jq

# Remove stale lease
rm .leases/<task-id>.json

# Clear all leases (CAUTION: stop agents first!)
make agents-stop
rm .leases/*.json
```

### Sprint Operations

```bash
# Complete current sprint
make sprint-complete

# Start new sprint
make sprint-new

# View sprint status (JSON)
cat .oodatcaa/work/SPRINT_STATUS.json | jq
```

### Log Management

```bash
# View logs
tail -100 .oodatcaa/work/AGENT_LOG.md
tail -50 .oodatcaa/work/SPRINT_LOG.md

# Search logs
grep "<search-term>" .oodatcaa/work/AGENT_LOG.md

# Rotate logs
bash scripts/rotate-logs.sh

# Check log sizes
wc -l .oodatcaa/work/*.md
```

### Troubleshooting

```bash
# Validate environment
make validate-env

# Check system health
jq empty .oodatcaa/work/SPRINT_QUEUE.json
git status
df -h .

# View agent errors
grep -i "error\|failed" .oodatcaa/work/AGENT_LOG.md | tail -20

# Check recent changes
git log --oneline -10
```

---

## Development Workflows 🔄

### Workflow 1: Feature Development

**Goal:** Implement a new feature

**Steps:**
1. **Plan:** Call planner with feature requirements
2. **Build:** Builder implements in feature branch
3. **Test:** Tester validates acceptance criteria
4. **Refine:** If issues, refiner adapts (or restart)
5. **Integrate:** Integrator merges to main
6. **Done:** Feature complete!

**Command sequence:**
```bash
# 1. Check sprint has capacity
make sprint-dashboard

# 2. Add story to queue (or call planner)
# 3. Start agents
make agents-start

# 4. Monitor progress
watch -n 10 'make sprint-dashboard'

# 5. Verify completion
git log --oneline -10
```

### Workflow 2: Bug Fix

**Goal:** Fix a reported bug

**Steps:**
1. **Triage:** Triage agent assesses urgency
2. **Plan:** Planner creates fix plan (if complex)
3. **Build:** Builder implements fix
4. **Test:** Tester validates bug is fixed
5. **Integrate:** Fast-track to main (hotfix)

**Command sequence:**
```bash
# 1. Create bug task in SPRINT_QUEUE.json
# 2. Set high priority, mark as ready
# 3. Builder claims and fixes
# 4. Tester validates
# 5. Integrator fast-tracks
```

### Workflow 3: Documentation Update

**Goal:** Update documentation

**Steps:**
1. **Plan:** Identify docs to update
2. **Build:** Builder updates docs
3. **Test:** Tester validates accuracy, links
4. **Integrate:** Merge to main

**Command sequence:**
```bash
# Similar to feature development
# Typically faster (no code changes)
# Focus on markdown quality, link validation
```

### Workflow 4: Refactoring

**Goal:** Improve code without changing behavior

**Steps:**
1. **Plan:** Planner outlines refactor scope
2. **Build:** Builder refactors code
3. **Test:** Tester validates no behavior change
4. **Integrate:** Merge after thorough testing

**Command sequence:**
```bash
# Requires comprehensive test suite
# No new features, only structural changes
# High test coverage critical
```

---

## Best Practices ✨

### For Operators

1. **Regular Monitoring:**
   - Check `make sprint-dashboard` daily
   - Review blocked tasks weekly
   - Monitor log sizes (rotate at 1000 lines)

2. **Proactive Maintenance:**
   - Weekly git cleanup (delete merged branches)
   - Monthly archive compression
   - Regular dependency updates

3. **Sprint Management:**
   - Clear objectives before sprint start
   - Mid-sprint reviews (check progress, unblock tasks)
   - Proper sprint completion (archive, tag, changelog)

4. **Agent Management:**
   - Run agents as daemons for autonomy
   - Monitor WIP limits (adjust for system capacity)
   - Graceful shutdowns (SIGTERM not SIGKILL)

### For Developers

1. **Understanding the System:**
   - Read agent prompts (understand their role)
   - Review `OODATCAA_LOOP_GUIDE.md`
   - Study completion reports for patterns

2. **Writing Good Plans:**
   - Clear acceptance criteria
   - Step-by-step procedures
   - Examples and edge cases
   - Realistic time estimates

3. **Quality Standards:**
   - Follow quality gates (black, ruff, mypy, pytest)
   - Test coverage ≥ 85%
   - Documentation with code changes
   - Commit message conventions

4. **Collaboration:**
   - Review other agent work
   - Provide feedback in reports
   - Update prompts when patterns emerge
   - Share learnings in retrospectives

### Common Pitfalls to Avoid

1. ❌ **Don't skip quality gates** - Compromises system integrity
2. ❌ **Don't force push to main** - Use PR workflow
3. ❌ **Don't manually edit SPRINT_QUEUE.json** (use agents or jq carefully)
4. ❌ **Don't ignore blocked tasks** - Address dependencies promptly
5. ❌ **Don't let logs grow unbounded** - Rotate regularly
6. ❌ **Don't run agents as root** - Security risk
7. ❌ **Don't skip sprint completion** - Breaks next sprint initialization

---

## Next Steps 🎓

### Beginner → Intermediate

**You've completed Quick Start. Next, deepen your knowledge:**

1. **Study Agent Prompts** (2 hours)
   - Read all 11 agent prompts in `.oodatcaa/prompts/`
   - Understand each agent's role and decision authority
   - Note common patterns across agents

2. **Review Sprint 1/2 Reports** (1 hour)
   - Browse `.oodatcaa/work/reports/`
   - See real examples of agent work
   - Learn from adaptation cycles

3. **Practice Manual Execution** (3 hours)
   - Run each agent type manually at least once
   - Planner → Builder → Tester → Integrator
   - Observe the full cycle

### Intermediate → Advanced

**You understand basics. Now master the system:**

1. **System Architecture** (2 hours)
   - Read `ARCHITECTURE.md` (when available)
   - Understand file-based coordination
   - Study lease and lock mechanisms

2. **Advanced Operations** (3 hours)
   - Background agent daemons
   - Custom agent prompts
   - Performance tuning
   - Advanced troubleshooting

3. **Process Improvement** (ongoing)
   - Analyze sprint retrospectives
   - Propose agent enhancements
   - Contribute to OODATCAA development

### Recommended Reading Order

1. **Start Here:**
   - ✅ This document (ONBOARDING.md)
   - `.oodatcaa/START_HERE.md`
   - `.oodatcaa/QUICK_START.md`

2. **Core Documentation:**
   - `.oodatcaa/OODATCAA_LOOP_GUIDE.md` - The development loop
   - `.oodatcaa/AGENT_ROLES_MATRIX.md` - Agent capabilities
   - `.oodatcaa/AGENT_INTERACTION_GUIDE.md` - Coordination patterns

3. **Operational Guides:**
   - `.oodatcaa/RUNBOOK.md` - 20+ operational scenarios
   - `.oodatcaa/TROUBLESHOOTING.md` - 30+ issue resolutions
   - `docs/BACKGROUND_AGENTS.md` - Daemon system

4. **Advanced Topics:**
   - `.oodatcaa/AGENT_GAP_ANALYSIS.md` - System improvements
   - `.oodatcaa/ARCHITECTURE.md` - System design
   - `.oodatcaa/config/UserRules.md` - OODATCAA doctrine

### Additional Resources

**Internal:**
- [CONTRIBUTING.md](../docs/CONTRIBUTING.md) - Contribution guidelines
- [SECURITY.md](../docs/SECURITY.md) - Security policy
- [BRANCH_PROTECTION.md](../docs/BRANCH_PROTECTION.md) - Git workflow
- [CHANGELOG.md](../CHANGELOG.md) - Release history

**External:**
- OODATCAA concept (OODA loop + TCA)
- Multi-agent systems literature
- Autonomous software development research

---

## Getting Help 🆘

### Self-Service Resources

1. **Quick Diagnostics:**
   ```bash
   make validate-env
   make sprint-dashboard
   tail -100 .oodatcaa/work/AGENT_LOG.md
   ```

2. **Documentation:**
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 30+ common issues
   - [RUNBOOK.md](RUNBOOK.md) - Operational procedures
   - Agent prompts (`.oodatcaa/prompts/`)

3. **Inspect State:**
   - `.oodatcaa/work/SPRINT_QUEUE.json` - Task state
   - `.oodatcaa/work/AGENT_LOG.md` - Activity log
   - `.oodatcaa/work/reports/` - Completion reports

### Community Support

1. **GitHub Issues**
   - Search existing issues
   - Create new issue with diagnostic output
   - Include: OS, Python version, error messages

2. **Contributing**
   - See [CONTRIBUTING.md](../docs/CONTRIBUTING.md)
   - PRs welcome for docs and features
   - Follow quality gates and commit conventions

### Debugging Tips

**When something goes wrong:**

1. **Check logs first:**
   ```bash
   tail -200 .oodatcaa/work/AGENT_LOG.md
   grep -i "error\|failed\|blocked" .oodatcaa/work/AGENT_LOG.md
   ```

2. **Validate critical files:**
   ```bash
   jq empty .oodatcaa/work/SPRINT_QUEUE.json
   git status
   make validate-env
   ```

3. **Check recent changes:**
   ```bash
   git log --oneline -20
   jq '.tasks[] | select(.status == "in_progress")' .oodatcaa/work/SPRINT_QUEUE.json
   ```

4. **Consult TROUBLESHOOTING.md:**
   - [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
   - 30+ issues with solutions
   - Diagnostic procedures included

---

## Glossary 📖

**Terms you'll encounter:**

- **AC** - Acceptance Criteria (defines task success)
- **DoD** - Definition of Done (quality standards)
- **WIP** - Work In Progress (limit on concurrent tasks)
- **Lease** - Claim on a task (prevents race conditions)
- **TTL** - Time To Live (lease expiration time)
- **Sprint** - Development cycle (1-4 weeks)
- **Story** - High-level feature (e.g., P001, P002)
- **Task** - Subtask of story (e.g., P001-B01)
- **Agent** - AI worker (planner, builder, tester, etc.)
- **Protocol** - Agent instruction set (`.oodatcaa/prompts/<agent>.md`)
- **Queue** - Task list (`.oodatcaa/work/SPRINT_QUEUE.json`)
- **Start-Over Gate** - Restart task after 2+ failed adapt cycles
- **Autonomous Operation** - Agent claims and completes work without manual intervention

**Task Type Codes:**
- **B** - Build (implementation)
- **T** - Test (validation)
- **R** - Refine (adaptation)
- **I** - Integrate (merge)
- **P** - Plan (planning)

**Agent Naming:**
- **agent-builder-A** - Primary builder instance
- **agent-builder-cursor** - Builder run via Cursor
- **agent-builder-daemon** - Builder running as background daemon

---

## Quick Reference Card 🎴

**Essential Commands:**

| Task | Command |
|------|---------|
| **Setup** | `./scripts/setup-dev.sh` |
| **Validate** | `make validate-env` |
| **Status** | `make sprint-dashboard` |
| **Start Agents** | `make agents-start` |
| **Stop Agents** | `make agents-stop` |
| **View Logs** | `tail -50 .oodatcaa/work/AGENT_LOG.md` |
| **Ready Tasks** | `jq '.tasks[] \| select(.status == "ready")' .oodatcaa/work/SPRINT_QUEUE.json` |
| **Sprint Complete** | `make sprint-complete` |
| **Sprint New** | `make sprint-new` |
| **Rotate Logs** | `bash scripts/rotate-logs.sh` |

**Key Directories:**

| Directory | Purpose |
|-----------|---------|
| `.oodatcaa/prompts/` | Agent protocols |
| `.oodatcaa/work/` | Sprint execution files |
| `.oodatcaa/objectives/` | Sprint goals |
| `.leases/` | Active task leases |
| `.locks/` | File locks |
| `scripts/` | Automation scripts |
| `docs/` | Project documentation |

**Help Resources:**

| Resource | Description |
|----------|-------------|
| [RUNBOOK.md](RUNBOOK.md) | 20+ operational scenarios |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | 30+ issue resolutions |
| [AGENT_ROLES_MATRIX.md](AGENT_ROLES_MATRIX.md) | Agent capabilities |
| [BACKGROUND_AGENTS.md](../docs/BACKGROUND_AGENTS.md) | Daemon documentation |
| [CONTRIBUTING.md](../docs/CONTRIBUTING.md) | Contribution guide |

---

## Feedback & Improvement 💬

This onboarding guide is a living document. Help us improve it!

**Found something unclear?**
- Open an issue on GitHub
- Suggest improvements via PR
- Update this document directly

**Had a great onboarding experience?**
- Share your success story
- Help onboard the next person
- Contribute to documentation

**Struggled with something?**
- Document the issue in TROUBLESHOOTING.md
- Update this guide with what you learned
- Help prevent others from hitting the same issue

---

**Document Version:** 1.0  
**Last Updated:** 2025-10-04  
**Maintained By:** OODATCAA System Team  
**Next Review:** 2025-11-04

**Welcome to the OODATCAA community! Happy autonomous developing! 🚀**

For questions or issues, refer to [CONTRIBUTING.md](../docs/CONTRIBUTING.md) or open an issue.

