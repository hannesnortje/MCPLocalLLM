# Implementation Plan — T001: Training Framework Research & Selection

**Plan Version:** 1.0  
**Created:** 2025-10-06T07:57:00+02:00  
**Planner:** agent-planner-A  
**Status:** Planning Complete  
**Branch:** `feat/T001-step-01-framework-selection`

---

## Traceability

**Objective ID:** OBJ-2025-002 (Small Coder Model Training with MCP Integration)  
**Epic:** Training System Foundation  
**Sprint:** Sprint 4 (2025-10-05 → 2025-10-15)  
**Backlog Item:** T001 - Training Framework Research & Selection  
**Objective Link:** Training System (Core) → QLoRA Setup → Framework selection

**Dependencies:** None (first task in Sprint 4)  
**Unblocks:** T002 (QLoRA Configuration), T003 (Dataset Schema)

---

## Problem Statement

### Current State
- **Sprint 3 Complete**: MCP server infrastructure fully integrated (61 files, 12 dependencies, Qdrant configured)
- **Training Infrastructure**: None — no training framework, no model loading, no QLoRA configuration
- **Hardware Target**: Apple M1 Max with 32GB RAM (Metal acceleration available)
- **Model Target**: Qwen2.5-Coder-7B-Instruct (7B parameters, instruct-tuned)
- **Training Method**: QLoRA (LoRA rank=16, alpha=32, 4-bit quantization)

### Impact
Without a training framework, we cannot:
- Fine-tune Qwen2.5-Coder-7B on procedural knowledge and custom definitions
- Implement daily learning cycles with overnight training
- Validate QLoRA memory constraints (≤16GB RAM target)
- Proceed with dataset creation and training pipeline (Sprint 4 blocks T002-T008)

### Problem
**Select and validate a training framework** for fine-tuning Qwen2.5-Coder-7B with QLoRA on M1 Max hardware, optimizing for:
1. **Memory Efficiency**: ≤16GB RAM during training (32GB available, leaving headroom)
2. **M1 Max Optimization**: Native Metal acceleration support
3. **Ease of Use**: Quick setup, good documentation, active community
4. **QLoRA Support**: Built-in LoRA/QLoRA with 4-bit quantization
5. **Model Compatibility**: Works with Qwen2.5-Coder-7B-Instruct

---

## Constraints, Interfaces & Risks

### Constraints

**Hardware:**
- Apple M1 Max (32GB RAM, Metal GPU)
- No NVIDIA GPU (CUDA not available)
- Local-only (no cloud dependencies)

**Software:**
- Python 3.11+ (existing project constraint)
- Must integrate with existing MCP infrastructure
- Type hints (mypy strict mode)
- Quality gates: black, ruff, mypy, pytest, pip-audit

**Model:**
- Qwen2.5-Coder-7B-Instruct (HuggingFace model)
- QLoRA training (rank=16, alpha=32, 4-bit quantization)
- Target model size: ≤8GB quantized (GGUF Q4_K_M)

**Timeline:**
- Framework selection: 120-180 minutes (Medium complexity)
- Must unblock T002 (QLoRA config) and T003 (Dataset schema)

### Interfaces

**Inputs:**
- OBJECTIVE.md requirements (QLoRA, Qwen2.5-Coder-7B, M1 Max)
- Existing MCP infrastructure (src/mcp_local/, pyproject.toml)
- Hardware specifications (M1 Max capabilities)

**Outputs:**
- Framework selection report with pros/cons comparison
- Proof-of-concept installation guide
- Basic inference test (model responds to prompt)
- Memory usage profile (training and inference)
- Updated pyproject.toml with framework dependencies
- Documentation for Builder to implement

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Memory overflow** (>32GB RAM during training) | Medium | High | Profile memory with small batch sizes first; QLoRA 4-bit should fit |
| **Framework incompatibility** with M1 Max | Low | High | Test both frameworks; MLX-LM has native M1 support |
| **Model download failures** (7B model ~14GB) | Low | Medium | Document download process; use HuggingFace mirror if needed |
| **Installation complexity** (many dependencies) | Medium | Medium | Use isolated venv; document exact versions |
| **Poor documentation** (framework issues) | Low | Medium | Both frameworks have active communities; fallback to other framework |
| **QLoRA not supported** | Very Low | High | Both frameworks explicitly support QLoRA |

