# Test Plan — W002: Execute MCP Server Migration

**Work Item:** W002 | **Sprint:** 1 | **Created:** 2025-10-02

---

## Test Commands

### Format Check
```bash
black --check .
```
**Expected:** PASS (no formatting issues in migrated code)  
**Note:** May need to run `black .` first if MCP source has different formatting

---

### Lint Check
```bash
ruff check .
```
**Expected:** PASS or warnings only (no critical errors)  
**Note:** Import errors expected until W003 (dependencies not installed yet)

---

### Type Check
```bash
mypy .
```
**Expected:** Import errors expected (MCP dependencies not installed)  
**Action:** Verify no type errors in existing mdnotes module

---

### Unit Tests (Existing Only)
```bash
pytest -q tests/test_smoke.py
```
**Expected:** PASS (existing tests unaffected by migration)  
**CRITICAL:** This is a rollback trigger if it fails

---

### Acceptance Tests (Existing Only)
```bash
pytest -q tests/acceptance
```
**Expected:** PASS (existing tests unaffected)

---

### Coverage Check (Existing Only)
```bash
pytest --cov=src/mdnotes --cov-report=term-missing --cov-fail-under=85
```
**Expected:** PASS (mdnotes coverage maintained)  
**Note:** MCP code coverage will be tested in W006

---

### Build Check
```bash
python -m build
```
**Expected:** PASS (package still builds)  
**Note:** MCP not yet importable (dependencies in W003)

---

### Security Audit
```bash
pip-audit
```
**Expected:** PASS (no new dependencies added in W002)  
**Note:** MCP dependencies will be audited in W003

---

## Acceptance Testing

### AC1: All 67 Essential MCP Files Copied
**Test:**
```bash
# Count Python files in src/mcp/
python_files=$(find src/mcp -name '*.py' | wc -l)
echo "Python files: $python_files (expected: ~40+)"

# Count policy files
policy_files=$(find policy -name '*.md' | wc -l)
echo "Policy files: $policy_files (expected: ~4)"

# Count total MCP files
total_files=$(find src/mcp policy docs/mcp scripts server.py launcher.py memory_server.py docker-compose.yml -type f 2>/dev/null | wc -l)
echo "Total MCP files: $total_files (expected: 60-70)"
```
**Pass Criteria:** Total files between 60-70, Python files ~40+, policy files ~4

---

### AC2: No UI Files Copied
**Test:**
```bash
# Should return empty (no UI files)
find src/mcp -name '*ui*' -o -name '*UI*' -o -name '*pyside*'
echo "Exit code: $?"
```
**Pass Criteria:** No files found (exit code 0 with empty output)

---

### AC3: Infrastructure Files Copied
**Test:**
```bash
ls -la docker-compose.yml .env.example server.py
ls -la src/mcp/mcp_server.py src/mcp/memory_manager.py src/mcp/qdrant_manager.py
```
**Pass Criteria:** All listed files exist

---

