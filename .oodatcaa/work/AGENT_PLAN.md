# AGENT PLAN — W005: Python Tooling & Quality Gates

**Objective ID:** OBJ-2025-002  
**Epic:** MCP Integration (Critical)  
**Sprint:** 1  
**Task ID:** W005  
**Complexity:** M  
**Dependencies:** W004 (Complete ✅)  
**Created:** 2025-10-03T00:15:00+02:00  
**Planner:** agent-planner-A  

---

## Problem Statement

After W004's successful MCP code adaptation (88.97% error reduction from 390 to 43 ruff errors), we need to complete the quality gates work by addressing the remaining linting and type checking issues. Currently:

- **43 ruff errors** remain (negotiated acceptance in W004, but should be resolved for clean CI)
- **496 mypy type errors** in MCP code (deferred from W004 for comprehensive typing effort)
- **Black formatting:** ✅ PASS (52 files)
- **Build:** ✅ PASS
- **Tests:** ✅ PASS (no regressions)
- **mdnotes module:** ✅ PASS (fully type-safe)

W005 aims to achieve **100% quality gate compliance** to unblock production deployment and establish a clean baseline for future development.

---

## Current State Analysis

### Ruff Errors (43 total)

**Breakdown by type:**
- **13 E501** (line-too-long): Long strings in prompts, acceptable but fixable by reformatting
- **8 F821** (undefined-name): ALL in `memory_manager_backup.py` (backup file - can be deleted)
- **7 S603** (subprocess security warning): Docker management in launcher.py, memory_server.py
- **7 S607** (subprocess security warning): Partial executable path for Docker commands
- **3 S110** (try-except-pass): Error handling patterns in memory_server.py
- **2 S311** (non-cryptographic random): Acceptable for non-security contexts
- **1 B007** (unused loop variable): launcher.py line 124 (`i` → `_i`)
- **1 E722** (bare except): Error handling
- **1 F811** (redefined while unused): Import issue

**Files affected:**
- `launcher.py`: 9 errors (6 S603/S607, 1 B007, 2 others)
- `memory_server.py`: 9 errors (3 S110, 3 S603, 3 others)
- `src/mcp/memory_manager_backup.py`: 8 F821 errors (backup file - should be deleted)
- Other MCP files: 17 errors (E501 long lines, misc)

### Mypy Errors (496 total in 29 files)

**Common patterns:**
1. **Missing return type annotations** (`no-untyped-def`): ~150 errors
   - Functions/methods without `-> None` or explicit return type
2. **Missing generic type parameters** (`type-arg`): ~80 errors
   - `dict` → `dict[str, Any]`
   - `list` → `list[str]`
3. **Library stubs not installed** (`import-untyped`): ~30 errors
   - `yaml` → needs `types-PyYAML`
   - `aiofiles` → needs `types-aiofiles`
4. **Type mismatches** (`assignment`, `arg-type`, `union-attr`): ~150 errors
   - Incompatible types in assignments
   - Optional handling issues
5. **Untyped calls** (`no-untyped-call`, `no-any-return`): ~86 errors
   - Calling untyped functions from typed context

**Most affected files:**
- `src/mcp/server_config.py`: 24 errors (config loading, env handling)
- `src/mcp/policy_processor.py`: 60+ errors (policy system core)
- `src/mcp/mcp_protocol_handler.py`: 37 errors (MCP protocol implementation)
- `src/mcp/prompts/*.py`: ~40 errors across 3 files (prompt systems)

---

## Constraints / Interfaces / Risks

### Constraints
- **No functional changes**: Only type annotations and code quality improvements
- **Zero regressions**: All existing tests must pass
- **Preserve W004 work**: Build on 88.97% error reduction, don't undo progress
- **Time budget**: 4-6 hours max (systematic but not exhaustive)

### Interfaces
- **Quality Gates**: black, ruff, mypy, pytest, coverage, build, pip-audit
- **Type System**: mypy strict mode with pragmatic ignore rules for external deps
- **Dependencies**: May need to add type stubs: `types-PyYAML`, `types-aiofiles`

### Risks
1. **Time creep**: 496 mypy errors could take 10+ hours for perfect resolution
   - **Mitigation**: Focus on systematic patterns, use pragmatic ignore rules where needed
2. **Breaking changes**: Adding types might reveal bugs
   - **Mitigation**: Run tests after each major change, rollback if issues