---

## Definition of Done (DoD)

### Functional Requirements
1. ✅ **Framework Selected**: Clear recommendation (MLX-LM or axolotl) with documented rationale
2. ✅ **Installation Working**: Proof-of-concept setup completed successfully
3. ✅ **Model Loading**: Can load Qwen2.5-Coder-7B-Instruct base model
4. ✅ **Basic Inference**: Model responds to test prompt (code generation task)
5. ✅ **Memory Profiled**: Training and inference memory usage documented

### Non-Functional Requirements
6. ✅ **Documentation**: Installation guide with exact commands and dependencies
7. ✅ **Dependencies**: pyproject.toml updated with framework + model dependencies
8. ✅ **Quality Gates**: All gates pass (black, ruff, mypy, pytest, pip-audit)

---

## Acceptance Criteria (ACs)

### AC1: Framework Evaluation Complete ✅
- [ ] **MLX-LM** evaluated with pros/cons documented
- [ ] **axolotl** evaluated with pros/cons documented
- [ ] Comparison matrix created (memory, speed, ease of use, QLoRA support, M1 Max optimization)
- [ ] Framework selected with explicit rationale (minimum 3 decision factors)
- [ ] Alternative framework documented as fallback option

**Validation:** Evaluation report exists with 2 frameworks compared and 1 selected

### AC2: Framework Selected with Rationale ✅
- [ ] Selected framework explicitly stated (MLX-LM or axolotl)
- [ ] Rationale documented with minimum 3 decision factors:
  - Memory efficiency (≤16GB RAM target)
  - M1 Max optimization (Metal acceleration)
  - Ease of use (setup time, documentation quality)
- [ ] Trade-offs acknowledged (what we gain, what we lose)
- [ ] Fallback plan documented if selected framework fails

**Validation:** Selection section in report with clear decision reasoning

### AC3: Proof-of-Concept Installation Successful ✅
- [ ] Framework installed in project venv
- [ ] Installation guide documented with exact commands
- [ ] All framework dependencies resolved
- [ ] Installation validated (import test passes)
- [ ] No conflicts with existing MCP dependencies

**Validation:** `pip list | grep <framework>` shows installed, import test passes

### AC4: Qwen2.5-Coder-7B-Instruct Model Loaded ✅
- [ ] Model downloaded from HuggingFace (or documented download process)
- [ ] Model loaded successfully in Python
- [ ] Model tokenizer working
- [ ] Model architecture validated (7B parameters confirmed)
- [ ] Model ready for inference

**Validation:** Python script loads model, prints architecture summary, no errors

### AC5: Basic Inference Test Passes ✅
- [ ] Test prompt defined (code generation task, e.g., "Write a Python function to...")
- [ ] Model generates response (minimum 20 tokens)
- [ ] Response is coherent (not gibberish)
- [ ] Inference time measured and documented
- [ ] Test script provided for Builder to reproduce

**Validation:** Inference script runs, generates response, inference time logged

### AC6: Memory Usage Profiled and Documented ✅
- [ ] **Inference memory** measured (model loading + single inference)
- [ ] **Training memory** estimated (with QLoRA, batch size 1)
- [ ] Memory usage documented in MB/GB
- [ ] Comparison with 16GB target (headroom calculated)
- [ ] Peak memory usage captured (not just average)

**Validation:** Memory profile document with numbers (e.g., "Inference: 8.2GB, Training est: 14.5GB")

### AC7: Installation Guide Documented ✅
- [ ] Step-by-step installation instructions
- [ ] Exact commands provided (copy-paste ready)
- [ ] Dependencies listed with versions
- [ ] Troubleshooting section (common issues)
- [ ] Verification steps (how to confirm installation worked)

**Validation:** `docs/training/FRAMEWORK_SETUP.md` exists with complete installation guide

### AC8: Dependencies Added to pyproject.toml ✅
- [ ] Framework package added to dependencies
- [ ] Model packages added (transformers, torch/mlx, etc.)
- [ ] Versions specified (not unpinned)
- [ ] Optional dependencies documented if applicable
- [ ] pip-audit passes (no high-severity vulnerabilities)

