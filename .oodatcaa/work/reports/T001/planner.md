# Planner Completion Report — T001: Training Framework Research & Selection

**Agent:** agent-planner-A  
**Task:** T001 - Training Framework Research & Selection  
**Role:** Planner (Observe+Orient+Decide)  
**Status:** ✅ COMPLETE  
**Timestamp:** 2025-10-06T08:15:00+02:00

---

## Objective

Plan the implementation for selecting and validating a training framework (MLX-LM or axolotl) for fine-tuning Qwen2.5-Coder-7B with QLoRA on M1 Max (32GB RAM), ensuring memory usage ≤16GB during training.

**Objective Link:** Training System (Core) → QLoRA Setup → Framework selection

---

## Actions Taken

### 1. Observe Phase (Repository & Constraint Analysis)
- ✅ Analyzed current state: MCP server integrated (Sprint 3 complete), no training infrastructure exists
- ✅ Reviewed hardware constraints: M1 Max with 32GB RAM, Metal GPU acceleration available
- ✅ Reviewed model requirements: Qwen2.5-Coder-7B-Instruct (~14GB download, 7B parameters)
- ✅ Reviewed training requirements: QLoRA (rank=16, alpha=32, 4-bit quantization), ≤16GB RAM target
- ✅ Reviewed existing dependencies: pyproject.toml with MCP dependencies, no conflicts expected
- ✅ Repository inventory: src/mcp_local/ (47 modules), tests/mcp/ (3 test files), docs/mcp/ (7 docs)

### 2. Orient Phase (Framework Evaluation)
- ✅ **Framework 1: Apple MLX-LM** — Native M1 Max support, Metal acceleration, memory-optimized, built-in QLoRA
- ✅ **Framework 2: Axolotl** — PyTorch-based, battle-tested, comprehensive but less M1 Max optimized
- ✅ **Framework 3: Direct HuggingFace** — Maximum control, minimal dependencies, but high effort (240-360 min)
- ✅ Created comparison matrix: Memory, Speed, Ease of Use, QLoRA Support, M1 Max Optimization
- ✅ Identified decision factors: M1 Max optimization (critical), memory efficiency (high), ease of use (medium), QLoRA support (high)

### 3. Decide Phase (Framework Selection)
- ✅ **Selected: Apple MLX-LM (Alternative 1)**
- ✅ **Rationale:**
  1. **M1 Max Optimization (Critical)**: Native Metal acceleration provides significant performance advantage over PyTorch MPS
  2. **Memory Efficiency (High Priority)**: Unified memory architecture optimization aligns with ≤16GB RAM target
  3. **Ease of Use (Medium Priority)**: Simple pip install, minimal dependencies (60-90 min vs 120-150 min for axolotl)
  4. **QLoRA Support (High Priority)**: Built-in LoRA fine-tuning with quantization examples
  5. **Future-Proof (Low Priority)**: Apple's ongoing MLX development benefits M1 Max-focused objective
- ✅ **Trade-offs Accepted:** Smaller ecosystem (acceptable - MLX-LM docs sufficient), M1-only (acceptable - OBJECTIVE.md targets M1 Max), newer framework (acceptable - Apple backing)
- ✅ **Fallback Plan:** Switch to axolotl if MLX-LM has model compatibility or memory issues (+135 min total fallback cost)

### 4. Plan Phase (Implementation Design)
- ✅ Created 8-step implementation plan:
  1. Research & Framework Evaluation (30 min)
  2. MLX-LM Installation & Setup (20 min)
  3. Model Download & Loading (25 min)
  4. Basic Inference Test (20 min)
  5. Memory Profiling (25 min) — **CRITICAL: ≤16GB validation**
  6. Installation Guide Documentation (20 min)
  7. Update pyproject.toml Dependencies (10 min)
  8. Quality Gates & Commit (10 min)
- ✅ Defined 8 acceptance criteria (framework evaluation, installation, model loading, inference, memory profile, docs, dependencies, quality gates)
- ✅ Broke down into 3 subtasks:
  - T001-B01: Steps 1-5 (Research, Install, Model Load, Inference, Memory) — 120 min, **ready**
  - T001-B02: Steps 6-8 (Docs, Dependencies, Quality Gates) — 40 min, blocked by B01
  - T001-T01: Validation (All 8 ACs) — 20 min, blocked by B02
