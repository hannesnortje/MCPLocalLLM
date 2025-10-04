# TEST_PLAN: P007 - Integration Testing & Quality Validation

**Task ID:** P007  
**Objective:** SPRINT-2025-002 (OODATCAA Process Improvement)  
**Sprint:** 2  
**Tester:** TBD  
**Created:** 2025-10-04T17:00:00+02:00

---

## Testing Strategy

**Task Type:** Quality Validation & Integration Testing (No Functional Changes)

**Testing Approach:**
1. **Quality Gates Execution:** Run all 8 gates (black, ruff, mypy, pytest unit, pytest acceptance, coverage, build, pip-audit)
2. **Baseline Comparison:** Compare Sprint 2 vs Sprint 1 baselines to detect regressions
3. **Regression Testing:** Run full test suite (unit + acceptance + mcp + smoke + daemon)
4. **Integration Testing:** Validate P001 (daemon), P002 (rotation), P003 (sprint mgmt) end-to-end
5. **Performance Validation:** Verify benchmarks met (test suite < 30s, build < 10s, tools < 5s)
6. **Coverage Analysis:** Verify ≥ 85% overall and for new code
7. **Standards Documentation:** Document quality standards for Sprint 3+
8. **Certification:** Certify Sprint 2 production-ready

**Note:** This task validates Sprint 2 quality without making functional changes. Technical debt (29 ruff, ~400 mypy) is acceptable if not regressed.

---

## Quality Gates (All 8 Must Run)

### Standard Python Quality Gates
1. **Format (Black):** `black --check .`
   - Expected: PASS or document formatting issues
   - Baseline: Sprint 1 passing

2. **Lint (Ruff):** `ruff check .`
   - Expected: ≤ 29 errors (Sprint 1 baseline from W008)
   - Acceptable: 29 errors (documented technical debt)
   - Regression: > 29 errors (must investigate)

3. **Types (Mypy):** `mypy .`
   - Expected: ≤ 400 errors (Sprint 1 baseline from W005)
   - Acceptable: ~400 errors (documented technical debt)
   - Regression: > 450 errors (must investigate)

4. **Unit Tests:** `pytest -q`
   - Expected: ≥ 13 passed (Sprint 1 baseline from W007)
   - Expected: 3 skipped (Qdrant unavailable - acceptable)
   - Expected: 0 failed (critical)

5. **Acceptance Tests:** `pytest -q tests/acceptance`
   - Expected: All pass or skip (Qdrant-related skips acceptable)

6. **Coverage:** `pytest --cov=src --cov-report=term-missing --cov-fail-under=85`
   - Expected: ≥ 85% overall coverage
   - Expected: ≥ 85% coverage for new code (P001-P006)

7. **Build:** `python -m build`
   - Expected: Clean build, no errors
   - Expected: dist/ artifacts created

8. **Security:** `pip-audit`
   - Expected: No high-severity vulnerabilities
   - Acceptable: Low/medium severity with documented mitigation

---

## Acceptance Criteria (12 Total)

### AC1: All Quality Gates Executed ✅
**Requirement:** All 8 quality gates run and results documented

**Test Procedure:**
1. Run all 8 quality gates in sequence
2. Capture output logs for each gate
3. Document pass/fail status
4. Compare to Sprint 1 baseline

**Pass Criteria:**
- All 8 gates executed successfully (command runs without errors)
- Output logs captured: `gate1_black.log`, `gate2_ruff.log`, ..., `gate8_security.log`
- Results documented in `.oodatcaa/work/quality_gates_sprint2.md`
- Baseline comparison included

**Verification:**
```bash
# Verify all gate logs exist
ls -lh .oodatcaa/work/gate*.log | wc -l  # Should be 8
# Verify results document exists
ls -lh .oodatcaa/work/quality_gates_sprint2.md
```

---

### AC2: Full Test Suite Passes (Zero Critical Regressions) ✅
**Requirement:** All tests pass or skip acceptably, no unexpected failures

**Test Procedure:**
1. Run full test suite: `pytest -v --tb=short`
2. Run test categories: smoke, mcp, daemon, acceptance
3. Analyze results: passed, skipped, failed
4. Compare to Sprint 1 baseline (13 passed, 3 skipped)

**Pass Criteria:**
- **Passed:** ≥ 13 tests (Sprint 1 baseline)
- **Skipped:** 3 tests (Qdrant unavailable - acceptable)
- **Failed:** 0 tests (critical - must investigate any failures)
- **Execution Time:** < 30 seconds (performance baseline)

