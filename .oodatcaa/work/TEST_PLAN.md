# W006 Test Plan — Basic Integration Testing

**Planner:** agent-planner-A  
**Test Plan Version:** 1.0  
**Created:** 2025-10-03T04:05:00+02:00  
**Story:** W006 - Basic Integration Testing

---

## Test Strategy

**Scope:** Integration tests for MCP server initialization, memory operations, and policy system  
**Approach:** Pytest with async support, Qdrant dependency handling, test isolation  
**Coverage Target:** ≥85% line coverage on new test files

---

## Quality Gate Commands

### 1. Format Check
```bash
black tests/mcp/
black --check tests/mcp/
```
**Expected:** All files formatted, no changes needed

---

### 2. Lint Check
```bash
ruff check tests/mcp/
```
**Expected:** 0 errors, 0 warnings

---

### 3. Type Check (Optional for Tests)
```bash
mypy tests/mcp/ || echo "Type checking tests is optional"
```
**Expected:** Clean or acceptable errors (tests excluded from strict mypy)

---

### 4. Unit Tests (Existing)
```bash
pytest tests/test_smoke.py -v
```
**Expected:** 2/2 tests pass (test_greets, test_package_import)

---

### 5. Integration Tests (New)
```bash
pytest tests/mcp/ -v -m integration
```
**Expected:** 12 tests pass (4 server + 5 memory + 3 policy)

---

### 6. Full Test Suite
```bash
pytest tests/ -v
```
**Expected:** 14 tests pass total (2 smoke + 12 integration), 0 failures

---

### 7. Coverage Check
```bash
pytest --cov=tests/mcp --cov-report=term-missing --cov-fail-under=85
```
**Expected:** ≥85% line coverage on tests/mcp/

---

### 8. Build Check
```bash
python -m build
```
**Expected:** Successfully builds wheel and sdist in dist/

---

### 9. Security Audit
```bash
pip-audit
```
**Expected:** 0 high-severity vulnerabilities

---

## Acceptance Criteria Validation

### AC1: MCP Server Initialization ✅
**Test File:** `tests/mcp/test_server_initialization.py`  
**Tests:**
- `test_server_can_initialize`: Creates MemoryMCPServer instance
- `test_memory_manager_available`: Verifies memory_manager is not None
- `test_health_check`: Calls get_system_health(), validates response
- `test_available_tools`: Calls get_available_tools(), checks tool list

**Validation Command:**
```bash
pytest tests/mcp/test_server_initialization.py -v
```
**Expected:** 4/4 tests pass

**AC Pass Criteria:** ✅ All 4 server initialization tests pass

---

### AC2: Memory CRUD Operations ✅
**Test File:** `tests/mcp/test_memory_operations.py`  
**Tests:**
- `test_create_memory`: Stores a memory, verifies creation
- `test_read_memory`: Retrieves memory by ID
- `test_search_memories`: Searches memories by text query
- `test_update_memory`: Modifies existing memory
- `test_delete_memory`: Removes memory, verifies deletion

**Validation Command:**
```bash
pytest tests/mcp/test_memory_operations.py -v
```
**Expected:** 5/5 tests pass

**AC Pass Criteria:** ✅ All 5 memory CRUD tests pass

---

### AC3: Policy System ✅
**Test File:** `tests/mcp/test_policy_system.py`  
**Tests:**
- `test_policy_initialization`: Verifies PolicyProcessor loads
- `test_preservation_levels`: Checks strict/moderate/flexible levels
- `test_rule_compliance`: Validates rule compliance markers

**Validation Command:**
```bash
pytest tests/mcp/test_policy_system.py -v
```
**Expected:** 3/3 tests pass

**AC Pass Criteria:** ✅ All 3 policy system tests pass

---

### AC4: No Regressions ✅
**Test File:** `tests/test_smoke.py` (existing)

**Validation Command:**
```bash
pytest tests/test_smoke.py -v
```
**Expected:** 2/2 tests pass (test_greets, test_package_import)

**AC Pass Criteria:** ✅ All existing tests still pass, zero regressions

---

