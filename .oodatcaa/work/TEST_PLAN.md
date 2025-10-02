# Test Plan — W003: Integrate MCP Dependencies

**Work Item:** W003 | **Sprint:** 1 | **Created:** 2025-10-02

---

## Test Commands

### Format Check
```bash
black --check .
```
**Expected:** PASS (no formatting issues in pyproject.toml or existing code)

---

### Lint Check
```bash
ruff check .
```
**Expected:** Warnings/errors in MCP code are OK (defer to W004)  
**Expected:** No new errors in mdnotes code

---

### Type Check (mdnotes only)
```bash
mypy src/mdnotes
```
**Expected:** PASS (existing mdnotes code type checks)  
**Note:** MCP type errors expected until W004 (code adaptation)

---

### Unit Tests (Existing Only)
```bash
pytest -q tests/test_smoke.py
```
**Expected:** PASS (2/2 tests)  
**CRITICAL:** This is a rollback trigger if it fails

---

### Acceptance Tests (Existing Only)
```bash
pytest -q tests/acceptance
```
**Expected:** PASS (existing tests unaffected by dependency installation)

---

### Coverage Check (mdnotes only)
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
**Expected:** PASS (wheel and sdist created)  
**Note:** Should include MCP modules in package

---

### Security Audit
```bash
pip-audit
```
**Expected:** No high-severity vulnerabilities  
**Note:** May have informational warnings about large dependency tree

---

### Dependency Installation Test
```bash
pip install -e .[dev]
```
**Expected:** Completes successfully, ~2.1GB installed  
**Time:** 5-15 minutes depending on network and CPU

---

## Acceptance Testing

### AC1: pyproject.toml Updated with MCP Production Dependencies
**Test:**
```bash
python -c "
import tomllib
config = tomllib.load(open('pyproject.toml', 'rb'))
deps = config['project']['dependencies']
required = ['mcp>=1.13.1,<2.0.0', 'qdrant-client>=1.7.0,<2.0.0', 
            'sentence-transformers>=2.5.1,<3.0.0', 'numpy>=1.26.0,<2.0.0',
            'markdown>=3.5.0,<4.0.0', 'beautifulsoup4>=4.12.0,<5.0.0',
            'python-dotenv>=1.0.0,<2.0.0', 'pyyaml>=6.0.0,<7.0.0',
            'aiofiles>=24.1.0,<25.0.0', 'aiohttp>=3.9.1,<4.0.0']
missing = [r for r in required if r not in deps]
print(f'Missing: {missing}' if missing else '✅ All 10 MCP deps present')
"
```
**Pass Criteria:** Output shows "✅ All 10 MCP deps present"

---

### AC2: pyproject.toml Updated with MCP Dev Dependencies
**Test:**
```bash
python -c "
import tomllib
config = tomllib.load(open('pyproject.toml', 'rb'))
dev_deps = config['project']['optional-dependencies']['dev']
required = ['pytest-asyncio>=1.1.0,<2.0.0', 'types-markdown>=3.5.0,<4.0.0']
missing = [r for r in required if r not in dev_deps]
print(f'Missing: {missing}' if missing else '✅ Both MCP dev deps present')
"
```
**Pass Criteria:** Output shows "✅ Both MCP dev deps present"

---

### AC3: Python Version Constraint Updated
**Test:**
```bash
python -c "
import tomllib
config = tomllib.load(open('pyproject.toml', 'rb'))
python_req = config['project']['requires-python']
print(f'Python constraint: {python_req}')
assert python_req == '>=3.11,<3.13', 'Wrong Python constraint'
print('✅ Python version constraint correct')
"
```
**Pass Criteria:** Output shows "✅ Python version constraint correct"

---

### AC4: All Dependencies Install Successfully
**Test:**
```bash
pip install -e .[dev] 2>&1 | tee install.log
echo "Exit code: $?"
```
**Pass Criteria:** Exit code 0, no error messages in install.log

---

