# Agent Plan — W004: Adapt MCP for Training Use Case

**Objective:** OBJ-2025-002 | **Epic:** MCP Integration | **Sprint:** 1 | **Work Item:** W004  
**Plan Version:** 1.0 | **Created:** 2025-10-02 | **Agent:** Planner

---

## Problem Statement

Adapt and clean up the migrated MCP server code to pass all quality gates and work optimally for the training use case. Fix 385 ruff linting errors (primarily import sorting, type annotations, deprecated syntax) and resolve mypy type errors. Remove or disable UI-related code, simplify unnecessary features, and ensure core MCP functionality (memory management, vector search, policy system) remains intact.

**Context:** W002 migrated 61 MCP files and W003 installed all dependencies. However, the MCP code has quality issues: 385 ruff errors (318 auto-fixable) and multiple mypy type errors. Most issues are mechanical (import sorting, type annotations using old syntax like `List[]` instead of `list[]`, `Optional[]` instead of `| None`). The code is functional but doesn't meet project quality standards.

---

## Constraints / Risks

**Constraints:**
- MUST preserve core MCP functionality (memory, vector search, policy system)
- MUST NOT break existing mdnotes functionality
- MUST pass all quality gates (black, ruff, mypy, pytest)
- MCP SDK (`mcp` package) lacks type stubs - will need type: ignore comments
- MUST maintain compatibility with installed dependencies

**Key Risks & Mitigation:**
- **Breaking MCP functionality (HIGH):** Automated fixes could break code → Run tests after each fix batch
- **Type annotation errors (MEDIUM):** Complex types may need manual fixes → Start with auto-fixes, then manual
- **Import errors from changes (MEDIUM):** Refactoring could break imports → Test imports after changes
- **Loss of needed functionality (LOW):** Removing code could break features → Only remove UI-specific code, keep core

---

## Definition of Done

**Functional:**
- [ ] **AC1:** All ruff linting errors resolved (0 errors in `ruff check .`)
- [ ] **AC2:** Import sorting corrected (all imports properly ordered)
- [ ] **AC3:** Type annotations modernized (PEP 585/604: `list[]` not `List[]`, `| None` not `Optional[]`)
- [ ] **AC4:** Mypy type checking passes on MCP code (with reasonable ignores for untyped libraries)
- [ ] **AC5:** UI-related code identified and disabled/removed
- [ ] **AC6:** Core MCP functionality preserved (memory, vector search, policy)
- [ ] **AC7:** Existing tests still pass (no regressions)

**Non-Functional:**
- [ ] **AC8:** Black formatting passes on all code
- [ ] **AC9:** Build succeeds with cleaned code
- [ ] **AC10:** No new security issues introduced

---

## Alternatives & Choice

**Alternative 1:** Manual fixes for all issues → ❌ REJECTED (time-consuming, error-prone for 385 errors)  
**Alternative 2:** Automated ruff --fix + targeted manual fixes → ✅ **CHOSEN** (fast, reliable, 318/385 auto-fixable)  
**Alternative 3:** Disable type checking for MCP → ❌ REJECTED (defeats quality goals)

**Rationale:** Alternative 2 leverages automated tooling for mechanical fixes (85% of issues) and focuses manual effort on complex type annotations. This is efficient and maintains code quality.

---

## Implementation Plan

### Step 1: Branch Setup and Baseline
**Branch:** `feat/W004-step-01-adapt-mcp-code`  
**Actions:**
1. Create baseline tag: `pre/W004-$(date -Iseconds)`
2. Create and checkout adaptation branch
3. Run initial quality check to document baseline errors

**Exit Gate:** Branch ready, baseline documented (385 ruff errors, multiple mypy errors)

---

### Step 2: Automated Ruff Fixes (Batch 1)
**Actions:**
1. Run `ruff check src/mcp --fix` to auto-fix 318 errors:
   - Import sorting (36 errors)
   - Type annotations: `List[]` → `list[]` (220 errors)
   - Type annotations: `Optional[]` → `| None` (34 errors)
   - Type annotations: `Union[]` → `|` (8 errors)
   - F-string fixes (13 errors)
   - Remove unused imports (5 errors)
   - Other mechanical fixes (2 errors)
2. Run black to format changed files
3. Commit: `[refactor] W004: Apply automated ruff fixes to MCP code`

**Expected Outcome:** ~318 errors fixed, ~67 errors remaining  
**Exit Gate:** Ruff errors reduced significantly, code still compiles

---

### Step 3: Manual Ruff Fixes (Batch 2)
**Actions:**
1. Fix remaining ~67 ruff errors that need manual attention:
   - Trailing whitespace (9 errors)
   - Line too long (7 errors)
   - Security warnings (subprocess calls: 8 errors)
   - Unused variables (4 errors)
   - Other non-auto-fixable issues
2. Run black to format
3. Commit: `[refactor] W004: Fix remaining ruff issues in MCP code`