**Verification:**
```bash
# Run full test suite
pytest -v --tb=short > .oodatcaa/work/regression_tests_full.log 2>&1
# Check for failures
grep -i "failed" .oodatcaa/work/regression_tests_full.log
# Count passed tests
grep -c "PASSED" .oodatcaa/work/regression_tests_full.log  # >= 13
```

---

### AC3: P001 Daemon Integration Validated ✅
**Requirement:** P001 daemon system works end-to-end

**Test Procedure:**
1. Run unit tests: `pytest tests/test_agent_daemon.py -v`
2. Test daemon help: `python scripts/agent-daemon.py --help`
3. Test queue validation: `python scripts/agent-daemon.py --validate-queue`
4. Test Makefile commands: `make -n daemon-start`, `make -n daemon-status`
5. Document results

**Pass Criteria:**
- Unit tests: All 10 methods pass (5 test classes)
- Help command: Displays usage without errors
- Queue validation: Validates SPRINT_QUEUE.json successfully
- Makefile commands: Dry-run shows correct commands
- Integration report: `.oodatcaa/work/integration_p001_daemon.md` complete

**Verification:**
```bash
# Run daemon tests
pytest tests/test_agent_daemon.py -v | tee .oodatcaa/work/test_daemon.log
# Check test results
grep -c "PASSED" .oodatcaa/work/test_daemon.log  # >= 10
# Verify integration report
ls -lh .oodatcaa/work/integration_p001_daemon.md
```

---

### AC4: P002 Log Rotation Integration Validated ✅
**Requirement:** P002 log rotation works under real workload

**Test Procedure:**
1. Verify rotation script: `bash scripts/rotate-logs.sh --dry-run`
2. Verify archive structure: `.oodatcaa/work/archive/sprint_2/`
3. Test index generation: `bash scripts/generate-archive-index.sh`
4. Check log sizes: `wc -l .oodatcaa/work/AGENT_LOG.md`
5. Document results

**Pass Criteria:**
- Rotation script: Dry-run successful, no errors
- Archive structure: Sprint 1 and Sprint 2 directories exist
- Index generation: `ARCHIVE_INDEX.md` created successfully
- Log sizes: AGENT_LOG.md and SPRINT_LOG.md sizes documented
- Integration report: `.oodatcaa/work/integration_p002_rotation.md` complete

**Verification:**
```bash
# Dry-run rotation
bash scripts/rotate-logs.sh --dry-run > .oodatcaa/work/test_rotation.log 2>&1
echo "Exit code: $?" >> .oodatcaa/work/test_rotation.log
# Verify archive structure
ls -lh .oodatcaa/work/archive/sprint_1/ | head -5
ls -lh .oodatcaa/work/archive/sprint_2/ | head -5
# Verify integration report
ls -lh .oodatcaa/work/integration_p002_rotation.md
```

---

### AC5: P003 Sprint Management Integration Validated ✅
**Requirement:** P003 sprint management lifecycle works end-to-end

**Test Procedure:**
1. Test dashboard: `make sprint-status`
2. Test status JSON: `python3 -m json.tool .oodatcaa/work/SPRINT_STATUS.json`
3. Test completion script help: `bash scripts/sprint-complete.sh --help`
4. Test initialization script help: `bash scripts/sprint-new.sh --help`
5. Document results

**Pass Criteria:**
- Dashboard: Displays Sprint 2 status without errors
- Status JSON: Valid JSON, includes sprint_id, status, tasks
- Completion script: Help text displayed
- Initialization script: Help text displayed
- Response time: < 5 seconds (achieved 0.199s in P003!)
- Integration report: `.oodatcaa/work/integration_p003_sprint_mgmt.md` complete

**Verification:**
```bash
# Test dashboard
time make sprint-status > .oodatcaa/work/test_dashboard.log 2>&1
# Validate JSON
python3 -m json.tool .oodatcaa/work/SPRINT_STATUS.json > /dev/null 2>&1
echo "JSON valid: $?" >> .oodatcaa/work/test_dashboard.log
# Verify integration report
ls -lh .oodatcaa/work/integration_p003_sprint_mgmt.md
```

---

### AC6: Cross-System Integration Validated ✅
**Requirement:** P001 + P002 + P003 work together

**Test Procedure:**
1. Test daemon reads SPRINT_QUEUE.json (P003 format)
2. Test log rotation handles daemon logs (P001 + P002)
3. Test sprint management works with current queue (P003 + P001)
4. Run end-to-end scenario (all 3 systems)
5. Document results

**Pass Criteria:**
- Daemon + Sprint Mgmt: Daemon reads queue successfully
- Daemon + Log Rotation: Logs handled correctly
- Sprint Mgmt + Log Rotation: Archive integration works
- End-to-end: All systems functional together
- Cross-system report: `.oodatcaa/work/integration_cross_system.md` complete

