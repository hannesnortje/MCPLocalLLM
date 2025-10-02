# W007: Configuration & Environment Setup — AGENT PLAN

**Task ID:** W007  
**Task Title:** Configuration & Environment Setup  
**Type:** Infra  
**Complexity:** S (Small)  
**Objective:** OBJ-2025-002  
**Sprint:** 1  
**Dependencies:** W003 (satisfied ✅)  

**Planner:** agent-planner-A  
**Plan Version:** 1.0  
**Created:** 2025-10-03T15:50:00+00:00  

---

## Traceability

**Objective ID:** OBJ-2025-002 — Small Coder Model Training with MCP Integration  
**Epic:** MCP Server Foundation (Sprint 1)  
**Sprint Goal:** Migrate and integrate MCP server infrastructure  
**Sprint:** 1  

**Links to Objective:**
- OBJECTIVE.md → Deployment Ready → Docker containers for Qdrant and training environment
- OBJECTIVE.md → Deployment Ready → Automated setup scripts
- OBJECTIVE.md → Documentation & Deployment → Setup instructions

---

## Problem Statement

The MCP server was successfully migrated (W002), dependencies integrated (W003), code quality improved (W004-W005), and integration tests added (W006). However, the configuration and environment setup is incomplete for the training use case:

1. **No `.env.example` file** — Developers don't have a template for environment variables
2. **Docker configuration incomplete** — `docker-compose.yml` references production settings, needs training mode
3. **Configuration needs training adaptation** — `config.example.yaml` has generic settings, needs training-specific values
4. **Setup instructions missing** — No documented setup process for new developers
5. **Environment validation missing** — No way to verify correct configuration

This blocks developers from easily setting up and running the MCP server for training workflows.

---

## Constraints & Interfaces

### Constraints
- **Must preserve existing functionality** — MCP server tests (W006) must still pass
- **Training-focused configuration** — Settings optimized for local M1 Max training, not production
- **Qdrant local mode** — Must support local Docker Qdrant for development (no cloud dependency)
- **Python version constraint** — Must work with Python 3.11-3.12 (as per pyproject.toml)
- **Documentation must be clear** — Non-technical users should be able to follow setup

### Interfaces
- **config.py** — Environment variable loading mechanism
- **server_config.py** — YAML configuration management
- **docker-compose.yml** — Container orchestration
- **pyproject.toml** — Python dependencies (already configured in W003)
- **README.md** — User-facing documentation

### Risks
- **Configuration conflicts** — Incorrect environment variables could break tests
- **Docker compatibility** — Docker Desktop might not work on all systems (fallback needed)
- **Path issues** — Relative vs absolute paths in configuration
- **Security** — API keys or secrets must not be committed to repo

---

## Definition of Done (DoD)

### Functional Requirements
1. ✅ **`.env.example` created** with all required environment variables documented
2. ✅ **Docker configuration validated** with training-optimized settings
3. ✅ **Configuration files adapted** for training use case (CPU inference, local Qdrant)
4. ✅ **Setup script working** (`scripts/setup-dev.sh` or equivalent)
5. ✅ **Environment validation tool** to check prerequisites

### Non-Functional Requirements
1. ✅ **All existing tests pass** (W006 integration tests remain functional)
2. ✅ **Quality gates pass** (black, ruff, mypy, pytest, build)
3. ✅ **Documentation updated** (README with setup instructions)
4. ✅ **Zero regressions** in MCP functionality

---

## Acceptance Criteria (Explicit)

### Functional ACs

**AC1: `.env.example` File Created**
- File path: `.env.example` at project root
- Contains all environment variables used by config.py and server_config.py
- Each variable documented with inline comment
- Example values provided (no real secrets)
- Covers: Qdrant, embedding, server, logging, policy, memory configuration

**AC2: Docker Configuration Validated**
- `docker-compose.yml` reviewed for training mode settings
- Qdrant container configured for local development
- Volume mounts correct (./data, ./logs, ./policy)
- Health checks working
- Container names appropriate for training project
- Memory limits appropriate for M1 Max (32GB RAM)

**AC3: Config Files Adapted for Training**
- `config.example.yaml` updated with training-specific defaults
- Comments added explaining training-specific choices

**AC4: Setup Script Functional**
- Script exists: `scripts/setup-dev.sh` (or updated if exists)
- Creates virtual environment, installs dependencies, creates directories
- Provides clear error messages if prerequisites missing