**Validation:** pyproject.toml updated, `pip install -e .` works, pip-audit clean

---

## Alternatives Considered

### Alternative 1: Apple MLX-LM 🥇 **RECOMMENDED**

**Description:** Apple's native machine learning framework for M1/M2 chips with Metal acceleration.

**Pros:**
- ✅ **Native M1 Max support** — Built specifically for Apple Silicon with Metal GPU acceleration
- ✅ **Memory efficient** — Optimized for unified memory architecture
- ✅ **Easy setup** — pip install, minimal dependencies
- ✅ **Good documentation** — Apple maintains comprehensive guides
- ✅ **Active development** — Regular updates, growing community
- ✅ **LoRA/QLoRA support** — Built-in LoRA fine-tuning with examples
- ✅ **Fast inference** — Metal acceleration provides excellent inference speed
- ✅ **Quantization support** — Built-in 4-bit, 8-bit quantization

**Cons:**
- ⚠️ **M1/M2 only** — Not portable to NVIDIA/AMD GPUs (but not a constraint for this project)
- ⚠️ **Smaller ecosystem** — Fewer community examples than PyTorch/Axolotl
- ⚠️ **Newer framework** — Less battle-tested than PyTorch-based solutions
- ⚠️ **Model support** — Not all HuggingFace models officially tested (but Qwen supported)

**Decision Factors:**
1. **M1 Max Optimization**: Native Metal acceleration is critical for performance on our hardware
2. **Memory Efficiency**: Unified memory architecture optimization aligns with ≤16GB target
3. **Ease of Use**: Simple pip install, minimal setup overhead
4. **QLoRA Support**: Built-in LoRA with quantization examples
5. **Apple Backing**: Official Apple support provides confidence in M1 Max optimization

**Estimated Effort:** 60-90 minutes (setup + validation)

---

### Alternative 2: Axolotl (HuggingFace/PyTorch-based)

**Description:** Popular LoRA/QLoRA training framework built on HuggingFace Transformers and PyTorch.

**Pros:**
- ✅ **Battle-tested** — Widely used in community, many examples
- ✅ **Comprehensive** — Supports almost all HuggingFace models
- ✅ **Rich ecosystem** — Many community configs, troubleshooting resources
- ✅ **QLoRA built-in** — Excellent LoRA/QLoRA support with bitsandbytes
- ✅ **Flexible** — Highly configurable for advanced use cases
- ✅ **Portable** — Works on CUDA, MPS (Metal), CPU

**Cons:**
- ⚠️ **PyTorch MPS backend** — MPS (Metal Performance Shaders) support is less mature than CUDA
- ⚠️ **Memory overhead** — PyTorch can be memory-hungry, especially with transformers
- ⚠️ **Complex setup** — More dependencies, configuration files, potential conflicts
- ⚠️ **M1 Max optimization** — Not specifically optimized for Apple Silicon (generic MPS support)
- ⚠️ **Slower inference** — PyTorch MPS generally slower than native MLX on M1 Max
- ⚠️ **Dependency conflicts** — More dependencies increases risk of conflicts with existing MCP packages

**Decision Factors:**
1. **Ecosystem Maturity**: Large community, many examples and troubleshooting resources
2. **Model Compatibility**: Guaranteed to work with Qwen2.5-Coder-7B-Instruct
3. **QLoRA Experience**: Well-documented QLoRA training recipes
4. **Fallback Option**: If MLX-LM has issues, axolotl is proven alternative

**Estimated Effort:** 120-150 minutes (more complex setup)

---

### Alternative 3: Minimal Setup (No Framework, Direct HuggingFace Transformers + LoRA)

**Description:** Use HuggingFace Transformers + PEFT (Parameter-Efficient Fine-Tuning) libraries directly without a higher-level framework.

**Pros:**
- ✅ **Minimal dependencies** — Only transformers + peft + torch
- ✅ **Maximum control** — Write custom training loops
- ✅ **Well-documented** — HuggingFace docs are excellent
- ✅ **Flexible** — Can optimize exactly for our use case

