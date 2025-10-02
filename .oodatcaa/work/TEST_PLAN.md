# W007: Configuration & Environment Setup — TEST PLAN

**Task ID:** W007  
**Test Plan Version:** 1.0  
**Created:** 2025-10-03T15:50:00+00:00  
**Tester:** TBD (W007-T01)  

---

## Test Objectives

Verify that W007 Configuration & Environment Setup delivers a complete, functional setup experience for developers starting with the MCPLocalLLM project for training use case.

**Primary Goal:** Ensure fresh environment setup is successful and well-documented  
**Secondary Goal:** Verify zero regressions in existing MCP functionality  
**Quality Goal:** All configuration files valid and properly documented  

---

## Test Commands

### Format Check
```bash
black --check .
```
**Expected:** All files formatted correctly OR minimal formatting changes

### Lint Check
```bash
ruff check .
```
**Expected:** Pass OR ≤28 errors (W005 baseline)

### Type Check
```bash
mypy .
```
**Expected:** Pass OR ≤401 errors (W005 baseline)

### Unit Tests
```bash
pytest -q
```
**Expected:** All tests pass (smoke + integration)

### Integration Tests
```bash
pytest -q tests/mcp/
```
**Expected:** 10 passed, 3 skipped (W006 baseline maintained)

### Build Test
```bash
python -m build
```
**Expected:** Successfully built mdnotes-0.1.0 (wheel + sdist)

### Security Audit
```bash
pip-audit
```
**Expected:** No high-severity vulnerabilities

### Environment Validation
```bash
make validate-env
```
**Expected:** All checks pass OR clear actionable error messages

### Setup Script Test
```bash
./scripts/setup-dev.sh
```
**Expected:** Setup completes successfully, creates venv, dirs, .env

---

## Acceptance Criteria Testing

### AC1: `.env.example` File Created
**Test Steps:**
1. Verify file exists: `ls -la .env.example`
2. Check file contents: `cat .env.example`
3. Verify all config.py env vars present:
   - QDRANT_HOST, QDRANT_PORT, QDRANT_API_KEY
   - EMBEDDING_MODEL, EMBEDDING_DIMENSION
   - CHUNK_SIZE, CHUNK_OVERLAP
   - SIMILARITY_THRESHOLD, MAX_RESULTS
   - DEFAULT_AGENT_ID, LOG_LEVEL
   - POLICY_DIRECTORY
4. Verify inline comments present for each variable
5. Verify example values (not real secrets)
6. Verify header comment explains purpose

**Pass Criteria:**
- ✅ File exists at project root
- ✅ All 11+ environment variables present
- ✅ Each variable has inline comment
- ✅ Example values appropriate (no secrets)
- ✅ Header comment clear

---

### AC2: Docker Configuration Validated
**Test Steps:**
1. Review docker-compose.yml: `cat docker-compose.yml`
2. Verify Qdrant service:
   - Image: `qdrant/qdrant:latest`
   - Ports: 6333, 6334
   - Volume: `qdrant_data:/qdrant/storage`
   - Health check present
3. Verify comments for training mode present
4. Test docker-compose syntax: `docker-compose config`

**Pass Criteria:**
- ✅ Qdrant service configured correctly
- ✅ Volume mounts include ./data, ./logs, ./policy
- ✅ Health checks working
- ✅ Container names appropriate
- ✅ Comments explain training mode
- ✅ `docker-compose config` passes

---

### AC3: Config Files Adapted for Training
**Test Steps:**
1. Review config.example.yaml: `cat config.example.yaml`
2. Verify training-specific settings:
   - `server.name: "mcp-local-llm-training"` OR similar
   - `qdrant.mode: "local"`
   - `embedding.device: "cpu"`
   - `markdown.chunk_size: 1000`
   - `logging.level: "INFO"`
3. Verify comments explain training choices
4. Validate YAML syntax: `python -c "import yaml; yaml.safe_load(open('config.example.yaml'))"`

**Pass Criteria:**
- ✅ Training-specific defaults present
- ✅ CPU inference configured
- ✅ Local Qdrant mode
- ✅ Comments explain choices
- ✅ YAML syntax valid

---