**AC5: Environment Validation Tool**
- Python script or Makefile target: `make validate-env`
- Checks Python version, dependencies, Docker, Qdrant, .env file, directories
- Output: Clear success/failure with actionable error messages

### Quality ACs

**AC6: All Tests Pass (CRITICAL)**
- `pytest -q` → All tests pass (integration + smoke)
- W006 integration tests remain functional
- Zero test failures, zero test regressions

**AC7: Quality Gates Pass**
- `black --check .` → Pass
- `ruff check .` → Pass (or ≤28 errors as per W005 baseline)
- `mypy .` → Pass (or ≤401 errors as per W005 baseline)
- `python -m build` → Success
- `pip-audit` → No high-severity issues

**AC8: Documentation Updated (CRITICAL)**
- README.md includes "Setup & Installation" section
- Step-by-step setup instructions (5-10 steps max)
- Prerequisites listed (Python 3.11+, Docker optional)
- Troubleshooting section for common issues
- Configuration section explaining .env and config.yaml

**AC9: No Secrets Committed**
- `.gitignore` includes `.env`
- No real API keys, passwords, or secrets in `.env.example` or config files

**AC10: Clean Repository State**
- No temporary files committed
- All configuration files properly formatted
- Git status clean after work (only intended files)

---

## Implementation Plan (Step-by-Step)

### Step 1: Pre-Flight Setup (10 min) → W007-B01
1. Create feature branch from main
2. Create baseline tag
3. Inventory existing configuration
4. Document findings

### Step 2: Create `.env.example` File (30 min) → W007-B01
1. Create `.env.example` at project root
2. Add all environment variables with documentation
3. Verify .gitignore includes `.env`

### Step 3: Adapt Configuration for Training (25 min) → W007-B01
1. Review `config.example.yaml`
2. Update for training-specific defaults
3. Add comments explaining choices
4. Validate YAML syntax

### Step 4: Review/Update Docker Configuration (20 min) → W007-B01
1. Review `docker-compose.yml`
2. Verify Qdrant service configuration
3. Add comments for training mode
4. Test docker-compose syntax

### Step 5: Create/Update Setup Script (30 min) → W007-B01
1. Create or update `scripts/setup-dev.sh`
2. Make executable
3. Test script

### Step 6: Create Environment Validation (25 min) → W007-B01
1. Add `validate-env` target to `Makefile`
2. Create `scripts/validate-env.py`
3. Make executable
4. Test validation

### Step 7: Update README Documentation (30 min) → W007-B02
1. Add "Setup & Installation" section to README.md
2. Review for clarity and completeness

### Step 8: Quality Gates & Commit (20 min) → W007-B02
1. Run all quality gates
2. Verify all gates pass
3. Verify W006 integration tests still pass
4. Commit changes
5. Update AGENT_LOG.md, SPRINT_QUEUE.json

### Step 9: Final Validation (15 min) → W007-T01 (Tester)
1. Clone repo to fresh directory
2. Run setup script
3. Validate environment
4. Verify all 10 ACs
5. Document test results

---

## Task Breakdown (for SPRINT_QUEUE.json)

### W007-B01: Configuration Files + Setup Scripts (Steps 1-6)
- **Type:** Implementation
- **Complexity:** S
- **Status:** ready
- **Dependencies:** []
- **Plan Steps:** 1-6
- **Estimated Time:** ~2 hours

### W007-B02: Documentation + Quality Gates (Steps 7-8)
- **Type:** Implementation
- **Complexity:** S
- **Status:** blocked (depends on W007-B01)
- **Dependencies:** [W007-B01]
- **Plan Steps:** 7-8
- **Estimated Time:** ~50 minutes

### W007-T01: Testing & Validation (Step 9)
- **Type:** Testing
- **Complexity:** S
- **Status:** blocked (depends on W007-B02)
- **Dependencies:** [W007-B02]
- **Plan Steps:** 9
- **Estimated Time:** ~15 minutes

---

## Success Metrics

**Primary Metrics:**
- ✅ All 10 acceptance criteria pass
- ✅ Fresh setup completes in < 5 minutes (excluding download time)
- ✅ All W006 integration tests pass (zero regressions)
- ✅ All quality gates pass (or meet W005 baseline)

**Time Metrics:**
- Total estimated time: 3 hours 15 minutes (2h build + 50m docs + 15m test)
- Target completion: Within 4 hours (including buffer for issues)

---

**Plan Status:** COMPLETE  
**Next Action:** Negotiator assigns W007-B01 to Builder  
**Expected Completion:** 2025-10-03T19:00:00+00:00 (within ~3-4 hours from start)
