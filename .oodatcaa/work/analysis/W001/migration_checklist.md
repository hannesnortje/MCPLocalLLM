# W001 Step 5: MCP Server Migration Checklist

**Work Item:** W001 | **Sprint:** 1 | **Created:** 2025-10-02  
**Purpose:** Executable checklist for W002 (Execute MCP Server Migration)

---

## Executive Summary

This checklist provides a step-by-step guide for migrating the MCP server from `/media/hannesn/storage/Code/MCP/` to this project. Each step is designed to be executed sequentially with verification points.

**Migration Approach:** Selective copy with explicit inclusion list (NOT bulk copy)  
**Estimated Time:** 2-3 hours  
**Risk Level:** LOW (all conflicts resolved, protection strategies in place)

---

## Pre-Migration Setup

### ☐ 1. Create Baseline Tag

```bash
cd /media/hannesn/storage/Code/MCPLocalLLM
git tag "pre/W002-$(date -Iseconds)"
git push origin "pre/W002-$(date -Iseconds)"
```

**Purpose:** Enable rollback if migration fails  
**Verification:** `git tag | grep pre/W002`

---

### ☐ 2. Create Migration Branch

```bash
git checkout main
git pull origin main
git checkout -b feat/W002-step-01-copy-mcp-core
```

**Purpose:** Isolated work environment  
**Verification:** `git branch --show-current` → `feat/W002-step-01-copy-mcp-core`

---

### ☐ 3. Verify Source Exists

```bash
ls -la /media/hannesn/storage/Code/MCP/
```

**Purpose:** Confirm MCP source is accessible  
**Verification:** Directory exists with expected structure (src/, policy/, docs/, etc.)

---

## Phase 1: Copy Core MCP Source Files

### ☐ 4. Create Target Directory Structure

```bash
cd /media/hannesn/storage/Code/MCPLocalLLM
mkdir -p src/mcp
mkdir -p tests/mcp
mkdir -p docs/mcp
mkdir -p scripts
```

**Purpose:** Prepare coexistence with existing modules  
**Verification:** `ls -la src/` → Shows both `mdnotes/` and `mcp/`

---

### ☐ 5. Copy Core MCP Server Files

```bash
# Copy main server files
cp /media/hannesn/storage/Code/MCP/src/mcp_server.py src/mcp/
cp /media/hannesn/storage/Code/MCP/src/memory_manager.py src/mcp/
cp /media/hannesn/storage/Code/MCP/src/qdrant_manager.py src/mcp/
cp /media/hannesn/storage/Code/MCP/src/markdown_processor.py src/mcp/
cp /media/hannesn/storage/Code/MCP/src/config.py src/mcp/

# Copy __init__.py
cp /media/hannesn/storage/Code/MCP/src/__init__.py src/mcp/
```

**Purpose:** Copy essential MCP server modules  
**Verification:** `ls src/mcp/*.py` → 6 files present  
**Files Copied:** 6 core modules

---

### ☐ 6. Copy MCP Subdirectories

```bash
# Copy handlers (exclude ui/)
cp -r /media/hannesn/storage/Code/MCP/src/handlers src/mcp/
cp -r /media/hannesn/storage/Code/MCP/src/memory src/mcp/
cp -r /media/hannesn/storage/Code/MCP/src/prompts src/mcp/
cp -r /media/hannesn/storage/Code/MCP/src/tools src/mcp/

# IMPORTANT: Do NOT copy src/ui/ directory
```

**Purpose:** Copy supporting modules, exclude UI  
**Verification:** 
- `ls -la src/mcp/` → Shows handlers/, memory/, prompts/, tools/
- `ls src/mcp/ui 2>/dev/null` → Should fail (ui not copied)  
**Directories Copied:** 4 subdirectories (handlers, memory, prompts, tools)

---

### ☐ 7. Copy Policy Files

```bash
mkdir -p policy
cp -r /media/hannesn/storage/Code/MCP/policy/*.md policy/
```