**Verification:**
```bash
# Test end-to-end scenario
make sprint-status > /dev/null 2>&1
wc -l .oodatcaa/work/AGENT_LOG.md
python scripts/agent-daemon.py --validate-queue > /dev/null 2>&1
echo "Cross-system check: $?" >> .oodatcaa/work/test_cross_system.log
# Verify integration report
ls -lh .oodatcaa/work/integration_cross_system.md
```

---

### AC7: Performance Benchmarks Met ✅
**Requirement:** All performance baselines met or exceeded

**Test Procedure:**
1. Test suite performance: `time pytest -q > /dev/null 2>&1`
2. Build performance: `time python -m build > /dev/null 2>&1`
3. Sprint tools performance: `time make sprint-status > /dev/null 2>&1`
4. Rotation performance: `time bash scripts/rotate-logs.sh --dry-run > /dev/null 2>&1`
5. Quality gates performance: `time make gates > /dev/null 2>&1`

**Pass Criteria:**
- **Test suite:** < 30 seconds (Sprint 1 baseline: ~18-20s)
- **Build:** < 10 seconds
- **Sprint tools:** < 5 seconds (P003 achieved 0.199s!)
- **Log rotation:** < 2 seconds
- **Quality gates:** < 60 seconds
- Performance report: `.oodatcaa/work/performance_validation.md` complete

**Verification:**
```bash
# Run performance tests
echo "Test suite:" >> .oodatcaa/work/performance.log
time pytest -q > /dev/null 2>&1
echo "Build:" >> .oodatcaa/work/performance.log
rm -rf dist/ && time python -m build > /dev/null 2>&1
echo "Sprint tools:" >> .oodatcaa/work/performance.log
time make sprint-status > /dev/null 2>&1
# Verify performance report
ls -lh .oodatcaa/work/performance_validation.md
```

---

### AC8: Coverage ≥ 85% Overall and New Code ✅
**Requirement:** Overall coverage ≥ 85%, new code coverage ≥ 85%

**Test Procedure:**
1. Run coverage: `pytest --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=85`
2. Analyze overall coverage percentage
3. Analyze new code coverage (P001-P006)
4. Identify coverage gaps
5. Document results

**Pass Criteria:**
- **Overall coverage:** ≥ 85% (project standard)
- **New code coverage:** ≥ 85% for Python modules (bash scripts exempt)
- **Pass:** Coverage meets fail-under threshold
- **Gaps identified:** Documented for Sprint 3
- Coverage report: `.oodatcaa/work/coverage_analysis.md` complete
- HTML report: `htmlcov/index.html` generated

**Verification:**
```bash
# Run coverage
pytest --cov=src --cov-report=term-missing --cov-report=html --cov-fail-under=85 > .oodatcaa/work/coverage_report.log 2>&1
echo "Coverage exit code: $?" >> .oodatcaa/work/coverage_report.log
# Extract coverage percentage
grep "TOTAL" .oodatcaa/work/coverage_report.log | tail -1
# Verify coverage report
ls -lh .oodatcaa/work/coverage_analysis.md
ls -lh htmlcov/index.html
```

---

### AC9: Sprint 1 vs Sprint 2 Baseline Comparison Complete ✅
**Requirement:** Detailed comparison of Sprint 1 vs Sprint 2 quality baselines

**Test Procedure:**
1. Document Sprint 1 baseline: ruff 29, mypy ~400, tests 13 passed/3 skipped
2. Document Sprint 2 results: actual metrics
3. Calculate deltas (improvements/regressions)
4. Analyze changes: acceptable vs unacceptable
5. Document results

**Pass Criteria:**
- Sprint 1 baseline: Documented in `.oodatcaa/work/quality_baseline_sprint1.md`
- Sprint 2 results: Documented in `.oodatcaa/work/quality_gates_sprint2.md`
- Comparison: Side-by-side metrics with delta analysis
- Regressions: None critical, all documented and explained
- Improvements: Documented and celebrated

**Verification:**
```bash
# Verify baseline documents exist
ls -lh .oodatcaa/work/quality_baseline_sprint1.md
ls -lh .oodatcaa/work/quality_gates_sprint2.md
# Check for comparison section
grep -i "sprint 1 vs sprint 2" .oodatcaa/work/quality_gates_sprint2.md
grep -i "baseline" .oodatcaa/work/quality_gates_sprint2.md
```

---

### AC10: Quality Standards Documented for Sprint 3+ ✅
**Requirement:** Comprehensive quality standards document created