### AC5: MCP Imports Work (CRITICAL)
**Test:**
```bash
# Test core MCP imports
python -c "import mcp; print('✅ mcp imported successfully')"
python -c "import qdrant_client; print('✅ qdrant_client imported successfully')"
python -c "import sentence_transformers; print('✅ sentence_transformers imported successfully')"

# Test supporting imports
python -c "import numpy; print('✅ numpy imported')"
python -c "import markdown; print('✅ markdown imported')"
python -c "import bs4; print('✅ beautifulsoup4 imported')"
python -c "import dotenv; print('✅ python-dotenv imported')"
python -c "import yaml; print('✅ pyyaml imported')"
python -c "import aiofiles; print('✅ aiofiles imported')"
python -c "import aiohttp; print('✅ aiohttp imported')"
```
**Pass Criteria:** All 10 imports succeed  
**ROLLBACK TRIGGER:** Any critical import fails (mcp, qdrant_client, sentence_transformers)

---

### AC6: Existing mdnotes Imports Still Work (CRITICAL)
**Test:**
```bash
python -c "from mdnotes import core; print('✅ mdnotes.core imported')"
python -c "import click, rich, whoosh; print('✅ mdnotes dependencies work')"
```
**Pass Criteria:** All imports succeed  
**ROLLBACK TRIGGER:** Any existing import fails

---

### AC7: Existing Tests Still Pass (CRITICAL)
**Test:**
```bash
pytest -q tests/test_smoke.py
```
**Pass Criteria:** 2/2 tests pass  
**ROLLBACK TRIGGER:** Any test failures

---

### AC8: Tool Configurations Updated
**Test:**
```bash
# Check mypy packages
python -c "
import tomllib
config = tomllib.load(open('pyproject.toml', 'rb'))
packages = config['tool']['mypy']['packages']
print(f'Mypy packages: {packages}')
assert 'mcp' in packages, 'mcp not in mypy packages'
print('✅ mypy configured for MCP')
"

# Check pytest asyncio mode
python -c "
import tomllib
config = tomllib.load(open('pyproject.toml', 'rb'))
mode = config['tool']['pytest']['ini_options'].get('asyncio_mode')
print(f'Asyncio mode: {mode}')
assert mode == 'auto', 'asyncio_mode not set to auto'
print('✅ pytest configured for async tests')
"

# Check ruff known-first-party
python -c "
import tomllib
config = tomllib.load(open('pyproject.toml', 'rb'))
known_first_party = config['tool']['ruff']['lint']['isort']['known-first-party']
print(f'Known first-party: {known_first_party}')
assert 'mcp' in known_first_party, 'mcp not in known-first-party'
print('✅ ruff configured for MCP')
"
```
**Pass Criteria:** All 3 checks pass

---

### AC9: pip-audit Clean
**Test:**
```bash
pip-audit 2>&1 | tee audit.log
# Count high/critical severity issues
grep -i "CRITICAL\|HIGH" audit.log || echo "✅ No high-severity issues"
```
**Pass Criteria:** No HIGH or CRITICAL severity vulnerabilities  
**Note:** Informational/LOW/MEDIUM may be acceptable

---

### AC10: Build Succeeds
**Test:**
```bash
python -m build
ls -lh dist/
```
**Pass Criteria:** 
- Build completes without errors
- dist/ contains wheel (.whl) and sdist (.tar.gz)

---

## Critical Verification Checks

### Verification 1: TOML Syntax Valid
**Test:**
```bash
python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb')); print('✅ TOML syntax valid')"
```
**Expected:** No syntax errors

---

### Verification 2: Dependency Version Constraints
**Test:**
```bash
python -c "
import tomllib
config = tomllib.load(open('pyproject.toml', 'rb'))
deps = config['project']['dependencies']
# Check all MCP deps have upper bounds
mcp_deps = [d for d in deps if any(pkg in d for pkg in ['mcp', 'qdrant', 'sentence-transformers', 'numpy', 'markdown', 'beautifulsoup4', 'dotenv', 'pyyaml', 'aiofiles', 'aiohttp'])]
for dep in mcp_deps:
    assert '<' in dep, f'{dep} missing upper bound'
print('✅ All MCP deps have version upper bounds')
"
```
**Expected:** All MCP dependencies have version constraints

---

