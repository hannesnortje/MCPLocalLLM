# W001 Step 4: MCP Dependencies Analysis

**Work Item:** W001 | **Sprint:** 1 | **Created:** 2025-10-02  
**Purpose:** Extract and analyze all MCP dependencies for integration into this project

---

## Executive Summary

**Total MCP Dependencies:** 9 core + 3 utils + 4 UI (excluded) + 6 dev = 22 total  
**Dependencies to Add:** 12 (9 core + 3 utils, excluding 4 UI packages)  
**Dev Dependencies to Add:** 2 (pytest-asyncio, types-markdown)  
**Compatibility Status:** ✅ ALL COMPATIBLE with Python >=3.11  
**Version Conflicts:** NONE - All MCP deps compatible with current project deps

---

## MCP Source Dependencies (from pyproject.toml)

### Core Dependencies (Poetry Format)

```toml
python = "^3.10,<3.13"
mcp = "^1.13.1"
qdrant-client = "^1.7.0"
sentence-transformers = "^2.5.1"
numpy = "^1.26.0"
python-dotenv = "^1.0.0"
markdown = "^3.5.0"
beautifulsoup4 = "^4.12.0"
aiofiles = "^24.1.0"
pyyaml = "^6.0.0"
```

### UI Dependencies (EXCLUDE - Not Needed for Training)

```toml
PySide6 = "^6.7.0"        # Qt6 desktop UI - NOT NEEDED
requests = "^2.32.1"      # HTTP fallback - NOT NEEDED (have aiohttp)
websockets = "^12.0"      # WebSocket UI updates - NOT NEEDED
aiohttp = "^3.9.1"        # Async HTTP - INCLUDE (useful for MCP)
```

### Dev Dependencies

```toml
black = "^25.1.0"         # Already in current project
flake8 = "^7.3.0"         # Current project uses ruff instead
mypy = "^1.17.1"          # Already in current project
pytest = "^8.4.1"         # Already in current project
pytest-asyncio = "^1.1.0" # NEW - Needed for MCP async tests
types-markdown = "^3.5.0" # NEW - Type stubs for markdown package
```

---

## Dependency Categorization

### ✅ Core MCP Dependencies (INCLUDE - 9 packages)

| Package | MCP Version | Purpose | Setuptools Format |
|---------|-------------|---------|-------------------|
| `mcp` | ^1.13.1 | Model Context Protocol SDK | `mcp>=1.13.1,<2.0.0` |
| `qdrant-client` | ^1.7.0 | Vector database client | `qdrant-client>=1.7.0,<2.0.0` |
| `sentence-transformers` | ^2.5.1 | Text embeddings | `sentence-transformers>=2.5.1,<3.0.0` |
| `numpy` | ^1.26.0 | Numerical arrays | `numpy>=1.26.0,<2.0.0` |
| `python-dotenv` | ^1.0.0 | Environment config | `python-dotenv>=1.0.0,<2.0.0` |
| `markdown` | ^3.5.0 | Markdown parsing | `markdown>=3.5.0,<4.0.0` |
| `beautifulsoup4` | ^4.12.0 | HTML/XML parsing | `beautifulsoup4>=4.12.0,<5.0.0` |
| `aiofiles` | ^24.1.0 | Async file I/O | `aiofiles>=24.1.0,<25.0.0` |
| `pyyaml` | ^6.0.0 | YAML parsing | `pyyaml>=6.0.0,<7.0.0` |

**Justification:** All essential for MCP memory system, policy management, and vector search

---

### ✅ Utility Dependencies (INCLUDE - 1 package)

| Package | MCP Version | Purpose | Setuptools Format |
|---------|-------------|---------|-------------------|
| `aiohttp` | ^3.9.1 | Async HTTP client | `aiohttp>=3.9.1,<4.0.0` |

**Justification:** Useful for MCP communication, async web requests in training pipeline

**Note:** Excluding `requests` (redundant with aiohttp) and `websockets` (UI-specific)

---

### ❌ UI Dependencies (EXCLUDE - 3 packages)

| Package | MCP Version | Purpose | Exclusion Reason |
|---------|-------------|---------|------------------|
| `PySide6` | ^6.7.0 | Qt6 desktop UI | Training system has no GUI |
| `websockets` | ^12.0 | WebSocket client | Used only for UI real-time updates |
| `requests` | ^2.32.1 | HTTP requests | Redundant with aiohttp (async preferred) |

**Total Size Saved:** ~150MB (PySide6 is very large)

---

### ✅ Dev Dependencies (ADD - 2 packages)