**Expected Outcome:** 0 ruff errors  
**Exit Gate:** `ruff check .` passes with 0 errors

---

### Step 4: Add Type Annotations for Mypy
**Actions:**
1. Add return type annotations to functions missing them
2. Add type parameters to generic types (`dict` → `dict[str, Any]`, `list` → `list[str]`)
3. Add `# type: ignore[import-untyped]` for mcp SDK imports (no type stubs available)
4. Fix any complex type issues
5. Create mypy configuration exclusions if needed for external libraries
6. Commit: `[refactor] W004: Add type annotations for mypy compliance`

**Expected Outcome:** Mypy errors significantly reduced  
**Exit Gate:** Mypy passes on MCP code (with documented ignores for untyped libraries)

---

### Step 5: Remove/Disable UI Components
**Actions:**
1. Identify UI-related code (already excluded src/ui/ directory in W002)
2. Check for UI imports in remaining code (PySide6, websockets references)
3. Comment out or remove UI-specific code blocks
4. Verify no UI dependencies remain
5. Commit: `[refactor] W004: Remove UI-related code references`

**Expected Outcome:** Zero UI dependencies in code  
**Exit Gate:** No references to PySide6, websockets, or UI-specific code

---

### Step 6: Verify Core Functionality
**Actions:**
1. Test MCP core imports:
   ```python
   from mcp import memory_manager
   from mcp import qdrant_manager
   from mcp import mcp_server
   ```
2. Verify memory management imports work
3. Verify policy system imports work
4. Verify tools and handlers import correctly
5. Document any disabled features

**Exit Gate:** All core MCP modules import without errors

---

### Step 7: Run All Quality Gates
**Actions:**
1. Run `black --check .` → must pass
2. Run `ruff check .` → must pass (0 errors)
3. Run `mypy src/mcp` → must pass (with documented ignores)
4. Run `mypy src/mdnotes` → must pass
5. Run `pytest -q tests/test_smoke.py` → must pass (critical)
6. Run `pytest -q tests/acceptance` → must pass
7. Run `python -m build` → must pass

**Exit Gate:** All quality gates pass

---

### Step 8: Commit, Push, and Document
**Actions:**
1. Stage all changes
2. Create comprehensive commit message with stats
3. Push branch to origin
4. Update SPRINT_QUEUE.json: W004 status → awaiting_test
5. Update AGENT_LOG.md with W004 completion summary
6. Release locks

**Exit Gate:** Branch pushed, documentation updated

---

## Testing Strategy

See TEST_PLAN.md. Summary: Quality gate validation, import verification, core functionality testing, no regressions.

**Rollback Triggers:**
- Core MCP functionality breaks (imports fail)
- Existing tests fail
- Build fails
- Cannot resolve type errors reasonably

---

## Rollback Plan

**Baseline:** `pre/W004-<timestamp>` (created in Step 1)  
**Trigger Conditions:** Critical functionality breaks, tests fail, insurmountable type errors  
**Steps:**
```bash
git reset --hard pre/W004-<timestamp>
git push origin feat/W004-step-01-adapt-mcp-code --force-with-lease
echo "W004 aborted: <reason>" >> .oodatcaa/work/SPRINT_DISCUSS.md
```

---

## Branch & Commits

**Branch:** `feat/W004-step-01-adapt-mcp-code`  
**Commit Labels:** `[refactor]` for code quality improvements  
**PR:** Single PR after all quality gates pass  
**Merge Strategy:** No-FF merge to preserve feature branch history

---

## Dependencies

**Upstream:** W002 (COMPLETE - MCP files migrated), W003 (COMPLETE - dependencies installed)  
**Downstream:** W005 (Python Tooling), W006 (Integration Testing), W007 (Configuration), W008 (Documentation)

**Artifacts from Previous Work:**
- W002: 61 MCP files in `src/mcp/`, `policy/`, `docs/mcp/`
- W003: 12 dependencies installed, tools configured

---

## Effort Estimate

**Complexity:** M (Medium) | **Time:** 3-4 hours  
- Step 1 (Setup): 5 min
- Step 2 (Auto ruff fixes): 15 min
- Step 3 (Manual ruff fixes): 45 min
- Step 4 (Type annotations): 90 min
- Step 5 (Remove UI): 15 min
- Step 6 (Verify functionality): 15 min
- Step 7 (Quality gates): 20 min
- Step 8 (Commit & docs): 15 min

**Risk Level:** MEDIUM (automated fixes are safe, but type annotations need care)

---

## Builder Task Breakdown

**W004-B01:** Steps 1-3 (Setup + Automated Fixes + Manual Fixes)  
**W004-B02:** Steps 4-5 (Type Annotations + Remove UI)  
**W004-B03:** Steps 6-8 (Verify + Quality Gates + Commit)

**Tester Task:**  
**W004-T01:** Verify all 10 ACs, validate quality gates, test core functionality

---

**Status:** ✅ APPROVED | **Ready for:** Builder Agent Execution
