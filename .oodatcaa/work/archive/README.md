# Sprint Archive

This directory contains archived logs from completed or in-progress sprints to maintain performance and manageability of active working files.

## Structure

```
archive/
└── sprint_N/
    ├── AGENT_LOG_archive_NNN.md    # Agent action logs (rotated when >1000 lines)
    ├── SPRINT_LOG_final.md         # Complete sprint log (archived at sprint end)
    ├── SPRINT_PLAN_final.md        # Final sprint plan (archived at sprint end)
    └── SPRINT_DISCUSS.md           # All negotiations (archived at sprint end)
```

## Rotation Policy

### During Sprint (Automatic)
When any active log file exceeds **1,000 lines**:
- Archive oldest 50-60% to `archive/sprint_N/FILENAME_archive_NNN.md`
- Keep recent 40-50% in active file
- Add header note indicating archival

### Sprint Completion (Integrator)
When Integrator marks sprint complete:
- Move ALL current logs to `archive/sprint_N/` with `_final` suffix
- Start new sprint with fresh, empty logs
- AGENT_REPORTS.md stays as permanent index (never archived)

## Benefits
- **Performance:** Faster file operations for AI and tools
- **Scalability:** Can handle 10+ sprints without bloat
- **Audit Trail:** Complete history preserved
- **Context:** Recent entries always accessible

## Archive Timeline

### Sprint 1
- **2025-10-03T12:40:00+00:00:** AGENT_LOG.md rotated (4,807 lines → 606 active, 4,207 archived)
  - Archive: `sprint_1/AGENT_LOG_archive_001.md` (entries from W001-W005 early actions)
  - Active: Recent ~600 lines (W005 final actions through W006-B01)

