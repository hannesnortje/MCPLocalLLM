# MCP Essential Components Analysis

**Work Item:** W001 Step 2 | **Created:** 2025-10-02 | **Source:** `/media/hannesn/storage/Code/MCP/`

---

## Inclusion Strategy

Use **explicit inclusion list** with selective copying. This approach:
- ✅ Minimizes risk of OODATCAA overwrite
- ✅ Prevents UI bloat
- ✅ Provides clear traceability
- ✅ Enables systematic verification

---

## Essential Components (INCLUDE)

### Core Application Files (`src/`)

#### Server Core (7 files)
- `src/mcp_server.py` - **Main MCP server implementation**
  - Purpose: MCP protocol stdin/stdout communication
  - Dependencies: mcp, asyncio
  - Size: ~500 lines
  - Rationale: Core server required for Cursor integration

- `src/mcp_protocol_handler.py` - **MCP protocol logic**
  - Purpose: Message parsing, tool routing
  - Dependencies: mcp library
  - Rationale: Protocol compliance

- `src/memory_manager.py` - **Memory operations**
  - Purpose: CRUD operations for all memory types
  - Dependencies: qdrant_manager, markdown_processor
  - Rationale: Core functionality

- `src/qdrant_manager.py` - **Vector database interface**
  - Purpose: Qdrant client, collection management, vector operations
  - Dependencies: qdrant-client, sentence-transformers
  - Rationale: Vector storage backend

- `src/config.py` - **Configuration loader**
  - Purpose: Environment variables, YAML config
  - Dependencies: python-dotenv, pyyaml
  - Rationale: Runtime configuration

- `src/server_config.py` - **Server configuration**
  - Purpose: Server initialization, health checks
  - Rationale: Server setup

- `src/error_handler.py` - **Error management**
  - Purpose: Centralized error handling, logging
  - Rationale: Robustness

#### Processing & Features (8 files)
- `src/markdown_processor.py` - **Markdown parsing**
  - Purpose: Extract sections, clean content, YAML front matter
  - Dependencies: markdown, beautifulsoup4
  - Rationale: Document processing

- `src/policy_processor.py` - **Policy governance**
  - Purpose: Load policies, semantic search, compliance tracking
  - Dependencies: policy/ directory
  - Rationale: Training quality control

- `src/resource_handlers.py` - **MCP resources**
  - Purpose: Read-only resource handlers
  - Rationale: MCP protocol resources

- `src/tool_handlers.py` - **MCP tools**
  - Purpose: Tool implementation dispatch
  - Rationale: MCP protocol tools

- `src/tool_definitions.py` - **Tool schemas**
  - Purpose: MCP tool definitions and schemas
  - Rationale: Tool metadata

- `src/prompt_handlers.py` - **Prompt management**
  - Purpose: Template engine, prompt generation
  - Rationale: Agent prompts

- `src/system_health_monitor.py` - **Health monitoring**
  - Purpose: System health, metrics
  - Rationale: Observability

- `src/collection_manager.py` - **Collection management**
  - Purpose: Qdrant collection operations
  - Rationale: Vector storage

- `src/generic_memory_service.py` - **Memory service**
  - Purpose: Memory service interface
  - Rationale: Service abstraction

#### Package Init
- `src/__init__.py` - **Package marker**
  - Rationale: Python package structure

---

### Subdirectory: `src/handlers/` (6 files - COPY ALL)

**Purpose:** Modular tool handler implementations

- `src/handlers/__init__.py`
- `src/handlers/core_memory_handlers.py` - Core memory CRUD
- `src/handlers/agent_management_handlers.py` - Agent registry
- `src/handlers/markdown_processing_handlers.py` - Markdown tools
- `src/handlers/policy_and_guidance_handlers.py` - Policy tools
- `src/handlers/system_and_collections_handlers.py` - System tools

**Rationale:** Clean separation of tool implementations. Essential for MCP functionality.

---

### Subdirectory: `src/memory/` (6 files - COPY ALL)

