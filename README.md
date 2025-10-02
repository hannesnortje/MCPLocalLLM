# MCPLocalLLM — Small Coder Model Training with MCP Integration

A locally fine-tuned coding assistant with context preservation and daily learning capabilities, built on the Model Context Protocol (MCP).

**Building a 7B parameter model optimized for M1 Max** that embeds procedural knowledge, custom definitions, and architectural patterns while providing dual-layer context preservation through MCP integration.

Built with the OODATCAA autonomous development loop: Observe → Orient → Decide → Act → Test → Check → Adapt → Archive

---

## ⚡ Quick Start

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

## 🛠 Setup & Installation

Complete setup guide for the MCP Local LLM training system.

### Prerequisites

Before you begin, ensure you have:

- **Python 3.11 or 3.12** (required)
- **32GB RAM** (recommended for M1 Max)
- **Docker Desktop** (optional, for Qdrant vector database)
- **Git** (for version control)
- **pip** (Python package manager)

### Step 1: Clone and Navigate

```bash
git clone <repository-url>
cd MCPLocalLLM
```

### Step 2: Run Automated Setup

The setup script will create a virtual environment, install dependencies, and configure the project:

```bash
./scripts/setup-dev.sh
```

This script will:
- ✅ Check Python version (3.11+)
- ✅ Create virtual environment (`.venv/`)
- ✅ Install Python dependencies
- ✅ Create required directories (`data/`, `logs/`, `policy/`)
- ✅ Copy configuration templates (`.env.example` → `.env`, `config.example.yaml` → `config.yaml`)
- ✅ Verify Docker availability (optional)
- ✅ Display setup summary

### Step 3: Validate Environment

Verify your environment is correctly configured:

```bash
make validate-env
# or: python scripts/validate-env.py
```

This will check:
- ✅ Python version compatibility
- ✅ Virtual environment activated
- ✅ Required directories exist
- ✅ Configuration files present
- ✅ Python dependencies installed
- ⚠️ Docker availability (optional)
- ⚠️ Qdrant connection (optional)

### Step 4: Configure Environment Variables

Edit `.env` to customize your setup:

```bash
# Qdrant Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_MODE=local

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
EMBEDDING_DEVICE=cpu

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/mcp-server.log

# Training-specific
MARKDOWN_CHUNK_SIZE=1000
MARKDOWN_CHUNK_OVERLAP=200
```

See `.env.example` for all available options and documentation.

### Step 5: Start Qdrant (Optional)

If using Docker for Qdrant:

```bash
docker-compose up -d qdrant
```

Verify Qdrant is running:
```bash
curl http://localhost:6333/health
```

### Configuration Files

**`.env`** — Environment variables for runtime configuration
- Qdrant connection settings
- Embedding model configuration
- Logging levels
- Training parameters

**`config.yaml`** — Application configuration
- Server name and mode
- Memory management settings
- Policy system configuration
- Search and retrieval parameters

Both files are created from templates during setup. Customize as needed for your training workflow.

### Troubleshooting

#### Issue 1: Python Version Mismatch
**Problem:** Setup script fails with "Python 3.11+ required"
**Solution:** 
```bash
# Install Python 3.11+ using pyenv or system package manager
pyenv install 3.11.9
pyenv local 3.11.9
```

#### Issue 2: Virtual Environment Not Activated
**Problem:** Dependencies not found or wrong Python version
**Solution:**
```bash
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
```

#### Issue 3: Docker/Qdrant Connection Failed
**Problem:** Validation fails with Qdrant connection error
**Solution:** 
- Docker is **optional** for development
- Start Qdrant: `docker-compose up -d qdrant`
- Or use Qdrant in memory mode (no Docker needed)

#### Issue 4: Permission Denied on Setup Script
**Problem:** `bash: ./scripts/setup-dev.sh: Permission denied`
**Solution:**
```bash
chmod +x scripts/setup-dev.sh
./scripts/setup-dev.sh
```

#### Issue 5: Missing Dependencies
**Problem:** Import errors or missing packages
**Solution:**
```bash
pip install -e ".[dev]"  # Reinstall all dependencies
```

For more troubleshooting, see `docs/mcp/TROUBLESHOOTING.md` or check the validation output for specific issues.

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

