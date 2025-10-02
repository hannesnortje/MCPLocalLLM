# Agent Plan — W002: Execute MCP Server Migration

**Objective:** OBJ-2025-002 | **Epic:** MCP Integration | **Sprint:** 1 | **Work Item:** W002  
**Plan Version:** 1.0 | **Created:** 2025-10-02 | **Agent:** Planner

---

## Problem Statement

Execute the MCP server migration from `/media/hannesn/storage/Code/MCP/` to this project, following the comprehensive analysis and migration checklist created in W001. Copy 67 essential MCP files (core server, memory, handlers, tools, policy) while preserving OODATCAA framework and existing `mdnotes` module.

**Context:** W001 analysis complete with LOW risk assessment. Migration checklist provides 24 step-by-step instructions. Selective copy approach minimizes risk of conflicts.

---

## Constraints / Risks

**Constraints:**
- MUST preserve `.oodatcaa/` directory (verified in Steps 14, rollback trigger if violated)
- MUST keep `src/mdnotes/` module working (verified in Step 15)
- MUST exclude UI components: `src/ui/`, PySide6, websockets dependencies
- MUST use selective copy (NOT `cp -r /source/* /dest/`)
- Python >=3.11,<3.13 (compatibility verified in W001)

**Key Risks & Mitigation:**
- **OODATCAA overwrite (HIGH impact):** Verification step 14, rollback trigger if any changes detected
- **mdnotes module break (HIGH):** Verification step 15, smoke test in step 22
- **UI files accidentally copied (MEDIUM):** Explicit exclusion in commands, verification in step 17
- **Incomplete migration (MEDIUM):** File count verification in step 21 (~67 expected files)
- **Syntax errors in copied files (LOW):** Python syntax check in step 20

---

## Definition of Done

**Functional:**
- [ ] **AC1:** All 67 essential MCP files copied to correct locations (src/mcp/, policy/, docs/mcp/)
- [ ] **AC2:** No UI files copied (src/ui/ excluded, verified in step 17)
- [ ] **AC3:** Infrastructure files copied: docker-compose.yml, .env.example, server.py
- [ ] **AC4:** .gitignore merged with MCP-specific entries (qdrant_storage/, .env)
- [ ] **AC5:** `.oodatcaa/` directory untouched (step 14 verification)
- [ ] **AC6:** `src/mdnotes/` module preserved (step 15 verification)
- [ ] **AC7:** Existing tests still pass (step 22 smoke test)

**Non-Functional:**
- [ ] **AC8:** File count ~60-70 files (step 21, matches W001 analysis)
- [ ] **AC9:** No Python syntax errors in copied files (step 20)
- [ ] **AC10:** Git history clean with descriptive commit (step 19)

---

## Alternatives & Choice

**Alternative 1:** Bulk copy with cleanup → ❌ REJECTED (High risk of OODATCAA overwrite)  
**Alternative 2:** Selective copy per W001 migration checklist → ✅ **CHOSEN** (Low risk, traceable)  
**Alternative 3:** Git submodule → ❌ REJECTED (OBJECTIVE requires "copy and adapt")

**Rationale:** Alternative 2 was validated in W001 analysis (LOW risk), provides step-by-step verification, and aligns with OBJECTIVE.md requirements.

---

## Implementation Plan

### Step 1: Pre-Migration Setup & Baseline
**Branch:** `feat/W002-step-01-copy-mcp-core`  
**Migration Checklist:** Steps 1-3  
**Actions:**
1. Create baseline tag: `pre/W002-$(date -Iseconds)`
2. Create and checkout migration branch
3. Verify MCP source exists and is accessible

**Exit Gate:** Baseline tag created, branch ready, source verified

---

### Step 2: Copy Core MCP Source Files
**Migration Checklist:** Steps 4-6  
**Actions:**
1. Create target directory structure (src/mcp/, tests/mcp/, docs/mcp/)
2. Copy 6 core MCP server files (mcp_server.py, memory_manager.py, qdrant_manager.py, markdown_processor.py, config.py, __init__.py)
3. Copy 4 subdirectories: handlers/, memory/, prompts/, tools/ (EXCLUDE ui/)

**Expected Files:** ~40+ Python files in src/mcp/  
**Exit Gate:** Core modules copied, no ui/ directory present

---

### Step 3: Copy Supporting Files & Infrastructure
**Migration Checklist:** Steps 7-12  
**Actions:**
1. Copy policy/ governance documents (~4 markdown files)
2. Copy docs/mcp/ documentation
3. Copy scripts/ directory
4. Copy server entry points: server.py, launcher.py, memory_server.py
5. Copy docker-compose.yml for Qdrant setup
6. Copy .env.example and config.example.yaml

