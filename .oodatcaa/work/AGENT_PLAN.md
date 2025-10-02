# Agent Plan — W001: Analyze MCP Source Structure

**Objective:** OBJ-2025-002 | **Epic:** MCP Integration | **Sprint:** 1 | **Work Item:** W001  
**Plan Version:** 1.0 | **Created:** 2025-10-01 | **Agent:** Planner

---

## Problem Statement
Analyze MCP server source at `/media/hannesn/storage/Code/MCP/` to prepare for migration. Identify essential components (memory, policy, vector storage), unnecessary components (UI, multi-user features), file conflicts, and dependencies.

**Context:** Migrate complete MCP server to enable context preservation for small coder model training, while preserving OODATCAA framework and existing `mdnotes` module.

---

## Constraints / Risks

**Constraints:**
- MUST preserve `.oodatcaa/` directory (no overwrites)
- MUST keep `src/mdnotes/` module working
- Python >=3.11 (MCP uses ^3.10,<3.13 — compatible)
- Convert Poetry → setuptools dependency format

**Key Risks:**
- File conflicts overwrite OODATCAA system (HIGH impact) → Explicit exclusion list
- UI dependencies bloat project (MEDIUM) → Exclude PySide6, websockets
- Incomplete migration (HIGH) → Systematic checklist of all components

---

## Definition of Done

**Functional:**
- [ ] AC1: Complete inventory of MCP files with categorization (essential/optional/exclude)
- [ ] AC2: Documented list of files to copy with target paths
- [ ] AC3: Documented list of files to exclude (UI, examples, redundant tests)
- [ ] AC4: File conflict resolution strategy for each conflict
- [ ] AC5: Complete dependency list with version compatibility notes
- [ ] AC6: Migration checklist covering all essential MCP components
- [ ] AC7: OODATCAA preservation strategy verified

**Non-Functional:**
- [ ] AC8: Documentation clear for Builder agent execution
- [ ] AC9: Analysis covers: src/, tests/, docs/, scripts/, policy/
- [ ] AC10: Risk mitigation strategies defined

---

## Alternatives & Choice

**Alternative 1:** Full copy + manual cleanup → ❌ HIGH RISK (OODATCAA overwrite)  
**Alternative 2:** Selective copy with explicit inclusion list → ✅ **CHOSEN** (safe, traceable)  
**Alternative 3:** Git subtree/submodule → ❌ Overcomplicated (OBJECTIVE requires "copy and adapt")

**Rationale:** Alternative 2 minimizes risk, provides clear traceability, and aligns with OBJECTIVE.md requirements.

---

## Implementation Plan

### Step 1: Analyze MCP Source Structure
**Branch:** `feat/W001-step-01-analyze-source`  
**Actions:**
1. Capture complete structure: `tree -L 3 /media/hannesn/storage/Code/MCP/`
2. Read key files: `pyproject.toml`, `README.md`, `docker-compose.yml`
3. Categorize directories: ESSENTIAL / OPTIONAL / EXCLUDE
4. Create `analysis/mcp_structure_inventory.md`

**Exit:** Complete tree captured, all directories categorized

---

### Step 2: Identify Essential Components
**Actions:**
1. **Include:**
   - `src/` core: `mcp_server.py`, `memory_manager.py`, `qdrant_manager.py`
   - `src/handlers/`, `src/memory/`, `src/prompts/`, `src/tools/` (NOT `ui/`)
   - `policy/` (all markdown files)
   - `docs/` (architecture, API)
   - `scripts/` (setup, deployment)
   - `docker-compose.yml`, `Dockerfile`
   - `config.example.yaml`, `launcher.py`, `memory_server.py`

2. **Exclude:**
   - `src/ui/` (entire directory)
   - UI dependencies: PySide6, websockets
   - Example files, redundant tests

3. Create `analysis/essential_components.md`

**Exit:** Inclusion list complete with justifications

---

