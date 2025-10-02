# W001 Step 4: pyproject.toml Update Strategy

**Work Item:** W001 | **Sprint:** 1 | **Created:** 2025-10-02  
**Purpose:** Document exact changes needed to merge MCP dependencies into current pyproject.toml

---

## Current vs. Target State

### Current pyproject.toml (Core Sections)

```toml
[project]
name = "mdnotes"
version = "0.1.0"
description = "CLI tool for managing and searching Markdown notes"
requires-python = ">=3.11"

dependencies = [
    "click>=8.1.0",
    "rich>=13.0.0",
    "whoosh>=2.7.4",
]

[project.optional-dependencies]
dev = [
  "black>=24.0.0",
  "ruff>=0.5.0",
  "mypy>=1.8.0",
  "pytest>=8.0.0",
  "pytest-cov>=4.1.0",
  "pip-audit>=2.7.0",
  "bandit>=1.7.7",
  "build>=1.2.1",
  "types-setuptools"
]
```

---

## Target pyproject.toml Changes

### 1. Update Package Metadata (OPTIONAL - W004)

**Current:**
```toml
name = "mdnotes"
description = "CLI tool for managing and searching Markdown notes"
```

**Consideration for Future:** 
- Could rename to "mcp-local-llm" (matches OBJECTIVE)
- Or keep "mdnotes" and add MCP as additional entry point
- **Decision: DEFER to W004** (Adapt MCP for Training Use Case)

**Recommended:** Keep "mdnotes" as primary package name for now

---

### 2. Update Python Version Constraint

**Current:**
```toml
requires-python = ">=3.11"
```

**Target:**
```toml
requires-python = ">=3.11,<3.13"
```

**Rationale:**
- MCP tested with Python <3.13 only
- Adds upper bound for safety
- Still allows Python 3.11 and 3.12

---

### 3. Add MCP Core Dependencies

**Current:**
```toml
dependencies = [
    "click>=8.1.0",
    "rich>=13.0.0",
    "whoosh>=2.7.4",
]
```

**Target:**
```toml
dependencies = [
    # Existing mdnotes dependencies
    "click>=8.1.0",
    "rich>=13.0.0",
    "whoosh>=2.7.4",
    
    # MCP Core - Memory & Vector Search
    "mcp>=1.13.1,<2.0.0",
    "qdrant-client>=1.7.0,<2.0.0",
    "sentence-transformers>=2.5.1,<3.0.0",
    
    # Data Processing
    "numpy>=1.26.0,<2.0.0",
    "markdown>=3.5.0,<4.0.0",
    "beautifulsoup4>=4.12.0,<5.0.0",
    
    # Configuration & Async Utilities
    "python-dotenv>=1.0.0,<2.0.0",
    "pyyaml>=6.0.0,<7.0.0",
    "aiofiles>=24.1.0,<25.0.0",
    "aiohttp>=3.9.1,<4.0.0",
]
```

**Changes:**
- ✅ Keep all existing dependencies (mdnotes still functional)
- ✅ Add 10 MCP dependencies with version bounds
- ✅ Group by purpose with comments
- ✅ Alphabetically sorted within groups (optional, recommended)

---

### 4. Add MCP Dev Dependencies

**Current:**
```toml
[project.optional-dependencies]
dev = [
  "black>=24.0.0",
  "ruff>=0.5.0",
  "mypy>=1.8.0",
  "pytest>=8.0.0",
  "pytest-cov>=4.1.0",
  "pip-audit>=2.7.0",
  "bandit>=1.7.7",
  "build>=1.2.1",
  "types-setuptools"
]
```

**Target:**
```toml
[project.optional-dependencies]
dev = [
  "black>=24.0.0",
  "ruff>=0.5.0",
  "mypy>=1.8.0",
  "pytest>=8.0.0",
  "pytest-asyncio>=1.1.0,<2.0.0",  # NEW: For MCP async tests
  "pytest-cov>=4.1.0",
  "pip-audit>=2.7.0",
  "bandit>=1.7.7",
  "build>=1.2.1",
  "types-setuptools",
  "types-markdown>=3.5.0,<4.0.0",  # NEW: Type stubs for markdown
]
```

**Changes:**
- ✅ Add `pytest-asyncio` (required for async MCP tests)
- ✅ Add `types-markdown` (type stubs for mypy strict mode)
- ✅ Keep all existing dev dependencies
- ✅ Maintain alphabetical order (optional)

---

### 5. Update Tool Configurations

#### 5a. Black (No Change Needed)

