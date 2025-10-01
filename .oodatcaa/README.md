# OODATCAA System Files — Autonomous Mode

This directory contains all files for the **fully autonomous** OODATCAA multi-agent development system.

**Key Concept:** You only edit `objectives/OBJECTIVE.md`. Agents handle everything else — sprint planning, work breakdown, implementation, testing, and completion detection.

## Directory Structure

### `config/`
Cursor Rules that define the agent behavior and protocols:
- **UserRules.md** - Global multi-agent doctrine (paste into Cursor → User Rules)
- **ProjectRules.md** - Python-specific commands and gates (paste into Cursor → Project Rules)

### `objectives/`
Strategic planning and release management:
- **OBJECTIVE.md** - 👈 **USER INPUT** - The only file you need to edit! Product vision, success criteria, constraints.
- **SPRINT_GOAL.md** - 🤖 **AGENT-GENERATED** - Sprint goals created by Sprint Planner based on your objective.
- **RELEASE_CHECKLIST.md** - Release criteria and validation

### `work/`
Active sprint working files (updated by agents):
- **SPRINT_BACKLOG.md** - Sprint backlog work items
- **SPRINT_PLAN.md** - Current sprint assignments by role
- **AGENT_PLAN.md** - Detailed step-by-step implementation plan
- **TEST_PLAN.md** - Test commands and acceptance criteria
- **AGENT_LOG.md** - Append-only execution log (gate results, decisions)
- **SPRINT_LOG.md** - Sprint summary (shipped, rolled back, decisions)
- **SPRINT_QUEUE.json** - Work queue with task status and dependencies

### `prompts/`
Agent prompt templates for different roles:

**Autonomous Coordination:**
- **negotiator.md** - 🎯 **START HERE** - Control plane that coordinates everything
- **sprint-planner.md** - Generates sprint goals and detects project completion
- **project-completion-detector.md** - Evaluates objective achievement

**Development Workflow (triggered by Negotiator):**
- **planner.md** - Observe/Orient/Decide - creates detailed plans
- **builder.md** - Act - implements code changes
- **tester.md** - Test/Check - validates acceptance criteria
- **refiner.md** - Adapt - decides fixes vs rollbacks
- **integrator.md** - Archive - merges and documents

**Utilities:**
- **sprint-close.md** - Sprint retrospective
- **release.md** - Release finalization
- **triage.md** - Bug triage workflow

### `scripts/`
Helper scripts for lease and lock management:
- **lease.sh** - Acquire/heartbeat/release task leases
- **lock.sh** - Acquire/release file locks for shared documents

## Quick Start (Autonomous Mode)

### 1. Configure Cursor (one-time setup)
   - Copy `config/UserRules.md` → Cursor → Settings → User Rules
   - Copy `config/ProjectRules.md` → Cursor → Settings → Project Rules

### 2. Define Your Product (the ONLY file you edit!)
   - Edit `objectives/OBJECTIVE.md` with:
     - Vision (what problem you're solving)
     - Outcome (what success looks like)
     - Success criteria (measurable checkboxes)
     - Constraints (technical requirements)

### 3. Launch Autonomous System
   - Open Cursor chat and paste:
     ```
     Load @Cursor Rules and @Project Rules. 
     Run the prompt in .oodatcaa/prompts/negotiator.md exactly. 
     Return only file diffs.
     ```
   - Click **Run in Background**
   - **That's it!** Negotiator will tell you when/which other agents to launch.
   - See `AGENT_MANAGEMENT.md` for detailed agent lifecycle guide.

### 4. Monitor Progress (optional)
   - `objectives/SPRINT_GOAL.md` — Current sprint & objective progress %
   - `work/SPRINT_QUEUE.json` — Task status
   - `work/AGENT_LOG.md` — Detailed execution log
   - `work/SPRINT_LOG.md` — Sprint summaries

### 5. Project Completion
   - Agents detect when 100% of success criteria met
   - Generate `objectives/PROJECT_COMPLETION_REPORT.md`
   - System automatically stops

## Detailed Workflow

See `AUTONOMOUS_WORKFLOW.md` for complete lifecycle documentation.

## File Organization Benefits

- **Clean root directory** - All OODATCAA system files in one place
- **Clear separation** - Config vs objectives vs active work
- **Hidden by default** - Dotfile prefix keeps it out of the way
- **Easy to ignore** - Can gitignore `work/` files if desired
- **Discoverable** - Organized structure is self-documenting