**Purpose:** Copy governance policy documents  
**Verification:** `ls policy/*.md` → 4 markdown files  
**Files Copied:** ~4 policy markdown files

---

### ☐ 8. Copy Documentation

```bash
# Copy MCP-specific docs to subdirectory
cp -r /media/hannesn/storage/Code/MCP/docs/* docs/mcp/
```

**Purpose:** Preserve MCP documentation  
**Verification:** `ls docs/mcp/` → MCP architecture and API docs present  
**Note:** Existing docs/ files (CONTRIBUTING.md, SECURITY.md) remain untouched

---

### ☐ 9. Copy Scripts

```bash
cp /media/hannesn/storage/Code/MCP/scripts/*.sh scripts/ 2>/dev/null || true
cp /media/hannesn/storage/Code/MCP/scripts/*.py scripts/ 2>/dev/null || true
```

**Purpose:** Copy MCP utility scripts  
**Verification:** `ls scripts/` → MCP helper scripts present

---

### ☐ 10. Copy Server Entry Points

```bash
cp /media/hannesn/storage/Code/MCP/server.py .
cp /media/hannesn/storage/Code/MCP/launcher.py . 2>/dev/null || true
cp /media/hannesn/storage/Code/MCP/memory_server.py . 2>/dev/null || true
```

**Purpose:** Copy MCP server launch scripts  
**Verification:** `ls *.py | grep -E '(server|launcher|memory_server)'`

---

## Phase 2: Copy Infrastructure Files

### ☐ 11. Copy Docker Configuration

```bash
cp /media/hannesn/storage/Code/MCP/docker-compose.yml .
```

**Purpose:** Qdrant database setup  
**Verification:** `cat docker-compose.yml | grep qdrant`  
**Action:** Review and update service names if needed

---

### ☐ 12. Copy Environment Examples

```bash
cp /media/hannesn/storage/Code/MCP/.env.example .
cp /media/hannesn/storage/Code/MCP/config.example.yaml . 2>/dev/null || true
```

**Purpose:** Configuration templates  
**Verification:** `ls .env.example config.example.yaml`

---

### ☐ 13. Merge .gitignore

```bash
# Add MCP-specific entries to existing .gitignore
cat >> .gitignore << 'EOF'

# MCP specific
qdrant_storage/
.env
policy/*.lock
EOF
```

**Purpose:** Ignore MCP runtime files  
**Verification:** `git diff .gitignore` → Shows added entries  
**Note:** Existing .gitignore entries preserved

---

## Phase 3: Verification & Protection

### ☐ 14. Verify OODATCAA Protection

```bash
git status .oodatcaa/
```

**Expected:** NO changes to `.oodatcaa/` directory  
**Rollback Trigger:** ANY modifications to `.oodatcaa/` → ABORT migration

---

### ☐ 15. Verify mdnotes Preservation

```bash
git status src/mdnotes/
git diff src/mdnotes/
```

**Expected:** NO changes to `src/mdnotes/` module  
**Rollback Trigger:** ANY modifications to `src/mdnotes/` → ABORT migration

---

### ☐ 16. Verify MCP Files Copied

```bash
# Count copied files
echo "Core MCP files: $(find src/mcp -name '*.py' | wc -l)"
echo "Policy files: $(find policy -name '*.md' | wc -l)"
echo "MCP docs: $(find docs/mcp -type f | wc -l)"
```

**Expected:**
- Core MCP files: ~40+ Python files
- Policy files: ~4 markdown files
- MCP docs: ~5+ documentation files

---

### ☐ 17. Check for Unwanted UI Files

```bash
# Should return nothing
find src/mcp -name '*ui*' -o -name '*UI*' -o -name '*pyside*'
```

**Expected:** No results (UI files excluded)  
**Rollback Trigger:** Any UI files found → Remove them

---

## Phase 4: Initial Commit

