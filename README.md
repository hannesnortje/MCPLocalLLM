# Cursor OODATCAA Dev Pack — Python (Autonomous Mode)

A fully autonomous multi-agent development system for Python. **You define the objective, agents build the product.**

Built on the OODATCAA loop: Observe → Orient → Decide → Act → Test → Check → Adapt → Archive

---

## ⚡ Quick Start (3 Steps)

### 1. Install Dependencies
```bash
cd /path/to/PYTemplate
pip install -e .[dev]
pre-commit install  # optional
```

### 2. Configure Cursor Rules
- Open Cursor → Settings → Rules → **User Rules**
  - Paste contents of `.oodatcaa/config/UserRules.md`
- Open Cursor → Settings → Rules → **Project Rules**
  - Paste contents of `.oodatcaa/config/ProjectRules.md`

### 3. Define Your Product Objective
**Edit `.oodatcaa/objectives/OBJECTIVE.md`** (this is the ONLY file you need to edit):

```markdown
## Vision (Why)
Build a fast CSV parser for data pipelines

## Outcome (What)
- Parse CSV files with 10M+ rows
- Support RFC 4180 spec
- Performance: p95 < 100ms for 100k rows

## Success Criteria (Measurable)
- [ ] Functional: 100% of RFC 4180 test cases pass
- [ ] Performance: Benchmark tests meet p95 threshold
- [ ] Quality: ≥ 85% coverage; 0 high-severity audit issues
- [ ] Documentation: README + API docs complete

## Constraints
- Python 3.11+
- Type hints (mypy strict)
- Security: pip-audit clean
```

### 4. Launch the Autonomous System
Open a Cursor chat and paste:
```
Load @Cursor Rules and @Project Rules. 
Run the prompt in .oodatcaa/prompts/negotiator.md exactly. 
Return only file diffs.
```

Click **Run in Background** ✨

**That's it!** The Negotiator will coordinate everything and tell you when to launch other agents as work becomes available.

📖 See `.oodatcaa/AGENT_MANAGEMENT.md` for detailed agent lifecycle management.

---

## 🤖 What Happens Next (Fully Autonomous)

1. **Negotiator** starts and reads your OBJECTIVE.md
2. Negotiator tells you: "⚠️ LAUNCH AGENT: Sprint Planner"
3. You launch **Sprint Planner** → generates Sprint 1 goal
4. Negotiator tells you: "⚠️ LAUNCH AGENT: Planner"
5. You launch **Planner** → breaks tasks into detailed plans
6. Negotiator tells you: "⚠️ LAUNCH AGENT: Builder"
7. You launch **Builder(s)** → implement features on branches
8. Negotiator tells you: "⚠️ LAUNCH AGENT: Tester"
9. You launch **Tester** → validates acceptance criteria
10. Negotiator coordinates **Integrator** → merges PRs and tags releases
11. **Sprint Planner** detects when project is 100% complete

**The Negotiator guides you!** It will tell you exactly when and which agents to launch.

**You just watch the agents work!** Monitor progress in:
- `.oodatcaa/objectives/SPRINT_GOAL.md` — Current sprint & progress
- `.oodatcaa/work/AGENT_LOG.md` — Detailed execution log
- `.oodatcaa/work/SPRINT_LOG.md` — Sprint summaries

When complete, agents generate `.oodatcaa/objectives/PROJECT_COMPLETION_REPORT.md`

---

## 📂 Repository Structure