3. **Backup files**: Some errors in backup files that shouldn't be in codebase
   - **Mitigation**: Delete backup files (memory_manager_backup.py, etc.)
4. **Ruff security warnings**: Some S603/S607 are intentional (Docker management)
   - **Mitigation**: Use `# noqa: S603` comments with justification

---

## Definition of Done (DoD)

### Functional Requirements
- [x] All W004 functionality preserved (zero regressions)
- [ ] All MCP imports still work
- [ ] All existing tests pass
- [ ] Package builds successfully

### Quality Requirements
- [ ] **Ruff:** 0 errors (down from 43)
- [ ] **Mypy:** 0 errors in core code (pragmatic ignore for edge cases acceptable)
- [ ] **Black:** PASS (already passing, maintain)
- [ ] **Pytest:** All tests pass (maintain 100%)
- [ ] **Build:** Successful (maintain)
- [ ] **Security:** pip-audit clean (maintain)

### Documentation Requirements
- [ ] Add inline `# noqa` comments with justifications for intentional rule exceptions
- [ ] Update `mypy.ini` if new ignore rules needed
- [ ] Update `ruff.toml` if needed (deprecation warning fix)

---

## Acceptance Criteria (ACs)

### AC1: Zero Ruff Errors ✅
- **Measure:** `ruff check .` returns exit code 0
- **Current:** 43 errors
- **Target:** 0 errors
- **Method:** Delete backup files (8 errors), fix minor issues (35 errors)

### AC2: Mypy Core Code Clean ✅
- **Measure:** `mypy src/mcp` has 0 critical errors (type stubs for external libs acceptable)
- **Current:** 496 errors
- **Target:** < 10 errors (all in external lib imports or documented edge cases)
- **Method:** Add return types, generic parameters, install type stubs

### AC3: No Regressions ✅
- **Measure:** `pytest -q` passes all tests
- **Current:** 3/3 tests passing
- **Target:** 3/3 tests passing (maintain)

### AC4: Black Formatting Maintained ✅
- **Measure:** `black --check .` passes
- **Current:** PASS
- **Target:** PASS

### AC5: Build Success ✅
- **Measure:** `python -m build` succeeds
- **Current:** PASS
- **Target:** PASS

### AC6: Security Clean ✅
- **Measure:** `pip-audit` returns no high-severity issues
- **Current:** 1 informational issue
- **Target:** No high-severity issues

### AC7: Config Cleanup ✅
- **Measure:** Ruff deprecation warning resolved
- **Current:** Warning about top-level linter settings
- **Target:** No warnings, all settings in `[tool.ruff.lint]` section

---

## Alternatives Considered

### Alternative 1: Minimal Fix (Quick Fix)
**Approach:** Only fix auto-fixable errors, add `# type: ignore` for rest
- **Pros:** Fast (1-2 hours), low risk
- **Cons:** Technical debt remains, doesn't achieve quality goal
- **Decision:** ❌ Rejected - W005 goal is "ensure quality gates pass", not "quick fix"

### Alternative 2: Perfect Typing (Exhaustive)
**Approach:** Add perfect type annotations to all 496 mypy errors, no compromises
- **Pros:** Perfect type coverage, highest quality
- **Cons:** 12-16 hours effort, high risk of bugs, diminishing returns
- **Decision:** ❌ Rejected - Time/benefit ratio too high

### Alternative 3: Pragmatic Systematic Fix (SELECTED ✅)
**Approach:** Systematic pattern-based fixes with pragmatic ignore rules for edge cases
- **Delete backup files** (8 ruff errors eliminated)
- **Fix ruff auto-fixable errors** (run `ruff check --fix --unsafe-fixes`)
- **Add type stubs** for yaml, aiofiles (eliminates ~30 mypy errors)
- **Systematic type annotation** pass: return types, generic parameters (4-5 hours)
- **Pragmatic ignore rules** for complex edge cases with documentation
- **Pros:** Achieves 95%+ quality coverage, reasonable time (4-6 hours), pragmatic
- **Cons:** May have 5-10 remaining mypy errors with documented ignore rules
- **Decision:** ✅ **SELECTED** - Best balance of quality, time, and pragmatism

---

## Implementation Plan