- ✅ Identified 6 risks with mitigation strategies (memory overflow, framework incompatibility, model download failures, installation conflicts, poor documentation, QLoRA not supported)

---

## Deliverables

### 1. AGENT_PLAN.md ✅
- **Location:** `.oodatcaa/work/AGENT_PLAN.md`
- **Size:** ~1,640 lines
- **Contents:**
  - Traceability (Objective, Epic, Sprint, Dependencies)
  - Problem statement (current state, impact, problem definition)
  - Constraints, interfaces, risks (6 risks identified)
  - Definition of Done (8 functional + non-functional requirements)
  - 8 Acceptance Criteria (testable, measurable)
  - 3 Alternatives analyzed (MLX-LM, axolotl, direct HuggingFace)
  - Chosen alternative (MLX-LM) with rationale (5 decision factors)
  - 8-step implementation plan with exit gates
  - 3 subtask breakdown for SPRINT_QUEUE.json
  - 11 deliverables summary (7 docs + 3 scripts + 1 config)
  - Risk mitigation matrix
  - Sprint impact analysis
  - Handoff notes for Builder

### 2. TEST_PLAN.md ✅
- **Location:** `.oodatcaa/work/TEST_PLAN.md`
- **Size:** ~760 lines
- **Contents:**
  - Test overview (objective, scope, out of scope)
  - 8 Quality gates with exact commands (black, ruff, mypy, pytest, coverage, build, pip-audit)
  - 8 Acceptance criteria tests with validation commands
  - Integration tests (E2E framework workflow, MCP integration not broken)
  - Regression tests (existing tests pass, quality gates maintained)
  - Performance benchmarks (model loading time, inference speed)
  - Test execution checklist (13 steps for Tester)
  - Troubleshooting guide (4 common issues with solutions)
  - Success criteria (all gates pass, ACs pass, no regressions, memory ≤16GB)

### 3. SPRINT_QUEUE.json ✅
- **Location:** `.oodatcaa/work/SPRINT_QUEUE.json`
- **Updates:**
  - T001 status: needs_plan → planning_complete
  - T001-B01 added: ready (Steps 1-5, 120 min)
  - T001-B02 added: blocked by B01 (Steps 6-8, 40 min)
  - T001-T01 added: blocked by B02 (Validation, 20 min)
  - Dependencies updated (T002, T003 blocked by T001)
  - Metadata updated (planning_complete_tasks: 1, ready_tasks: 1)

### 4. SPRINT_PLAN.md ✅
- **Location:** `.oodatcaa/work/SPRINT_PLAN.md`
- **Updates:**
  - Sprint 4 section added at top (current assignments)
  - T001 plan summary (8 steps, 3 subtasks, deliverables, exit criteria)
  - Planner assignment documented (assigned, completed, plan version)
  - Next assignment: Builder → T001-B01 (ready)
  - Sprint 3 marked as historical (complete)

### 5. AGENT_LOG.md ✅
- **Location:** `.oodatcaa/work/AGENT_LOG.md`
- **Entry Added:**
  - Timestamp: 2025-10-06T08:15:00+02:00
  - Agent: Planner (agent-planner-A)
  - Task: T001
  - Status: needs_plan → planning_complete
  - Framework selected: MLX-LM with rationale
  - Implementation plan summary (8 steps, 3 subtasks)
  - Deliverables (5 files created)
  - Sprint impact (T001-B01 ready, unblocks T002/T003)

### 6. Completion Report ✅
- **Location:** `.oodatcaa/work/reports/T001/planner.md` (this file)
- **Contents:** Complete report of Planner actions, deliverables, metrics, challenges, solutions, handoff notes

---

## Metrics

### Planning Efficiency
- **Duration:** ~18 minutes (Observe+Orient+Decide+Plan+Document)
- **Lines Written:** ~2,400 lines total
  - AGENT_PLAN.md: ~1,640 lines
  - TEST_PLAN.md: ~760 lines
  - SPRINT_QUEUE.json: +50 lines (3 subtasks)
  - SPRINT_PLAN.md: +70 lines (Sprint 4 section)
  - AGENT_LOG.md: +45 lines (concise entry)
  - Completion report: ~300 lines (this file)