### ☐ 18. Stage Core MCP Files

```bash
git add src/mcp/
git add policy/
git add docs/mcp/
git add scripts/
git add server.py launcher.py memory_server.py
git add docker-compose.yml .env.example
git add .gitignore
```

**Purpose:** Stage all copied files  
**Verification:** `git status` → Shows staged files in green

---

### ☐ 19. Commit Migration

```bash
git commit -m "[impl] W002: Copy core MCP server files from source repository

- Copy src/mcp/ with handlers, memory, prompts, tools (exclude ui/)
- Copy policy/ governance documents
- Copy docs/mcp/ documentation
- Copy server.py and helper scripts
- Add docker-compose.yml for Qdrant setup
- Merge .gitignore with MCP-specific entries
- Preserve .oodatcaa/ and src/mdnotes/ untouched"
```

**Purpose:** Record migration in git history  
**Verification:** `git log -1 --stat` → Shows commit details

---

## Phase 5: Post-Migration Validation

### ☐ 20. Verify Python Syntax

```bash
source .venv/bin/activate
python -m py_compile src/mcp/*.py
```

**Expected:** No syntax errors  
**Note:** Import errors expected (dependencies not installed yet)

---

### ☐ 21. Verify File Count

```bash
echo "Expected: 67 essential MCP files"
echo "Actual: $(find src/mcp policy docs/mcp scripts -type f | wc -l) files copied"
```

**Expected:** ~60-70 files (close to 67 essential files identified in analysis)

---

### ☐ 22. Run Existing Tests (Smoke Test)

```bash
source .venv/bin/activate
pytest -q tests/test_smoke.py
```

**Expected:** PASS (existing mdnotes tests unaffected)  
**Rollback Trigger:** Existing tests fail → Investigate changes to mdnotes

---

## Phase 6: Push to Remote

### ☐ 23. Push Migration Branch

```bash
git push origin feat/W002-step-01-copy-mcp-core
```

**Purpose:** Backup migration work  
**Verification:** Branch visible on GitHub

---

### ☐ 24. Update SPRINT_QUEUE.json

```bash
# Update W002 status from "needs_plan" to "in_progress"
# This will be done by the Builder agent in the final step
```

---

## Rollback Plan

If migration fails at any point:

```bash
# Restore from baseline
cd /media/hannesn/storage/Code/MCPLocalLLM
git reset --hard pre/W002-<timestamp>
git push origin feat/W002-step-01-copy-mcp-core --force-with-lease

# Document failure
echo "Migration aborted: <reason>" >> .oodatcaa/work/SPRINT_DISCUSS.md
```

**Trigger Conditions:**
- Any modifications to `.oodatcaa/`
- Any modifications to `src/mdnotes/`
- Critical MCP files missing (>10% of expected files)
- Existing tests fail

---

## Post-Migration Tasks (W003-W004)

After W002 completes, the following tasks will address:

**W003 (Integrate Dependencies):**
- [ ] Merge pyproject.toml with MCP dependencies
- [ ] Install MCP packages: `pip install -e .[dev]`
- [ ] Verify imports: `python -c "import mcp; import qdrant_client"`

**W004 (Adapt for Training):**
- [ ] Fix import statements (flat imports → `mcp.` prefix)
- [ ] Remove UI references in code
- [ ] Update package name: "mcp-memory-server" → "mcp-local-llm"
- [ ] Run quality gates: black, ruff, mypy

---

## Summary

**Total Steps:** 24 checklist items  
**Estimated Time:** 2-3 hours  
**Files to Copy:** ~67 essential files  
**Directories:** src/mcp/, policy/, docs/mcp/, scripts/  
**Protected:** .oodatcaa/, src/mdnotes/  
**Next Task:** W003 (Integrate MCP Dependencies)

---

**Checklist Status:** ✅ READY FOR W002 EXECUTION  
**Safety Level:** ✅ HIGH (all protections in place, rollback plan ready)