**Test Procedure:**
1. Verify `.oodatcaa/QUALITY_STANDARDS.md` exists
2. Check for required sections:
   - Quality gates definitions
   - Acceptance thresholds
   - Technical debt policy
   - Coverage requirements
   - Performance benchmarks
   - Security requirements
   - Testing standards
   - CI/CD requirements
3. Verify Sprint 2 baseline documented
4. Verify standards are actionable for Sprint 3+

**Pass Criteria:**
- Quality standards document: `.oodatcaa/QUALITY_STANDARDS.md` exists
- All 8+ sections present and complete
- Sprint 2 baseline: Documented with clear metrics
- Technical debt: Policy defined (when to accept, when to fix)
- Testing standards: Clear requirements for unit, integration, acceptance
- CI/CD requirements: Roadmap for Sprint 3+

**Verification:**
```bash
# Verify document exists
ls -lh .oodatcaa/QUALITY_STANDARDS.md
# Check for key sections
grep -c "^##" .oodatcaa/QUALITY_STANDARDS.md  # >= 8 sections
grep -i "quality gates" .oodatcaa/QUALITY_STANDARDS.md
grep -i "technical debt" .oodatcaa/QUALITY_STANDARDS.md
grep -i "coverage" .oodatcaa/QUALITY_STANDARDS.md
grep -i "CI/CD" .oodatcaa/QUALITY_STANDARDS.md
```

---

### AC11: CI/CD Readiness Assessed ✅
**Requirement:** CI/CD readiness assessment complete with roadmap

**Test Procedure:**
1. Verify `.oodatcaa/work/cicd_readiness.md` exists
2. Check for required sections:
   - CI/CD requirements identified
   - Current tooling assessment
   - Gaps identified
   - Roadmap created (Sprint 3-5)
3. Verify readiness decision: ready / needs work / not ready
4. Verify actionable recommendations

**Pass Criteria:**
- CI/CD readiness document: `.oodatcaa/work/cicd_readiness.md` exists
- Requirements: What runs on PR, merge, main, nightly
- Assessment: Current tooling (Makefile, scripts) evaluated
- Gaps: Identified with priority
- Roadmap: Sprint 3-5 plan for CI/CD implementation
- Readiness decision: Clear and justified

**Verification:**
```bash
# Verify document exists
ls -lh .oodatcaa/work/cicd_readiness.md
# Check for key sections
grep -i "readiness" .oodatcaa/work/cicd_readiness.md
grep -i "roadmap" .oodatcaa/work/cicd_readiness.md
grep -i "sprint 3" .oodatcaa/work/cicd_readiness.md
grep -i "gaps" .oodatcaa/work/cicd_readiness.md
```

---

### AC12: Sprint 2 Certified Production-Ready ✅
**Requirement:** Sprint 2 quality certification complete with decision

**Test Procedure:**
1. Verify `.oodatcaa/work/sprint2_quality_certification.md` exists
2. Check for required sections:
   - Executive summary
   - Quality gates status (8/8)
   - Regression test results
   - Integration test results (P001, P002, P003)
   - Performance results
   - Coverage results
   - Technical debt summary
   - Certification decision: APPROVED / CONDITIONAL / REJECTED
3. Verify known issues documented
4. Verify recommendations for Sprint 3

**Pass Criteria:**
- Certification document: `.oodatcaa/work/sprint2_quality_certification.md` exists
- All sections complete with actual results
- Certification decision: **APPROVED** (Sprint 2 production-ready)
- Known issues: 29 ruff, ~400 mypy, 3 skipped tests (all documented and accepted)
- Recommendations: High/medium/low priority for Sprint 3+
- Executive summary: 3-sentence summary of Sprint 2 quality status

**Verification:**
```bash
# Verify document exists
ls -lh .oodatcaa/work/sprint2_quality_certification.md
# Check for certification decision
grep -i "APPROVED\|CONDITIONAL\|REJECTED" .oodatcaa/work/sprint2_quality_certification.md
grep -i "production-ready" .oodatcaa/work/sprint2_quality_certification.md
grep -i "executive summary" .oodatcaa/work/sprint2_quality_certification.md
```

---

## Manual Testing Procedures

### Test 1: Quality Gates Smoke Test
**Goal:** Quick verification all quality gates can run

**Procedure:**
1. Run each gate manually in sequence
2. Verify no "command not found" errors
3. Verify output is parseable
4. Verify exit codes are meaningful

**Expected Result:** All 8 gates execute successfully (even if some fail, they should run)

---

### Test 2: Integration Test - Real Daemon Scenario
**Goal:** Validate daemon system under realistic conditions