**Expected Files:** ~20 additional files  
**Exit Gate:** Infrastructure ready, documentation copied

---

### Step 4: Merge Configuration Files
**Migration Checklist:** Step 13  
**Actions:**
1. Merge .gitignore with MCP-specific entries:
   - qdrant_storage/
   - .env
   - policy/*.lock

**Exit Gate:** .gitignore updated without removing existing entries

---

### Step 5: Critical Verification & Protection Checks
**Migration Checklist:** Steps 14-17  
**Actions:**
1. **CRITICAL:** Verify `.oodatcaa/` untouched → `git status .oodatcaa/` → NO changes
2. **CRITICAL:** Verify `src/mdnotes/` preserved → `git status src/mdnotes/` → NO changes
3. Verify MCP files copied: ~40+ Python files, ~4 policy files, ~5 docs
4. Verify NO UI files present: `find src/mcp -name '*ui*'` → NO results

**Exit Gate:** All protection checks PASS, rollback if any critical check fails

---

### Step 6: Commit Migration Work
**Migration Checklist:** Steps 18-19  
**Actions:**
1. Stage all copied files (src/mcp/, policy/, docs/mcp/, scripts/, server.py, etc.)
2. Commit with `[impl]` label and descriptive message
3. Include file counts and exclusions in commit message

**Exit Gate:** Clean git commit with full migration recorded

---

### Step 7: Post-Migration Validation
**Migration Checklist:** Steps 20-22  
**Actions:**
1. Run Python syntax check on all src/mcp/*.py files
2. Verify file count: ~60-70 files total (matches W001 analysis)
3. **CRITICAL:** Run existing tests: `pytest -q tests/test_smoke.py` → MUST PASS

**Exit Gate:** No syntax errors, file count correct, existing tests pass

---

### Step 8: Push & Update Documentation
**Migration Checklist:** Steps 23-24  
**Actions:**
1. Push migration branch to origin
2. Update SPRINT_QUEUE.json: W002 status → awaiting_test
3. Update AGENT_LOG.md with migration summary
4. Release locks

**Exit Gate:** Work pushed, documentation updated, ready for tester

---

## Testing Strategy

See TEST_PLAN.md. Summary: Critical protection checks (OODATCAA, mdnotes), file count verification, syntax validation, existing tests smoke test.

**Rollback Triggers:**
- ANY modifications to `.oodatcaa/`
- ANY modifications to `src/mdnotes/`
- Critical MCP files missing (>10% of expected 67 files)
- Existing tests fail

---

## Rollback Plan

**Baseline:** `pre/W002-<timestamp>` (created in Step 1)  
**Trigger Conditions:** Any critical verification failure in Step 5 or Step 7  
**Steps:**
```bash
git reset --hard pre/W002-<timestamp>
git push origin feat/W002-step-01-copy-mcp-core --force-with-lease
echo "Migration aborted: <reason>" >> .oodatcaa/work/SPRINT_DISCUSS.md
```

---

## Branch & Commits

**Branch:** `feat/W002-step-01-copy-mcp-core`  
**Commit Labels:** `[impl]` for migration execution  
**PR:** Single PR after all verification passes  
**Merge Strategy:** No-FF merge to preserve feature branch history

---

## Dependencies

**Upstream:** W001 (COMPLETE - analysis ready)  
**Downstream:** W003 (Integrate MCP Dependencies), W004 (Adapt MCP for Training)

**Artifacts Required from W001:**
- `.oodatcaa/work/analysis/W001/migration_checklist.md` ✅
- `.oodatcaa/work/analysis/W001/essential_components.md` ✅
- `.oodatcaa/work/analysis/W001/conflict_resolution.md` ✅

---

## Effort Estimate

**Complexity:** M (Medium) | **Time:** 2-3 hours  
- Step 1 (Setup): 15 min
- Steps 2-3 (Copy files): 45 min
- Step 4 (Config merge): 15 min
- Step 5 (Verification): 20 min
- Step 6 (Commit): 10 min
- Step 7 (Validation): 20 min
- Step 8 (Push & docs): 15 min

**Risk Level:** LOW (per W001 analysis, comprehensive verification in place)

---

## Builder Task Breakdown

**W002-B01:** Steps 1-3 (Setup + Core Copy)  
**W002-B02:** Steps 4-6 (Config + Verification + Commit)  
**W002-B03:** Steps 7-8 (Validation + Push)

**Tester Task:**  
**W002-T01:** Verify all 10 ACs, run standard CI gates

---

**Status:** ✅ APPROVED | **Ready for:** Builder Agent Execution