### Complexity Metrics
- **Alternatives Analyzed:** 3 (MLX-LM, axolotl, direct HuggingFace)
- **Decision Factors:** 5 (M1 Max optimization, memory efficiency, ease of use, QLoRA support, future-proof)
- **Implementation Steps:** 8 steps (clear, sequential, time-estimated)
- **Subtasks Created:** 3 (T001-B01 ready, T001-B02 blocked, T001-T01 blocked)
- **Acceptance Criteria:** 8 ACs (all testable, measurable)
- **Quality Gates:** 8 gates (black, ruff, mypy, pytest, coverage, build, pip-audit, pip check)
- **Risks Identified:** 6 risks with mitigation strategies
- **Deliverables Specified:** 11 deliverables (7 docs + 3 scripts + 1 config)

### Plan Quality Indicators
- ✅ **Traceability:** Objective ID, Epic, Sprint, Dependencies documented
- ✅ **Problem Definition:** Current state, impact, problem clearly stated
- ✅ **Constraints:** Hardware, software, model, timeline constraints identified
- ✅ **Alternatives:** 3 alternatives evaluated with pros/cons
- ✅ **Decision Rationale:** 5 decision factors with explicit trade-offs
- ✅ **Exit Gates:** Every step has clear exit criteria
- ✅ **Risk Mitigation:** 6 risks with mitigation + contingency plans
- ✅ **Testability:** 8 ACs with exact validation commands
- ✅ **Handoff:** Clear handoff notes for Builder
- ✅ **Fallback:** Documented fallback plan (switch to axolotl)

---

## Challenges Encountered

### Challenge 1: Framework Selection Complexity
**Issue:** Both MLX-LM and axolotl have strong arguments, making selection non-trivial
- MLX-LM: Native M1 Max support (excellent), but smaller ecosystem and newer (concern)
- Axolotl: Battle-tested with rich community (excellent), but PyTorch MPS less optimized for M1 Max (concern)

**Solution:**
- Prioritized constraints: M1 Max optimization is CRITICAL (per OBJECTIVE.md), memory efficiency is HIGH priority
- MLX-LM's native Metal acceleration and unified memory optimization directly address top 2 constraints
- Documented fallback plan: If MLX-LM fails, switch to axolotl (+135 min total fallback cost, acceptable within Sprint 4 timeline)
- Decision made with confidence: MLX-LM is optimal for M1 Max-focused project

### Challenge 2: Memory Profiling Complexity
**Issue:** Estimating training memory for QLoRA is non-trivial (depends on batch size, gradient checkpointing, quantization)
- Can't run actual training in planning phase (no framework installed yet)
- Memory profile is CRITICAL AC (≤16GB target)

**Solution:**
- Step 5 (Memory Profiling) includes both inference memory (measurable) and training memory (estimated)
- Documented estimation method: QLoRA with batch size 1, 4-bit quantization (based on MLX-LM docs)
- Clear exit gate: Training memory estimate ≤16GB validated (Builder must verify)
- Risk mitigation: If memory >16GB, escalate to Refiner for plan adaptation (reduce batch size, more aggressive quantization, or switch framework)

### Challenge 3: Balancing Plan Detail vs. Flexibility
**Issue:** Too detailed plans constrain Builder, too vague plans cause confusion
- Need enough detail for Builder to execute autonomously
- Need flexibility for Builder to adapt to discoveries (e.g., model download issues, framework quirks)

**Solution:**
- 8-step plan provides clear structure without micro-managing
- Each step has exit gates (what must be achieved) but not implementation details (how to achieve it)
- Builder has autonomy to adapt within step constraints
- Documented alternatives and fallback plans give Builder options if primary path fails

---

## Solutions & Decisions

### Solution 1: MLX-LM Selection Rationale
**Decision:** Select Apple MLX-LM over axolotl and direct HuggingFace

