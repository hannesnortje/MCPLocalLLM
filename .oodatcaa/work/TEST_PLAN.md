# Test Plan — T001: Training Framework Research & Selection

**Test Plan Version:** 1.0  
**Created:** 2025-10-06T07:57:00+02:00  
**Task:** T001 - Training Framework Research & Selection  
**Planner:** agent-planner-A  
**Status:** Ready for Testing

---

## Test Overview

**Objective:** Validate that the training framework (MLX-LM) is correctly selected, installed, and functional for fine-tuning Qwen2.5-Coder-7B-Instruct with QLoRA on M1 Max.

**Scope:** Framework evaluation, installation verification, model loading, inference testing, memory profiling

**Out of Scope:** Actual training (T002), dataset creation (T003-T004), production deployment

---

## Quality Gates (Must Pass)

All standard project quality gates must pass before T001 can be marked complete:

### Gate 1: Code Formatting ✅
```bash
black --check .
```
**Expected:** No formatting issues  
**Reason:** Documentation and scripts must follow project style

---

### Gate 2: Linting ✅
```bash
ruff check .
```
**Expected:** 0 new ruff errors (baseline: 28 errors acceptable from Sprint 3)  
**Reason:** No regressions in code quality

---

### Gate 3: Type Checking ✅
```bash
mypy .
```
**Expected:** 0 new mypy errors (baseline: ~401 errors acceptable from Sprint 3)  
**Reason:** Type safety maintained, no new type issues in training scripts

---

### Gate 4: Unit Tests ✅
```bash
pytest -q
```
**Expected:** All existing tests pass (≥10 passed, 3 skipped expected)  
**Reason:** No regressions in existing MCP functionality

---

### Gate 5: Integration Tests ✅
```bash
pytest -q tests/acceptance
```
**Expected:** All integration tests pass or skip gracefully  
**Reason:** MCP integration still functional after framework installation

---

### Gate 6: Coverage ✅
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=85
```
**Expected:** ≥85% line coverage maintained  
**Reason:** Coverage does not regress (new training scripts may be below 85%, acceptable for Sprint 4)

---

### Gate 7: Build ✅
```bash
python -m build
```
**Expected:** Package builds successfully  
**Reason:** Installation still works after dependency changes

---

### Gate 8: Security Audit ✅
```bash
pip-audit
```
**Expected:** 0 high-severity vulnerabilities  
**Reason:** New MLX-LM dependencies must not introduce security issues

---

## Acceptance Criteria Tests

### AC1: Framework Evaluation Complete ✅

**Test:** Verify framework evaluation report exists and is comprehensive

**Commands:**
```bash
# Check evaluation report exists
test -f docs/training/T001_framework_evaluation.md && echo "PASS: Evaluation report exists" || echo "FAIL: Evaluation report missing"

# Check for MLX-LM section
grep -q "MLX-LM" docs/training/T001_framework_evaluation.md && echo "PASS: MLX-LM evaluated" || echo "FAIL: MLX-LM section missing"

# Check for axolotl section
grep -q "axolotl" docs/training/T001_framework_evaluation.md && echo "PASS: axolotl evaluated" || echo "FAIL: axolotl section missing"

# Check for comparison matrix
grep -q "comparison\|matrix\|pros\|cons" docs/training/T001_framework_evaluation.md && echo "PASS: Comparison matrix exists" || echo "FAIL: No comparison matrix"

# Check for decision rationale (minimum 3 factors)
grep -i -c "decision\|rationale\|selected\|chosen" docs/training/T001_framework_evaluation.md
# Expected: Count >= 3
```

**Validation Criteria:**
- [ ] `docs/training/T001_framework_evaluation.md` exists
- [ ] MLX-LM section present with pros/cons
- [ ] axolotl section present with pros/cons
- [ ] Comparison matrix with 5 criteria (memory, speed, ease, QLoRA, M1 Max)
- [ ] Framework selected (MLX-LM) with explicit rationale
- [ ] Minimum 3 decision factors documented

**Expected Result:** PASS (all 6 checks pass)

---

### AC2: Framework Selected with Rationale ✅

**Test:** Verify framework selection is explicit and well-justified

**Commands:**
```bash
# Check for explicit selection statement
grep -E "selected|chosen|recommend" docs/training/T001_framework_evaluation.md | grep -i "mlx"
# Expected: Found line like "MLX-LM is selected/recommended"