### Verification 3: Installation Size
**Test:**
```bash
du -sh .venv/lib/python3.*/site-packages/ | awk '{print "Installed size: "$1}'
```
**Expected:** ~2-3GB (sentence-transformers + PyTorch are large)

---

## Performance Tests

**Not applicable for W003** (dependency installation task, no code performance impact)

---

## Integration Tests to Add

**Not applicable for W003** (MCP code integration tests deferred to W006)

---

## Test Execution Order

### Phase 1: Pre-Test Validation
1. Verify branch checked out: `feat/W003-step-01-integrate-dependencies`
2. Verify baseline tag exists: `git tag | grep pre/W003`

### Phase 2: TOML Validation
3. **AC3:** Python version constraint updated
4. **AC1:** 10 MCP production deps present
5. **AC2:** 2 MCP dev deps present
6. **AC8:** Tool configurations updated
7. **Verification 1:** TOML syntax valid

### Phase 3: Dependency Installation (CRITICAL)
8. **AC4:** `pip install -e .[dev]` succeeds → ROLLBACK if fails

### Phase 4: Import Verification (CRITICAL)
9. **AC5:** MCP imports work → ROLLBACK if critical imports fail
10. **AC6:** mdnotes imports work → ROLLBACK if fails

### Phase 5: Quality & Security Checks
11. **AC7:** Existing tests pass → ROLLBACK if fails
12. **AC9:** pip-audit clean (no high-severity)
13. **AC10:** Build succeeds

### Phase 6: Tool Configuration Validation
14. **AC8:** mypy, pytest, ruff configs work

---

## Rollback Procedure

**Trigger Conditions:**
1. AC4 fails (dependency installation fails)
2. AC5 fails (critical MCP imports fail: mcp, qdrant_client, sentence_transformers)
3. AC6 fails (existing mdnotes imports fail)
4. AC7 fails (existing tests fail)
5. AC9 fails (high-severity security vulnerabilities found)

**Rollback Steps:**
```bash
cd /media/hannesn/storage/Code/MCPLocalLLM

# Restore pyproject.toml
git checkout HEAD -- pyproject.toml

# Uninstall MCP dependencies
pip uninstall -y mcp qdrant-client sentence-transformers numpy markdown \
  beautifulsoup4 python-dotenv pyyaml aiofiles aiohttp pytest-asyncio types-markdown

# Clean up any partial installations
pip cache purge

# Reinstall original environment
pip install -e .[dev]

# Verify rollback
pytest -q tests/test_smoke.py

# Document failure
echo "W003 aborted: <reason>" >> .oodatcaa/work/SPRINT_DISCUSS.md
```

---

## Exit Criteria

- [ ] All 10 acceptance criteria (AC1-AC10) verified and documented
- [ ] All 3 critical import checks pass (AC5: MCP, AC6: mdnotes, AC7: tests)
- [ ] TOML syntax valid
- [ ] Dependencies install without errors (~2.1GB)
- [ ] No high-severity security vulnerabilities
- [ ] Tool configurations work (mypy, pytest, ruff)
- [ ] Build succeeds (wheel + sdist)
- [ ] Branch pushed to origin
- [ ] Ready for W004 (Adapt MCP for Training Use Case)

---

## Test Artifacts

**Pre-Integration:**
- Baseline tag: `pre/W003-<timestamp>`
- Current pyproject.toml backup

**Post-Integration:**
- Updated pyproject.toml
- Installation log (install.log)
- pip-audit report (audit.log)
- Import verification output
- Build artifacts (dist/*.whl, dist/*.tar.gz)

---

## Success Metrics

**Functional Success:**
- 10 MCP production dependencies installed
- 2 MCP dev dependencies installed
- All imports work (12 total: 10 MCP + 2 mdnotes checks)
- Zero test regressions

**Quality Success:**
- TOML syntax valid
- No high-severity security issues
- Build succeeds
- Tool configurations functional

**Risk Mitigation Success:**
- All rollback triggers monitored
- Critical imports verified
- Existing functionality preserved

---

**Test Plan Status:** ✅ APPROVED  
**Ready for:** Builder Execution → Tester Validation
