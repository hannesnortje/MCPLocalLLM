# TEST PLAN — W005: Python Tooling & Quality Gates

**Task ID:** W005  
**Objective ID:** OBJ-2025-002  
**Sprint:** 1  
**Created:** 2025-10-03T00:15:00+02:00  
**Planner:** agent-planner-A  

---

## Test Commands (Standard CI Gates)

### 1. Black Formatting
```bash
black --check .
```
**Expected:** All files pass, exit code 0  
**Current Baseline:** ✅ PASS (52 files)

### 2. Ruff Linting
```bash
ruff check .
```
**Expected:** 0 errors, exit code 0  
**Current Baseline:** ❌ 43 errors

### 3. Mypy Type Checking (MDNotes)
```bash
mypy src/mdnotes
```
**Expected:** Success, no issues, exit code 0  
**Current Baseline:** ✅ PASS (2 files)

### 4. Mypy Type Checking (MCP)
```bash
mypy src/mcp
```
**Expected:** < 10 errors (documented edge cases acceptable), exit code 0 or 1  
**Current Baseline:** ❌ 496 errors in 29 files

### 5. Unit Tests (Smoke)
```bash
pytest -q tests/test_smoke.py
```
**Expected:** 2/2 tests pass, exit code 0  
**Current Baseline:** ✅ PASS

### 6. Unit Tests (All)
```bash
pytest -q
```
**Expected:** 3/3 tests pass (smoke + acceptance placeholder), exit code 0  
**Current Baseline:** ✅ PASS

### 7. Code Coverage
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=85
```
**Expected:** ≥ 85% coverage, exit code 0  
**Current Baseline:** ✅ 100% on mdnotes (MCP not yet covered)

### 8. Build Package
```bash
python -m build
```
**Expected:** Wheel + sdist created successfully, exit code 0  
**Current Baseline:** ✅ PASS

### 9. Security Audit
```bash
pip-audit
```
**Expected:** No high-severity vulnerabilities, exit code 0  
**Current Baseline:** ✅ 1 informational issue only

### 10. Optional: Bandit Security Scan
```bash
bandit -r src -ll
```
**Expected:** No high-severity issues (S603/S607 Docker warnings acceptable)  
**Current Baseline:** ⚠️ Some subprocess warnings (expected)

---

## Acceptance Criteria Testing

### AC1: Zero Ruff Errors ✅
**Test:**
```bash
ruff check .
echo "Exit code: $?"
```
**Pass Criteria:**
- Exit code = 0
- Output: "All checks passed!"
- No errors reported

**Validation Method:**
1. Run `ruff check .` → Expect 0 errors
2. Verify no warnings (config deprecation fixed)
3. Spot-check 3 files manually for code quality

**Edge Cases:**
- Long lines in prompts → Should be reformatted or have `# noqa: E501` with reason
- Security warnings → Should have `# noqa: S603` with "Docker management - trusted input"

---

### AC2: Mypy Core Code Clean ✅
**Test:**
```bash
mypy src/mcp 2>&1 | tee mypy_results.txt
grep "Found [0-9]* error" mypy_results.txt
```
**Pass Criteria:**
- < 10 errors (all documented with `# type: ignore` and reason)
- No `no-untyped-def` errors in core files
- No `type-arg` errors (all generics have parameters)
- Library stub errors for external deps acceptable

**Validation Method:**
1. Run `mypy src/mcp` → Expect < 10 errors
2. For each remaining error:
   - Verify `# type: ignore[error-code]  # <reason>` comment present
   - Verify reason is documented and valid
3. Spot-check 5 files for type annotation quality:
   - `src/mcp/config.py`
   - `src/mcp/server_config.py`
   - `src/mcp/memory_manager.py`
   - `src/mcp/handlers/core_memory_handlers.py`
   - `src/mcp/policy_processor.py`

**Edge Cases:**
- External library imports (aiofiles, yaml) → Stubs installed OR ignore rules in mypy.ini
- Complex union types → May need cast() or assert is not None
- Any types → Acceptable for truly dynamic data

---

### AC3: No Regressions ✅
**Test:**
```bash
pytest -q
```
**Pass Criteria:**
- 3/3 tests pass
- No new failures
- No warnings about deprecated imports

**Validation Method:**
1. Run `pytest -q` → All tests green
2. Run `pytest -q tests/test_smoke.py` → 2/2 pass (critical)
3. Manual smoke test:
   ```python
   from mdnotes.core import MDNotes
   from mcp.memory_manager import MemoryManager
   from mcp.config import Config
   # All imports work
   ```

**Edge Cases:**
- Type annotations might catch latent bugs → If so, fix bug OR adjust type
- Import order changes → Verify no circular dependencies

---

### AC4: Black Formatting Maintained ✅
**Test:**
```bash
black --check .
```
**Pass Criteria:**
- "All done! ✨ 🍰 ✨"
- "X files would be left unchanged"
- Exit code 0