### AC4: .gitignore Merged
**Test:**
```bash
grep -A 3 "# MCP specific" .gitignore
```
**Pass Criteria:** Shows MCP entries (qdrant_storage/, .env, policy/*.lock)

---

### AC5: .oodatcaa/ Directory Untouched (CRITICAL)
**Test:**
```bash
git status .oodatcaa/
```
**Pass Criteria:** Output shows "nothing to commit" or NO changes to .oodatcaa/  
**ROLLBACK TRIGGER:** Any modifications to .oodatcaa/

---

### AC6: src/mdnotes/ Module Preserved (CRITICAL)
**Test:**
```bash
git status src/mdnotes/
git diff src/mdnotes/
```
**Pass Criteria:** No changes to src/mdnotes/  
**ROLLBACK TRIGGER:** Any modifications to src/mdnotes/

---

### AC7: Existing Tests Still Pass (CRITICAL)
**Test:**
```bash
pytest -q tests/test_smoke.py
```
**Pass Criteria:** All tests pass  
**ROLLBACK TRIGGER:** Any test failures

---

### AC8: File Count Matches Expected
**Test:**
```bash
total_files=$(find src/mcp policy docs/mcp scripts -type f 2>/dev/null | wc -l)
echo "Total files: $total_files"
# Expected: 60-70 files
```
**Pass Criteria:** File count between 60-70 (±10% of 67 essential files)

---

### AC9: No Python Syntax Errors
**Test:**
```bash
for file in src/mcp/*.py; do
    python -m py_compile "$file" || echo "Syntax error in $file"
done
```
**Pass Criteria:** No syntax errors reported  
**Note:** Import errors are OK (dependencies not installed)

---

### AC10: Git History Clean
**Test:**
```bash
git log -1 --stat
git log -1 --pretty=format:"%s"
```
**Pass Criteria:** 
- Commit message starts with `[impl] W002:`
- Commit shows added files in src/mcp/, policy/, docs/mcp/
- No modifications to .oodatcaa/ or src/mdnotes/

---

## Critical Verification Checks

### Verification 1: Directory Structure
**Test:**
```bash
ls -la src/
```
**Expected Output:**
- `mdnotes/` (existing, untouched)
- `mcp/` (new, contains migrated files)

---

### Verification 2: MCP Subdirectories Present
**Test:**
```bash
ls -la src/mcp/
```
**Expected Output:**
- `handlers/` directory
- `memory/` directory
- `prompts/` directory
- `tools/` directory
- NO `ui/` directory

---

### Verification 3: Policy Files Present
**Test:**
```bash
ls -la policy/
```
**Expected Output:** ~4 markdown files with governance policies

---

## Performance Tests

**Not applicable for W002** (file copy operation, no performance requirements)

---

## Integration Tests to Add

**Not applicable for W002** (MCP not functional until W003-W004)

Future W006 will add:
- MCP server initialization tests
- Memory CRUD operation tests
- Policy system functionality tests
- Qdrant integration tests

---

## Test Execution Order

### Phase 1: Pre-Test Setup
1. Ensure migration branch checked out
2. Activate venv: `source .venv/bin/activate`

### Phase 2: Critical Protection Checks (MUST PASS)
1. **AC5:** `.oodatcaa/` untouched → ROLLBACK if fails
2. **AC6:** `src/mdnotes/` preserved → ROLLBACK if fails
3. **AC7:** Existing tests pass → ROLLBACK if fails

### Phase 3: File Verification Checks
4. **AC1:** File count 60-70
5. **AC2:** No UI files
6. **AC3:** Infrastructure files exist
7. **AC4:** .gitignore merged
8. **AC9:** No syntax errors

### Phase 4: Quality Checks
9. **AC8:** File count matches W001 analysis
10. **AC10:** Git history clean

### Phase 5: Standard CI Gates
11. Run `black --check .` or `black .` then commit
12. Run `ruff check .` (warnings OK, no critical errors)
13. Run existing pytest suite
14. Run `python -m build`

---

## Rollback Procedure

**Trigger Conditions:**
1. AC5 fails (`.oodatcaa/` modified)
2. AC6 fails (`src/mdnotes/` modified)
3. AC7 fails (existing tests fail)
4. File count <50 or >80 (>20% deviation from expected 67)

**Rollback Steps:**
```bash
cd /media/hannesn/storage/Code/MCPLocalLLM
git reset --hard pre/W002-<timestamp>
git push origin feat/W002-step-01-copy-mcp-core --force-with-lease
echo "Migration aborted: <reason>" >> .oodatcaa/work/SPRINT_DISCUSS.md
```

**Documentation:**
- Update `.oodatcaa/work/AGENT_LOG.md` with rollback reason
- Update `.oodatcaa/work/SPRINT_QUEUE.json`: W002 status → blocked
- Negotiate with Refiner agent for revised approach

---

## Exit Criteria

- [ ] All 10 acceptance criteria (AC1-AC10) verified and documented
- [ ] All 3 critical protection checks pass (AC5, AC6, AC7)
- [ ] File count verification within expected range
- [ ] No UI files present in migrated code
- [ ] Standard CI commands run successfully (black, ruff, pytest on existing code)
- [ ] Git commit clean and descriptive
- [ ] Branch pushed to origin
- [ ] Ready for W003 (Integrate MCP Dependencies)

---

## Test Artifacts

**Pre-Migration:**
- Baseline tag: `pre/W002-<timestamp>`
- W001 analysis documents (migration_checklist.md, essential_components.md)

**Post-Migration:**
- Migration commit in `feat/W002-step-01-copy-mcp-core` branch
- File count verification output
- Existing test results
- Protection check verification (git status .oodatcaa/, git status src/mdnotes/)

---

## Success Metrics

**Functional Success:**
- 67 essential MCP files copied (±10% acceptable)
- Zero modifications to protected areas (OODATCAA, mdnotes)
- All existing tests pass

**Quality Success:**
- No Python syntax errors
- Git history clean and traceable
- No UI bloat (src/ui/ excluded)

**Risk Mitigation Success:**
- All rollback triggers monitored
- Verification steps executed at each phase
- Protection checks validated before commit

---

**Test Plan Status:** ✅ APPROVED  
**Ready for:** Builder Execution → Tester Validation