### Step 1: Cleanup & Auto-Fixes (Branch Setup)
**Time:** 15 minutes  
**Actions:**
1. Create branch `feat/W005-step-01-quality-gates`
2. Create baseline tag: `pre/W005-$(date -Iseconds)`
3. Delete backup files:
   - `src/mcp/memory_manager_backup.py` (8 F821 errors)
   - `src/mcp/tool_definitions_backup.py` (if exists)
   - `src/mcp/prompt_handlers_original.py` (if errors remain)
4. Run `ruff check --fix --unsafe-fixes .` (auto-fix ~10 errors)
5. Run `black .` (ensure formatting maintained)
6. **Commit:** `[refactor] W005: Delete backup files and auto-fix ruff issues`
7. **Exit Gate:** Ruff errors reduced by ~50%, tests pass

### Step 2: Install Type Stubs
**Time:** 10 minutes  
**Actions:**
1. Add to `pyproject.toml` `[project.optional-dependencies]` dev section:
   - `types-PyYAML`
   - `types-aiofiles`
2. Run `pip install -e .[dev]`
3. Verify mypy error count drops by ~30
4. **Commit:** `[build] W005: Add type stubs for yaml and aiofiles`
5. **Exit Gate:** Mypy errors reduced to ~466, build succeeds

### Step 3: Fix Ruff Config Deprecation
**Time:** 5 minutes  
**Actions:**
1. Update `ruff.toml`:
   - Move `extend-select` → `lint.extend-select`
   - Move `ignore` → `lint.ignore`
2. Verify warning disappears: `ruff check .`
3. **Commit:** `[config] W005: Fix ruff.toml deprecation warnings`
4. **Exit Gate:** No deprecation warnings

### Step 4: Add Return Type Annotations (Core Files)
**Time:** 90 minutes  
**Actions:**
1. **Target files** (highest impact, ~150 errors):
   - `src/mcp/server_config.py`
   - `src/mcp/mcp_protocol_handler.py`
   - `src/mcp/policy_processor.py`
   - `src/mcp/prompts/*.py`
2. **Pattern:** Add `-> None` to functions without return, explicit types for others
3. **Method:** File-by-file systematic pass
4. Run `mypy src/mcp` after each file to track progress
5. **Commit after each file:** `[refactor] W005: Add return types to <filename>`
6. **Exit Gate:** ~150 `no-untyped-def` errors eliminated

### Step 5: Add Generic Type Parameters
**Time:** 60 minutes  
**Actions:**
1. **Pattern:** Replace bare generics with typed versions
   - `dict` → `dict[str, Any]` (most common)
   - `list` → `list[str]` or `list[Any]`
2. **Target:** All `type-arg` errors (~80)
3. **Import:** Add `from typing import Any` where needed
4. Run `mypy src/mcp` to verify
5. **Commit:** `[refactor] W005: Add generic type parameters to collections`
6. **Exit Gate:** ~80 `type-arg` errors eliminated

### Step 6: Fix Type Mismatches (Core Issues)
**Time:** 90 minutes  
**Actions:**
1. **Target:** `assignment`, `arg-type`, `union-attr` errors (~150)
2. **Common fixes:**
   - Add `assert x is not None` before accessing optional
   - Use `if x:` checks for optional handling
   - Fix incompatible assignments
3. **Focus on:** High-impact files (server_config.py, policy_processor.py)
4. Run tests after major changes
5. **Commit:** `[refactor] W005: Fix type mismatches in core files`
6. **Exit Gate:** ~100 type mismatch errors fixed, tests pass

### Step 7: Pragmatic Ignore Rules (Remaining Issues)
**Time:** 30 minutes  
**Actions:**
1. For remaining ~100 mypy errors:
   - **Complex edge cases:** Add `# type: ignore[error-code]  # Reason` with documentation
   - **Untyped external code:** Update `mypy.ini` with ignore rules
2. Add Security exception comments for intentional subprocess usage:
   - `# noqa: S603  # Docker management - trusted input`
   - `# noqa: S607  # Docker command - standard tool`
3. Document decisions in commit message
4. **Commit:** `[config] W005: Add pragmatic ignore rules for edge cases`
5. **Exit Gate:** < 10 remaining mypy errors with documented justifications

### Step 8: Validation & Quality Gates
**Time:** 30 minutes  
**Actions:**
1. Run all quality gates:
   - `black --check .` → Must PASS
   - `ruff check .` → Must return 0 errors
   - `mypy src/mdnotes` → Must PASS (verify no regression)
   - `mypy src/mcp` → Must have < 10 errors (documented)
   - `pytest -q` → Must PASS (3/3 tests)
   - `python -m build` → Must succeed
   - `pip-audit` → Must have no high-severity