**Validation Method:**
1. Run `black --check .` → Must PASS
2. If fails: Run `black .` and commit formatting fixes
3. Verify line-length=100 respected

**Edge Cases:**
- Long string literals → Black won't break them (expected)
- Docstrings → Black formats them (verify readable)

---

### AC5: Build Success ✅
**Test:**
```bash
rm -rf dist/
python -m build
ls -lh dist/
```
**Pass Criteria:**
- `dist/mdnotes-0.1.0.tar.gz` created
- `dist/mdnotes-0.1.0-py3-none-any.whl` created
- Exit code 0
- No errors or warnings

**Validation Method:**
1. Clean `dist/` directory
2. Run `python -m build`
3. Verify both wheel and sdist artifacts present
4. Spot-check wheel contents:
   ```bash
   unzip -l dist/mdnotes-0.1.0-py3-none-any.whl | grep -E "(mdnotes|mcp)"
   ```

**Edge Cases:**
- Missing files → Verify `MANIFEST.in` or `pyproject.toml` includes all needed files
- Large files → Check if unnecessary files included (should be in `.gitignore`)

---

### AC6: Security Clean ✅
**Test:**
```bash
pip-audit
```
**Pass Criteria:**
- No high-severity vulnerabilities
- No medium-severity vulnerabilities (or documented exceptions)
- Exit code 0

**Validation Method:**
1. Run `pip-audit`
2. Review any findings:
   - Informational → Acceptable
   - Low → Review, likely acceptable
   - Medium/High → Must fix or document mitigation
3. Document any accepted risks in commit message

**Edge Cases:**
- Transitive dependencies → May need to update parent package
- False positives → Document in security notes

---

### AC7: Config Cleanup ✅
**Test:**
```bash
ruff check . 2>&1 | grep "warning:"
```
**Pass Criteria:**
- No output (no warnings)
- Exit code 0 (only if no errors)

**Validation Method:**
1. Run `ruff check .`
2. Verify no deprecation warnings about top-level linter settings
3. Verify `ruff.toml` has settings in `[tool.ruff.lint]` section

**Edge Cases:**
- New ruff version → May introduce new warnings (document)

---

## Integration Testing

### MCP Core Functionality Verification

**Test 1: MCP Imports**
```python
# File: tests/test_w005_mcp_imports.py
import pytest

def test_mcp_core_imports():
    """Verify all core MCP modules import without errors"""
    from mcp.config import Config
    from mcp.memory_manager import MemoryManager
    from mcp.handlers.core_memory_handlers import CoreMemoryHandlers
    from mcp.memory.embedding_service import EmbeddingService
    from mcp.tools.core_memory_tools import get_core_memory_tools
    assert Config is not None
    assert MemoryManager is not None
    # Imports succeed = test passes
```

**Test 2: Type Annotations Runtime**
```python
# File: tests/test_w005_type_runtime.py
import pytest
from typing import get_type_hints

def test_type_annotations_present():
    """Verify type annotations are present on key functions"""
    from mcp.config import Config
    from mcp.memory_manager import MemoryManager
    
    # Config class has type hints
    hints = get_type_hints(Config.__init__)
    assert hints  # Not empty
    
    # MemoryManager methods have hints
    if hasattr(MemoryManager, 'store_memory'):
        hints = get_type_hints(MemoryManager.store_memory)
        assert hints
```

**Test 3: No Runtime Type Errors**
```python
# File: tests/test_w005_no_runtime_errors.py
import pytest

def test_mdnotes_unchanged():
    """Verify mdnotes module still works"""
    from mdnotes.core import parse_markdown
    result = parse_markdown("# Test\n\nContent")
    assert result  # Basic functionality works

def test_mcp_basic_instantiation():
    """Verify MCP classes can be instantiated if they have defaults"""
    from mcp.config import Config
    # If Config() works, it works
    # If it needs args, that's expected
    try:
        config = Config()
    except TypeError:
        pass  # Expected if args required
```

---

## Performance Tests (Optional)

### Type Checking Speed
**Goal:** Ensure mypy runs in reasonable time

**Test:**
```bash
time mypy src/mcp
```
**Expected:** < 30 seconds on M1 Max
**Baseline:** Unknown (first strict mypy run)

### Build Speed
**Goal:** Ensure type annotations don't slow build

**Test:**
```bash
time python -m build
```
**Expected:** < 15 seconds
**Baseline:** ~10 seconds

---

## Rollback Testing

### Rollback Trigger Tests

**Trigger 1: Test Failures**
```bash
pytest -q
if [ $? -ne 0 ]; then
  echo "ROLLBACK TRIGGER: Tests failed"
  git reset --hard <baseline-tag>
fi
```