**Cons:**
- ❌ **High effort** — Must write training loops, config management, checkpointing from scratch
- ❌ **Reinventing wheel** — Frameworks like MLX-LM already provide this
- ❌ **Time-consuming** — Estimated 4-6 hours to build training pipeline
- ❌ **Error-prone** — More code to maintain and debug
- ❌ **No M1 Max optimization** — Generic PyTorch MPS, not optimized for Apple Silicon

**Decision Factors:**
1. **Time Constraint**: 120-180 minutes for T001 insufficient for custom implementation
2. **Framework Benefits**: MLX-LM/axolotl provide tested, optimized solutions
3. **Maintenance**: Less code to maintain with framework
4. **Risk**: Higher risk of bugs in custom implementation

**Estimated Effort:** 240-360 minutes (Large complexity, beyond T001 scope)

**Recommendation:** ❌ **REJECT** — Not viable within T001 timeline

---

## Chosen Alternative: MLX-LM (Alternative 1) 🥇

### Rationale

We select **Apple MLX-LM** for the following reasons:

1. **M1 Max Optimization (Critical)**: Native Metal acceleration provides significant performance advantage over PyTorch MPS backend. This is our primary hardware constraint and MLX-LM is purpose-built for it.

2. **Memory Efficiency (High Priority)**: Unified memory architecture optimization in MLX-LM aligns perfectly with our ≤16GB RAM target. Apple engineers tuned this specifically for M1/M2 memory characteristics.

3. **Ease of Use (Medium Priority)**: Simple `pip install mlx-lm` with minimal dependencies reduces setup complexity and risk. Estimated 60-90 minutes vs 120-150 minutes for axolotl.

4. **QLoRA Support (High Priority)**: Built-in LoRA fine-tuning with quantization examples in MLX-LM documentation. Proven to work with 7B models on M1 Max.

5. **Future-Proof (Low Priority)**: As Apple continues developing MLX, we benefit from ongoing optimizations for Apple Silicon. Aligns with local-first, M1 Max-focused objective.

### Trade-offs Accepted

- **Smaller Ecosystem**: Fewer community examples than PyTorch/axolotl (acceptable — we can reference MLX-LM docs)
- **Portability**: Locked to M1/M2 hardware (acceptable — OBJECTIVE.md explicitly targets M1 Max)
- **Newer Framework**: Less battle-tested than PyTorch (acceptable — Apple backing provides confidence)

### Fallback Plan

If MLX-LM fails during implementation (e.g., model compatibility issues, unexpected memory problems):
1. **Quick validation** (30 min): Test axolotl with same proof-of-concept
2. **Switch decision** (15 min): Update plan, document switch rationale
3. **Axolotl implementation** (90 min): Follow Alternative 2 setup
4. **Total fallback cost**: ~135 minutes (still within Sprint 4 buffer)

---

## Step-by-Step Implementation Plan

### Step 1: Research & Framework Evaluation (30 minutes)

**Goal:** Evaluate MLX-LM and axolotl, confirm Qwen2.5-Coder-7B compatibility

**Tasks:**
1. Read MLX-LM documentation (installation, LoRA examples, Qwen support)
2. Read axolotl documentation (MPS backend, Qwen configs)
3. Check community reports for Qwen2.5-Coder-7B on M1 Max
4. Create comparison matrix (memory, speed, ease, QLoRA, M1 Max)
5. Document decision rationale (3+ factors)

**Exit Gate:**
- [ ] Comparison matrix complete (2 frameworks, 5 criteria)
- [ ] Framework selected (MLX-LM expected)
- [ ] Rationale documented with minimum 3 decision factors

**Branch:** Not needed (research only)  
**Deliverable:** `docs/training/T001_framework_evaluation.md`

---

### Step 2: MLX-LM Installation & Setup (20 minutes)

**Goal:** Install MLX-LM framework in project venv, validate imports

**Tasks:**
1. Create new branch: `feat/T001-step-01-framework-selection`
2. Activate project venv: `source .venv/bin/activate`
3. Install MLX-LM: `pip install mlx-lm`
4. Install dependencies: `pip install mlx transformers` (if not auto-installed)
5. Verify installation: `python -c "import mlx_lm; print(mlx_lm.__version__)"`
6. Update pyproject.toml with MLX-LM dependencies

**Exit Gate:**
- [ ] MLX-LM installed successfully
- [ ] Import test passes (no errors)
- [ ] pyproject.toml updated with dependencies
- [ ] No conflicts with existing MCP packages (pip check passes)

