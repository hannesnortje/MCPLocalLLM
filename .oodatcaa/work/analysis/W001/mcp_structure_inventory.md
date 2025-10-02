# MCP Source Structure Inventory

**Work Item:** W001 | **Created:** 2025-10-02 | **Source:** `/media/hannesn/storage/Code/MCP/`

---

## Overview

Complete inventory of MCP server source repository. Total: **23 directories, 161 files**.

---

## Root Level Files

| File | Size Category | Type | Categorization | Notes |
|------|---------------|------|----------------|-------|
| `pyproject.toml` | Small | Config | **MERGE** | Dependency source, Poetry format |
| `poetry.lock` | Large | Config | **EXCLUDE** | Lock file, regenerate |
| `requirements.txt` | Small | Config | **OPTIONAL** | May be generated from pyproject.toml |
| `README.md` | Medium | Docs | **MERGE** | Integration guide |
| `docker-compose.yml` | Small | Infra | **COPY** | Qdrant setup |
| `Dockerfile` | Small | Infra | **COPY** | Container build |
| `config.example.yaml` | Small | Config | **COPY** | Runtime config template |
| `launcher.py` | Small | Script | **COPY** | Server launcher |
| `memory_server.py` | Medium | Core | **COPY** | Main entry point |
| `agent_creation_prompt.md` | Small | Docs | **OPTIONAL** | Context for agents |
| `delete_documents_example.py` | Small | Example | **EXCLUDE** | Example script |
| `ingest_documents.py` | Small | Script | **COPY** | Document ingestion utility |
| `DOCUMENT_INGESTION*.md` | Medium | Docs | **OPTIONAL** | How-to guides |
| `GENERIC_MEMORY*.md` | Medium | Docs | **OPTIONAL** | Design docs |
| `IMPLEMENTATION_PLAN.md` | Medium | Docs | **OPTIONAL** | Historical plan |
| `MCP_MEMORY_SERVER_GUIDE.md` | Medium | Docs | **COPY** | User guide |
| `MEMORY_SERVER_README.md` | Medium | Docs | **MERGE** | Additional guide |
| `STEP_BY_STEP*.md` | Medium | Docs | **OPTIONAL** | Implementation history |
| `TOOLS_ONLY*.md` | Medium | Docs | **OPTIONAL** | Design variant |
| `UI_*.md` | Medium | Docs | **EXCLUDE** | UI-specific docs |
| `test_*.py` (12 files) | Small | Test | **EXCLUDE** | Root-level manual tests |

**Summary:**
- **COPY**: 6 files (core entry points, infrastructure)
- **MERGE**: 3 files (config, docs)
- **OPTIONAL**: 7 files (guides, design docs)
- **EXCLUDE**: 13 files (examples, manual tests, UI docs, lock files)

---

## Directory: `src/` (Core Application)

### Root `src/` Files

| File | Purpose | Categorization | Notes |
|------|---------|----------------|-------|
| `__init__.py` | Package init | **COPY** | Required |
| `mcp_server.py` | Main server | **COPY** | Core MCP implementation |
| `mcp_protocol_handler.py` | Protocol | **COPY** | MCP protocol logic |
| `memory_manager.py` | Memory ops | **COPY** | Core memory CRUD |
| `memory_manager_backup.py` | Backup | **EXCLUDE** | Backup file |
| `qdrant_manager.py` | Vector DB | **COPY** | Qdrant interface |
| `config.py` | Config loader | **COPY** | Runtime configuration |
| `server_config.py` | Server config | **COPY** | Server setup |
| `ui_config.py` | UI config | **EXCLUDE** | UI-specific |
| `error_handler.py` | Error handling | **COPY** | Error management |
| `markdown_processor.py` | MD processing | **COPY** | Markdown parser |
| `policy_processor.py` | Policy engine | **COPY** | Policy system |
| `resource_handlers.py` | MCP resources | **COPY** | Resource handlers |
| `tool_handlers.py` | MCP tools | **COPY** | Tool implementations |
| `tool_definitions.py` | Tool schemas | **COPY** | Tool definitions |
| `tool_definitions_backup.py` | Backup | **EXCLUDE** | Backup file |
| `prompt_handlers.py` | Prompt mgmt | **COPY** | Prompt system |
| `prompt_handlers_original.py` | Original | **EXCLUDE** | Historical version |
| `system_health_monitor.py` | Monitoring | **COPY** | Health checks |
| `collection_manager.py` | Collections | **COPY** | Collection management |
| `generic_memory_service.py` | Service | **COPY** | Memory service interface |

