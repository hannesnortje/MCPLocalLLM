# Agent Plan — W003: Integrate MCP Dependencies

**Objective:** OBJ-2025-002 | **Epic:** MCP Integration | **Sprint:** 1 | **Work Item:** W003  
**Plan Version:** 1.0 | **Created:** 2025-10-02 | **Agent:** Planner

---

## Problem Statement

Integrate MCP dependencies into `pyproject.toml` and install packages to enable MCP functionality. Add 10 production dependencies (mcp, qdrant-client, sentence-transformers, etc.) and 2 dev dependencies (pytest-asyncio, types-markdown) identified in W001 analysis. Update tool configurations (mypy, pytest, ruff) to support MCP code.

**Context:** W002 successfully migrated 61 MCP files. These files currently have import errors because dependencies (mcp, qdrant-client, sentence-transformers) are not installed. W001 analysis provided complete dependency list with version constraints and tool configuration updates.

---

## Constraints / Risks

**Constraints:**
- MUST maintain compatibility with Python >=3.11,<3.13
- MUST preserve existing mdnotes dependencies (click, rich, whoosh)
- Large installation size: ~2.1GB (sentence-transformers brings PyTorch)
- MUST pass pip-audit security scan
- Tool configurations must work for both mdnotes and mcp code

**Key Risks & Mitigation:**
- **Dependency conflicts (MEDIUM):** W001 analysis verified zero conflicts → Use exact versions from analysis
- **Installation size (LOW):** ~2.1GB expected for ML training system → Document in README
- **Import errors persist (MEDIUM):** Missing transitive dependencies → Install with verbose logging, verify all imports
- **Tool configuration breaks (LOW):** Config updates minimal → Test incrementally
- **Security vulnerabilities (MEDIUM):** Large dependency tree → Run pip-audit and document findings

---

## Definition of Done

**Functional:**
- [ ] **AC1:** pyproject.toml updated with 10 MCP production dependencies
- [ ] **AC2:** pyproject.toml updated with 2 MCP dev dependencies
- [ ] **AC3:** Python version constraint updated to `>=3.11,<3.13`
- [ ] **AC4:** All dependencies install successfully: `pip install -e .[dev]`
- [ ] **AC5:** MCP imports work: `import mcp`, `import qdrant_client`, `import sentence_transformers`
- [ ] **AC6:** Existing mdnotes imports still work
- [ ] **AC7:** Existing tests still pass after dependency installation

**Non-Functional:**
- [ ] **AC8:** Tool configurations updated (mypy packages, pytest asyncio_mode, ruff known-first-party)
- [ ] **AC9:** pip-audit clean (no high-severity vulnerabilities)
- [ ] **AC10:** Build succeeds: `python -m build` creates wheel and sdist

---

## Alternatives & Choice

**Alternative 1:** Manual pip install → ❌ REJECTED (not reproducible, no version control)  
**Alternative 2:** requirements.txt approach → ❌ REJECTED (pyproject.toml is standard for packages)  
**Alternative 3:** Update pyproject.toml + pip install → ✅ **CHOSEN** (standard, reproducible, version-controlled)

**Rationale:** Alternative 3 follows Python packaging best practices, provides reproducible installations, and integrates cleanly with existing tooling.

---

## Implementation Plan

### Step 1: Backup and Branch Setup
**Branch:** `feat/W003-step-01-integrate-dependencies`  
**Actions:**
1. Create baseline tag: `pre/W003-$(date -Iseconds)`
2. Create and checkout integration branch
3. Backup current pyproject.toml for rollback

**Exit Gate:** Branch ready, backup created, baseline tag exists

---

### Step 2: Update pyproject.toml - Core Metadata
**Actions:**
1. Update `requires-python = ">=3.11,<3.13"` (add upper bound)
2. Update description to mention MCP integration (optional)
3. Add MCP-related keywords: "mcp", "vector-database" (optional)

**Expected Changes:** 1-3 lines modified  
**Exit Gate:** Python version constraint updated

---

### Step 3: Add MCP Production Dependencies
**Actions:**
1. Add 10 MCP dependencies to `[project.dependencies]`:
   ```python
   # MCP Core - Memory & Vector Search
   "mcp>=1.13.1,<2.0.0",
   "qdrant-client>=1.7.0,<2.0.0",
   "sentence-transformers>=2.5.1,<3.0.0",
   
   # Data Processing
   "numpy>=1.26.0,<2.0.0",
   "markdown>=3.5.0,<4.0.0",
   "beautifulsoup4>=4.12.0,<5.0.0",
   
   # Configuration & Async Utilities
   "python-dotenv>=1.0.0,<2.0.0",
   "pyyaml>=6.0.0,<7.0.0",
   "aiofiles>=24.1.0,<25.0.0",
   "aiohttp>=3.9.1,<4.0.0",
   ```
2. Maintain existing dependencies (click, rich, whoosh)
3. Group dependencies with comments for clarity

**Expected Changes:** ~10 lines added  
**Exit Gate:** Dependencies section complete, TOML syntax valid

---

### Step 4: Add MCP Dev Dependencies
**Actions:**
1. Add 2 MCP dev dependencies to `[project.optional-dependencies.dev]`:
   ```python
   "pytest-asyncio>=1.1.0,<2.0.0",
   "types-markdown>=3.5.0,<4.0.0",
   ```
2. Maintain existing dev dependencies
3. Maintain alphabetical order (optional but recommended)

**Expected Changes:** ~2 lines added  
**Exit Gate:** Dev dependencies updated, TOML syntax valid

---