# Check for rationale section
grep -A 20 -i "rationale\|decision" docs/training/T001_framework_evaluation.md

# Verify 3+ decision factors
grep -E "M1 Max|memory|ease|optimization|Metal" docs/training/T001_framework_evaluation.md | wc -l
# Expected: >= 3 matches

# Check for trade-offs acknowledgment
grep -i "trade-off\|downside\|limitation\|cons\|disadvantage" docs/training/T001_framework_evaluation.md | wc -l
# Expected: >= 2 matches

# Check for fallback plan
grep -i "fallback\|alternative\|backup" docs/training/T001_framework_evaluation.md
# Expected: Fallback plan documented
```

**Validation Criteria:**
- [ ] MLX-LM explicitly selected (clear statement)
- [ ] Rationale section with 3+ decision factors:
  - M1 Max optimization / Metal acceleration
  - Memory efficiency / unified memory
  - Ease of use / setup simplicity
- [ ] Trade-offs acknowledged (smaller ecosystem, M1-only, newer framework)
- [ ] Fallback plan documented (switch to axolotl if needed)

**Expected Result:** PASS (all checks pass)

---

### AC3: Proof-of-Concept Installation Successful ✅

**Test:** Verify MLX-LM framework is installed and functional

**Commands:**
```bash
# Check MLX-LM installation
pip list | grep "mlx-lm"
# Expected: mlx-lm X.Y.Z (version number present)

# Check MLX core installation
pip list | grep "^mlx "
# Expected: mlx X.Y.Z

# Check transformers installation
pip list | grep transformers
# Expected: transformers X.Y.Z

# Import test - MLX-LM
python3 -c "import mlx_lm; print('MLX-LM version:', mlx_lm.__version__)" 2>&1
# Expected: MLX-LM version: X.Y.Z (no errors)

# Import test - MLX core
python3 -c "import mlx; import mlx.core as mx; print('MLX version:', mlx.__version__); print('MLX core:', mx)" 2>&1
# Expected: MLX version: X.Y.Z, MLX core: <module> (no errors)

# Import test - transformers
python3 -c "import transformers; print('Transformers version:', transformers.__version__)" 2>&1
# Expected: Transformers version: X.Y.Z (no errors)

# Check for dependency conflicts
pip check
# Expected: No broken requirements found.

# Verify installation guide exists
test -f docs/training/FRAMEWORK_SETUP.md && echo "PASS: Installation guide exists" || echo "FAIL: Installation guide missing"
```

**Validation Criteria:**
- [ ] `mlx-lm` package installed (pip list shows version)
- [ ] `mlx` package installed
- [ ] `transformers` package installed
- [ ] All import tests pass (no ImportError)
- [ ] `pip check` passes (no dependency conflicts)
- [ ] No conflicts with existing MCP dependencies
- [ ] Installation guide documented

**Expected Result:** PASS (all 7 checks pass)

---

### AC4: Qwen2.5-Coder-7B-Instruct Model Loaded ✅

**Test:** Verify model can be downloaded and loaded successfully

**Commands:**
```bash
# Check if model loading script exists
test -f scripts/training/load_model_test.py && echo "PASS: Model load script exists" || echo "FAIL: Script missing"

# Run model loading test
python3 scripts/training/load_model_test.py 2>&1 | tee /tmp/model_load_output.txt
# Expected: Script completes without errors

# Verify model loading succeeded (check output)
grep -i "success\|loaded\|model" /tmp/model_load_output.txt | head -5

# Verify model architecture (7B parameters)
grep -E "7B|7 billion|7000M" /tmp/model_load_output.txt
# Expected: Found confirmation of 7B parameters