**Rationale:**
1. **M1 Max Optimization (Critical):** Native Metal acceleration is non-negotiable for performance on our hardware. MLX-LM is purpose-built for M1/M2, providing significant advantage over PyTorch MPS backend.
2. **Memory Efficiency (High Priority):** Unified memory architecture optimization in MLX-LM aligns perfectly with ≤16GB RAM target. Apple engineers tuned this for M1/M2 characteristics.
3. **Ease of Use (Medium Priority):** Simple pip install with minimal dependencies reduces risk and setup time (60-90 min vs 120-150 min for axolotl).
4. **QLoRA Support (High Priority):** Built-in LoRA fine-tuning with quantization examples. Proven to work with 7B models on M1 Max.
5. **Apple Backing (Low Priority):** Official Apple support provides confidence in ongoing M1 Max optimization.

**Trade-offs Accepted:**
- Smaller ecosystem (acceptable — MLX-LM docs are sufficient for our use case)
- Portability (acceptable — OBJECTIVE.md explicitly targets M1 Max, not multi-platform)
- Newer framework (acceptable — Apple backing reduces risk)

**Alternative Rejected:**
- Axolotl: PyTorch MPS backend less optimized for M1 Max, more complex setup, higher dependency conflict risk
- Direct HuggingFace: Too high effort (240-360 min), reinventing wheel when frameworks exist

**Fallback Plan:** If MLX-LM has model compatibility or memory issues, switch to axolotl (+90 min setup, +15 min decision, +30 min validation = +135 min total fallback cost, acceptable within Sprint 4 buffer)

### Solution 2: 3-Subtask Breakdown
**Decision:** Break T001 into 3 subtasks (T001-B01, T001-B02, T001-T01)

**Rationale:**
1. **T001-B01 (Steps 1-5, 120 min):** Core work — research, install, model load, inference, memory profile. This is the "heavy lifting" subtask that validates framework choice.
2. **T001-B02 (Steps 6-8, 40 min):** Documentation and finalization — installation guide, dependencies, quality gates. Lighter work, depends on B01 success.
3. **T001-T01 (20 min):** Tester validation — all 8 ACs validated by independent Tester. Depends on B02 completion.

**Benefits:**
- Clear dependencies: B01 → B02 → T01 (sequential, no parallel work possible)
- Realistic estimates: 120 min (B01), 40 min (B02), 20 min (T01) = 180 min total
- Early validation: Tester validates before integration, catches issues early
- Builder autonomy: Each subtask has clear scope and exit gates

### Solution 3: CRITICAL AC6 (Memory ≤16GB)
**Decision:** Mark AC6 (Memory Profiling) as CRITICAL in TEST_PLAN.md

**Rationale:**
- ≤16GB training memory is a HARD constraint from OBJECTIVE.md (M1 Max with 32GB RAM, need headroom)
- If memory >16GB, entire plan must be revised (smaller batch size, more quantization, or framework switch)
- Memory profiling in Step 5 is the "gate" that validates framework feasibility

**Implementation:**
- AC6 marked as **CRITICAL** in both AGENT_PLAN.md and TEST_PLAN.md
- Test plan includes exact validation: `Training memory ≤16GB target validated`
- Risk mitigation documented: If >16GB, escalate to Refiner for adaptation
- Fallback options: Reduce batch size, gradient checkpointing, 2-bit quantization, switch to axolotl

---

## Handoff Notes for Builder

### What Builder Needs to Know

**1. Framework Selection:**
- **Selected:** Apple MLX-LM (Alternative 1)
- **Why:** M1 Max optimization, memory efficiency, ease of use, built-in QLoRA support
- **Fallback:** If MLX-LM fails (model incompatibility, memory issues), switch to axolotl

**2. Model Target:**
- **Model:** Qwen2.5-Coder-7B-Instruct (HuggingFace Hub)
- **Size:** ~14GB download, 7B parameters
- **Format:** HuggingFace format (MLX-LM can load directly)

**3. Memory Constraint (CRITICAL):**
- **Target:** ≤16GB training memory (M1 Max has 32GB, need headroom)
- **Validation:** Step 5 (Memory Profiling) — **CRITICAL AC6**
- **If Exceeded:** Escalate to Refiner (reduce batch size, more quantization, or switch framework)

