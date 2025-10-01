# Sprint Backlog (AGENT-GENERATED)

> **This file is managed by agents.** The Sprint Planner and Planner agents will populate this based on OBJECTIVE.md.

**Status:** Awaiting first sprint planning — Launch the Negotiator to begin!

---

## How the Backlog Works

When Sprint Planner runs, it will:
1. Analyze your OBJECTIVE.md success criteria
2. Break them into logical sprints (Sprint 1: Foundation, Sprint 2: Core, etc.)
3. Create work items for each sprint
4. Agents will then execute these items

---

## Example Backlog (What Agents Will Generate)

### Sprint 1 — Foundation
- [ ] **W001** — Setup project structure and packaging  
      Type: Infra • Objective: OBJ-2025-001 • Sprint: 1  
      ACs: pyproject.toml exists; src/mdnotes/ created; pip install -e . works

- [ ] **W002** — Implement CLI entry point with Click  
      Type: Story • Objective: OBJ-2025-001 • Sprint: 1  
      ACs: `mdnotes --help` works; `mdnotes --version` shows version

- [ ] **W003** — Add development tooling (black, ruff, mypy)  
      Type: Infra • Objective: OBJ-2025-001 • Sprint: 1  
      ACs: All gates pass; CI configured

- [ ] **W004** — Implement file discovery for .md files  
      Type: Story • Objective: OBJ-2025-001 • Sprint: 1  
      ACs: Recursively finds .md files; respects .gitignore; unit tests pass

### Sprint 2 — Core Indexing
- [ ] **W005** — Implement Markdown parser for metadata  
      Type: Story • Objective: OBJ-2025-001 • Sprint: 2  
      ACs: Extracts title, tags, wikilinks; handles malformed files gracefully

- [ ] **W006** — Create search index with Whoosh  
      Type: Story • Objective: OBJ-2025-001 • Sprint: 2  
      ACs: Index created; full-text search works; p95 < 500ms for 1000 notes

- [ ] **W007** — Implement `mdnotes index` command  
      Type: Story • Objective: OBJ-2025-001 • Sprint: 2  
      ACs: CLI command works; shows progress bar; handles errors

- [ ] **W008** — Implement `mdnotes search` command  
      Type: Story • Objective: OBJ-2025-001 • Sprint: 2  
      ACs: Fuzzy search works; results ranked by relevance; nice output formatting

### Sprint 3 — Links & Graph
- [ ] **W009** — Implement backlink resolution  
      Type: Story • Objective: OBJ-2025-001 • Sprint: 3  
      ACs: Finds [[wikilinks]]; bidirectional links work; `mdnotes links` command

- [ ] **W010** — Generate knowledge graph with NetworkX  
      Type: Story • Objective: OBJ-2025-001 • Sprint: 3  
      ACs: Graph structure created; nodes=notes, edges=links

- [ ] **W011** — Create HTML visualization with D3.js  
      Type: Story • Objective: OBJ-2025-001 • Sprint: 3  
      ACs: `mdnotes graph` generates graph.html; interactive; looks good

### Sprint 4 — Polish & Release
- [ ] **W012** — Add tag filtering and `mdnotes tags` command  
      Type: Story • Objective: OBJ-2025-001 • Sprint: 4  
      ACs: Tag extraction works; filter by multiple tags; usage counts

- [ ] **W013** — Complete documentation (README, examples)  
      Type: Docs • Objective: OBJ-2025-001 • Sprint: 4  
      ACs: README complete; example notes repo; architecture diagram

- [ ] **W014** — Performance optimization and benchmarking  
      Type: TechDebt • Objective: OBJ-2025-001 • Sprint: 4  
      ACs: Meets performance criteria; benchmark tests in CI

- [ ] **W015** — Package for PyPI and final QA  
      Type: Infra • Objective: OBJ-2025-001 • Sprint: 4  
      ACs: Published to PyPI; installable; cross-platform tested

---

## Legend
- **Type:** Story (feature), TechDebt (refactor), Quality (testing), Infra (tooling), Docs
- **Status:** Will be tracked in SPRINT_QUEUE.json
- **ACs:** Acceptance Criteria (how to verify done)

