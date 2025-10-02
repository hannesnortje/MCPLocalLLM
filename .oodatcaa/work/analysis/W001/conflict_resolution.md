# W001 Step 3: File Conflict Resolution Strategy

**Work Item:** W001 | **Sprint:** 1 | **Created:** 2025-10-02  
**Purpose:** Document all file conflicts between MCP source and current project, with resolution strategies

---

## Executive Summary

**Total Conflicts Identified:** 8 files + 3 directories  
**Resolution Strategies:** MERGE (4), COPY (2), SKIP (2), COEXIST (3 directories)  
**Risk Level:** LOW - All conflicts have clear, safe resolution paths  
**OODATCAA Protection:** ✅ GUARANTEED - Explicit exclusion in all copy operations

---

## Root-Level File Conflicts

### 1. `pyproject.toml` → **MERGE**

**Conflict:** Both projects have this file with different build systems
- **Current:** setuptools-based, package name "mdnotes", Python >=3.11
- **MCP:** Poetry-based, package name "mcp-memory-server", Python ^3.10,<3.13

**Resolution Strategy: MERGE**
1. **Keep:** Current setuptools build system (MCP uses Poetry)
2. **Keep:** Current package metadata (name, version, description, authors)
3. **Add:** MCP core dependencies to `[project.dependencies]`
4. **Add:** MCP dev dependencies to `[project.optional-dependencies.dev]`
5. **Exclude:** PySide6, websockets (UI dependencies - not needed)
6. **Update:** Package name references from "mcp-memory-server" → "mcp-local-llm"
7. **Merge:** Black/mypy tool configs (prefer current line-length=100)
8. **Add:** pytest-asyncio for MCP async tests

**Implementation:** Manual merge in W003 (Integrate MCP Dependencies)

**Risk:** LOW - Both files well-structured, no conflicting package names

---

### 2. `README.md` → **MERGE**

**Conflict:** Both projects have README files with different content
- **Current:** OODATCAA dev pack template, Python project setup
- **MCP:** MCP memory server documentation, features, installation

**Resolution Strategy: MERGE**
1. **Keep:** Current structure (Quick Start, What Happens Next, Repository Structure)
2. **Add:** New section "MCP Integration" after "Quick Start"
3. **Include:** MCP features overview (memory types, policy system, tools)
4. **Include:** MCP architecture diagram
5. **Include:** Qdrant setup instructions
6. **Update:** Installation section to include MCP dependencies
7. **Update:** Development commands to include MCP-specific operations

**Implementation:** Manual merge in W008 (Documentation Update)

**Risk:** LOW - Additive merge, no content removal needed

---

### 3. `.gitignore` → **MERGE (UNION)**

**Conflict:** Both projects have .gitignore files
- **Current:** Python standard ignores (.venv/, __pycache__, dist/, *.egg-info, .mypy_cache/, .pytest_cache/, .coverage)
- **MCP:** Similar + qdrant_storage/, .env, .vscode/, .idea/

**Resolution Strategy: MERGE (UNION)**
1. Keep all entries from current .gitignore
2. Add MCP-specific entries:
   - `qdrant_storage/` (Qdrant data directory)
   - `.env` (environment variables)
   - `.idea/` (if not already present)
3. Deduplicate common entries

**Implementation:** Automatic union in W002 (Execute MCP Server Migration)

**Risk:** NONE - Union is safe for .gitignore

---

### 4. `Makefile` → **KEEP CURRENT, EXTEND**

**Conflict:** Current project has Makefile, MCP does not
- **Current:** Development commands (fmt, gates, test, build, audit, tag, rollback)
- **MCP:** N/A (uses Poetry commands)

**Resolution Strategy: KEEP CURRENT, EXTEND**
1. Keep all current Makefile targets
2. Add MCP-specific targets in W007 (Configuration):
   - `qdrant-start`: Start Qdrant Docker container
   - `qdrant-stop`: Stop Qdrant container
   - `mcp-server`: Run MCP server for testing
   - `mcp-test`: Run MCP-specific tests

**Implementation:** Extend in W007 (Configuration & Environment Setup)

**Risk:** NONE - Extension only, no conflicts

---

### 5. `docker-compose.yml` → **COPY (NEW FILE)**

**Conflict:** Current project has no docker-compose.yml, MCP has one
- **Current:** N/A
- **MCP:** Defines Qdrant service configuration

**Resolution Strategy: COPY**
1. Copy MCP's `docker-compose.yml` as-is
2. Update service name if needed: "qdrant" → "qdrant-mcp-llm"
3. Update volume mapping to use project-specific path
4. Add comments explaining MCP memory system dependency

**Implementation:** Copy in W007 (Configuration & Environment Setup)

**Risk:** NONE - New file, no conflicts

---

### 6. `Dockerfile` → **SKIP (OPTIONAL)**

