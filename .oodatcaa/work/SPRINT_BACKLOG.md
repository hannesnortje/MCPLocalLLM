# Sprint 1 Backlog (AGENT-GENERATED)

> **Sprint Goal:** MCP Server Foundation — Migrate and integrate MCP server infrastructure

---

## Work Items

### W001: Analyze MCP Source Structure
**Type:** Story  
**Complexity:** S  
**Status:** needs_plan

**Description:**  
Analyze the source MCP repository at `/media/hannesn/storage/Code/MCP/` to identify:
- Essential components (memory, policy, vector storage)
- Unnecessary components (UI, examples not needed for training)
- Potential file conflicts with current project structure
- Dependency requirements

**Acceptance Criteria:**
- [ ] Documented list of files/directories to copy
- [ ] Identified files to exclude or modify
- [ ] Conflict resolution strategy defined (preserve `.oodatcaa/`)
- [ ] Dependency list extracted from MCP source

**Links to Objective:**  
OBJECTIVE.md → MCP Integration (Critical) → Server Migration

---

### W002: Execute MCP Server Migration
**Type:** Story  
**Complexity:** M  
**Status:** needs_plan

**Description:**  
Copy the MCP server codebase from `/media/hannesn/storage/Code/MCP/` to this project:
- Use `cp -r` to migrate essential files
- Resolve file conflicts (prioritize MCP files, preserve `.oodatcaa/`)
- Rename package from "mcp-memory-server" to "mcp-local-llm"
- Update all internal references to new package name

**Acceptance Criteria:**
- [ ] All essential MCP files copied successfully
- [ ] File conflicts resolved without breaking OODATCAA system
- [ ] Package renamed in all Python modules and configs
- [ ] Import statements updated to reflect new package name
- [ ] No orphaned references to old package name

**Links to Objective:**  
OBJECTIVE.md → MCP Integration (Critical) → Server Migration → Complete file system migration

---

### W003: Integrate MCP Dependencies
**Type:** Story  
**Complexity:** M  
**Status:** needs_plan

**Description:**  
Update project dependencies to include MCP requirements:
- Extract dependencies from MCP source
- Add to `pyproject.toml` with compatible versions
- Resolve any conflicts with existing dependencies (mdnotes module)
- Install and verify in clean venv

**Acceptance Criteria:**
- [ ] `pyproject.toml` includes all MCP dependencies
- [ ] Dependencies install cleanly: `pip install -e .`
- [ ] No version conflicts between MCP and existing deps
- [ ] `requirements.txt` or lock file generated
- [ ] Qdrant and vector DB dependencies included

**Links to Objective:**  
OBJECTIVE.md → MCP Integration (Critical) → Update dependencies and configuration

---

### W004: Adapt MCP for Training Use Case
**Type:** Story  
**Complexity:** M  
**Status:** needs_plan

**Description:**  
Clean and customize MCP server for small coder training project:
- Remove UI components not needed for training system
- Simplify or remove unnecessary features (e.g., multi-user support)
- Adapt configuration for training-focused use case
- Ensure core functionality remains: memory, vector search, policy system

**Acceptance Criteria:**
- [ ] Unnecessary UI/frontend code removed or disabled
- [ ] Core functionality verified: memory management, vector storage, policy system
- [ ] Configuration adapted for single-developer training workflow
- [ ] Code simplified without breaking essential features
- [ ] Memory footprint reduced where possible

**Links to Objective:**  
OBJECTIVE.md → MCP Integration (Critical) → Clean and adapt for training focus

---

### W005: Python Tooling & Quality Gates
**Type:** Quality  
**Complexity:** M  
**Status:** needs_plan

**Description:**  
Ensure migrated MCP code passes all quality gates:
- Format with black: `black .`
- Lint with ruff: `ruff check .`
- Type check with mypy: `mypy .`
- Fix any issues in migrated code
- Update mypy.ini / pyproject.toml for MCP modules if needed

**Acceptance Criteria:**
- [ ] `black --check .` passes on all MCP code
- [ ] `ruff check .` passes with 0 errors
- [ ] `mypy .` passes (may exclude strict mode initially)
- [ ] All linter issues in migrated code resolved
- [ ] CI-ready: all quality gates green

**Links to Objective:**  
OBJECTIVE.md → Quality & Performance → Code Quality → black, ruff, mypy pass

---

### W006: Basic Integration Testing
**Type:** Quality  
**Complexity:** S  
**Status:** needs_plan

**Description:**  
Create and run basic integration tests for MCP components:
- Verify MCP server can initialize
- Test memory storage and retrieval
- Validate policy system operations
- Ensure no regressions in existing `mdnotes` module
- Run existing test suite: `pytest -q`

**Acceptance Criteria:**
- [ ] Basic smoke test for MCP server initialization passes
- [ ] Memory CRUD operations tested (create, read, update, delete)
- [ ] Policy system basic tests pass
- [ ] Existing tests in `tests/` still pass
- [ ] No breaking changes to existing functionality

**Links to Objective:**  
OBJECTIVE.md → Quality & Performance → Integration Testing → MCP protocol stable

---

### W007: Configuration & Environment Setup
**Type:** Infra  
**Complexity:** S  
**Status:** needs_plan

**Description:**  
Set up configuration files and environment for MCP server:
- Configure Qdrant vector database (Docker or local)
- Create/update `.env` template with MCP settings
- Document environment variables needed
- Provide setup scripts or Makefile targets

**Acceptance Criteria:**
- [ ] Qdrant configuration ready (docker-compose or local setup)
- [ ] Environment variables documented in README
- [ ] `.env.example` or similar template provided
- [ ] Setup instructions clear and tested
- [ ] Can run MCP server in development mode

**Links to Objective:**  
OBJECTIVE.md → Deployment Ready → Docker containers for Qdrant

---

### W008: Documentation Update
**Type:** Docs  
**Complexity:** S  
**Status:** needs_plan

**Description:**  
Update project documentation to reflect MCP integration:
- README: Add MCP integration overview section
- Document migration process and rationale
- Setup instructions for MCP server
- Architecture notes on how MCP enables training workflow
- Troubleshooting section for common MCP issues

**Acceptance Criteria:**
- [ ] README includes MCP integration section
- [ ] Installation instructions cover MCP dependencies
- [ ] Architecture documentation explains MCP role
- [ ] Setup process documented end-to-end
- [ ] Examples or quick-start guide provided

**Links to Objective:**  
OBJECTIVE.md → Documentation & Deployment → Comprehensive Documentation

---

## Summary

**Total Items:** 8  
**Complexity Breakdown:**
- Small (S): 3 items
- Medium (M): 5 items
- Large (L): 0 items

**Type Breakdown:**
- Story: 4 items
- Quality: 2 items
- Infra: 1 item
- Docs: 1 item

**Critical Path:**  
W001 (Analyze) → W002 (Migrate) → W003 (Dependencies) → W004 (Adapt) → W005 (Quality) → W006 (Testing) → W007 (Config) → W008 (Docs)

---

**Next Steps:** Negotiator will initialize SPRINT_QUEUE.json and assign first task to Planner for detailed planning.