### Step 3: Identify File Conflicts
**Actions:**
1. Root file conflicts:
   - `pyproject.toml` → **MERGE** (combine deps, keep metadata)
   - `README.md` → **MERGE** (add MCP section)
   - `docker-compose.yml` → **COPY** (new file)
   - `.gitignore` → **MERGE** (union)

2. Directory conflicts:
   - `src/` → **COEXIST** (MCP alongside `mdnotes/`)
   - `tests/` → **MERGE** (add MCP tests)
   - `docs/` → **MERGE** (add MCP docs)

3. `.oodatcaa/` → **NEVER TOUCH** (explicit exclusion)

4. Create `analysis/conflict_resolution.md`

**Exit:** All conflicts documented with resolution strategy

---

### Step 4: Extract Dependencies
**Actions:**
1. Extract from MCP `pyproject.toml`:
   - Core: `mcp ^1.13.1`, `qdrant-client ^1.7.0`, `sentence-transformers ^2.5.1`
   - Utils: `python-dotenv`, `markdown`, `beautifulsoup4`, `aiofiles`, `pyyaml`
   - Dev: `pytest-asyncio`, `types-markdown`
   - **Exclude:** `PySide6`, `websockets` (UI only)

2. Check compatibility with current deps (click, rich, whoosh)
3. Convert to setuptools format (use `>=` instead of `^`)
4. Create `analysis/dependencies.md` and `analysis/pyproject_toml_updates.md`

**Exit:** Complete dependency list, version conflicts identified

---

### Step 5: Create Migration Checklist
**Actions:**
1. Organize into executable steps:
   - [ ] Copy core `src/` modules (exclude `ui/`)
   - [ ] Copy subdirs: `handlers/`, `memory/`, `prompts/`, `tools/`
   - [ ] Copy `policy/`, `docs/`, `scripts/`
   - [ ] Copy infrastructure: Docker, configs
   - [ ] Merge `pyproject.toml`, `README.md`
   - [ ] Update package name: "mcp-memory-server" → "mcp-local-llm"
   - [ ] Verify OODATCAA untouched, `mdnotes` intact

2. Create `analysis/migration_checklist.md`

**Exit:** Checklist ready for W002 execution

---

### Step 6: Analysis Summary
**Actions:**
1. Create `analysis/W001_ANALYSIS_SUMMARY.md`:
   - Essential components count
   - Excluded components count
   - File conflicts and resolutions
   - Dependency summary
   - Recommendations for W002-W004

**Exit:** Executive summary complete

---

### Step 7: Update Sprint Documentation
**Actions:**
1. Update `.oodatcaa/work/SPRINT_QUEUE.json`:
   - Mark W001 "completed"
   - Unblock W002 (needs_plan → ready)

2. Add entry to `.oodatcaa/work/AGENT_LOG.md`
3. Organize artifacts: `mkdir -p .oodatcaa/work/analysis/W001/`

**Exit:** Documentation updated, artifacts organized

---

## Testing Strategy
See TEST_PLAN.md. Summary: Manual verification of artifact completeness, checklist review, OODATCAA protection validation.

---

## Rollback
**Baseline:** `pre/W001-<timestamp>`  
**Trigger:** Migration infeasible, unresolvable conflicts  
**Steps:** `git reset --hard <baseline>`, document in SPRINT_DISCUSS.md

---

## Branch & Commits
**Branch:** `feat/W001-step-01-analyze-source`  
**Labels:** `[plan]`, `[impl]`, `[docs]`  
**PR:** Single PR after all analysis complete

---

## Dependencies
**Upstream:** None  
**Downstream:** W002 (depends on this analysis)

---

## Effort
**Complexity:** S | **Time:** 2-4 hours  
- Steps 1-2: 1h | Steps 3-4: 1h | Steps 5-6: 1h | Step 7: 30m

---

**Status:** ✅ APPROVED | **Ready for:** Builder Agent