**Categorization:**
- **COPY (ESSENTIAL)**: 17 files
- **EXCLUDE**: 4 files (backups, originals, UI config)

---

### Directory: `src/handlers/`

All files in this directory are **ESSENTIAL**.

| File | Purpose |
|------|---------|
| `__init__.py` | Package init |
| `core_memory_handlers.py` | Core memory operations |
| `agent_management_handlers.py` | Agent registry |
| `markdown_processing_handlers.py` | Markdown tool handlers |
| `policy_and_guidance_handlers.py` | Policy tools |
| `system_and_collections_handlers.py` | System tools |

**Categorization:** **COPY ALL** (6 files)

---

### Directory: `src/memory/`

All files in this directory are **ESSENTIAL**.

| File | Purpose |
|------|---------|
| `__init__.py` | Package init |
| `vector_operations.py` | Vector search |
| `embedding_service.py` | Embedding generation |
| `collection_manager.py` | Qdrant collections |
| `agent_registry.py` | Agent tracking |
| `file_metadata_manager.py` | File metadata |

**Categorization:** **COPY ALL** (6 files)

---

### Directory: `src/prompts/`

All files in this directory are **ESSENTIAL**.

| File | Purpose |
|------|---------|
| `__init__.py` | Package init |
| `core_agent_prompts.py` | Agent prompt templates |
| `memory_management_prompts.py` | Memory prompts |
| `policy_compliance_prompts.py` | Policy prompts |

**Categorization:** **COPY ALL** (4 files)

---

### Directory: `src/tools/`

All files in this directory are **ESSENTIAL**.

| File | Purpose |
|------|---------|
| `__init__.py` | Package init |
| `core_memory_tools.py` | Memory CRUD tools |
| `agent_management_tools.py` | Agent tools |
| `collection_tools.py` | Collection tools |
| `markdown_tools.py` | Markdown tools |
| `policy_tools.py` | Policy tools |
| `guidance_tools.py` | Guidance tools |
| `batch_tools.py` | Batch operations |
| `system_tools.py` | System tools |

**Categorization:** **COPY ALL** (9 files)

---

### Directory: `src/ui/` ❌

**ENTIRE DIRECTORY EXCLUDED** - UI components not needed for training system.

Contents:
- `config.py`, `__init__.py`
- `main.py`, `main_window.py`
- `direct_memory_service.py`, `generic_direct_memory_service.py`
- `local_memory_client.py`
- `dialogs/`, `services/`, `widgets/` subdirectories

**Categorization:** **EXCLUDE ALL** (entire directory)

**Rationale:** UI built with PySide6 for desktop interface. Training system uses CLI/API only. Excluding saves ~2MB and removes PySide6 dependency.

---

### Directory: `src/__pycache__/`

**Categorization:** **EXCLUDE** (Python bytecode, regenerated)

---

## Directory: `policy/`

All policy markdown files are **ESSENTIAL** for governance system.

| File | Purpose |
|------|---------|
| `01-principles.md` | Core principles |
| `02-forbidden-actions.md` | Prohibited actions |
| `03-required-sections.md` | Required sections |
| `04-style-guide.md` | Style guide |

**Categorization:** **COPY ALL** (4 files)

---

## Directory: `docs/`

| File | Categorization | Notes |
|------|----------------|-------|
| `API.md` | **COPY** | API documentation |
| `DEPLOYMENT.md` | **COPY** | Deployment guide |
| `TROUBLESHOOTING.md` | **COPY** | Troubleshooting |
| `PROMPT_EXAMPLES.md` | **OPTIONAL** | Example prompts |
| `GUIDANCE_CONTENT.md` | **OPTIONAL** | Guidance details |
| `mcp-qdrant-reference-architecture.md` | **COPY** | Architecture |
| `mcp-qdrant4Web4Files.md` | **OPTIONAL** | Use case doc |
| `*.drawio` | **OPTIONAL** | Diagrams (3 files) |
| `*FEASIBILITY_REPORT.md` | **OPTIONAL** | Design reports (2 files) |

**Summary:**
- **COPY**: 4 files (essential docs)
- **OPTIONAL**: 8 files (examples, diagrams, reports)

---

## Directory: `scripts/`

