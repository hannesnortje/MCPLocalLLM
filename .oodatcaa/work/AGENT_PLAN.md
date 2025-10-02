# W006 Implementation Plan — Basic Integration Testing

**Planner:** agent-planner-A  
**Plan Version:** 1.0  
**Created:** 2025-10-03T04:05:00+02:00  
**Branch:** `feat/W006-step-01-integration-tests`  
**Objective:** OBJ-2025-002 → Quality & Performance → Integration Testing

---

## Traceability

**Epic:** Sprint 1 - MCP Server Foundation  
**Story:** W006 - Basic Integration Testing  
**Dependencies:** W004 (Adapt MCP for Training Use Case) ✅ SATISFIED  
**Blocks:** W008 (Documentation Update - partial)

---

## Problem Statement

After migrating and adapting the MCP server (W001-W005), we need **integration tests** to verify that core MCP functionality works correctly before moving to documentation and deployment. Currently:

- ❌ **No MCP integration tests exist** (tests/mcp/ directory is empty)
- ✅ Only smoke tests for mdnotes module (tests/test_smoke.py)
- ⚠️ MCP server initialization, memory operations, and policy system are **untested**
- ⚠️ Risk of regressions without automated test coverage

**Goal:** Create **basic integration tests** to verify MCP server initialization, memory CRUD operations, policy system, and ensure no regressions in existing functionality.

---

## Constraints, Interfaces & Risks

### Constraints
- **Qdrant dependency:** Tests require Qdrant server running (Docker or local)
- **Async testing:** MCP server uses async operations (requires pytest-asyncio)
- **Test isolation:** Each test should clean up data to avoid cross-test pollution
- **Performance:** Integration tests should complete in <30 seconds total
- **Coverage target:** ≥85% line coverage on new test code

### Key Interfaces
- **MCP Server API:** `MemoryMCPServer` class in `src/mcp/mcp_server.py`
- **Memory Manager:** `QdrantMemoryManager` in `src/mcp/memory_manager.py`
- **Policy Processor:** `PolicyProcessor` in `src/mcp/policy_processor.py`
- **Test Framework:** pytest with pytest-asyncio (already in dev dependencies)

### Risks & Mitigation
1. **Risk:** Qdrant not running → tests fail immediately
   - **Mitigation:** Add pytest fixture to check/start Qdrant, skip tests if unavailable
2. **Risk:** Test data pollution across tests
   - **Mitigation:** Use unique collection names per test, cleanup fixtures
3. **Risk:** Slow integration tests (>1 minute)
   - **Mitigation:** Mark as integration tests, allow parallel execution
4. **Risk:** Existing mdnotes tests break
   - **Mitigation:** Run full test suite before/after, verify zero regressions

---

## Definition of Done (DoD)

### Functional ACs
1. ✅ **MCP Server Initialization:** Test creates MemoryMCPServer instance successfully
2. ✅ **Memory CRUD Operations:** Test stores, retrieves, updates, and deletes memories
3. ✅ **Policy System:** Test validates policy operations (preservation levels, compliance)
4. ✅ **No Regressions:** Existing mdnotes tests still pass (test_smoke.py)
5. ✅ **Test Organization:** Tests in `tests/mcp/` directory with clear structure

### Non-Functional ACs
6. ✅ **Performance:** Integration tests complete in <30 seconds
7. ✅ **Quality Gates:** All gates pass (black, ruff, mypy, pytest, build, security)
8. ✅ **Coverage:** Test files have ≥85% line coverage
9. ✅ **Isolation:** Tests can run independently or in any order
10. ✅ **Documentation:** Docstrings explain what each test validates

---

## Alternatives Considered

### Alternative 1: Minimal Smoke Tests Only (NOT CHOSEN)
**Approach:** Only test server initialization, skip CRUD and policy tests  
**Pros:**
- Fastest to implement (30 minutes)
- Low complexity

**Cons:**
- ❌ Insufficient coverage of critical functionality
- ❌ Doesn't validate memory operations
- ❌ Misses policy system validation
- ❌ Doesn't meet AC2, AC3

**Verdict:** Rejected - too minimal for integration milestone

---

### Alternative 2: Comprehensive Integration Test Suite ✅ CHOSEN
**Approach:** Create structured integration tests covering server, memory, and policy  
**Pros:**
- ✅ Validates all critical MCP functionality (server, memory CRUD, policy)
- ✅ Meets all 10 acceptance criteria
- ✅ Provides safety net against future regressions
- ✅ Sets foundation for future test expansion
- ✅ Reasonable scope (3-4 test files, ~150-200 lines total)

**Cons:**
- Slightly longer implementation (~90 minutes vs 30 minutes)
- Requires Qdrant setup

**Verdict:** CHOSEN - best balance of coverage and effort

---

### Alternative 3: Full End-to-End Test Suite (NOT CHOSEN)
**Approach:** Include Cursor IDE integration, MCP protocol communication, tool calls  
**Pros:**
- Maximum coverage

**Cons:**
- ❌ Out of scope for "Basic Integration Testing"
- ❌ Would require 4+ hours implementation
- ❌ Complex test setup (Cursor IDE mocking)
- ❌ Better suited for future W00X task

**Verdict:** Rejected - over-scoped for this story

---

## Implementation Plan — Comprehensive Integration Tests (Alternative 2)