**Commands:**
```bash
git checkout -b feat/T001-step-01-framework-selection
pip install mlx-lm mlx transformers
python -c "import mlx_lm; import mlx; import transformers; print('MLX-LM:', mlx_lm.__version__); print('MLX:', mlx.__version__); print('Transformers:', transformers.__version__)"
pip check
```

**Deliverable:** Updated `pyproject.toml` with MLX-LM dependencies

---

### Step 3: Model Download & Loading (25 minutes)

**Goal:** Download Qwen2.5-Coder-7B-Instruct, load model in Python

**Tasks:**
1. Research Qwen2.5-Coder-7B-Instruct on HuggingFace (model card, download size)
2. Check MLX-LM model format requirements (HuggingFace Hub, local path, or MLX format)
3. Download model using HuggingFace CLI or mlx_lm tool
4. Create Python script to load model with MLX-LM
5. Verify model architecture (7B parameters, instruct-tuned)
6. Document model download process

**Exit Gate:**
- [ ] Qwen2.5-Coder-7B-Instruct downloaded (~14GB)
- [ ] Model loaded successfully in Python script
- [ ] Model architecture validated (7B parameters confirmed)
- [ ] Tokenizer working (can encode/decode test strings)
- [ ] Script documented for reproducibility

**Commands:**
```bash
# Option 1: MLX-LM automatic download
python -c "from mlx_lm import load; model, tokenizer = load('Qwen/Qwen2.5-Coder-7B-Instruct')"

# Option 2: HuggingFace Hub CLI (if needed)
pip install huggingface_hub
huggingface-cli download Qwen/Qwen2.5-Coder-7B-Instruct
```

**Deliverable:** `scripts/training/load_model_test.py` (model loading script)

---

### Step 4: Basic Inference Test (20 minutes)

**Goal:** Run inference with Qwen2.5-Coder-7B-Instruct, validate model works

**Tasks:**
1. Create inference test script
2. Define test prompt (code generation task, e.g., "Write a Python function to calculate Fibonacci sequence")
3. Run inference with model (generate 50-100 tokens)
4. Validate response is coherent (not gibberish, relevant to prompt)
5. Measure inference time (seconds per token, total time)
6. Document inference parameters (temperature, max_tokens, etc.)

**Exit Gate:**
- [ ] Inference test script runs without errors
- [ ] Model generates coherent response (minimum 20 tokens)
- [ ] Inference time measured and documented
- [ ] Test prompt and output saved for validation
- [ ] Script reproducible (Builder can run it)

**Commands:**
```bash
python scripts/training/inference_test.py
```

**Expected Output:**
```
Test Prompt: Write a Python function to calculate Fibonacci sequence
Model Response: def fibonacci(n): ...
Inference Time: 2.3 seconds (21.7 tokens/sec)
Response Coherent: Yes
```

**Deliverable:** `scripts/training/inference_test.py` + `docs/training/inference_test_results.md`

---

### Step 5: Memory Profiling (25 minutes)

**Goal:** Measure memory usage (inference + training estimate), validate ≤16GB target

**Tasks:**
1. Create memory profiling script using `psutil` or macOS `memory_pressure`
2. Measure inference memory (model loading + single inference run)
3. Estimate training memory (QLoRA with batch size 1, based on MLX-LM docs)
4. Calculate peak memory usage (not just average)
5. Compare with 16GB target (headroom calculation)
6. Document memory profile with numbers

**Exit Gate:**
- [ ] Inference memory measured (MB/GB)
- [ ] Training memory estimated (based on QLoRA 4-bit quantization)
- [ ] Peak memory usage documented
- [ ] Comparison with 16GB target (e.g., "14.5GB training, 1.5GB headroom")
- [ ] Profile reproducible (Builder can verify)

**Commands:**
```bash
python scripts/training/memory_profile.py
# or: /usr/bin/time -l python scripts/training/inference_test.py
```

**Expected Output:**
```
Inference Memory: 8.2GB (model loading + single inference)
Training Memory (est): 14.5GB (QLoRA, batch size 1, 4-bit quantization)
Peak Memory: 14.8GB
Headroom from 16GB target: 1.2GB (acceptable)
```