All scripts are **ESSENTIAL** for deployment and maintenance.

| File | Purpose |
|------|---------|
| `setup-dev.sh` | Dev environment setup |
| `deploy.sh` | Deployment automation |
| `maintenance.sh` | Maintenance tasks |

**Categorization:** **COPY ALL** (3 files)

---

## Directory: `sample_data/`

Sample markdown files for testing.

| File | Categorization | Notes |
|------|----------------|-------|
| `backend_agent_context.md` | **OPTIONAL** | Example data |
| `frontend_agent_context.md` | **OPTIONAL** | Example data |
| `deployment_lessons.md` | **OPTIONAL** | Example data |
| `global_standards.md` | **OPTIONAL** | Example data |

**Categorization:** **OPTIONAL** (4 files) - Useful for testing migration

---

## Directory: `tests/`

Structured pytest test suite.

| File | Categorization | Notes |
|------|----------------|-------|
| `test_basic_functionality.py` | **COPY** | Core tests |
| `test_agent_management.py` | **COPY** | Agent tests |
| `test_markdown_processor_enhanced.py` | **COPY** | Markdown tests |
| `test_tool_handlers_enhanced.py` | **COPY** | Tool tests |
| `test_mcp_prompts.py` | **COPY** | Prompt tests |
| `test_mcp_resources.py` | **COPY** | Resource tests |
| `test_policy_system.py` | **COPY** | Policy tests |
| `test_cosine_similarity_deduplication.py` | **COPY** | Dedup tests |
| Other test files (11 files) | **OPTIONAL** | Integration/exploratory |

**Summary:**
- **COPY (ESSENTIAL)**: 8 core test files
- **OPTIONAL**: 11 additional test files
- **EXCLUDE**: `__pycache__/` directory

---

## Summary Statistics

### Essential Components (COPY)
- **Core `src/` files**: 17 files
- **`src/handlers/`**: 6 files
- **`src/memory/`**: 6 files
- **`src/prompts/`**: 4 files
- **`src/tools/`**: 9 files
- **`policy/`**: 4 files
- **`docs/`**: 4 files
- **`scripts/`**: 3 files
- **`tests/`**: 8 files
- **Root files**: 6 files

**Total ESSENTIAL: ~67 files**

### Excluded Components
- **`src/ui/`**: Entire directory (~20 files)
- **Root-level tests**: 12 files
- **Backup/original files**: 4 files
- **UI documentation**: 3 files
- **`__pycache__/` directories**: Multiple
- **`poetry.lock`**: 1 file

**Total EXCLUDED: ~40+ files**

### Optional Components
- **Documentation**: ~20 files (guides, diagrams, reports)
- **Sample data**: 4 files
- **Additional tests**: 11 files

**Total OPTIONAL: ~35 files**

---

## File Conflict Analysis

### Root-Level Conflicts

| File | Conflict | Resolution |
|------|----------|------------|
| `pyproject.toml` | ✅ YES | **MERGE** - Combine dependencies |
| `README.md` | ✅ YES | **MERGE** - Add MCP section |
| `.gitignore` | ✅ LIKELY | **MERGE** - Union of patterns |
| `docker-compose.yml` | ❌ NO | **COPY** - New file |
| `Dockerfile` | ❌ NO | **COPY** - New file |

### Directory Conflicts

| Directory | Conflict | Resolution |
|-----------|----------|------------|
| `src/` | ✅ YES | **COEXIST** - MCP alongside `mdnotes/` |
| `tests/` | ✅ YES | **MERGE** - Add MCP tests to existing |
| `docs/` | ✅ YES | **MERGE** - Add MCP docs |
| `scripts/` | ❌ NO | **COPY** - New directory |
| `policy/` | ❌ NO | **COPY** - New directory |

### Protected Directories

| Directory | Action |
|-----------|--------|
| `.oodatcaa/` | **NEVER TOUCH** - Explicit exclusion |
| `src/mdnotes/` | **PRESERVE** - Existing module |

---

## Next Steps

1. ✅ **Step 1 Complete**: Structure captured and categorized
2. **Step 2**: Document essential components with inclusion/exclusion lists
3. **Step 3**: Detailed conflict resolution strategy
4. **Step 4**: Extract and document dependencies
5. **Step 5**: Create migration checklist
6. **Step 6**: Analysis summary

---

**Artifact Status:** ✅ COMPLETE  
**Next Artifact:** `essential_components.md`