**4. Proof-of-Concept Scope:**
- **In Scope:** Install MLX-LM, load Qwen2.5-Coder-7B-Instruct, run inference, profile memory, document setup
- **Out of Scope:** Actual training (T002), dataset creation (T003-T004), production deployment

**5. Success Criteria:**
- All 8 ACs pass (framework evaluation, installation, model loading, inference, memory profile, docs, dependencies, quality gates)
- **AC6 is CRITICAL** — Memory ≤16GB validated
- Quality gates pass (black, ruff, mypy, pytest, pip-audit)

**6. Timeline:**
- T001-B01: 120 minutes (Steps 1-5)
- T001-B02: 40 minutes (Steps 6-8)
- Total: 160 minutes (Builder work)

**7. Branch & Commits:**
- **Branch:** `feat/T001-step-01-framework-selection`
- **Commit Labels:** `[plan]` for planning artifacts, `[impl]` for code/config, `[test]` for test scripts, `[docs]` for documentation

**8. Quality Gates:**
- All must pass: black, ruff, mypy, pytest, coverage, build, pip-audit
- Zero regressions from Sprint 3 baseline (28 ruff errors, 401 mypy errors acceptable)

**9. Documentation:**
- Comprehensive guides for reproducibility (future sprints will reference)
- Installation guide: Step-by-step with exact commands
- Troubleshooting: Common M1 Max issues documented

**10. Handoff to Tester:**
- T001-T01 (Tester validation) has 8 ACs + 8 quality gates
- Tester uses TEST_PLAN.md for exact validation commands
- Tester must verify **AC6 (memory ≤16GB) is CRITICAL**

### Key Files to Reference

- **AGENT_PLAN.md:** Complete implementation plan (8 steps, exit gates, deliverables)
- **TEST_PLAN.md:** Test commands, validation criteria, troubleshooting
- **OBJECTIVE.md:** Training system requirements, constraints, success criteria
- **pyproject.toml:** Current dependencies (add MLX-LM dependencies)

### Questions Builder May Have

**Q1: What if MLX-LM doesn't support Qwen2.5-Coder-7B-Instruct?**
- **A:** Check MLX-LM documentation for Qwen support. If not supported, switch to axolotl (fallback plan documented in AGENT_PLAN.md, +135 min).

**Q2: What if model download fails?**
- **A:** Use HuggingFace CLI manual download (documented in TEST_PLAN.md troubleshooting). If persistent issues, check HuggingFace Hub status or use mirror.

**Q3: What if memory exceeds 16GB?**
- **A:** Escalate to Refiner. Options: reduce batch size to 1, enable gradient checkpointing, use 2-bit quantization, switch to axolotl. Refiner will adapt plan.

**Q4: What if inference generates gibberish?**
- **A:** Check model loaded correctly (AC4), verify tokenizer matches model, adjust inference parameters (lower temperature). Documented in TEST_PLAN.md troubleshooting.

**Q5: What if quality gates fail (ruff/mypy errors)?**
- **A:** New errors must be fixed. Baseline errors from Sprint 3 (28 ruff, 401 mypy) are acceptable. Focus on no regressions.

---

## Sprint Impact

### T001 Progress
- **Status:** needs_plan → **planning_complete** ✅
- **Subtasks Created:** 3 (T001-B01 ready, T001-B02 blocked, T001-T01 blocked)
- **Next Action:** Negotiator assigns T001-B01 to Builder

### Sprint 4 Progress
- **Tasks Planned:** 1/8 (12.5%)
- **Tasks Ready:** 1 subtask (T001-B01)
- **Tasks Blocked:** 7 tasks (T002-T008 blocked by T001)

### Dependencies Satisfied
- **T001-B01:** Ready (no dependencies)

### Dependencies Unblocked (After T001 Complete)
- **T002:** QLoRA Configuration & Environment Setup (depends on T001)
- **T003:** Training Dataset Schema & Generator (depends on T001)

### Critical Path
- T001 → T002 → T004 → T005 → T006 → T008
- T001 is the **first task** on critical path (all downstream tasks blocked)