**Purpose:** Memory and vector operations

- `src/memory/__init__.py`
- `src/memory/vector_operations.py` - Vector search algorithms
- `src/memory/embedding_service.py` - Sentence transformer interface
- `src/memory/collection_manager.py` - Qdrant collection lifecycle
- `src/memory/agent_registry.py` - Agent tracking
- `src/memory/file_metadata_manager.py` - File metadata storage

**Rationale:** Core memory system. Required for context preservation and RAG.

---

### Subdirectory: `src/prompts/` (4 files - COPY ALL)

**Purpose:** Prompt templates and management

- `src/prompts/__init__.py`
- `src/prompts/core_agent_prompts.py` - Agent role prompts
- `src/prompts/memory_management_prompts.py` - Memory operation prompts
- `src/prompts/policy_compliance_prompts.py` - Policy enforcement prompts

**Rationale:** Training dataset generation, agent coordination.

---

### Subdirectory: `src/tools/` (9 files - COPY ALL)

**Purpose:** MCP tool implementations

- `src/tools/__init__.py`
- `src/tools/core_memory_tools.py` - add/query memory
- `src/tools/agent_management_tools.py` - agent registration
- `src/tools/collection_tools.py` - collection operations
- `src/tools/markdown_tools.py` - markdown ingestion
- `src/tools/policy_tools.py` - policy queries
- `src/tools/guidance_tools.py` - guidance retrieval
- `src/tools/batch_tools.py` - batch operations
- `src/tools/system_tools.py` - system status

**Rationale:** Complete MCP tool set. Essential for Cursor integration.

---

### Directory: `policy/` (4 files - COPY ALL)

**Purpose:** Policy governance markdown files

- `policy/01-principles.md` - Core principles
- `policy/02-forbidden-actions.md` - Prohibited patterns
- `policy/03-required-sections.md` - Required document structure
- `policy/04-style-guide.md` - Code style rules

**Rationale:** Training quality control. Defines acceptable code patterns.

---

### Directory: `docs/` (4 essential files)

**Essential Documentation:**
- `docs/API.md` - API reference
- `docs/DEPLOYMENT.md` - Deployment guide
- `docs/TROUBLESHOOTING.md` - Common issues
- `docs/mcp-qdrant-reference-architecture.md` - Architecture overview

**Optional Documentation:**
- `docs/PROMPT_EXAMPLES.md` - Example prompts
- `docs/GUIDANCE_CONTENT.md` - Guidance details
- `docs/*.drawio` - Diagram source files (3 files)
- `docs/*FEASIBILITY_REPORT.md` - Design exploration (2 files)

**Rationale:** Essential docs support deployment and troubleshooting. Optional docs provide context but not required.

---

### Directory: `scripts/` (3 files - COPY ALL)

**Purpose:** Deployment and maintenance automation

- `scripts/setup-dev.sh` - Development environment setup
- `scripts/deploy.sh` - Production deployment
- `scripts/maintenance.sh` - Maintenance tasks

**Rationale:** Automated setup reduces errors. Essential for operational readiness.

---

### Directory: `tests/` (8 core files + optionals)

**Core Tests (COPY):**
- `tests/test_basic_functionality.py` - Core memory operations
- `tests/test_agent_management.py` - Agent registry
- `tests/test_markdown_processor_enhanced.py` - Markdown processing
- `tests/test_tool_handlers_enhanced.py` - Tool handlers
- `tests/test_mcp_prompts.py` - Prompt system
- `tests/test_mcp_resources.py` - Resource handlers
- `tests/test_policy_system.py` - Policy engine
- `tests/test_cosine_similarity_deduplication.py` - Deduplication

**Optional Tests:**
- `tests/test_integration_comprehensive.py` - Full integration
- `tests/test_performance.py` - Performance benchmarks
- Other exploratory test files (9 additional)

**Rationale:** Core tests validate essential functionality. Optional tests provide additional coverage.

---