**Trigger 2: MCP Import Failures**
```bash
python -c "from mcp.memory_manager import MemoryManager"
if [ $? -ne 0 ]; then
  echo "ROLLBACK TRIGGER: MCP imports broken"
  git reset --hard <baseline-tag>
fi
```

**Trigger 3: Build Failures**
```bash
python -m build
if [ $? -ne 0 ]; then
  echo "ROLLBACK TRIGGER: Build failed"
  git reset --hard <baseline-tag>
fi
```

---

## Test Artifacts

### Files to Generate
1. **mypy_results.txt**: Full mypy output for analysis
2. **ruff_results.txt**: Full ruff output showing 0 errors
3. **test_output.txt**: pytest output with all tests passing
4. **build_artifacts/**: dist/ directory with wheel and sdist

### Reports to Create
1. **Quality Gate Report**: All 10 gates with PASS/FAIL
2. **Error Reduction Report**: 
   - Ruff: 43 → 0 (100% reduction)
   - Mypy: 496 → < 10 (98% reduction)
3. **Type Annotation Coverage**: % of functions with type hints

---

## Exit Criteria

### Required (Must Pass)
- ✅ **AC1:** `ruff check .` → 0 errors
- ✅ **AC2:** `mypy src/mcp` → < 10 errors (documented)
- ✅ **AC3:** `pytest -q` → 3/3 tests pass
- ✅ **AC4:** `black --check .` → pass
- ✅ **AC5:** `python -m build` → success
- ✅ **AC6:** `pip-audit` → no high-severity
- ✅ **AC7:** No ruff config warnings

### Optional (Nice to Have)
- ⚪ **Coverage:** ≥ 85% (mdnotes already at 100%)
- ⚪ **Bandit:** No high-severity (some subprocess warnings acceptable)
- ⚪ **Type hint coverage:** ≥ 90% of public functions

### Blockers (Fail Fast)
- ❌ **Any test regression:** Immediate rollback
- ❌ **MCP imports break:** Immediate rollback
- ❌ **Build fails:** Immediate rollback

---

## Validation Procedure

### Step-by-Step Validation (For Tester)

1. **Environment Setup**
   ```bash
   cd /media/hannesn/storage/Code/MCPLocalLLM
   git checkout feat/W005-step-01-quality-gates
   pip install -e .[dev]
   ```

2. **Run All Quality Gates**
   ```bash
   black --check . > test_results/ac4_black.txt 2>&1
   ruff check . > test_results/ac1_ruff.txt 2>&1
   mypy src/mdnotes > test_results/ac3_mypy_mdnotes.txt 2>&1
   mypy src/mcp > test_results/ac2_mypy_mcp.txt 2>&1
   pytest -q > test_results/ac3_pytest.txt 2>&1
   python -m build > test_results/ac5_build.txt 2>&1
   pip-audit > test_results/ac6_security.txt 2>&1
   ```

3. **Verify Each AC**
   - AC1: Check `test_results/ac1_ruff.txt` → "All checks passed!"
   - AC2: Check `test_results/ac2_mypy_mcp.txt` → < 10 errors
   - AC3: Check `test_results/ac3_pytest.txt` → "3 passed"
   - AC4: Check `test_results/ac4_black.txt` → "would be left unchanged"
   - AC5: Check `test_results/ac5_build.txt` → "Successfully built"
   - AC6: Check `test_results/ac6_security.txt` → "No vulnerabilities"
   - AC7: Check `test_results/ac1_ruff.txt` → No "warning:" lines

4. **Manual Spot Checks**
   - Open 3 random MCP files → Verify type annotations present
   - Run MCP imports → Verify no errors
   - Check code readability → Verify types improve, not obscure

5. **Generate Test Report**
   ```bash
   cat > test_results/W005_VALIDATION_REPORT.md << 'EOF'
   # W005 Validation Report
   
   ## Summary
   - **AC1 (Ruff):** PASS/FAIL
   - **AC2 (Mypy):** PASS/FAIL (X errors remaining)
   - **AC3 (Tests):** PASS/FAIL
   - **AC4 (Black):** PASS/FAIL
   - **AC5 (Build):** PASS/FAIL
   - **AC6 (Security):** PASS/FAIL
   - **AC7 (Config):** PASS/FAIL
   
   ## Details
   [Include error counts, notable issues, edge cases]
   
   ## Decision: APPROVE / NEEDS_ADAPT / ROLLBACK
   EOF
   ```

---

## Success Criteria Summary

**W005 is DONE when:**
1. ✅ All 7 ACs pass
2. ✅ Zero regressions in existing tests
3. ✅ All MCP imports work
4. ✅ Build succeeds
5. ✅ < 10 mypy errors (documented)
6. ✅ 0 ruff errors
7. ✅ All quality gates green

**Estimated Test Time:** 45 minutes (automated tests + manual validation)
