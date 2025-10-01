# Product Objective — Markdown Notes CLI Tool

> **This is a realistic template example.** Replace this content with your actual product vision.

---

## Vision (Why)
Developers and technical writers need a simple, fast CLI tool to organize, search, and link Markdown notes across multiple projects. Existing tools are either too complex (Obsidian, Notion) or lack developer-friendly features (grep). We need a lightweight, terminal-native solution that fits into developer workflows.

---

## Outcome (What)
Build **mdnotes** — a Python CLI tool that:
- Indexes and searches Markdown files across directories with fuzzy matching
- Creates bi-directional links between notes (`[[note-name]]` syntax)
- Generates a static knowledge graph visualization (HTML output)
- Supports tags (`#python`, `#cli`) with tag-based filtering
- Provides sub-second search even with 1000+ notes
- Works offline, no cloud dependencies

---

## Success Criteria (Measurable)
*How will agents know when the project is complete?*

- [ ] **Functional:** CLI commands work correctly
  - `mdnotes init` creates config in current directory
  - `mdnotes index <path>` indexes all .md files recursively
  - `mdnotes search <query>` fuzzy search returns ranked results in <500ms
  - `mdnotes links` shows backlinks for a note
  - `mdnotes graph` generates HTML visualization with D3.js
  - `mdnotes tags` lists all tags with usage counts

- [ ] **Performance:** 
  - Search p95 < 500ms for 1000 notes (each ~5KB)
  - Indexing p95 < 2s for 1000 notes

- [ ] **Quality:** 
  - ≥ 85% line coverage on all modules
  - ≥ 75% branch coverage
  - 0 high-severity issues in pip-audit
  - black, ruff, mypy pass on all code

- [ ] **Documentation:** 
  - README with installation, usage, and examples
  - CLI help text for all commands
  - Example notes repository with 20+ sample notes
  - Architecture diagram showing indexing flow

- [ ] **Packaging:**
  - Installable via `pip install mdnotes`
  - Executable via `mdnotes` command after install
  - Works on Linux, macOS, Windows (cross-platform paths)

---

## Constraints / Guardrails

**Technical:**
- Python 3.11+ (use match statements, modern type hints)
- CLI framework: Click or Typer for command parsing
- Search: Whoosh or lunr.py for full-text indexing
- Graph viz: NetworkX + D3.js for HTML output
- Config: TOML or YAML for .mdnotes.toml config file

**Quality Gates:**
- Type checking: mypy strict mode enabled
- Formatting: black with line-length=100
- Linting: ruff with all recommended rules
- Security: pip-audit must be clean
- Tests: pytest with coverage plugin

**User Experience:**
- All commands must have `--help` text
- Errors must show helpful messages (not stack traces)
- Progress bars for indexing (use rich or tqdm)
- No required external dependencies (SQLite for index, no PostgreSQL)

---

## Non-Goals (Out of Scope)

**Explicitly NOT building:**
- ❌ Web/GUI interface (CLI only)
- ❌ Note editing (user uses their own $EDITOR)
- ❌ Sync/cloud features (local-only)
- ❌ Plugin system (keep it simple)
- ❌ Support for non-Markdown formats (no .txt, .org, .rst)
- ❌ Real-time file watching (manual re-index is OK)
- ❌ Mobile apps or web app

**Out of scope for v1.0 (maybe later):**
- AI-powered note summarization
- Advanced query language (boolean operators)
- Multi-user / team features

---

## Notes
- **Objective ID:** OBJ-2025-001
- **Created:** 2025-10-01
- **Target Users:** Software developers, technical writers, researchers
- **Inspiration:** notational velocity, nvALT, but for CLI
- **Success metric:** If 100 GitHub stars within 3 months of launch

---

## Example Usage (Vision)

```bash
# Initialize in a notes directory
cd ~/my-notes
mdnotes init

# Index all markdown files
mdnotes index .
# Output: Indexed 247 notes in 1.2s

# Fuzzy search
mdnotes search "python typing"
# Output: Ranked results with snippets

# Find backlinks
mdnotes links python-decorators.md
# Output: 
# Linked from:
#   - python-basics.md (line 45)
#   - advanced-python.md (line 102)

# Generate knowledge graph
mdnotes graph --output graph.html
# Opens browser with interactive D3.js graph

# Filter by tags
mdnotes search "typing" --tag python --tag tutorial
```

---

**Agents:** You may now plan sprints to achieve this objective!