| Package | MCP Version | Current Project | Action | Setuptools Format |
|---------|-------------|-----------------|--------|-------------------|
| `pytest-asyncio` | ^1.1.0 | Not present | **ADD** | `pytest-asyncio>=1.1.0,<2.0.0` |
| `types-markdown` | ^3.5.0 | Not present | **ADD** | `types-markdown>=3.5.0,<4.0.0` |
| `black` | ^25.1.0 | ✅ >=24.0.0 | Keep current | No change |
| `mypy` | ^1.17.1 | ✅ >=1.8.0 | Keep current | No change |
| `pytest` | ^8.4.1 | ✅ >=8.0.0 | Keep current | No change |
| `flake8` | ^7.3.0 | ❌ Uses ruff | **SKIP** | N/A |

**Justification:**
- `pytest-asyncio`: Required for MCP async test cases
- `types-markdown`: Type stubs for mypy strict mode compliance
- Skip `flake8`: Current project uses `ruff` (faster, more features)

---

## Version Compatibility Analysis

### Python Version Requirements

| Project | Python Version | Compatible? |
|---------|----------------|-------------|
| **Current** | >=3.11 | ✅ Yes |
| **MCP** | ^3.10,<3.13 | ✅ Yes |
| **Combined** | >=3.11,<3.13 | ✅ Compatible |

**Resolution:** Use `requires-python = ">=3.11,<3.13"` (intersection)

---

### Dependency Conflicts Check

**Current Project Core Dependencies:**
- `click>=8.1.0`
- `rich>=13.0.0`
- `whoosh>=2.7.4`

**MCP Core Dependencies:**
- None of the MCP packages conflict with `click`, `rich`, or `whoosh`

**Result:** ✅ NO CONFLICTS - All dependencies can coexist

---

### Transitive Dependencies Analysis

**Key Transitive Dependencies from MCP:**

1. **sentence-transformers** brings:
   - `torch` or `tensorflow` (ML framework) - Large dependency (~2GB)
   - `transformers` (Hugging Face) - ~500MB
   - `scikit-learn` - ~50MB
   - `scipy` - ~30MB

2. **qdrant-client** brings:
   - `grpcio` (gRPC protocol) - ~50MB
   - `httpx` (modern HTTP client) - ~10MB

3. **numpy** - Already required by sentence-transformers

**Total Additional Disk Space:** ~2.5-3GB (mostly PyTorch/ML models)

**Impact:** Acceptable for training system (OBJECTIVE requires ML capabilities)

---

## Poetry → Setuptools Conversion Rules

### Version Specifier Translation

| Poetry | Setuptools Equivalent | Example |
|--------|----------------------|---------|
| `^1.13.1` | `>=1.13.1,<2.0.0` | `mcp>=1.13.1,<2.0.0` |
| `^2.5.1` | `>=2.5.1,<3.0.0` | `sentence-transformers>=2.5.1,<3.0.0` |
| `^1.0.0` | `>=1.0.0,<2.0.0` | `python-dotenv>=1.0.0,<2.0.0` |
| `>=8.0.0` | `>=8.0.0` | `pytest>=8.0.0` (no change) |

**Rationale:** Poetry's `^` (caret) means "compatible version" (MAJOR.minor.patch)
- `^1.2.3` allows `>=1.2.3,<2.0.0`
- `^0.2.3` allows `>=0.2.3,<0.3.0` (special case for 0.x versions)

---

## Final Dependency List (Setuptools Format)

### Production Dependencies to Add

```python
# MCP Core - Memory & Vector Search
"mcp>=1.13.1,<2.0.0",
"qdrant-client>=1.7.0,<2.0.0", 
"sentence-transformers>=2.5.1,<3.0.0",

# Data Processing
"numpy>=1.26.0,<2.0.0",
"markdown>=3.5.0,<4.0.0",
"beautifulsoup4>=4.12.0,<5.0.0",

# Configuration & Utilities
"python-dotenv>=1.0.0,<2.0.0",
"pyyaml>=6.0.0,<7.0.0",
"aiofiles>=24.1.0,<25.0.0",
"aiohttp>=3.9.1,<4.0.0",
```

### Dev Dependencies to Add

```python
"pytest-asyncio>=1.1.0,<2.0.0",
"types-markdown>=3.5.0,<4.0.0",
```

---

## Installation Size Estimates

| Category | Size | Components |
|----------|------|------------|
| MCP SDK | ~5MB | `mcp` package |
| Vector DB | ~20MB | `qdrant-client` + gRPC |
| ML Framework | ~2GB | `sentence-transformers` + PyTorch |
| Text Processing | ~50MB | `markdown`, `beautifulsoup4`, `pyyaml` |
| Async Utils | ~15MB | `aiofiles`, `aiohttp` |
| **Total (Production)** | **~2.1GB** | All MCP dependencies |
| **Total (with Dev)** | **~2.1GB** | Minimal dev overhead |