### AC4: Setup Script Functional
**Test Steps:**
1. Verify script exists and executable: `ls -la scripts/setup-dev.sh`
2. Review script contents: `cat scripts/setup-dev.sh`
3. Test script (dry-run or fresh clone):
   ```bash
   ./scripts/setup-dev.sh
   ```
4. Verify script actions:
   - Creates venv directory
   - Installs dependencies
   - Creates data/, logs/ directories
   - Copies .env.example → .env (if not exists)
   - Checks Docker availability
5. Verify clear output and next steps provided

**Pass Criteria:**
- ✅ Script exists and executable (`chmod +x`)
- ✅ Script completes successfully
- ✅ Venv created and dependencies installed
- ✅ Directories created (data/, logs/)
- ✅ .env copied if missing
- ✅ Clear success message and next steps

---

### AC5: Environment Validation Tool
**Test Steps:**
1. Verify Makefile target: `grep validate-env Makefile`
2. Verify script exists: `ls -la scripts/validate-env.py`
3. Run validation: `make validate-env` OR `python scripts/validate-env.py`
4. Verify checks performed:
   - Python version (3.11-3.12)
   - .env file exists
   - Required directories exist (data/, logs/, policy/)
   - Docker available (optional warning)
   - Dependencies installed (optional)
5. Verify clear success/failure output

**Pass Criteria:**
- ✅ Makefile has `validate-env` target
- ✅ Script exists and executable
- ✅ Validation checks 5+ prerequisites
- ✅ Clear success message if all pass
- ✅ Actionable error messages if fail

---

### AC6: All Tests Pass (CRITICAL)
**Test Steps:**
1. Run smoke tests: `pytest tests/test_smoke.py -v`
2. Run integration tests: `pytest tests/mcp/ -v`
3. Run full test suite: `pytest -v`
4. Verify W006 baseline maintained:
   - 13 passed, 3 skipped
   - Performance < 30s

**Pass Criteria:**
- ✅ Smoke tests: 2/2 passing
- ✅ Integration tests: 10 passed, 3 skipped
- ✅ Full suite: 13 passed, 3 skipped
- ✅ Zero test failures
- ✅ Zero test regressions
- ✅ Performance maintained

**CRITICAL:** If any test fails, W007 MUST be marked needs_adapt

---

### AC7: Quality Gates Pass
**Test Steps:**
1. Run black: `black --check .`
2. Run ruff: `ruff check .`
3. Run mypy: `mypy .`
4. Run build: `python -m build`
5. Run security: `pip-audit`

**Pass Criteria:**
- ✅ Black: Pass OR minimal changes
- ✅ Ruff: Pass OR ≤28 errors (W005 baseline)
- ✅ Mypy: Pass OR ≤401 errors (W005 baseline)
- ✅ Build: Success (wheel + sdist)
- ✅ Security: No high-severity issues

**Note:** Negotiation allowed if ruff/mypy within W005 baseline

---

### AC8: Documentation Updated (CRITICAL)
**Test Steps:**
1. Review README.md: Search for "Setup" section
2. Verify prerequisites listed (Python 3.11+, Docker optional)
3. Verify step-by-step instructions (5-10 steps)
4. Verify configuration section explains .env and config.yaml
5. Verify troubleshooting section with common issues
6. Verify instructions are clear and actionable

**Pass Criteria:**
- ✅ README has "Setup & Installation" section
- ✅ Prerequisites clearly listed
- ✅ Step-by-step instructions (1-5 steps minimum)
- ✅ Configuration section present
- ✅ Troubleshooting section with 2+ common issues
- ✅ Instructions clear and actionable

---

### AC9: No Secrets Committed
**Test Steps:**
1. Verify .gitignore includes .env: `grep "^\.env$" .gitignore`
2. Check .env.example for secrets:
   ```bash
   rg -i "api[_-]?key.*[a-zA-Z0-9]{32,}" .env.example
   rg -i "password.*[a-zA-Z0-9]{8,}" .env.example
   ```
3. Check config.example.yaml for secrets:
   ```bash
   rg -i "api[_-]?key.*[a-zA-Z0-9]{32,}" config.example.yaml
   ```