### Root Files (6 essential)

**Infrastructure:**
- `docker-compose.yml` - Qdrant container setup
- `Dockerfile` - MCP server container
- `config.example.yaml` - Configuration template

**Entry Points:**
- `launcher.py` - Server launcher script
- `memory_server.py` - Alternative entry point
- `ingest_documents.py` - Document ingestion utility

**Rationale:** Infrastructure for Qdrant. Entry points for different use cases.

---

### Root Files (MERGE - 2 files)

**Configuration:**
- `pyproject.toml` - **MERGE REQUIRED**
  - Action: Combine MCP dependencies with existing dependencies
  - Preserve existing: name="mcp-local-llm", existing deps
  - Add: MCP core dependencies (mcp, qdrant-client, etc.)
  - Exclude: PySide6, websockets (UI only)

**Documentation:**
- `README.md` - **MERGE REQUIRED**
  - Action: Add MCP integration section
  - Preserve: Existing project description, OODATCAA references
  - Add: MCP server setup, Cursor configuration

---

## Excluded Components (EXCLUDE)

### UI System (Entire `src/ui/` directory)

**Excluded Directory:**
- `src/ui/` - **ENTIRE DIRECTORY EXCLUDED** (~20 files)
  - `config.py`, `main.py`, `main_window.py`
  - `direct_memory_service.py`, `local_memory_client.py`
  - `dialogs/`, `services/`, `widgets/` subdirectories

**Dependencies Removed:**
- `PySide6` (Qt6 bindings) - ~100MB
- `websockets` - WebSocket client
- `requests` - (may still be needed elsewhere)
- `aiohttp` - (may still be needed for async operations)

**Rationale:**
- Training system uses CLI/API, not desktop UI
- Saves ~2MB source code, ~100MB in PySide6 deps
- Reduces complexity and attack surface
- OBJECTIVE.md explicitly states: "CLI and IDE integration only" (non-goal: GUI interface)

---

### Backup and Historical Files

**Excluded Files:**
- `src/memory_manager_backup.py` - Backup version
- `src/tool_definitions_backup.py` - Backup version
- `src/prompt_handlers_original.py` - Original version
- `src/ui_config.py` - UI configuration

**Rationale:** Backup files are historical artifacts, not needed.

---

### Root-Level Manual Test Scripts (12 files)

**Excluded:**
- `test_*.py` (all root-level test files)
  - `test_agent_registration.py`
  - `test_components.py`
  - `test_cursor_connection.py`
  - `test_cursor_exact.py`
  - `test_direct_memory.py`
  - `test_generic_integration.py`
  - `test_imports_only.py`
  - `test_memory_storage.py`
  - `test_minimal.py`
  - `test_query.py`
  - `test_raw_server.py`
  - `test_tool_call.py`
  - `test_ui_standalone.py`

**Rationale:** Manual exploratory tests. Not part of structured test suite. Formal tests in `tests/` directory are included.

---

### Example and Documentation Files

**Excluded:**
- `delete_documents_example.py` - Example script
- `UI_*.md` - UI implementation plans (3 files)
- `agent_creation_prompt.md` - Context file (optional, but low value)

**Rationale:** Examples not needed for production. UI docs irrelevant.

---

### Build Artifacts

**Excluded:**
- `__pycache__/` - All Python bytecode directories
- `poetry.lock` - Poetry lock file (regenerate for new project)

**Rationale:** Generated files, not source code.

---

### Optional Sample Data

**Optional (Low Priority):**
- `sample_data/*.md` - 4 example markdown files

**Rationale:** Useful for testing but not essential. Can copy if testing needed.

---

## Dependencies to Extract

### Core Dependencies (INCLUDE)

From `pyproject.toml`:

**MCP & Vector Storage:**
- `mcp = "^1.13.1"` - MCP protocol library
- `qdrant-client = "^1.7.0"` - Vector database client
- `sentence-transformers = "^2.5.1"` - Embedding generation