```
.
├── .oodatcaa/                      # All OODATCAA system files
│   ├── config/                     # Cursor Rules
│   │   ├── UserRules.md            # Global multi-agent doctrine
│   │   └── ProjectRules.md         # Python-specific commands & gates
│   ├── objectives/                 # Strategic planning
│   │   ├── OBJECTIVE.md            # 👈 YOU EDIT THIS (only file you need)
│   │   ├── SPRINT_GOAL.md          # Agent-generated sprint goals
│   │   └── RELEASE_CHECKLIST.md    # Release checklist
│   ├── work/                       # Active sprint work (agent-managed)
│   │   ├── SPRINT_BACKLOG.md       # Sprint backlog items
│   │   ├── SPRINT_PLAN.md          # Current sprint assignments
│   │   ├── AGENT_PLAN.md           # Detailed implementation plan
│   │   ├── TEST_PLAN.md            # Test commands & acceptance criteria
│   │   ├── AGENT_LOG.md            # Append-only execution log
│   │   ├── SPRINT_LOG.md           # Sprint summary & decisions
│   │   └── SPRINT_QUEUE.json       # Work queue with status & deps
│   ├── prompts/                    # Agent prompt templates
│   └── scripts/                    # Helper scripts (lease.sh, lock.sh)
├── docs/                           # Project documentation
├── src/app_pkg/                    # Source code (agents write here)
├── tests/                          # Tests (agents write here)
└── pyproject.toml                  # Package config (customize as needed)
```

## Repository Structure

```
.
├── .oodatcaa/                      # All OODATCAA system files
│   ├── config/                     # Cursor Rules
│   │   ├── UserRules.md            # Global multi-agent doctrine
│   │   └── ProjectRules.md         # Python-specific commands & gates
│   ├── objectives/                 # Strategic planning
│   │   ├── OBJECTIVE.md            # Product objective (what & why)
│   │   ├── SPRINT_GOAL.md          # Sprint exit criteria
│   │   └── RELEASE_CHECKLIST.md    # Release checklist
│   ├── work/                       # Active sprint work
│   │   ├── SPRINT_BACKLOG.md       # Sprint backlog items
│   │   ├── SPRINT_PLAN.md          # Current sprint assignments
│   │   ├── AGENT_PLAN.md           # Detailed implementation plan
│   │   ├── TEST_PLAN.md            # Test commands & acceptance criteria
│   │   ├── AGENT_LOG.md            # Append-only execution log
│   │   ├── SPRINT_LOG.md           # Sprint summary & decisions
│   │   └── SPRINT_QUEUE.json       # Work queue with status & deps
│   ├── prompts/                    # Agent prompt templates
│   └── scripts/                    # Helper scripts (lease.sh, lock.sh)
├── docs/                           # Project documentation
│   ├── CONTRIBUTING.md
│   ├── SECURITY.md
│   └── BRANCH_PROTECTION.md
├── src/app_pkg/                    # Source code
├── tests/                          # Tests (unit + acceptance)
└── .github/                        # CI workflows
```

## Development Commands

```bash
# Format code
make fmt

# Run all gates
make gates

# Run tests
make test

# Full check (gates + tests + coverage)
make check

# Build package
make build

# Security audit
make audit

# Create baseline tag
make tag TICKET=W123

# Rollback to baseline
make rollback TAG=pre/W123-YYYY-MM-DDTHH-MM-SS
```

## 🎯 Autonomous Workflow

The system operates in a continuous loop:

```
User: Define OBJECTIVE.md
  ↓
Negotiator: Check if sprint exists
  ↓ (no sprint)
Sprint Planner: Generate Sprint 1 goal from objective
  ↓
Planner: Break sprint into detailed tasks
  ↓
Builder(s): Implement features in parallel
  ↓
Tester: Validate acceptance criteria
  ↓
Integrator: Merge PRs, tag releases
  ↓
Negotiator: Check sprint completion
  ↓
Sprint Planner: Generate Sprint 2 (or declare project complete)
  ↓
... repeat until 100% objective achieved
```

### Key Features
- **Zero manual sprint planning** — Agents decide scope and timeline
- **Autonomous completion detection** — Agents know when project is done
- **Adaptive** — Refiner handles failures; Sprint Planner adjusts course
- **Parallel work** — Multiple builders work simultaneously
- **Full traceability** — Every decision logged

## License

See LICENSE file.

