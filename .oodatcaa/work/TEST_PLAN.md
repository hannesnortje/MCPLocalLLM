# Test Plan — W004: Adapt MCP for Training Use Case

**Work Item:** W004 | **Sprint:** 1 | **Created:** 2025-10-02

---

## Test Commands

### Format Check
```bash
black --check .
```
**Expected:** PASS (all code formatted correctly)

---

### Lint Check (CRITICAL)
```bash
ruff check .
```
**Expected:** PASS with 0 errors  
**ROLLBACK TRIGGER:** Any errors remaining after W004 completion

---

### Type Check - MCP Code
```bash
mypy src/mcp
```
**Expected:** PASS (with documented # type: ignore comments for untyped libraries)  
**Note:** Some ignores expected for mcp SDK (no type stubs)

---

### Type Check - mdnotes Code
```bash
mypy src/mdnotes
```
**Expected:** PASS (existing code should remain clean)  
**ROLLBACK TRIGGER:** Any new type errors in mdnotes

---

### Unit Tests (Existing Only)
```bash
pytest -q tests/test_smoke.py
```
**Expected:** PASS (2/2 tests)  
**ROLLBACK TRIGGER:** Any test failures

---

### Acceptance Tests (Existing Only)
```bash
pytest -q tests/acceptance
```
**Expected:** PASS (existing tests unaffected)

---

### Coverage Check
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=85
```
**Expected:** PASS (coverage maintained)

---

### Build Check
```bash
python -m build
```
**Expected:** PASS (package builds with cleaned MCP code)

---

### Security Audit
```bash
pip-audit
```
**Expected:** No new vulnerabilities introduced

---

## Acceptance Testing

### AC1: All Ruff Linting Errors Resolved (CRITICAL)
**Test:**
```bash
source .venv/bin/activate
ruff check . --statistics
echo "Exit code: $?"
```
**Pass Criteria:** Exit code 0, output shows "All checks passed!" or "Found 0 errors."  
**ROLLBACK TRIGGER:** Any errors remaining

---

### AC2: Import Sorting Corrected
**Test:**
```bash
source .venv/bin/activate
ruff check . --select I001 --statistics
```
**Pass Criteria:** 0 unsorted-imports errors

---

### AC3: Type Annotations Modernized
**Test:**
```bash
source .venv/bin/activate
# Check for old-style type annotations
ruff check . --select UP006,UP007,UP035,UP045 --statistics
```
**Pass Criteria:** 0 errors for:
- UP006 (non-pep585-annotation: `List[]` vs `list[]`)
- UP007 (non-pep604-annotation-union: `Union[]` vs `|`)
- UP035 (deprecated-import)
- UP045 (non-pep604-annotation-optional: `Optional[]` vs `| None`)

---

### AC4: Mypy Type Checking Passes on MCP Code
**Test:**
```bash
source .venv/bin/activate
mypy src/mcp 2>&1 | tee mypy-mcp.log
echo "Exit code: $?"

# Count errors (excluding acceptable ignores)
grep "error:" mypy-mcp.log | grep -v "import-untyped" | wc -l
```
**Pass Criteria:** 
- Exit code 0 OR
- Only "import-untyped" errors with appropriate `# type: ignore[import-untyped]` comments
- No "no-untyped-def", "type-arg", or other fixable errors

---

### AC5: UI-Related Code Disabled/Removed
**Test:**
```bash
# Check for UI imports
grep -r "PySide6\|QApplication\|QWidget" src/mcp/ || echo "✅ No UI imports"
grep -r "websockets" src/mcp/ --include="*.py" || echo "✅ No websockets imports"

# Verify UI directory not present
test ! -d "src/mcp/ui" && echo "✅ No UI directory"
```
**Pass Criteria:** All searches return "✅" messages (no matches found)

---

### AC6: Core MCP Functionality Preserved (CRITICAL)
**Test:**
```bash
source .venv/bin/activate

# Test core imports
python -c "from mcp import memory_manager; print('✅ memory_manager imports')"
python -c "from mcp import qdrant_manager; print('✅ qdrant_manager imports')"
python -c "from mcp import mcp_server; print('✅ mcp_server imports')"
python -c "from mcp import config; print('✅ config imports')"

# Test handlers
python -c "from mcp.handlers import core_memory_handlers; print('✅ core_memory_handlers imports')"
python -c "from mcp.handlers import policy_and_guidance_handlers; print('✅ policy_and_guidance_handlers imports')"

# Test memory subsystem
python -c "from mcp.memory import embedding_service; print('✅ embedding_service imports')"
python -c "from mcp.memory import vector_operations; print('✅ vector_operations imports')"

# Test tools
python -c "from mcp.tools import core_memory_tools; print('✅ core_memory_tools imports')"
python -c "from mcp.tools import policy_tools; print('✅ policy_tools imports')"
```
**Pass Criteria:** All 10 imports succeed  
**ROLLBACK TRIGGER:** Any core import fails

---

### AC7: Existing Tests Still Pass (CRITICAL)
**Test:**
```bash
source .venv/bin/activate
pytest -q tests/test_smoke.py -v
```
**Pass Criteria:** 2/2 tests pass  
**ROLLBACK TRIGGER:** Any test failures

---

### AC8: Black Formatting Passes
**Test:**
```bash
source .venv/bin/activate
black --check . 2>&1 | tee black-check.log
echo "Exit code: $?"
```
**Pass Criteria:** Exit code 0, "All checks passed!" or "would be left unchanged"

---

### AC9: Build Succeeds
**Test:**
```bash
source .venv/bin/activate
python -m build 2>&1 | tee build.log
ls -lh dist/
```
**Pass Criteria:** 
- Build completes without errors
- dist/ contains wheel and sdist
- Both mdnotes and mcp modules included in package

---

### AC10: No New Security Issues
**Test:**
```bash
source .venv/bin/activate
pip-audit 2>&1 | tee audit.log
# Check for HIGH/CRITICAL issues
grep -i "HIGH\|CRITICAL" audit.log && echo "⚠️ Security issues found" || echo "✅ No high-severity issues"
```
**Pass Criteria:** No HIGH or CRITICAL security issues introduced

---

## Critical Verification Checks

### Verification 1: Ruff Error Count Progression
**Test:**
```bash
# Document error reduction
echo "Baseline: 385 errors (from W003 completion)"
source .venv/bin/activate
ruff check . --statistics | grep "Found"
```
**Expected:** "Found 0 errors" or "All checks passed!"

---

### Verification 2: Code Still Compiles
**Test:**
```bash
source .venv/bin/activate
python -m py_compile src/mcp/*.py
python -m py_compile src/mcp/handlers/*.py
python -m py_compile src/mcp/memory/*.py
python -m py_compile src/mcp/prompts/*.py
python -m py_compile src/mcp/tools/*.py
```
**Expected:** No syntax errors

---

### Verification 3: Import Structure Intact
**Test:**
```bash
source .venv/bin/activate
python -c "import sys; sys.path.insert(0, 'src'); import mcp; print(dir(mcp))"
```
**Expected:** Lists mcp module contents without errors

---

## Performance Tests

**Not applicable for W004** (code quality task, no performance impact expected)

---

## Integration Tests to Add

**Deferred to W006** (Basic Integration Testing)

Future tests will verify:
- MCP server initialization
- Memory CRUD operations
- Policy system functionality
- Vector search operations

---

## Test Execution Order

### Phase 1: Pre-Test Baseline
1. Verify branch: `feat/W004-step-01-adapt-mcp-code`
2. Verify baseline tag exists
3. Document initial error counts (385 ruff, multiple mypy)

### Phase 2: Post-Automated-Fixes Verification
4. **AC1:** Ruff errors reduced significantly (expect ~67 remaining)
5. **AC2:** Import sorting fixed
6. **AC3:** Type annotations modernized
7. **AC8:** Black formatting passes

### Phase 3: Post-Manual-Fixes Verification
8. **AC1:** Ruff errors = 0 (CRITICAL)
9. **AC4:** Mypy passes on MCP code

### Phase 4: Functionality Verification (CRITICAL)
10. **AC6:** Core MCP imports work → ROLLBACK if fails
11. **AC7:** Existing tests pass → ROLLBACK if fails

### Phase 5: Final Quality Checks
12. **AC5:** UI code removed
13. **AC9:** Build succeeds
14. **AC10:** Security audit clean

---

## Rollback Procedure

**Trigger Conditions:**
1. AC1 fails (ruff errors remain after all attempts)
2. AC6 fails (core MCP functionality breaks)
3. AC7 fails (existing tests fail)
4. AC4 fails (insurmountable mypy errors)
5. Build fails after changes

**Rollback Steps:**
```bash
cd /media/hannesn/storage/Code/MCPLocalLLM

# Restore from baseline
git reset --hard pre/W004-<timestamp>
git push origin feat/W004-step-01-adapt-mcp-code --force-with-lease

# Verify rollback
source .venv/bin/activate
pytest -q tests/test_smoke.py

# Document failure
echo "W004 aborted: <reason>" >> .oodatcaa/work/SPRINT_DISCUSS.md
```

---

## Exit Criteria

- [ ] All 10 acceptance criteria (AC1-AC10) verified and documented
- [ ] All 3 critical checks pass (AC1: ruff, AC6: imports, AC7: tests)
- [ ] Ruff errors reduced from 385 to 0
- [ ] Mypy errors resolved (with documented ignores)
- [ ] Black formatting passes
- [ ] Build succeeds
- [ ] No regressions in existing functionality
- [ ] Branch pushed to origin
- [ ] Ready for W005 (if needed) and W006 (Integration Testing)

---

## Test Artifacts

**Pre-Adaptation:**
- Baseline tag: `pre/W004-<timestamp>`
- Initial ruff report: 385 errors
- Initial mypy report: multiple type errors

**Post-Adaptation:**
- Final ruff report: 0 errors
- Final mypy report: pass (with documented ignores)
- Black check: pass
- Test results: all pass
- Build artifacts: wheel + sdist

---

## Success Metrics

**Functional Success:**
- 385 ruff errors → 0 errors (100% fixed)
- Mypy type errors resolved
- All core MCP imports work (10/10)
- Zero test regressions

**Quality Success:**
- Black formatting: 100% pass
- Ruff linting: 100% pass  
- Mypy type checking: pass (with reasonable ignores)
- Build: success
- Security: no new high-severity issues

**Risk Mitigation Success:**
- All rollback triggers monitored
- Core functionality verified
- Existing tests protected

---

**Test Plan Status:** ✅ APPROVED  
**Ready for:** Builder Execution → Tester Validation