### AC5: Test Organization ✅
**Expected Structure:**
```
tests/
├── mcp/
│   ├── __init__.py (empty)
│   ├── conftest.py (fixtures)
│   ├── test_server_initialization.py
│   ├── test_memory_operations.py
│   └── test_policy_system.py
├── test_smoke.py (existing)
└── acceptance/ (existing)
```

**Validation Command:**
```bash
ls -la tests/mcp/
pytest --collect-only tests/mcp/
```
**Expected:** 4 test files in tests/mcp/, pytest discovers 12 tests

**AC Pass Criteria:** ✅ Tests organized in tests/mcp/ with clear structure

---

### AC6: Performance ⚡
**Validation Command:**
```bash
time pytest tests/mcp/ -v
```
**Expected:** Total time <30 seconds

**AC Pass Criteria:** ✅ Integration tests complete in <30 seconds

---

### AC7: Quality Gates 🛡️
**Validation Commands:**
```bash
black --check tests/mcp/
ruff check tests/mcp/
pytest tests/ -v
python -m build
pip-audit
```
**Expected:** All commands pass with 0 errors

**AC Pass Criteria:** ✅ All quality gates (black, ruff, pytest, build, security) pass

---

### AC8: Coverage 📊
**Validation Command:**
```bash
pytest --cov=tests/mcp --cov-report=term-missing --cov-fail-under=85
```
**Expected:** ≥85% line coverage on tests/mcp/

**AC Pass Criteria:** ✅ Test files have ≥85% line coverage

---

### AC9: Isolation 🔒
**Validation Commands:**
```bash
# Run tests in random order
pytest tests/mcp/ --random-order -v
# Run tests in parallel
pytest tests/mcp/ -n auto -v
```
**Expected:** All tests pass regardless of execution order

**AC Pass Criteria:** ✅ Tests can run independently or in any order

---

### AC10: Documentation 📝
**Expected:** Each test file has:
- Module docstring explaining purpose
- Test function docstrings explaining what is validated
- Clear assertions with helpful failure messages

**Validation Command:**
```bash
# Check docstrings exist
python -c "import tests.mcp.test_server_initialization; print(tests.mcp.test_server_initialization.__doc__)"
```
**Expected:** Non-None docstring returned

**AC Pass Criteria:** ✅ Docstrings present explaining test purpose

---

## Test Execution Summary

**Full Validation Sequence:**
```bash
# 1. Format
black tests/mcp/
black --check tests/mcp/

# 2. Lint
ruff check tests/mcp/

# 3. Run existing tests (regression check)
pytest tests/test_smoke.py -v

# 4. Run new integration tests
pytest tests/mcp/ -v

# 5. Run full test suite
pytest tests/ -v

# 6. Check coverage
pytest --cov=tests/mcp --cov-report=term-missing --cov-fail-under=85

# 7. Build
python -m build

# 8. Security
pip-audit
```

**Expected Final Results:**
- ✅ 14 tests pass (2 smoke + 12 integration)
- ✅ 0 failures, 0 errors
- ✅ ≥85% coverage on tests/mcp/
- ✅ All quality gates pass
- ✅ Build succeeds
- ✅ No high-severity vulnerabilities

---

## Acceptance Tests to Add

**New Integration Test Files:**
1. `tests/mcp/conftest.py` - Pytest fixtures (qdrant_available, mcp_server, test_collection, cleanup_test_data)
2. `tests/mcp/test_server_initialization.py` - 4 tests for server initialization
3. `tests/mcp/test_memory_operations.py` - 5 tests for memory CRUD
4. `tests/mcp/test_policy_system.py` - 3 tests for policy system

**Total New Tests:** 12 integration tests

---

## Performance/Benchmark Setup

**Target:** Integration tests complete in <30 seconds

**Measurement:**
```bash
time pytest tests/mcp/ -v
```

**Acceptable Range:** 5-30 seconds (depending on Qdrant startup time)

---

## Test Plan Complete

Tester (W006-T01) should validate all 10 acceptance criteria using the commands above. All ACs must pass before W006 can be marked "ready for integrator".