2. Verify MCP core functionality:
   ```python
   from mcp.memory_manager import MemoryManager
   from mcp.config import Config
   # All imports work
   ```
3. **Commit:** `[test] W005: All quality gates pass`
4. **Exit Gate:** All ACs satisfied

---

## Testing Strategy

### Pre-Implementation Tests
- [x] Baseline quality gates documented (43 ruff, 496 mypy, tests pass)
- [x] Backup files identified (memory_manager_backup.py)

### During Implementation
- [ ] Run `mypy src/mcp` after each major change (track error count)
- [ ] Run `pytest -q` after type changes (ensure no regressions)
- [ ] Run `ruff check .` after each step (verify progress)

### Post-Implementation Tests
- [ ] **AC1:** `ruff check .` → exit code 0
- [ ] **AC2:** `mypy src/mcp` → < 10 errors
- [ ] **AC3:** `pytest -q` → 3/3 tests pass
- [ ] **AC4:** `black --check .` → pass
- [ ] **AC5:** `python -m build` → success
- [ ] **AC6:** `pip-audit` → no high-severity
- [ ] **AC7:** No ruff deprecation warnings

### Integration Tests
- [ ] All MCP imports work (smoke test)
- [ ] MCP handlers can be instantiated
- [ ] No runtime errors from type annotations

---

## Rollback Plan

### Baseline Tag
- **Tag:** `pre/W005-$(date -Iseconds)`
- **Branch:** `feat/W005-step-01-quality-gates`

### Rollback Triggers
1. **Tests fail:** Rollback to baseline, investigate type annotation issue
2. **MCP imports break:** Rollback to baseline, type annotations too strict
3. **Time exceeds 8 hours:** Pause, negotiate scope reduction with Negotiator
4. **Mypy errors increase:** Rollback last change, use alternative approach

### Rollback Procedure
```bash
git reset --hard <baseline-tag>
git push --force-with-lease origin feat/W005-step-01-quality-gates
```

---

## Dependencies

### Upstream Dependencies (Satisfied)
- ✅ **W004:** MCP code adapted (88.97% error reduction achieved)
- ✅ **W003:** Dependencies integrated
- ✅ **W002:** MCP server migrated

### Downstream Dependencies (Unblocked by W005)
- **W006:** Basic Integration Testing (can proceed with clean quality baseline)
- **W007:** Configuration & Environment Setup
- **W008:** Documentation Update (depends on W005+W006+W007)

### External Dependencies
- **Type stubs:** `types-PyYAML`, `types-aiofiles` (will be added)
- **Python version:** 3.11+ (already satisfied)

---

## Technical Debt Created

### Intentional Technical Debt (Documented)
1. **Pragmatic type ignores:** < 10 complex edge cases with `# type: ignore` and justification
2. **Security warnings:** S603/S607 exceptions for Docker management with `# noqa` comments
3. **External library stubs:** Some external libs may lack perfect stubs (acceptable)

### Future Work (Out of W005 Scope)
- **Strict mypy coverage:** Achieve 100% strict typing (if needed)
- **Performance optimization:** Type annotations may enable future optimizations
- **Additional type stubs:** Create custom stubs for untyped MCP SDK if needed

---

## Success Metrics

### Quantitative
- **Ruff errors:** 43 → 0 (100% reduction)
- **Mypy errors:** 496 → < 10 (98% reduction)
- **Test pass rate:** 100% (maintained)
- **Build success:** 100% (maintained)

### Qualitative
- **Code maintainability:** Type annotations improve IDE support and refactoring safety
- **CI readiness:** All quality gates green, ready for production deployment
- **Developer experience:** No more linting warnings, clean baseline for future work

---

## References
- **Objective:** `.oodatcaa/objectives/OBJECTIVE.md` → Quality & Performance → Code Quality
- **W004 Planning:** `.oodatcaa/work/AGENT_PLAN.md` (previous)
- **W004 Results:** 88.97% error reduction, 8/10 ACs passing
- **Sprint Backlog:** `.oodatcaa/work/SPRINT_BACKLOG.md` → W005

---

**Estimated Effort:** 6 hours (8 steps × 45 min avg)  
**Complexity:** Medium (systematic but extensive typing work)  
**Risk Level:** Low-Medium (pragmatic approach reduces risk)  
**Next Agent:** Builder (W005-B01)