**Comparison:** Current project with dev deps: ~50MB  
**Increase:** ~42x larger (expected for ML training system)

**Mitigation:** This is acceptable for OBJECTIVE (requires ML model training)

---

## Dependency Installation Testing

### Test Installation Command (venv)

```bash
# Create test environment
python3.11 -m venv test_venv
source test_venv/bin/activate

# Test install MCP deps only
pip install \
  'mcp>=1.13.1,<2.0.0' \
  'qdrant-client>=1.7.0,<2.0.0' \
  'sentence-transformers>=2.5.1,<3.0.0' \
  'numpy>=1.26.0,<2.0.0' \
  'markdown>=3.5.0,<4.0.0' \
  'beautifulsoup4>=4.12.0,<5.0.0' \
  'python-dotenv>=1.0.0,<2.0.0' \
  'pyyaml>=6.0.0,<7.0.0' \
  'aiofiles>=24.1.0,<25.0.0' \
  'aiohttp>=3.9.1,<4.0.0'

# Verify imports work
python -c "import mcp; import qdrant_client; import sentence_transformers; print('✅ All imports successful')"
```

**Expected Output:** ✅ No conflicts, all imports successful

---

## Security Audit Notes

### Known Vulnerabilities (as of 2025-10-02)

- **None identified** in MCP core dependencies
- **PyTorch/TensorFlow:** Large surface area, monitor CVEs
- **Recommendation:** Run `pip-audit` after installation in W003

### Security-Sensitive Packages

| Package | Risk Level | Mitigation |
|---------|------------|------------|
| `pyyaml` | LOW | Only parse trusted configs |
| `beautifulsoup4` | LOW | Only parse markdown content |
| `aiohttp` | MEDIUM | Validate all network inputs |
| `sentence-transformers` | LOW | Only load trusted models |

**Action:** Review security best practices in W005 (Quality Gates)

---

## Tool Configuration Updates Needed

### Black Configuration

**Current:** `line-length = 100`, `target-version = ["py311"]`  
**MCP:** `line-length = 88`, `target-version = ["py310"]`  
**Resolution:** **KEEP CURRENT** (100 is more permissive, works for both)

---

### Mypy Configuration

**Current:** `python_version = "3.11"`, `strict = true`, `packages = ["mdnotes"]`  
**MCP:** `python_version = "3.10"`, `disallow_untyped_defs = true`  
**Resolution:** 
- **Update:** `python_version = "3.11"` (project requirement)
- **Add:** `packages = ["mdnotes", "mcp"]` (check both packages)
- **Keep:** `strict = true` (stricter than MCP's config)

---

### Pytest Configuration

**Current:** `testpaths = ["tests"]`, no asyncio_mode  
**MCP:** `testpaths = ["tests"]`, `asyncio_mode = "auto"`  
**Resolution:** **ADD** `asyncio_mode = "auto"` for MCP async tests

---

## Implementation Checklist (for W003)

**Dependency Addition:**
- [ ] Add 10 MCP production dependencies to `[project.dependencies]`
- [ ] Add 2 MCP dev dependencies to `[project.optional-dependencies.dev]`
- [ ] Update `requires-python = ">=3.11,<3.13"`
- [ ] Keep all current dependencies (click, rich, whoosh)

**Tool Configuration Updates:**
- [ ] Keep black line-length = 100
- [ ] Add "mcp" to mypy packages list
- [ ] Add asyncio_mode = "auto" to pytest config

**Installation Verification:**
- [ ] Run `pip install -e .[dev]` in fresh venv
- [ ] Verify all imports work
- [ ] Run `pip-audit` to check for vulnerabilities
- [ ] Run `mypy .` to ensure type checking works
- [ ] Run `pytest -q` to ensure tests still pass

**Documentation:**
- [ ] Update README installation instructions
- [ ] Document MCP-specific dependencies
- [ ] Note increased installation size (~2GB)

---

## Dependencies on Other Tasks

**Blocks:**
- W003 (Integrate MCP Dependencies) - needs this dependency list
- W005 (Python Tooling & Quality Gates) - needs tool config updates

**Blocked By:**
- W001-B01 (Structure Analysis) - ✅ COMPLETE
- W001-B02 (Conflict Resolution) - ✅ COMPLETE (this step)

---

**Status:** ✅ COMPLETE | **Next Step:** W001 Step 5 (Create Migration Checklist)