### Step 5: Update Tool Configurations
**Actions:**
1. **Ruff:** Add "mcp" to `[tool.ruff.lint.isort] known-first-party`
2. **Mypy:** Add "mcp" to `[tool.mypy] packages` list
3. **Pytest:** Add `asyncio_mode = "auto"` to `[tool.pytest.ini_options]`
4. Verify TOML syntax: `python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"`

**Expected Changes:** 3 lines modified  
**Exit Gate:** Tool configurations updated, TOML valid

---

### Step 6: Install Dependencies
**Actions:**
1. Upgrade pip: `pip install --upgrade pip`
2. Install project with dev dependencies: `pip install -e .[dev]`
3. Monitor installation (may take 5-10 minutes for sentence-transformers + PyTorch)
4. Capture installation log for troubleshooting

**Expected Outcome:** ~2.1GB dependencies installed, no errors  
**Exit Gate:** Installation completes successfully, no error messages

---

### Step 7: Verify Imports
**Actions:**
1. **Verify MCP core imports:**
   ```bash
   python -c "import mcp; print('✅ mcp imported')"
   python -c "import qdrant_client; print('✅ qdrant_client imported')"
   python -c "import sentence_transformers; print('✅ sentence_transformers imported')"
   ```
2. **Verify supporting imports:**
   ```bash
   python -c "import numpy, markdown, beautifulsoup4, aiohttp"
   ```
3. **Verify existing mdnotes imports:**
   ```bash
   python -c "from mdnotes import core; print('✅ mdnotes still works')"
   ```

**Expected Outcome:** All imports successful  
**Exit Gate:** Zero import errors

---

### Step 8: Run Quality Gates
**Actions:**
1. Run black: `black --check .` (should already pass)
2. Run ruff: `ruff check .` (expect MCP code issues, defer to W004)
3. Run mypy on mdnotes: `mypy src/mdnotes` (should pass)
4. Run existing tests: `pytest -q tests/test_smoke.py` (must pass)
5. Run pip-audit: `pip-audit` (check for vulnerabilities)
6. Run build: `python -m build` (verify package builds)

**Expected Outcome:** Existing code quality maintained, MCP issues deferred  
**Exit Gate:** Smoke tests pass, build succeeds, no high-severity security issues

---

### Step 9: Commit and Push
**Actions:**
1. Stage pyproject.toml: `git add pyproject.toml`
2. Commit with descriptive message:
   ```bash
   git commit -m "[impl] W003: Integrate MCP dependencies into pyproject.toml
   
   - Add 10 MCP production dependencies (mcp, qdrant-client, sentence-transformers, etc.)
   - Add 2 MCP dev dependencies (pytest-asyncio, types-markdown)
   - Update Python version constraint to >=3.11,<3.13
   - Update tool configurations (mypy, pytest, ruff)
   - Verified all imports work successfully"
   ```
3. Push branch: `git push origin feat/W003-step-01-integrate-dependencies`

**Exit Gate:** Changes committed and pushed

---

### Step 10: Update Documentation
**Actions:**
1. Update SPRINT_QUEUE.json: W003 status → awaiting_test
2. Update AGENT_LOG.md with dependency integration summary
3. Release locks

**Exit Gate:** Documentation updated, ready for tester

---

## Testing Strategy

See TEST_PLAN.md. Summary: Import verification, existing tests pass, pip-audit clean, tool configurations work.

**Rollback Triggers:**
- Dependency installation fails with conflicts
- Critical imports fail (mcp, qdrant_client, sentence_transformers)
- Existing tests fail after installation
- High-severity security vulnerabilities found

---

## Rollback Plan

**Baseline:** `pre/W003-<timestamp>` (created in Step 1)  
**Trigger Conditions:** Any critical verification failure in Steps 6-8  
**Steps:**
```bash
# Restore pyproject.toml
git checkout HEAD -- pyproject.toml

# Uninstall MCP dependencies
pip uninstall -y mcp qdrant-client sentence-transformers numpy markdown \
  beautifulsoup4 python-dotenv pyyaml aiofiles aiohttp pytest-asyncio types-markdown

# Reinstall original environment
pip install -e .[dev]

# Verify rollback
pytest -q

# Document failure
echo "W003 aborted: <reason>" >> .oodatcaa/work/SPRINT_DISCUSS.md
```

---

## Branch & Commits

**Branch:** `feat/W003-step-01-integrate-dependencies`  
**Commit Labels:** `[impl]` for pyproject.toml updates  
**PR:** Single PR after all verification passes  
**Merge Strategy:** No-FF merge to preserve feature branch history

---

## Dependencies

**Upstream:** W002 (COMPLETE - MCP files migrated)  
**Downstream:** W004 (Adapt MCP for Training), W005 (Python Tooling & Quality Gates)

**Artifacts Required from W001:**
- `.oodatcaa/work/analysis/W001/dependencies.md` ✅
- `.oodatcaa/work/analysis/W001/pyproject_toml_updates.md` ✅

---

## Effort Estimate

**Complexity:** M (Medium) | **Time:** 1-2 hours  
- Step 1 (Setup): 5 min
- Steps 2-5 (pyproject.toml updates): 20 min
- Step 6 (Install dependencies): 10-15 min (large download)
- Step 7 (Verify imports): 10 min
- Step 8 (Quality gates): 15 min
- Steps 9-10 (Commit & docs): 10 min

**Risk Level:** LOW (W001 verified zero conflicts, exact versions provided)

---

## Builder Task Breakdown

**W003-B01:** Steps 1-5 (Branch + pyproject.toml updates)  
**W003-B02:** Steps 6-8 (Install + Verify + Quality gates)  
**W003-B03:** Steps 9-10 (Commit + Documentation)

**Tester Task:**  
**W003-T01:** Verify all 10 ACs, validate imports, check security

---

**Status:** ✅ APPROVED | **Ready for:** Builder Agent Execution