# Verify tokenizer working
grep -i "tokenizer" /tmp/model_load_output.txt
# Expected: Tokenizer loaded successfully

# Check model download (if script caches location)
ls -lh ~/.cache/huggingface/hub/ 2>/dev/null | grep -i qwen | head -3
# Expected: Qwen2.5-Coder-7B-Instruct directory present (~14GB)

# Verify model script is documented
grep -i "load_model_test" docs/training/*.md
# Expected: Script referenced in documentation
```

**Validation Criteria:**
- [ ] `scripts/training/load_model_test.py` exists
- [ ] Model loading script runs without errors
- [ ] Model architecture validated (7B parameters confirmed)
- [ ] Tokenizer working (can encode/decode)
- [ ] Model downloaded successfully (~14GB in HuggingFace cache)
- [ ] Script documented for reproducibility

**Expected Result:** PASS (all 6 checks pass)

**Troubleshooting:**
- If model download fails: Check internet connection, HuggingFace Hub status
- If memory error: Confirm M1 Max has ≥32GB RAM
- If import error: Verify MLX-LM installation (AC3)

---

### AC5: Basic Inference Test Passes ✅

**Test:** Verify model can generate coherent responses to test prompts

**Commands:**
```bash
# Check if inference test script exists
test -f scripts/training/inference_test.py && echo "PASS: Inference script exists" || echo "FAIL: Script missing"

# Run inference test
python3 scripts/training/inference_test.py 2>&1 | tee /tmp/inference_output.txt
# Expected: Script completes, generates response

# Verify inference succeeded
grep -i "response\|output\|generated" /tmp/inference_output.txt | head -5

# Check response length (minimum 20 tokens)
grep -i "tokens\|length" /tmp/inference_output.txt
# Expected: Response length >= 20 tokens

# Verify inference time measured
grep -i "time\|seconds\|duration" /tmp/inference_output.txt
# Expected: Inference time documented (e.g., "2.3 seconds")

# Check response coherence (not gibberish)
# Manual validation: Read output, confirm it's relevant to prompt
echo "=== Generated Response ==="
grep -A 10 "Response:" /tmp/inference_output.txt | head -15

# Verify test results documented
test -f docs/training/inference_test_results.md && echo "PASS: Inference results documented" || echo "FAIL: Results missing"

# Check for test prompt in documentation
grep -i "test prompt\|example" docs/training/inference_test_results.md | head -3
```

**Validation Criteria:**
- [ ] `scripts/training/inference_test.py` exists
- [ ] Inference test runs without errors
- [ ] Model generates response (minimum 20 tokens)
- [ ] Response is coherent (relevant to prompt, not gibberish)
- [ ] Inference time measured and documented
- [ ] Test prompt and output saved in `docs/training/inference_test_results.md`
- [ ] Script reproducible (can be re-run)

**Expected Result:** PASS (all 7 checks pass)

**Manual Validation Required:**
- Tester must read generated response and confirm it's coherent
- Response should be relevant to test prompt (e.g., Python function if prompt asks for Python code)

---

### AC6: Memory Usage Profiled and Documented ✅

**Test:** Verify memory usage is measured and within ≤16GB target

**Commands:**
```bash
# Check if memory profiling script exists
test -f scripts/training/memory_profile.py && echo "PASS: Memory profile script exists" || echo "FAIL: Script missing"

# Run memory profiling (may take 2-3 minutes)
python3 scripts/training/memory_profile.py 2>&1 | tee /tmp/memory_profile_output.txt
# Expected: Script completes with memory measurements

# Verify inference memory measured
grep -i "inference.*memory\|model.*memory" /tmp/memory_profile_output.txt
# Expected: Inference memory in GB (e.g., "Inference: 8.2GB")

# Verify training memory estimated
grep -i "training.*memory\|qlora.*memory" /tmp/memory_profile_output.txt
# Expected: Training memory estimate in GB (e.g., "Training (est): 14.5GB")

# Verify peak memory captured
grep -i "peak.*memory\|max.*memory" /tmp/memory_profile_output.txt
# Expected: Peak memory documented

# Check headroom calculation
grep -i "headroom\|remaining\|available" /tmp/memory_profile_output.txt
# Expected: Headroom from 16GB target calculated

# Verify memory profile documented
test -f docs/training/memory_profile.md && echo "PASS: Memory profile documented" || echo "FAIL: Profile missing"

# Check for numeric values in documentation
grep -E "[0-9]+\.?[0-9]* ?GB" docs/training/memory_profile.md | head -5
# Expected: Multiple memory measurements in GB

# Validate training memory <= 16GB target
python3 -c "
import re
with open('docs/training/memory_profile.md', 'r') as f:
    content = f.read()
    training_mem = re.findall(r'Training.*?([0-9]+\.?[0-9]*) ?GB', content, re.IGNORECASE)
    if training_mem:
        mem_gb = float(training_mem[0])
        if mem_gb <= 16.0:
            print(f'PASS: Training memory {mem_gb}GB <= 16GB target')
        else:
            print(f'FAIL: Training memory {mem_gb}GB > 16GB target')
    else:
        print('FAIL: No training memory measurement found')
"
```

**Validation Criteria:**
- [ ] `scripts/training/memory_profile.py` exists
- [ ] Memory profiling script runs without errors
- [ ] Inference memory measured (in GB)
- [ ] Training memory estimated (QLoRA with batch size 1)
- [ ] Peak memory usage captured (not just average)
- [ ] Headroom calculation documented (e.g., "1.5GB headroom from 16GB target")
- [ ] Training memory ≤16GB target validated
- [ ] Memory profile documented in `docs/training/memory_profile.md`

**Expected Result:** PASS (all 8 checks pass)

**Acceptable Range:**
- Inference memory: 6-10GB (model size ~7B parameters)
- Training memory: 12-16GB (QLoRA 4-bit quantization)
- Peak memory: ≤16GB (target constraint)

**CRITICAL:** If training memory >16GB, T001 fails and plan must be revised (smaller batch size, more aggressive quantization, or framework switch)

---

### AC7: Installation Guide Documented ✅

**Test:** Verify comprehensive installation guide exists and is complete

**Commands:**
```bash
# Check installation guide exists
test -f docs/training/FRAMEWORK_SETUP.md && echo "PASS: Installation guide exists" || echo "FAIL: Guide missing"

# Verify step-by-step instructions present
grep -i "step\|installation\|setup" docs/training/FRAMEWORK_SETUP.md | head -5

# Check for exact commands (copy-paste ready)
grep -E "pip install|python|git|mlx" docs/training/FRAMEWORK_SETUP.md | wc -l
# Expected: >= 5 command lines

# Verify dependencies listed
grep -i "dependencies\|requirements\|packages" docs/training/FRAMEWORK_SETUP.md
# Expected: Dependencies section exists

# Check for troubleshooting section
grep -A 5 -i "troubleshooting\|common issues\|problems" docs/training/FRAMEWORK_SETUP.md | head -10
# Expected: Troubleshooting section with minimum 3 issues

# Verify verification steps documented
grep -i "verify\|validation\|test" docs/training/FRAMEWORK_SETUP.md | head -5
# Expected: Verification steps present

# Check guide completeness (minimum sections)
for section in "Prerequisites" "Installation" "Verification" "Troubleshooting"; do
    grep -i "$section" docs/training/FRAMEWORK_SETUP.md && echo "PASS: $section section found" || echo "FAIL: $section section missing"
done

# Verify cross-references to T001 evaluation
grep -i "T001\|evaluation\|framework.*selection" docs/training/FRAMEWORK_SETUP.md
# Expected: Reference to T001 evaluation report
```

**Validation Criteria:**
- [ ] `docs/training/FRAMEWORK_SETUP.md` exists
- [ ] Step-by-step installation instructions (clear, numbered)
- [ ] Exact commands provided (copy-paste ready, minimum 5 commands)
- [ ] Dependencies listed with versions
- [ ] Troubleshooting section (minimum 3 common issues)
- [ ] Verification steps documented (how to confirm setup worked)
- [ ] Prerequisites section (Python 3.11+, M1 Max, venv)
- [ ] Cross-references to T001 evaluation and next steps (T002)

**Expected Result:** PASS (all 8 checks pass)

**Guide Quality Check:**
- Tester should attempt to follow installation guide on clean venv
- All commands should work without errors
- Verification steps should pass

---

### AC8: Dependencies Added to pyproject.toml ✅

**Test:** Verify MLX-LM dependencies are correctly added to pyproject.toml

**Commands:**
```bash
# Check for mlx-lm dependency
grep -i "mlx-lm" pyproject.toml
# Expected: mlx-lm>=X.Y.Z,<W.0.0 (version constraint)

# Check for mlx core dependency
grep "\"mlx" pyproject.toml
# Expected: mlx>=X.Y.Z,<W.0.0

# Check for transformers dependency
grep "transformers" pyproject.toml
# Expected: transformers>=X.Y.Z,<W.0.0

# Check for huggingface-hub dependency
grep "huggingface" pyproject.toml
# Expected: huggingface-hub>=X.Y.Z,<W.0.0 or huggingface_hub

# Verify versions are pinned (not unpinned)
grep -E "mlx-lm|\"mlx\"|transformers|huggingface" pyproject.toml | grep -v ">=" && echo "FAIL: Unpinned dependencies found" || echo "PASS: All dependencies pinned"

# Test installation from pyproject.toml
pip install -e . 2>&1 | tee /tmp/install_output.txt
# Expected: Installation succeeds without errors

# Check installation output for MLX-LM
grep -i "mlx" /tmp/install_output.txt | head -5

# Verify pip check passes (no conflicts)
pip check
# Expected: No broken requirements found.

# Run security audit
pip-audit --desc 2>&1 | tee /tmp/audit_output.txt
# Expected: 0 high-severity vulnerabilities

# Check for high-severity issues
grep -i "high" /tmp/audit_output.txt && echo "FAIL: High-severity vulnerabilities found" || echo "PASS: No high-severity vulnerabilities"
```

**Validation Criteria:**
- [ ] `mlx-lm` added to pyproject.toml dependencies
- [ ] `mlx` (core library) added to dependencies
- [ ] `transformers` added to dependencies (if not already present)
- [ ] `huggingface-hub` added to dependencies
- [ ] All versions specified (pinned or ranged, not unpinned)
- [ ] `pip install -e .` works without errors
- [ ] `pip check` passes (no dependency conflicts)
- [ ] `pip-audit` passes (0 high-severity vulnerabilities)

**Expected Result:** PASS (all 8 checks pass)

**Dependency Versions (Reference):**
```toml
[project]
dependencies = [
    # ... existing dependencies ...
    "mlx-lm>=0.16.0,<1.0.0",
    "mlx>=0.16.0,<1.0.0",
    "transformers>=4.40.0,<5.0.0",
    "huggingface-hub>=0.23.0,<1.0.0",
]
```

---

## Integration Tests

### Integration Test 1: End-to-End Framework Workflow ✅

**Test:** Validate complete workflow from installation to inference

**Commands:**
```bash
# Run end-to-end test script (if created by Builder)
test -f scripts/training/e2e_framework_test.sh && bash scripts/training/e2e_framework_test.sh || echo "INFO: E2E script not required, manual validation"

# Manual E2E validation (if no script)
echo "=== E2E Framework Workflow Test ==="
echo "Step 1: Import MLX-LM"
python3 -c "import mlx_lm; print('✓ MLX-LM imported')"

echo "Step 2: Load Qwen2.5-Coder-7B-Instruct"
python3 scripts/training/load_model_test.py | grep -i "success\|loaded"

echo "Step 3: Run inference"
python3 scripts/training/inference_test.py | grep -i "response.*generated"

echo "Step 4: Profile memory"
python3 scripts/training/memory_profile.py | grep -i "memory.*GB"

echo "=== E2E Test Complete ==="
```

**Expected Result:** All 4 steps pass without errors

---

### Integration Test 2: MCP Integration Not Broken ✅

**Test:** Verify MLX-LM installation does not break existing MCP functionality

**Commands:**
```bash
# Test MCP server initialization
python3 -c "from mcp_local.mcp_server import create_server; print('✓ MCP server can be created')"

# Test MCP memory manager
python3 -c "from mcp_local.memory_manager import MemoryManager; print('✓ MemoryManager imports')"

# Test MCP Qdrant manager
python3 -c "from mcp_local.qdrant_manager import QdrantManager; print('✓ QdrantManager imports')"

# Run existing MCP tests
pytest -q tests/mcp/ 2>&1 | tee /tmp/mcp_tests_output.txt
# Expected: All tests pass or skip gracefully (no failures)

# Check for test failures
grep "FAILED" /tmp/mcp_tests_output.txt && echo "FAIL: MCP tests failed" || echo "PASS: MCP tests pass"
```

**Expected Result:** MCP imports work, existing tests pass (no regressions)

---

## Regression Tests

### Regression Test 1: Existing Tests Still Pass ✅

**Test:** Verify no regressions in existing test suite

**Commands:**
```bash
# Run full test suite
pytest -q 2>&1 | tee /tmp/regression_tests_output.txt

# Check for failures
grep "failed" /tmp/regression_tests_output.txt && echo "FAIL: Tests failed" || echo "PASS: Tests pass"

# Compare with baseline (Sprint 3 had 10 passed, 3 skipped)
grep -E "passed|skipped" /tmp/regression_tests_output.txt
# Expected: ≥10 passed, 3 skipped (or better)
```

**Expected Result:** All existing tests pass (≥10 passed, 3 skipped acceptable)

---

### Regression Test 2: Quality Gates Baseline Maintained ✅

**Test:** Verify quality gates do not regress from Sprint 3 baseline

**Commands:**
```bash
# Check ruff errors (Sprint 3 baseline: 28 errors)
ruff check . 2>&1 | tee /tmp/ruff_output.txt
ruff_count=$(grep -c "error" /tmp/ruff_output.txt || echo "0")
echo "Ruff errors: $ruff_count (baseline: 28)"
[ "$ruff_count" -le 28 ] && echo "PASS: Ruff not regressed" || echo "FAIL: Ruff regressed"

# Check mypy errors (Sprint 3 baseline: ~401 errors)
mypy . 2>&1 | tee /tmp/mypy_output.txt
mypy_count=$(grep -c "error:" /tmp/mypy_output.txt || echo "0")
echo "Mypy errors: $mypy_count (baseline: 401)"
[ "$mypy_count" -le 450 ] && echo "PASS: Mypy not regressed" || echo "FAIL: Mypy regressed"

# Coverage check
pytest --cov=src --cov-report=term-missing --cov-fail-under=85 2>&1 | tee /tmp/coverage_output.txt
grep "FAILED" /tmp/coverage_output.txt && echo "FAIL: Coverage regressed below 85%" || echo "PASS: Coverage ≥85%"
```

**Expected Result:** Quality gates maintained or improved (no regression)

---

## Performance Benchmarks

### Benchmark 1: Model Loading Time ⚡

**Test:** Measure model loading time (baseline for future optimization)

**Commands:**
```bash
# Measure model loading time
time python3 scripts/training/load_model_test.py 2>&1 | tee /tmp/load_time.txt
# Expected: <30 seconds on M1 Max

# Extract loading time
grep "real" /tmp/load_time.txt || grep -i "time\|duration" /tmp/load_time.txt
```

**Baseline Target:** <30 seconds (not enforced in Sprint 4)

---

### Benchmark 2: Inference Speed ⚡

**Test:** Measure inference speed (tokens per second)

**Commands:**
```bash
# Run inference test and capture timing
python3 scripts/training/inference_test.py 2>&1 | grep -i "tokens.*sec\|speed\|throughput"
# Expected: >10 tokens/sec on M1 Max
```

**Baseline Target:** >10 tokens/sec (not enforced in Sprint 4, reference only)

---

## Test Execution Checklist

**Tester (T001-T01) should execute tests in this order:**

1. ☐ **Quality Gates** (Gates 1-8) — Verify all pass
2. ☐ **AC1** — Framework evaluation complete
3. ☐ **AC2** — Framework selected with rationale
4. ☐ **AC3** — MLX-LM installation successful
5. ☐ **AC4** — Qwen2.5-Coder-7B-Instruct model loaded
6. ☐ **AC5** — Basic inference test passes
7. ☐ **AC6** — Memory usage profiled (CRITICAL: ≤16GB)
8. ☐ **AC7** — Installation guide documented
9. ☐ **AC8** — Dependencies added to pyproject.toml
10. ☐ **Integration Test 1** — E2E workflow
11. ☐ **Integration Test 2** — MCP integration not broken
12. ☐ **Regression Test 1** — Existing tests pass
13. ☐ **Regression Test 2** — Quality gates baseline maintained

**Total Test Time Estimate:** 20 minutes (T001-T01 complexity: Small)

---

## Test Deliverables

**Tester must create:**
1. Test completion report: `.oodatcaa/work/reports/T001/tester_T001-T01.md`
2. SPRINT_QUEUE.json updated with test results
3. AGENT_LOG.md entry (concise test summary)

**Report Contents:**
- Test execution summary (ACs passed/failed)
- Issues found (if any)
- Quality gates status
- Recommendations for Builder (if adaptations needed)
- Handoff notes for Integrator (if all ACs pass)

---

## Troubleshooting

### Issue 1: Model Download Fails

**Symptoms:** `load_model_test.py` fails with network error or timeout

**Diagnosis:**
```bash
curl -I https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct
# Expected: HTTP 200 OK
```

**Solution:**
- Check internet connection
- Try manual download: `huggingface-cli download Qwen/Qwen2.5-Coder-7B-Instruct`
- Use HuggingFace mirror if available

---

### Issue 2: Memory Exceeds 16GB Target

**Symptoms:** Memory profiling shows >16GB training memory

**Diagnosis:**
```bash
python3 scripts/training/memory_profile.py | grep -i "training"
# Check if training memory > 16GB
```

**Solution:**
- Reduce batch size to 1 (if not already)
- Enable gradient checkpointing (saves memory at cost of speed)
- Use more aggressive quantization (2-bit instead of 4-bit)
- Switch to axolotl framework (fallback plan)
- Escalate to Refiner for plan adaptation

---

### Issue 3: MLX-LM Import Fails

**Symptoms:** `import mlx_lm` raises ImportError

**Diagnosis:**
```bash
pip list | grep mlx
python3 -c "import sys; print(sys.path)"
```

**Solution:**
- Verify venv activated: `source .venv/bin/activate`
- Reinstall MLX-LM: `pip install --force-reinstall mlx-lm`
- Check for version conflicts: `pip check`

---

### Issue 4: Inference Generates Gibberish

**Symptoms:** Model response is incoherent or random characters

**Diagnosis:**
- Check model loaded correctly (AC4)
- Verify tokenizer matches model
- Inspect inference parameters (temperature, top_p)

**Solution:**
- Adjust inference parameters (lower temperature, e.g., 0.7)
- Verify model is Qwen2.5-Coder-7B-Instruct (not base model)
- Check for model corruption (re-download)

---

## Success Criteria

**T001 is complete when:**
- ✅ All 8 quality gates pass
- ✅ All 8 acceptance criteria pass
- ✅ All integration tests pass
- ✅ No regressions in existing functionality
- ✅ Memory usage ≤16GB target (CRITICAL)
- ✅ Documentation comprehensive and reproducible

**If any AC fails:** Tester marks T001-T01 as "needs_adapt", Refiner analyzes and proposes quick fix or rollback

**If all ACs pass:** Tester marks T001-T01 as "ready_for_integrator", Integrator merges to main

---

**Test Plan Status:** ✅ COMPLETE — Ready for Tester validation