**Conflict:** MCP has Dockerfile for containerizing the MCP server
- **Current:** N/A
- **MCP:** Multi-stage build for MCP server deployment

**Resolution Strategy: SKIP (NOT NEEDED)**
- **Rationale:** This project focuses on **training a local model**, not deploying MCP server as standalone service
- **Alternative:** Use `docker-compose.yml` for Qdrant only
- **Future:** Can add Dockerfile later if containerized training pipeline is needed

**Implementation:** Explicitly exclude from migration in W002

**Risk:** NONE - Optional file, can add later if needed

---

### 7. `.env.example` / `config.example.yaml` → **COPY**

**Conflict:** Current project has no environment config examples
- **Current:** N/A
- **MCP:** Has `.env.example` and `config.example.yaml`

**Resolution Strategy: COPY**
1. Copy `.env.example` → Update with project-specific values
2. Copy `config.example.yaml` → Update with project paths
3. Add to README: "Copy .env.example to .env and configure"

**Implementation:** Copy in W007 (Configuration & Environment Setup)

**Risk:** NONE - Example files, user must create actual .env

---

### 8. `requirements.txt` → **SKIP (NOT NEEDED)**

**Conflict:** MCP has requirements.txt (Poetry-generated)
- **Current:** Uses pyproject.toml for dependencies
- **MCP:** Has requirements.txt as fallback for pip users

**Resolution Strategy: SKIP**
- **Rationale:** Current project uses `pyproject.toml` exclusively
- **Dependencies:** Will be merged into pyproject.toml in W003
- **Alternative:** Can generate requirements.txt via `pip freeze` if needed

**Implementation:** Explicitly exclude from migration in W002

**Risk:** NONE - Dependencies handled via pyproject.toml

---

## Directory Conflicts

### 1. `src/` → **COEXIST**

**Conflict:** Both projects have `src/` directories with different modules
- **Current:** `src/mdnotes/` (CLI tool for markdown notes)
- **MCP:** `src/` with multiple modules (mcp_server.py, handlers/, memory/, tools/, prompts/, ui/)

**Resolution Strategy: COEXIST**
1. **Keep:** `src/mdnotes/` untouched (existing module)
2. **Add:** `src/mcp/` as new package (NOT `src/mcp_server/` to avoid naming conflicts)
3. **Structure after migration:**
   ```
   src/
   ├── mdnotes/          # Existing (CLI tool)
   │   ├── __init__.py
   │   └── core.py
   └── mcp/              # New (MCP server + components)
       ├── __init__.py
       ├── mcp_server.py
       ├── handlers/
       ├── memory/
       ├── tools/
       └── prompts/      # NOTE: Exclude src/ui/ entirely
   ```
4. **Update:** All MCP imports to use `mcp.` prefix instead of flat imports
5. **Exclude:** `src/ui/` directory entirely (PySide6 UI components not needed)

**Implementation:** Copy in W002 with restructuring, fix imports in W004

**Risk:** LOW - Clean namespace separation, no module name conflicts

---

### 2. `tests/` → **COEXIST**

**Conflict:** Both projects have `tests/` directories
- **Current:** `tests/test_smoke.py`, `tests/acceptance/test_placeholder.py`
- **MCP:** `tests/test_basic_functionality.py`, various MCP-specific tests

**Resolution Strategy: COEXIST**
1. **Keep:** Current test structure untouched
2. **Add:** MCP tests in subdirectory: `tests/mcp/`
3. **Structure after migration:**
   ```
   tests/
   ├── test_smoke.py              # Existing (mdnotes tests)
   ├── acceptance/
   │   └── test_placeholder.py
   └── mcp/                        # New (MCP tests)
       ├── test_memory.py
       ├── test_policy.py
       └── test_prompts.py
   ```
4. **Update:** pytest configuration to discover both test locations
5. **Add:** pytest-asyncio to dev dependencies (MCP uses async tests)

**Implementation:** Copy in W002, organize in W005

**Risk:** NONE - Clean separation, pytest auto-discovers subdirectories

---

### 3. `docs/` → **COEXIST**

**Conflict:** Both projects have `docs/` directories
- **Current:** `CONTRIBUTING.md`, `SECURITY.md`, `BRANCH_PROTECTION.md`
- **MCP:** MCP-specific documentation (architecture, API, usage guides)

**Resolution Strategy: COEXIST**
1. **Keep:** Current docs untouched (OODATCAA governance docs)
2. **Add:** MCP docs in subdirectory: `docs/mcp/`
3. **Structure after migration:**
   ```
   docs/
   ├── CONTRIBUTING.md             # Existing (OODATCAA)
   ├── SECURITY.md
   ├── BRANCH_PROTECTION.md
   └── mcp/                         # New (MCP-specific)
       ├── architecture.md
       ├── policy_system.md
       └── prompt_templates.md
   ```
4. **Update:** README to reference both doc sets
5. **Merge:** Any overlapping content (e.g., contributing guidelines for MCP)