**Deliverable:** `docs/training/memory_profile.md`

---

### Step 6: Installation Guide Documentation (20 minutes)

**Goal:** Create comprehensive installation guide for Builder

**Tasks:**
1. Create `docs/training/FRAMEWORK_SETUP.md`
2. Document step-by-step installation (exact commands)
3. List all dependencies with versions
4. Add troubleshooting section (common issues on M1 Max)
5. Add verification steps (how to confirm setup worked)
6. Cross-reference with T001 evaluation report

**Exit Gate:**
- [ ] Installation guide exists at `docs/training/FRAMEWORK_SETUP.md`
- [ ] Step-by-step instructions with exact commands
- [ ] Dependencies listed with versions
- [ ] Troubleshooting section (minimum 3 common issues)
- [ ] Verification steps documented

**Contents:**
- Prerequisites (Python 3.11+, M1 Max, venv)
- Installation commands (copy-paste ready)
- Verification (import test, model load test)
- Troubleshooting (M1 Max specific issues)
- Next steps (reference to T002 QLoRA configuration)

**Deliverable:** `docs/training/FRAMEWORK_SETUP.md`

---

### Step 7: Update pyproject.toml Dependencies (10 minutes)

**Goal:** Add MLX-LM and model dependencies to pyproject.toml

**Tasks:**
1. Add `mlx-lm` to dependencies section
2. Add `mlx` (MLX core library)
3. Add `transformers` (if not already present)
4. Add `huggingface_hub` (for model downloads)
5. Specify versions (pin or use ranges)
6. Add optional training dependencies group if needed
7. Run `pip-audit` to check for vulnerabilities

**Exit Gate:**
- [ ] pyproject.toml updated with MLX-LM dependencies
- [ ] Versions specified (not unpinned)
- [ ] `pip install -e .` works without errors
- [ ] `pip check` passes (no dependency conflicts)
- [ ] `pip-audit` passes (no high-severity vulnerabilities)

**Dependencies to Add:**
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

**Deliverable:** Updated `pyproject.toml`

---

### Step 8: Quality Gates & Commit (10 minutes)

**Goal:** Validate all quality gates pass, commit T001 work

**Tasks:**
1. Run black formatter: `make fmt`
2. Run ruff linter: `ruff check .`
3. Run mypy type checker: `mypy .`
4. Run pytest unit tests: `pytest -q`
5. Run pip-audit: `pip-audit`
6. Fix any issues (unlikely — documentation and scripts)
7. Commit changes with `[plan]` label

**Exit Gate:**
- [ ] `black --check .` passes
- [ ] `ruff check .` passes
- [ ] `mypy .` passes
- [ ] `pytest -q` passes (existing tests)
- [ ] `pip-audit` passes
- [ ] Changes committed with clear message

**Commands:**
```bash
make fmt
make gates
git add .
git commit -m "[plan] T001: Framework selection complete - MLX-LM chosen, installation validated, memory profiled"
```

**Commit Message Pattern:** `[plan] T001: <summary of work>`

**Deliverable:** Committed branch `feat/T001-step-01-framework-selection`

---

## Task Breakdown for SPRINT_QUEUE.json

### T001-B01: Steps 1-5 — Research, Install, Model Load, Inference, Memory Profile
**Complexity:** Medium  
**Estimated Time:** 120 minutes  
**Status:** ready  
**Dependencies:** None  
**Exit Gates:** Steps 1-5 complete, all ACs 1-6 validated

### T001-B02: Steps 6-8 — Documentation, Dependencies, Quality Gates
**Complexity:** Small  
**Estimated Time:** 40 minutes  
**Status:** blocked (depends on T001-B01)  
**Dependencies:** T001-B01  
**Exit Gates:** Steps 6-8 complete, ACs 7-8 validated

### T001-T01: Validation — Verify All 8 ACs Pass
**Complexity:** Small  
**Estimated Time:** 20 minutes  
**Status:** blocked (depends on T001-B02)  
**Dependencies:** T001-B02  
**Exit Gates:** All 8 ACs validated, TEST_PLAN.md checks pass

---

## Deliverables Summary