### Step 1: Test Infrastructure Setup (20 min)
**File:** `tests/mcp/conftest.py` (pytest fixtures)

**Actions:**
1. Create `tests/mcp/conftest.py` with shared fixtures:
   - `qdrant_available`: Check if Qdrant is running, skip tests if not
   - `mcp_server`: Initialize MemoryMCPServer instance (with cleanup)
   - `test_collection`: Create unique test collection name for isolation
   - `cleanup_test_data`: Teardown fixture to remove test collections
2. Add pytest markers for integration tests: `@pytest.mark.integration`
3. Configure pytest to discover and run MCP tests

**Exit Gate:** conftest.py created, fixtures functional, pytest --collect-only works

---

### Step 2: Server Initialization Tests (20 min)
**File:** `tests/mcp/test_server_initialization.py`

**Actions:**
1. Test 1: `test_server_can_initialize` - Verify MemoryMCPServer creates successfully
2. Test 2: `test_memory_manager_available` - Check memory_manager is not None
3. Test 3: `test_health_check` - Verify get_system_health() returns valid status
4. Test 4: `test_available_tools` - Check get_available_tools() returns tool list
5. Add docstrings explaining each test's purpose

**Exit Gate:** 4 tests pass, server initialization validated

---

### Step 3: Memory CRUD Operations Tests (30 min)
**File:** `tests/mcp/test_memory_operations.py`

**Actions:**
1. Test 1: `test_create_memory` - Store a memory and verify creation
2. Test 2: `test_read_memory` - Retrieve stored memory by ID
3. Test 3: `test_search_memories` - Search memories by text query
4. Test 4: `test_update_memory` - Modify existing memory
5. Test 5: `test_delete_memory` - Remove memory and verify deletion
6. Use unique collection names per test for isolation
7. Add cleanup in teardown to prevent data pollution

**Exit Gate:** 5 tests pass, memory CRUD validated

---

### Step 4: Policy System Tests (20 min)
**File:** `tests/mcp/test_policy_system.py`

**Actions:**
1. Test 1: `test_policy_initialization` - Verify PolicyProcessor loads correctly
2. Test 2: `test_preservation_levels` - Check strict/moderate/flexible levels work
3. Test 3: `test_rule_compliance` - Validate rule compliance markers
4. Use simple policy examples (no complex policy files needed)

**Exit Gate:** 3 tests pass, policy system validated

---

### Step 5: Regression Testing (10 min)
**Actions:**
1. Run existing test suite: `pytest tests/test_smoke.py -v`
2. Verify all existing tests still pass (zero regressions)
3. Run full test suite: `pytest tests/ -v`
4. Verify new integration tests pass

**Exit Gate:** All tests pass (existing + new), zero regressions

---

### Step 6: Quality Gates & Commit (20 min)
**Actions:**
1. Format: `black tests/mcp/`
2. Lint: `ruff check tests/mcp/`
3. Type check: `mypy tests/mcp/` (if applicable)
4. Coverage: `pytest --cov=tests/mcp --cov-report=term-missing`
5. Verify ≥85% coverage on new test files
6. Commit with label: `[test] W006: Add basic MCP integration tests`

**Exit Gate:** All quality gates pass, commit created

---

## Branch Strategy

**Branch Name:** `feat/W006-step-01-integration-tests`  
**Baseline Tag:** `pre/W006-integration-<ISO8601>`  
**Merge Target:** `main`  
**Commits:**
- `[plan]` W006: Initial test infrastructure and fixtures
- `[test]` W006: Add server initialization tests
- `[test]` W006: Add memory CRUD operation tests
- `[test]` W006: Add policy system tests
- `[test]` W006: Verify regression tests pass

---

## Task Breakdown for SPRINT_QUEUE.json

1. **W006-B01:** Steps 1-3 - Test infrastructure + Server tests + Memory CRUD tests (70 min)
2. **W006-B02:** Steps 4-6 - Policy tests + Regression validation + Quality gates (50 min)
3. **W006-T01:** Testing - Verify all 10 ACs pass (30 min)

**Total Estimated Time:** ~2.5 hours

---

## Handoff Notes for Builder

**Key Files to Create:**
- `tests/mcp/conftest.py` - Pytest fixtures for MCP testing
- `tests/mcp/test_server_initialization.py` - Server init tests (4 tests)
- `tests/mcp/test_memory_operations.py` - Memory CRUD tests (5 tests)
- `tests/mcp/test_policy_system.py` - Policy system tests (3 tests)

**Key Dependencies:**
- pytest-asyncio (already installed)
- Qdrant server running (check with fixture, skip if unavailable)

**Testing Commands:**
- Run MCP tests only: `pytest tests/mcp/ -v`
- Run all tests: `pytest tests/ -v`
- Check coverage: `pytest --cov=tests/mcp --cov-report=term-missing`

**Critical Requirements:**
1. Use `@pytest.mark.asyncio` for async tests
2. Add `@pytest.mark.integration` marker for integration tests
3. Use unique collection names per test (e.g., f"test_collection_{uuid.uuid4()}")
4. Clean up test data in teardown fixtures
5. Skip tests gracefully if Qdrant unavailable

---

**Plan Complete.** Builder should implement Steps 1-6, then Tester validates all 10 ACs.