**Utilities:**
- `numpy = "^1.26.0"` - Numerical operations (sentence-transformers dep)
- `python-dotenv = "^1.0.0"` - Environment variables
- `pyyaml = "^6.0.0"` - YAML configuration
- `aiofiles = "^24.1.0"` - Async file I/O

**Document Processing:**
- `markdown = "^3.5.0"` - Markdown parsing
- `beautifulsoup4 = "^4.12.0"` - HTML/XML parsing (markdown dep)

**Async HTTP (CHECK USAGE):**
- `aiohttp = "^3.9.1"` - May be needed for MCP async operations

---

### UI Dependencies (EXCLUDE)

**Excluded:**
- `PySide6 = "^6.7.0"` - Qt6 desktop UI (~100MB)
- `websockets = "^12.0"` - WebSocket client (UI real-time updates)
- `requests = "^2.32.1"` - HTTP client (may be used elsewhere, check before excluding)

**Rationale:** UI not needed per OBJECTIVE.md non-goals.

---

### Dev Dependencies (MERGE)

**MCP Dev Dependencies:**
- `pytest-asyncio = "^1.1.0"` - Async pytest support (ADD)
- `types-markdown = "^3.5.0"` - Markdown type stubs (ADD)

**Existing Dev Dependencies:**
- Keep existing: `black`, `ruff`, `mypy`, `pytest`
- Note: MCP uses `flake8`, we use `ruff` (ruff is superset, keep ruff)

---

## Summary Statistics

### Files to Copy

| Category | Count |
|----------|-------|
| Core `src/` files | 17 |
| `src/handlers/` | 6 |
| `src/memory/` | 6 |
| `src/prompts/` | 4 |
| `src/tools/` | 9 |
| `policy/` | 4 |
| `docs/` (essential) | 4 |
| `scripts/` | 3 |
| `tests/` (core) | 8 |
| Root files | 6 |
| **Total ESSENTIAL** | **67 files** |

### Files to Merge

| File | Strategy |
|------|----------|
| `pyproject.toml` | Combine dependencies |
| `README.md` | Add MCP section |
| `.gitignore` (if exists) | Union patterns |

### Files to Exclude

| Category | Count |
|----------|-------|
| `src/ui/` directory | ~20 |
| Root test scripts | 13 |
| Backup files | 4 |
| UI documentation | 3 |
| Build artifacts | Multiple |
| **Total EXCLUDED** | **~40+ files** |

---

## Preservation Strategy

### Protected (NEVER TOUCH)

**OODATCAA System:**
- `.oodatcaa/` - **EXPLICIT EXCLUSION** in all copy commands
- All `.oodatcaa/**/*` files must remain unchanged

**Existing Modules:**
- `src/mdnotes/` - Existing module, preserve completely
- `src/mdnotes/__init__.py` - Keep current functionality

---

### Coexistence Strategy

**`src/` Directory:**
- Current: `src/mdnotes/` (2 files)
- Add: MCP files (42 files in `src/`)
- Structure:
  ```
  src/
  ├── mdnotes/          # EXISTING - preserve
  │   ├── __init__.py
  │   └── core.py
  ├── handlers/         # NEW - MCP
  ├── memory/           # NEW - MCP
  ├── prompts/          # NEW - MCP
  ├── tools/            # NEW - MCP
  ├── mcp_server.py     # NEW - MCP
  ├── memory_manager.py # NEW - MCP
  └── ...               # NEW - MCP
  ```

**No Conflicts Expected:** MCP files don't overlap with `mdnotes` module.

---

## Next Steps

1. ✅ **Step 1 Complete**: Structure inventory
2. ✅ **Step 2 Complete**: Essential components documented
3. **Step 3**: Detailed conflict resolution strategy
4. **Step 4**: Extract and document dependencies
5. **Step 5**: Create migration checklist
6. **Step 6**: Analysis summary

---

**Artifact Status:** ✅ COMPLETE  
**Next Artifact:** `conflict_resolution.md`