4. Review docker-compose.yml for hardcoded secrets

**Pass Criteria:**
- ✅ .gitignore includes `.env` pattern
- ✅ No real API keys in .env.example
- ✅ No real secrets in config.example.yaml
- ✅ No hardcoded secrets in docker-compose.yml
- ✅ Security audit clean

---

### AC10: Clean Repository State
**Test Steps:**
1. Check git status: `git status`
2. Verify no temporary files: `find . -name "*.tmp" -o -name "*.bak"`
3. Verify no pycache committed: `git status | grep __pycache__`
4. Verify intended files only:
   - .env.example
   - config.example.yaml (modified)
   - docker-compose.yml (modified)
   - scripts/setup-dev.sh
   - scripts/validate-env.py
   - Makefile (modified)
   - README.md (modified)

**Pass Criteria:**
- ✅ Only intended files staged/committed
- ✅ No temporary files in git
- ✅ No __pycache__ committed
- ✅ All configuration files properly formatted
- ✅ Git status clean after commit

---

## Test Execution Summary Template

```
W007 Test Results
=================

Tester: [Name]
Date: [ISO 8601]
Duration: [X minutes]

Acceptance Criteria:
- AC1 (.env.example):        ✅ PASS / ❌ FAIL
- AC2 (Docker config):       ✅ PASS / ❌ FAIL
- AC3 (Config adapted):      ✅ PASS / ❌ FAIL
- AC4 (Setup script):        ✅ PASS / ❌ FAIL
- AC5 (Validation tool):     ✅ PASS / ❌ FAIL
- AC6 (All tests):           ✅ PASS / ❌ FAIL (CRITICAL)
- AC7 (Quality gates):       ✅ PASS / ❌ FAIL
- AC8 (Documentation):       ✅ PASS / ❌ FAIL (CRITICAL)
- AC9 (No secrets):          ✅ PASS / ❌ FAIL
- AC10 (Clean repo):         ✅ PASS / ❌ FAIL

Quality Gates:
- Black:     ✅ PASS / ❌ FAIL
- Ruff:      ✅ PASS / ⚠️ [X] errors (baseline ≤28)
- Mypy:      ✅ PASS / ⚠️ [X] errors (baseline ≤401)
- Pytest:    ✅ [X/Y] PASS / ❌ FAIL
- Build:     ✅ PASS / ❌ FAIL
- Security:  ✅ PASS / ❌ FAIL

Overall Result: ✅ PASS (X/10 ACs) / ❌ FAIL (needs_adapt)

Notes:
[Any issues, warnings, or observations]

Recommendation:
[ready_for_integrator / needs_adapt / Start-Over Gate]
```

---

## Rollback Triggers

**W007 MUST be marked needs_adapt if:**
1. ❌ AC6 fails — Any test regression detected
2. ❌ AC8 fails — Documentation insufficient/unclear
3. ❌ AC4 fails — Setup script doesn't work
4. ❌ ≥3 critical ACs fail — Fundamental issues

**Start-Over Gate (highly unlikely for W007):**
- Configuration completely breaks existing functionality
- Fundamental architectural issue discovered
- After 2 Adapt loops, ACs still unmet

---

## Test Environment

**Prerequisites:**
- Fresh clone of repository (or reset to W007 branch)
- Python 3.11 or 3.12 installed
- Docker Desktop available (optional)
- No existing .env file
- No existing venv directory

**Test Execution:**
1. Clone repository
2. Checkout W007 branch
3. Run setup script: `./scripts/setup-dev.sh`
4. Run validation: `make validate-env`
5. Execute all test commands
6. Verify all 10 ACs
7. Document results

---

## Success Criteria

W007 is approved for integration when:
- ✅ **All 10 acceptance criteria PASS**
- ✅ **All W006 integration tests pass** (zero regressions)
- ✅ **Fresh setup successful** (validated in clean environment)
- ✅ **Quality gates pass** (or within W005 baseline)
- ✅ **Documentation clear and actionable**

---

**Test Plan Status:** COMPLETE  
**Ready for:** Tester (W007-T01) after Builder completes W007-B01 + W007-B02  
**Estimated Test Duration:** 15-20 minutes