**Current:**
```toml
[tool.black]
line-length = 100
target-version = ["py311"]
```

**Target:** **NO CHANGE**
- Current config works for both mdnotes and MCP code
- line-length=100 is more permissive than MCP's 88

---

#### 5b. Ruff (No Change Needed)

**Current:**
```toml
[tool.ruff]
line-length = 100
src = ["src", "tests"]
# ... extend-select rules ...
```

**Target:** **NO CHANGE**
- Current config comprehensive, works for MCP code
- May need to adjust src paths if MCP code placed differently (W004)

---

#### 5c. Mypy (Add MCP Package)

**Current:**
```toml
[tool.mypy]
python_version = "3.11"
packages = ["mdnotes"]
strict = true
# ... other settings ...
exclude = ["tests/"]
```

**Target:**
```toml
[tool.mypy]
python_version = "3.11"
packages = ["mdnotes", "mcp"]  # Add MCP package
strict = true
warn_unused_configs = true
warn_redundant_casts = true
warn_unused_ignores = true
exclude = ["tests/"]
```

**Changes:**
- ✅ Add "mcp" to packages list
- ✅ Keep strict=true (stricter than MCP's config)
- ✅ Keep python_version = "3.11"

---

#### 5d. Pytest (Add Asyncio Mode)

**Current:**
```toml
[tool.pytest.ini_options]
addopts = "-q"
testpaths = ["tests"]
```

**Target:**
```toml
[tool.pytest.ini_options]
addopts = "-q"
testpaths = ["tests"]
asyncio_mode = "auto"  # NEW: For MCP async tests
```

**Changes:**
- ✅ Add `asyncio_mode = "auto"` (enables async test support)
- ✅ Keep all existing pytest config

---

#### 5e. Coverage (No Change Needed)

**Current:**
```toml
[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
show_missing = true
fail_under = 85
```

**Target:** **NO CHANGE**
- source = ["src"] automatically includes both mdnotes and mcp packages
- fail_under = 85 matches OBJECTIVE requirements

---

## Complete Updated pyproject.toml

**Full File (After W003 Implementation):**

```toml
[build-system]
requires = ["setuptools>=69", "wheel", "build"]
build-backend = "setuptools.build_meta"

[project]
name = "mdnotes"
version = "0.1.0"
description = "CLI tool for managing and searching Markdown notes with MCP integration"
readme = "README.md"
authors = [{ name = "Your Name", email = "you@example.com" }]
requires-python = ">=3.11,<3.13"
keywords = ["markdown", "notes", "cli", "knowledge-management", "search", "mcp", "vector-database"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "Topic :: Text Processing :: Markup",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]

dependencies = [
    # Existing mdnotes dependencies
    "click>=8.1.0",
    "rich>=13.0.0",
    "whoosh>=2.7.4",
    
    # MCP Core - Memory & Vector Search
    "mcp>=1.13.1,<2.0.0",
    "qdrant-client>=1.7.0,<2.0.0",
    "sentence-transformers>=2.5.1,<3.0.0",
    
    # Data Processing
    "numpy>=1.26.0,<2.0.0",
    "markdown>=3.5.0,<4.0.0",
    "beautifulsoup4>=4.12.0,<5.0.0",
    
    # Configuration & Async Utilities
    "python-dotenv>=1.0.0,<2.0.0",
    "pyyaml>=6.0.0,<7.0.0",
    "aiofiles>=24.1.0,<25.0.0",
    "aiohttp>=3.9.1,<4.0.0",
]

[project.scripts]
mdnotes = "mdnotes.cli:main"

[project.urls]
Homepage = "https://github.com/yourusername/mdnotes"
Repository = "https://github.com/yourusername/mdnotes"

[project.optional-dependencies]
dev = [
  "black>=24.0.0",
  "ruff>=0.5.0",
  "mypy>=1.8.0",
  "pytest>=8.0.0",
  "pytest-asyncio>=1.1.0,<2.0.0",
  "pytest-cov>=4.1.0",
  "pip-audit>=2.7.0",
  "bandit>=1.7.7",
  "build>=1.2.1",
  "types-setuptools",
  "types-markdown>=3.5.0,<4.0.0",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 100
target-version = ["py311"]

[tool.ruff]
line-length = 100
src = ["src", "tests"]
extend-select = [
  "F",  # pyflakes
  "E", "W",  # pycodestyle
  "I",       # isort imports
  "B",       # flake8-bugbear
  "UP",      # pyupgrade
  "S",       # bandit (security checks)
]
ignore = ["S101"]  # assert used in tests

[tool.ruff.lint.isort]
known-first-party = ["mdnotes", "mcp"]

[tool.mypy]
python_version = "3.11"
packages = ["mdnotes", "mcp"]
strict = true
warn_unused_configs = true
warn_redundant_casts = true
warn_unused_ignores = true
exclude = ["tests/"]

[tool.pytest.ini_options]
addopts = "-q"
testpaths = ["tests"]
asyncio_mode = "auto"

[tool.coverage.run]
branch = true
source = ["src"]

[tool.coverage.report]
show_missing = true
fail_under = 85
```

---

## Change Summary

| Section | Changes | Impact |
|---------|---------|--------|
| `requires-python` | Add upper bound `<3.13` | Safety constraint |
| `dependencies` | Add 10 MCP packages | Enable MCP functionality |
| `dev dependencies` | Add 2 packages (pytest-asyncio, types-markdown) | Enable async tests, type checking |
| `[tool.black]` | No change | Compatible as-is |
| `[tool.ruff]` | Add "mcp" to known-first-party | Import sorting |
| `[tool.mypy]` | Add "mcp" to packages | Type checking MCP code |
| `[tool.pytest.ini_options]` | Add `asyncio_mode = "auto"` | Async test support |
| `[tool.coverage]` | No change | Automatically covers MCP |

**Total Lines Added:** ~15 lines  
**Total Lines Modified:** ~3 lines  
**Breaking Changes:** NONE (all additive)

---

## Implementation Steps (for W003)

1. **Backup Current File:**
   ```bash
   cp pyproject.toml pyproject.toml.backup
   ```

2. **Apply Changes:**
   - Open `pyproject.toml` in editor
   - Update `requires-python` line
   - Add MCP dependencies to `[project.dependencies]`
   - Add MCP dev dependencies to `[project.optional-dependencies.dev]`
   - Add "mcp" to `[tool.ruff.lint.isort] known-first-party`
   - Add "mcp" to `[tool.mypy] packages`
   - Add `asyncio_mode = "auto"` to `[tool.pytest.ini_options]`

3. **Validate Changes:**
   ```bash
   # Verify TOML syntax
   python -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))"
   
   # Install dependencies
   pip install -e .[dev]
   
   # Verify imports work
   python -c "import mcp; import qdrant_client; print('✅ MCP imports OK')"
   ```

4. **Run Quality Gates:**
   ```bash
   black --check .
   ruff check .
   mypy .
   pytest -q
   pip-audit
   ```

5. **Commit Changes:**
   ```bash
   git add pyproject.toml
   git commit -m "[impl] W003: Integrate MCP dependencies into pyproject.toml"
   ```

---

## Rollback Plan

If dependency integration fails:

```bash
# Restore backup
cp pyproject.toml.backup pyproject.toml

# Reinstall original dependencies
pip uninstall -y mcp qdrant-client sentence-transformers numpy markdown beautifulsoup4 python-dotenv pyyaml aiofiles aiohttp pytest-asyncio types-markdown

# Reinstall clean environment
pip install -e .[dev]

# Verify rollback
pytest -q
```

---

## Verification Checklist (Post-W003)

- [ ] `requires-python = ">=3.11,<3.13"` present
- [ ] 10 MCP dependencies in `[project.dependencies]`
- [ ] 2 MCP dev dependencies in `[project.optional-dependencies.dev]`
- [ ] "mcp" in `[tool.ruff.lint.isort] known-first-party`
- [ ] "mcp" in `[tool.mypy] packages`
- [ ] `asyncio_mode = "auto"` in pytest config
- [ ] `pip install -e .[dev]` succeeds without errors
- [ ] `python -c "import mcp"` succeeds
- [ ] `python -c "import qdrant_client"` succeeds
- [ ] `python -c "import sentence_transformers"` succeeds
- [ ] `black --check .` passes
- [ ] `ruff check .` passes
- [ ] `mypy .` passes
- [ ] `pytest -q` passes (existing tests still work)
- [ ] `pip-audit` clean (no high-severity issues)

---

## Dependencies on Other Tasks

**Blocks:**
- W003 (Integrate MCP Dependencies) - implements these changes
- W005 (Python Tooling & Quality Gates) - validates tool configs

**Blocked By:**
- W001-B01 (Structure Analysis) - ✅ COMPLETE
- W001-B02 (Conflict Resolution) - ✅ COMPLETE (this step)

---

**Status:** ✅ COMPLETE | **Next Step:** W001 Step 5 (Create Migration Checklist)