**Procedure:**
1. Create test SPRINT_QUEUE.json with simple task
2. Run daemon in background for 1 minute
3. Monitor daemon logs
4. Verify lease acquisition
5. Stop daemon gracefully
6. Verify clean shutdown

**Expected Result:** Daemon runs successfully, acquires lease, logs activity, shuts down cleanly

---

### Test 3: Integration Test - Log Rotation Trigger
**Goal:** Validate log rotation with large logs

**Procedure:**
1. Check current AGENT_LOG.md size
2. If > 1000 lines, run rotation: `bash scripts/rotate-logs.sh`
3. Verify archival to `.oodatcaa/work/archive/sprint_2/`
4. Verify active log reduced size
5. Verify data integrity (no lost entries)

**Expected Result:** Rotation successful, archives created, active log smaller, zero data loss

---

### Test 4: Integration Test - Sprint Management Lifecycle
**Goal:** Validate complete sprint lifecycle

**Procedure:**
1. Run `make sprint-status` - verify current Sprint 2 status
2. Check SPRINT_STATUS.json - verify valid JSON
3. Review `bash scripts/sprint-complete.sh --help` - verify usage
4. Review `bash scripts/sprint-new.sh --help` - verify usage
5. Verify atomic operations documented

**Expected Result:** All sprint management tools functional, lifecycle documented

---

### Test 5: Baseline Comparison Analysis
**Goal:** Verify Sprint 2 vs Sprint 1 comparison is accurate

**Procedure:**
1. Review Sprint 1 baseline document
2. Review Sprint 2 results document
3. Manually verify key metrics:
   - Ruff: Sprint 1 = 29, Sprint 2 = ?
   - Mypy: Sprint 1 = ~400, Sprint 2 = ?
   - Tests: Sprint 1 = 13 passed/3 skipped, Sprint 2 = ?
4. Verify delta calculations correct
5. Verify regression analysis accurate

**Expected Result:** Baseline comparison accurate, deltas correct, regression analysis valid

---

## Acceptance Test Additions

**New Test Files:** None (validation task, no new code)

**Updated Test Files:** None (no code changes)

**Test Infrastructure:** None (no infrastructure changes)

**Note:** This task executes existing tests and creates validation reports, but does not add new tests or change test infrastructure.

---

## Performance/Benchmark Setup

**Benchmarks to Validate:**
1. **Test Suite:** < 30 seconds (Sprint 1 baseline: ~18-20s)
2. **Build:** < 10 seconds
3. **Sprint Tools:** < 5 seconds (P003 achieved 0.199s)
4. **Log Rotation:** < 2 seconds
5. **Quality Gates:** < 60 seconds

**Measurement Method:**
```bash
time <command> > /dev/null 2>&1
```

**Reporting:** Document all timing results in `.oodatcaa/work/performance_validation.md`

---

## Manual Validation Checklist

Before marking P007 complete, manually verify:

- [ ] **AC1:** All 8 quality gates executed, logs captured
- [ ] **AC2:** Full test suite passes (≥ 13 passed, 3 skipped, 0 failed)
- [ ] **AC3:** P001 daemon integration validated (10 unit tests + manual scenarios)
- [ ] **AC4:** P002 log rotation validated (scripts functional, archives exist)
- [ ] **AC5:** P003 sprint management validated (dashboard + status JSON + scripts)
- [ ] **AC6:** Cross-system integration validated (P001 + P002 + P003)
- [ ] **AC7:** Performance benchmarks met (all < targets)
- [ ] **AC8:** Coverage ≥ 85% overall and new code
- [ ] **AC9:** Sprint 1 vs Sprint 2 baseline comparison complete
- [ ] **AC10:** Quality standards documented (`.oodatcaa/QUALITY_STANDARDS.md`)
- [ ] **AC11:** CI/CD readiness assessed (roadmap for Sprint 3-5)
- [ ] **AC12:** Sprint 2 certified **APPROVED** (production-ready)

**Tester Sign-Off:** _______________  
**Date:** _______________

---

## Notes

- **No Code Changes:** This is validation-only, no functional changes
- **Accept Technical Debt:** 29 ruff and ~400 mypy errors are acceptable if not regressed
- **Integration Critical:** P001, P002, P003 are new systems, need thorough validation
- **Baseline Comparison:** Essential for detecting regressions
- **Certification Goal:** APPROVED certification enables Sprint 3
- **Sprint 2 Completion:** P007 is final task before Sprint 2 complete

---

**Test Plan Status:** ✅ Complete  
**Ready for:** Builder (P007-B01)  
**Total Acceptance Criteria:** 12