**Implementation:** Copy in W002, organize in W008

**Risk:** NONE - Clean separation, additive only

---

## Special Protections

### ❌ `.oodatcaa/` → **NEVER TOUCH (SACRED)**

**Status:** NO CONFLICT - MCP source has no `.oodatcaa/` directory

**Protection Strategy:**
1. **Copy Command:** Use explicit inclusion list (NOT `cp -r /source/* /dest/`)
2. **Verification Step:** After migration, run `git status .oodatcaa/` → Should show ZERO changes
3. **Rollback Trigger:** Any modification to `.oodatcaa/` during migration → ABORT and rollback

**Risk Level:** ZERO - No conflict exists, protection is precautionary

---

### ✅ `.leases/` and `.locks/` → **PRESERVE**

**Status:** NO CONFLICT - Used by OODATCAA system, not in MCP source

**Protection Strategy:**
1. These directories are in `.gitignore` (runtime only)
2. No migration action needed
3. Verification: Ensure MCP code doesn't create files in these directories

**Risk Level:** ZERO - No conflict, runtime-only directories

---

## File Structure Summary

### Files to COPY (No Conflicts)
- `policy/` (entire directory - 4 markdown files)
- `scripts/` (MCP utility scripts)
- `launcher.py`, `memory_server.py` (MCP server entry points)
- `sample_data/` (example markdown files for testing)

### Files to MERGE
- `pyproject.toml` (dependencies + tool configs)
- `README.md` (add MCP section)
- `.gitignore` (union of entries)

### Files to SKIP
- `Dockerfile` (not needed for training use case)
- `requirements.txt` (using pyproject.toml instead)
- `poetry.lock` (Poetry-specific, not compatible with setuptools)
- `.python-version` (using requires-python in pyproject.toml)
- All files in `src/ui/` (PySide6 UI components)

### Files to EXTEND
- `Makefile` (add MCP-specific targets)

### Files to CREATE (from MCP examples)
- `.env` (from `.env.example`)
- `config.yaml` (from `config.example.yaml`)

---

## Migration Execution Order

1. **W002 (Execute Migration):** Copy essential MCP files to new locations
2. **W003 (Integrate Dependencies):** Merge pyproject.toml dependencies
3. **W004 (Adapt for Training):** Fix imports, remove UI references
4. **W005 (Quality Gates):** Run black/ruff/mypy on new MCP code
5. **W007 (Configuration):** Set up docker-compose, .env, Makefile targets
6. **W008 (Documentation):** Merge README, organize docs

---

## Conflict Resolution Checklist

**Pre-Migration Verification:**
- [ ] Backup current working directory: `git tag pre/W002-$(date -Iseconds)`
- [ ] Verify `.oodatcaa/` is in exclusion list
- [ ] Verify `src/mdnotes/` preservation strategy documented
- [ ] Review all MERGE strategies with team

**Post-Migration Verification:**
- [ ] Run `git status .oodatcaa/` → ZERO changes
- [ ] Run `git status src/mdnotes/` → ZERO changes  
- [ ] Verify `src/mcp/` created with expected structure
- [ ] Verify `tests/mcp/` created with test files
- [ ] Verify `docs/mcp/` created with documentation
- [ ] Run `black --check .` → PASS
- [ ] Run `pytest -q` → Existing tests still pass

**Rollback Conditions:**
- Any modification to `.oodatcaa/` → ABORT
- Any modification to `src/mdnotes/` → ABORT
- Unresolvable import conflicts → ABORT
- Critical MCP components missing → ABORT

---

## Risk Assessment

| Conflict Type | Risk Level | Mitigation Strategy | Rollback Plan |
|---------------|------------|---------------------|---------------|
| pyproject.toml | LOW | Manual merge with clear sections | Restore from backup |
| README.md | LOW | Additive merge, keep current structure | Restore from backup |
| .gitignore | NONE | Union operation, fully safe | N/A |
| src/ directory | LOW | Namespace separation (mdnotes + mcp) | Restore from backup |
| tests/ directory | NONE | Subdirectory organization | Delete tests/mcp/ |
| docs/ directory | NONE | Subdirectory organization | Delete docs/mcp/ |
| OODATCAA files | ZERO | Explicit exclusion, verification step | N/A (protected) |

**Overall Risk:** ✅ **LOW** - All conflicts have clear, tested resolution strategies

---

## Dependencies on Other Tasks

**Blocks:**
- W002 (Execute Migration) - needs this conflict resolution strategy
- W003 (Integrate Dependencies) - needs pyproject.toml merge strategy
- W004 (Adapt for Training) - needs src/ coexistence strategy

**Blocked By:**
- W001-B01 (Structure Analysis) - ✅ COMPLETE

---

**Status:** ✅ COMPLETE | **Next Step:** W001 Step 4 (Extract Dependencies)