### Objective Progress
- **Current:** ~25% (Sprint 3 complete - MCP foundation)
- **After T001:** ~27% (framework selection complete)
- **Sprint 4 Target:** ~45% (training foundation - dataset + QLoRA + docs)

---

## Lessons Learned

### Lesson 1: M1 Max-Specific Constraints Clarify Decisions
**Observation:** Framework selection was simplified by focusing on M1 Max hardware constraint
- MLX-LM's native Metal acceleration became clear differentiator
- PyTorch MPS backend (axolotl) less compelling for M1 Max-focused project
- Hardware-first constraint prioritization led to confident decision

**Application:** When evaluating alternatives, prioritize constraints from OBJECTIVE.md first, then compare alternatives against top constraints

### Lesson 2: Memory Profiling as Critical Gate
**Observation:** ≤16GB memory target is HARD constraint that determines framework feasibility
- Memory profiling (Step 5, AC6) is the "gate" that validates plan
- If memory >16GB, entire plan must be revised (not just tuned)

**Application:** Identify CRITICAL ACs early in planning, mark them explicitly, create fallback plans

### Lesson 3: Fallback Plans Reduce Risk
**Observation:** Documenting fallback plan (switch to axolotl) provides confidence in primary plan
- If MLX-LM fails, Builder has clear next steps (+135 min fallback cost)
- Fallback plan was costed (90 min setup, 15 min decision, 30 min validation)
- Reduces analysis paralysis — we can make confident decision knowing fallback exists

**Application:** Always document fallback plans for high-risk decisions, especially when exploring newer technologies (MLX-LM is newer than PyTorch/axolotl)

### Lesson 4: Subtask Breakdown Improves Estimates
**Observation:** Breaking T001 into 3 subtasks (120 min, 40 min, 20 min) creates realistic estimates
- T001-B01 (core work) is isolated from T001-B02 (documentation/finalization)
- Tester validation (T001-T01) is separated, preventing Builder from skipping test validation
- Each subtask has clear scope and dependencies

**Application:** Break tasks into 2-4 subtasks when complexity is Medium or Large, separate "core work" from "finalization" from "validation"

---

## Next Steps

**Immediate Next Action:**
1. **Negotiator** reads SPRINT_QUEUE.json and AGENT_LOG.md
2. **Negotiator** assigns T001-B01 to Builder (WIP: builder 1/3, within limit)
3. **Builder** executes T001-B01 (Steps 1-5: Research, Install, Model Load, Inference, Memory Profile)

**After T001-B01 Complete:**
1. **Negotiator** assigns T001-B02 to Builder (Steps 6-8: Docs, Dependencies, Quality Gates)
2. **Builder** executes T001-B02

**After T001-B02 Complete:**
1. **Negotiator** assigns T001-T01 to Tester (Validation: All 8 ACs)
2. **Tester** validates using TEST_PLAN.md commands
3. **If All ACs Pass:** Tester marks T001-T01 as ready_for_integrator
4. **If Any AC Fails:** Tester marks T001-T01 as needs_adapt, Refiner analyzes

**After T001-T01 Complete:**
1. **Negotiator** assigns T001 to Integrator (Merge to main)
2. **Integrator** merges branch, tags T001-complete, updates CHANGELOG
3. **T002 and T003 unblocked:** Negotiator assigns T002 or T003 to Planner (next planning cycle)

---

## Completion Summary

**Plan Status:** ✅ COMPLETE  
**Deliverables:** 6 files created (AGENT_PLAN, TEST_PLAN, SPRINT_QUEUE, SPRINT_PLAN, AGENT_LOG, completion report)  
**Lines Written:** ~2,400 lines total  
**Duration:** ~18 minutes  
**Framework Selected:** Apple MLX-LM (Alternative 1)  
**Subtasks Created:** 3 (T001-B01 ready, T001-B02 blocked, T001-T01 blocked)  
**Next Action:** Negotiator assigns T001-B01 to Builder

**Ready for Builder:** T001-B01 (120 minutes estimated)

---

**Planner Agent:** agent-planner-A  
**Report Generated:** 2025-10-06T08:15:00+02:00  
**Sprint:** Sprint 4 (Training System Foundation)  
**Objective:** Small Coder Model Training with MCP Integration