| Deliverable | Location | Size Estimate | AC Coverage |
|-------------|----------|---------------|-------------|
| Framework Evaluation Report | `docs/training/T001_framework_evaluation.md` | ~500 lines | AC1, AC2 |
| Model Loading Script | `scripts/training/load_model_test.py` | ~50 lines | AC4 |
| Inference Test Script | `scripts/training/inference_test.py` | ~100 lines | AC5 |
| Inference Test Results | `docs/training/inference_test_results.md` | ~200 lines | AC5 |
| Memory Profile Script | `scripts/training/memory_profile.py` | ~80 lines | AC6 |
| Memory Profile Report | `docs/training/memory_profile.md` | ~300 lines | AC6 |
| Framework Setup Guide | `docs/training/FRAMEWORK_SETUP.md` | ~400 lines | AC7 |
| Updated pyproject.toml | `pyproject.toml` | +10 lines | AC8 |

**Total Deliverables:** 7 documentation files + 3 Python scripts + 1 config update = **11 files**  
**Estimated Total Lines:** ~1,640 lines (documentation + scripts)

---

## Risk Mitigation

| Risk | Mitigation Strategy | Contingency Plan |
|------|---------------------|------------------|
| MLX-LM incompatible with Qwen2.5-Coder-7B | Verify model support in Step 3 early | Switch to axolotl (Alternative 2), +90 min |
| Memory exceeds 16GB during training | Profile memory in Step 5 with batch size 1 | Reduce batch size, use gradient accumulation |
| Model download fails (14GB size) | Document download process, provide HuggingFace CLI alternative | Use HuggingFace mirror, local download |
| Installation conflicts with MCP packages | Run `pip check` in Step 2 | Use isolated venv, pin conflicting versions |
| Inference too slow (>5 sec/token) | Measure inference time in Step 4 | Document limitation, proceed (inference speed not Sprint 4 goal) |

---

## Sprint Impact

**Sprint 4 Progress:**
- T001: 0% → 100% (upon completion)
- Sprint 4: 0% → 12.5% (T001 is 1 of 8 tasks)
- Objective: ~25% → ~27% (T001 advances training foundation)

**Unblocks:**
- T002 (QLoRA Configuration) — Can configure LoRA rank, alpha, quantization
- T003 (Dataset Schema) — Can design dataset format for MLX-LM training

**Dependencies Satisfied:** None (T001 is first task in Sprint 4)

**Critical Path:** T001 → T002 → T004 → T005 → T006 → T008 (critical path dependencies)

---

## Handoff to Builder

### What Builder Needs to Know

1. **Framework Selection**: MLX-LM chosen for M1 Max optimization, memory efficiency, ease of use
2. **Model Target**: Qwen2.5-Coder-7B-Instruct (~14GB download, 7B parameters)
3. **Proof-of-Concept Scope**: Install MLX-LM, load model, run inference, profile memory (no training yet)
4. **Success Criteria**: All 8 ACs validated, especially AC6 (memory ≤16GB target)
5. **Timeline**: 160 minutes total (120 min T001-B01, 40 min T001-B02)

### Key Implementation Notes

- **Branch Naming**: `feat/T001-step-01-framework-selection`
- **Commit Labels**: `[plan]` for planning artifacts, `[impl]` for code/config changes
- **Quality Gates**: All must pass (black, ruff, mypy, pytest, pip-audit)
- **Documentation**: Comprehensive guides for reproducibility (future sprints will reference)
- **Memory Target**: ≤16GB training, ≤8GB inference (validate in Step 5)

### Exit Criteria Checklist

Builder should verify each AC before marking T001-B01/T001-B02 complete:
- [ ] AC1: Framework evaluation report exists with 2 frameworks compared
- [ ] AC2: Framework selected (MLX-LM) with 3+ decision factors
- [ ] AC3: MLX-LM installed, import test passes
- [ ] AC4: Qwen2.5-Coder-7B-Instruct loaded, architecture validated
- [ ] AC5: Inference test passes, generates coherent response
- [ ] AC6: Memory profiled (inference + training estimate)
- [ ] AC7: Installation guide documented
- [ ] AC8: pyproject.toml updated, pip-audit passes

---

**Plan Status:** ✅ COMPLETE — Ready for Builder assignment

**Next Action:** Negotiator assigns T001-B01 to Builder (120 min estimate)