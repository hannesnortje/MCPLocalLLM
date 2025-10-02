# Test Plan — W001: Analyze MCP Source Structure

**Work Item:** W001 | **Sprint:** 1 | **Created:** 2025-10-01

---

## Test Commands

Since W001 is an analysis task with no code changes, standard CI commands verify the repository remains intact:

### Format Check
```bash
black --check .
```
**Expected:** PASS (no files changed, so formatting unchanged)

### Lint Check
```bash
ruff check .
```
**Expected:** PASS (no code modified)

### Type Check
```bash
mypy .
```
**Expected:** PASS (no type changes)

### Unit Tests
```bash
pytest -q
```
**Expected:** PASS (existing tests continue to work)

### Integration Tests
```bash
pytest -q tests/acceptance
```
**Expected:** PASS (no integration changes)

### Coverage Check
```bash
pytest --cov=src --cov-report=term-missing --cov-fail-under=85
```
**Expected:** PASS (coverage unchanged, only analysis docs added)

### Build Check
```bash
python -m build
```
**Expected:** PASS (package still builds)

### Security Audit
```bash
pip-audit
```
**Expected:** PASS (no new dependencies added in W001)

**Optional:**
```bash
bandit -r src -ll
```
**Expected:** PASS (no code changes)

---

## Acceptance Testing

### Manual Verification Tasks

**AC1: Complete inventory of MCP files**
- [ ] Open `.oodatcaa/work/analysis/W001/mcp_structure_inventory.md`
- [ ] Verify all directories from `/media/hannesn/storage/Code/MCP/` are listed
- [ ] Verify categorization: ESSENTIAL, OPTIONAL, or EXCLUDE for each
- [ ] Spot check: Confirm `src/ui/` is marked EXCLUDE
- [ ] Spot check: Confirm `src/handlers/` is marked ESSENTIAL

**AC2: Documented list of files to copy**
- [ ] Open `.oodatcaa/work/analysis/W001/essential_components.md`
- [ ] Verify inclusion list has specific file paths
- [ ] Verify each entry has a "Purpose" justification
- [ ] Check: `src/mcp_server.py` included
- [ ] Check: `src/ui/` explicitly excluded

**AC3: Documented list of files to exclude**
- [ ] Same file as AC2
- [ ] Verify exclusion list exists with rationale
- [ ] Check: UI components (PySide6-related) listed
- [ ] Check: Example files identified for exclusion

**AC4: File conflict resolution strategy**
- [ ] Open `.oodatcaa/work/analysis/W001/conflict_resolution.md`
- [ ] Verify each root-level file conflict has resolution: MERGE/COPY/SKIP
- [ ] Check: `pyproject.toml` → MERGE strategy documented
- [ ] Check: `.oodatcaa/` → NEVER TOUCH explicitly stated
- [ ] Verify directory conflicts (src/, tests/, docs/) have coexist/merge strategy

**AC5: Complete dependency list**
- [ ] Open `.oodatcaa/work/analysis/W001/dependencies.md`
- [ ] Verify all MCP dependencies listed from `pyproject.toml`
- [ ] Check: Core deps (mcp, qdrant-client, sentence-transformers) present
- [ ] Check: UI deps (PySide6, websockets) marked for exclusion
- [ ] Verify version compatibility notes for Python 3.11+

**AC6: Migration checklist**
- [ ] Open `.oodatcaa/work/analysis/W001/migration_checklist.md`
- [ ] Verify checklist has actionable steps (checkbox format)
- [ ] Verify steps are ordered logically (dependencies first)
- [ ] Check: OODATCAA verification step included
- [ ] Check: Package rename step included

**AC7: OODATCAA preservation strategy**
- [ ] Review all analysis documents
- [ ] Confirm `.oodatcaa/` exclusion mentioned in conflict resolution
- [ ] Confirm no analysis suggests modifying OODATCAA files
- [ ] Verify migration checklist has OODATCAA verification step

**AC8: Documentation clarity**
- [ ] Have Builder agent (or reviewer) read summary
- [ ] Confirm: No ambiguity in what to copy
- [ ] Confirm: No ambiguity in how to resolve conflicts
- [ ] Confirm: No missing information for W002 execution

**AC9: Analysis coverage**
- [ ] Verify `src/` directory analysis complete (all subdirs)
- [ ] Verify `tests/` directory analyzed
- [ ] Verify `docs/` directory analyzed
- [ ] Verify `scripts/` directory analyzed
- [ ] Verify `policy/` directory analyzed
- [ ] Verify root-level files analyzed

**AC10: Risk mitigation strategies**
- [ ] Open `.oodatcaa/work/AGENT_PLAN.md` section 2 (Constraints/Risks)
- [ ] Verify each identified risk has mitigation strategy
- [ ] Check: OODATCAA overwrite risk → Explicit exclusion list
- [ ] Check: UI bloat risk → Exclusion of PySide6
- [ ] Check: Incomplete migration risk → Systematic checklist

---

## Performance Tests

**Not applicable for W001** (analysis task, no performance impact)

---

## Integration Tests to Add

**Not applicable for W001** (no new code to test)

Future W002 will need:
- Test MCP server initialization after migration
- Test memory CRUD operations
- Test policy system functionality

---

## Test Artifacts

All analysis documents serve as test artifacts:

1. `.oodatcaa/work/analysis/W001/mcp_structure_inventory.md`
2. `.oodatcaa/work/analysis/W001/essential_components.md`
3. `.oodatcaa/work/analysis/W001/conflict_resolution.md`
4. `.oodatcaa/work/analysis/W001/dependencies.md`
5. `.oodatcaa/work/analysis/W001/pyproject_toml_updates.md`
6. `.oodatcaa/work/analysis/W001/migration_checklist.md`
7. `.oodatcaa/work/analysis/W001/W001_ANALYSIS_SUMMARY.md`

---

## Test Execution Order

1. **Pre-execution:** Run all standard CI commands (baseline)
2. **During execution:** Builder creates analysis artifacts (Steps 1-6)
3. **Post-execution:** Manual verification of all 10 ACs
4. **Final:** Re-run all standard CI commands (should still pass)
5. **Sign-off:** Negotiator reviews summary and approves

---

## Exit Criteria

- [ ] All standard CI commands pass (black, ruff, mypy, pytest, build, pip-audit)
- [ ] All 10 acceptance criteria manually verified
- [ ] All 7 analysis artifacts exist and are complete
- [ ] Negotiator approval documented in AGENT_LOG.md
- [ ] W002 unblocked in SPRINT_QUEUE.json

---

**Test Plan Status:** ✅ APPROVED  
**Ready for:** Builder Agent execution
