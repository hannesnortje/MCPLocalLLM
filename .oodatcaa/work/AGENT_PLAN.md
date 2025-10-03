# AGENT_PLAN: P006 - Process Documentation & Runbook

**Plan Version:** 1.0  
**Task ID:** P006  
**Objective:** SPRINT-2025-002 (OODATCAA Process Improvement)  
**Sprint:** 2  
**Complexity:** Medium  
**Planner:** agent-planner-A  
**Created:** 2025-10-03T22:30:00+02:00

---

## Traceability

**Objective Link:** `.oodatcaa/objectives/SPRINT_2_OBJECTIVE.md` → Process Documentation Complete  
**Epic:** Sprint 2 - OODATCAA Process Improvement  
**Dependencies:** P001 (daemon system), P003 (sprint management), P004 (OODATCAA loop docs)

**Success Criteria Addressed:**
1. Runbook: Practical guide created with common scenarios, command reference, troubleshooting
2. Agent Protocols: Enhanced `.oodatcaa/prompts/*.md` with examples and edge cases
3. Onboarding Guide: New user/agent guide with system overview, quick start, architecture diagrams

---

## Problem Statement

**Current State:**
- Sprint 2 has delivered significant infrastructure (P001 daemon, P002 log rotation, P003 sprint management, P004 OODATCAA documentation)
- Multiple documentation files exist but lack integration and practical operational guidance
- No comprehensive runbook for common scenarios (failures, debugging, recovery)
- Agent prompts are functional but lack examples and edge case handling
- Onboarding new users/developers requires reading multiple disconnected documents

**Evidence:**
- 14 existing documentation files in `.oodatcaa/` directory
- Agent prompts in `.oodatcaa/prompts/` are protocol-focused, light on examples
- No centralized troubleshooting guide
- No operational runbook with step-by-step procedures
- Documentation scattered across README.md, QUICK_START.md, START_HERE.md, etc.

**Impact:**
- High onboarding friction for new developers or AI agents
- Difficult to troubleshoot issues without comprehensive guide
- Common operational tasks undocumented (sprint failures, lease recovery, rollback procedures)
- Agent prompts assume too much context, leading to errors

**Goal:**
Create comprehensive, integrated process documentation including operational runbook, enhanced agent protocols, and developer onboarding guide that consolidates existing docs and adds practical operational procedures.

---

## Constraints & Interfaces

### Technical Constraints
- **Documentation Format:** Markdown for all documentation files
- **Location:** `.oodatcaa/` directory for system docs, `docs/` for developer-facing docs
- **Integration:** Must reference P001, P002, P003, P004 systems
- **Accessibility:** Clear navigation, searchable, beginner-friendly

### Interfaces
**Input Documentation (Existing):**
- `.oodatcaa/README.md` - System overview
- `.oodatcaa/QUICK_START.md` - Quick start guide
- `.oodatcaa/AGENT_MANAGEMENT.md` - Agent details
- `.oodatcaa/OODATCAA_LOOP_GUIDE.md` - Loop documentation (P004)
- `.oodatcaa/prompts/*.md` - Agent protocol files
- `docs/SPRINT_MANAGEMENT.md` - Sprint management reference (P003)
- Existing README.md

**Output Documentation (New/Enhanced):**
- `.oodatcaa/RUNBOOK.md` - Operational procedures
- `.oodatcaa/TROUBLESHOOTING.md` - Common issues and solutions
- `.oodatcaa/ONBOARDING.md` - Developer onboarding guide
- `.oodatcaa/prompts/*.md` - Enhanced with examples
- `.oodatcaa/ARCHITECTURE.md` - System architecture diagrams
- Navigation improvements in existing docs

### Existing Infrastructure
- P001: Background agent daemon system
- P002: Automatic log rotation system
- P003: Sprint management (dashboard, transitions)
- P004: OODATCAA loop documentation
- Sprint 1: Complete MCP server foundation
- Sprint 2: Process improvement infrastructure

### Risks
1. **Documentation Sprawl:** Too many docs can be as confusing as too few
   - Mitigation: Clear navigation, consolidated index, cross-references
2. **Maintenance Burden:** Outdated docs worse than no docs
   - Mitigation: Link to code/prompts, date stamps, version numbers
3. **Over-Documentation:** Too detailed = nobody reads it
   - Mitigation: Tiered approach (quick start → runbook → deep dive)
4. **Fragmentation:** New docs don't integrate with existing
   - Mitigation: Navigation hub, consistent structure, cross-linking

---

## Definition of Done (DoD)

### Functional Requirements
1. **Operational Runbook:**
   - Common scenarios documented (20+ procedures)
   - Step-by-step instructions with commands
   - Troubleshooting section for each scenario
   - Emergency procedures (rollback, recovery, cleanup)

2. **Enhanced Agent Protocols:**
   - All 10 agent prompts include examples
   - Edge cases documented
   - Common errors and solutions
   - Input/output contracts clear

3. **Onboarding Guide:**
   - System overview with architecture diagram
   - 15-minute quick start path
   - First sprint walkthrough
   - Key concepts explained

4. **Troubleshooting Guide:**
   - 30+ common issues documented
   - Diagnostic procedures
   - Solution steps with commands
   - Prevention tips

5. **Architecture Documentation:**
   - System architecture diagram (Mermaid)
   - Agent interaction flows
   - File structure explained
   - Data flow diagrams

### Non-Functional Requirements
- **Usability:** Findable in < 30 seconds, understandable on first read
- **Completeness:** Covers all P001-P004 systems
- **Accuracy:** All commands tested, examples verified
- **Maintainability:** Modular structure, clear ownership

### Acceptance Criteria (Detailed in TEST_PLAN.md)
- AC1: RUNBOOK.md complete with 20+ scenarios
- AC2: TROUBLESHOOTING.md with 30+ issues
- AC3: ONBOARDING.md with quick start path
- AC4: All agent prompts enhanced with examples
- AC5: ARCHITECTURE.md with diagrams
- AC6: Navigation improved across all docs
- AC7: All documentation cross-linked
- AC8: Quality gates pass (links valid, formatting correct)
- AC9: Existing documentation consolidated
- AC10: Sprint 2 systems (P001-P004) documented

---

## Alternatives Considered

### Alternative 1: Minimal Documentation Updates
**Approach:**
- Only update agent prompts with examples
- Add troubleshooting section to existing README
- No new documentation files

**Pros:**
- Minimal work (~2 hours)
- Less maintenance burden
- Familiar structure

**Cons:**
- Doesn't address runbook need
- README becomes bloated
- No dedicated onboarding path
- Troubleshooting buried in large file

**Verdict:** ❌ **Rejected** - Insufficient for operational needs. Troubleshooting and runbook critical for autonomous operation.

---

### Alternative 2: Comprehensive Documentation Portal
**Approach:**
- Build HTML documentation site (Sphinx/MkDocs)
- Interactive tutorials
- Search functionality
- Version-controlled docs

**Pros:**
- Professional presentation
- Excellent searchability
- Multi-version support
- Interactive examples

**Cons:**
- Significant implementation time (~3-4 days)
- Additional build/deploy infrastructure
- Overkill for internal tool
- Maintenance complexity

**Verdict:** ❌ **Rejected** - Over-engineering for current needs. Markdown files sufficient for agent-driven development.

---

### Alternative 3: Structured Markdown Documentation (CHOSEN)
**Approach:**
- Create focused markdown files for each major topic
- Maintain existing structure, add new specialized docs
- Cross-link aggressively
- Keep in `.oodatcaa/` for agent accessibility
- Clear navigation hub

**Pros:**
- ✅ Right balance of structure and simplicity
- ✅ Agent-readable (markdown parsing easy)
- ✅ Version controlled with code
- ✅ No build infrastructure needed
- ✅ Easy to maintain and update
- ✅ Familiar developer workflow

**Cons:**
- No built-in search (mitigated by grep/IDE search)
- Manual cross-linking (acceptable maintenance cost)

**Verdict:** ✅ **CHOSEN** - Optimal for agent-driven development. Markdown keeps docs with code, easily parseable, low maintenance.

---

## Implementation Plan

### Step-by-Step Breakdown

#### **Step 1: Operational Runbook Creation (90 min)**
**Goal:** Create `.oodatcaa/RUNBOOK.md` - Practical operational procedures

**Scenarios to Document:**

**Sprint Operations (8 scenarios):**
1. Starting a new sprint
2. Monitoring sprint progress (`make sprint-status`)
3. Completing a sprint (`make sprint-complete`)
4. Handling sprint failures
5. Rolling back to previous sprint state
6. Emergency sprint reset
7. Sprint transition troubleshooting
8. Sprint retrospective process

**Agent Operations (6 scenarios):**
9. Launching Negotiator for first time
10. Running planner for new work item
11. Builder failure recovery
12. Tester acceptance criteria negotiation
13. Refiner quick fix vs rollback decision
14. Integrator merge conflicts

**System Maintenance (6 scenarios):**
15. Log rotation manual trigger
16. Archive cleanup and management
17. Lease cleanup (stale leases)
18. Lock recovery (broken locks >5m)
19. SPRINT_QUEUE.json repair
20. Git baseline tag management

**Format Per Scenario:**
   ```markdown
### Scenario: [Name]

**When:** [Situation description]
**Goal:** [What you want to achieve]

#### Procedure:
1. Step 1 with command
   ```bash
   command here
   ```
2. Step 2...

#### Expected Output:
```
output here
```

#### Troubleshooting:
- Issue: [common problem]
  - Solution: [how to fix]

#### See Also:
- Related scenario links
```

**Exit Gate:** 20+ scenarios documented, all commands tested

---

#### **Step 2: Troubleshooting Guide Creation (75 min)**
**Goal:** Create `.oodatcaa/TROUBLESHOOTING.md` - Diagnostic procedures

**Issue Categories:**

**Agent Issues (10 issues):**
1. Planner creates invalid AGENT_PLAN.md
2. Builder fails quality gates repeatedly
3. Tester rejects work unfairly
4. Refiner recommends wrong approach
5. Integrator merge conflicts
6. Negotiator coordination loops
7. Sprint Planner generates impossible sprint
8. Stale lease prevents work
9. Lock files not releasing
10. Agent reports missing

**System Issues (10 issues):**
11. SPRINT_QUEUE.json corruption
12. JSON parse errors
13. File permission errors
14. Disk space issues
15. Git conflicts in working files
16. Missing dependencies
17. Python version incompatibility
18. Virtual environment issues
19. Quality gate failures (black/ruff/mypy)
20. Test failures blocking progress

**Process Issues (10 issues):**
21. Sprint not progressing
22. Tasks stuck in "blocked" status
23. WIP limits preventing work
24. Dependencies never satisfied
25. Sprint completion criteria unclear
26. Integration tests always skipping
27. Coverage thresholds too high
28. Documentation out of sync
29. Logs growing too large
30. Archive structure corrupted

**Format Per Issue:**
   ```markdown
### Issue: [Problem Description]

**Symptoms:**
- What you observe

**Diagnosis:**
```bash
# Commands to diagnose
command to check state
```

**Solution:**
```bash
# Commands to fix
step-by-step fix
```

**Prevention:**
- How to avoid this issue

**Related Issues:** Links to similar problems
```

**Exit Gate:** 30+ issues documented, all diagnostic commands verified

---

#### **Step 3: Onboarding Guide Creation (60 min)**
**Goal:** Create `.oodatcaa/ONBOARDING.md` - New developer quick start

**Structure:**

**1. Welcome (5 minutes read)**
- What is OODATCAA?
- System overview (100-word summary)
- Key concepts (agents, sprints, loop)
- Prerequisites checklist

**2. Quick Start (15 minutes to first sprint)**
- Step 1: Review OBJECTIVE.md
- Step 2: Run Negotiator
- Step 3: Launch first agent
- Step 4: Monitor progress
- Step 5: First sprint completion

**3. Core Concepts (20 minutes read)**
- The OODATCAA loop explained
- Agent roles and responsibilities
- Sprint lifecycle
- Task states and transitions
- Quality gates

**4. First Sprint Walkthrough (30 minutes practice)**
- Sprint 1 case study (from actual Sprint 1)
- Task breakdown example
- Adaptation cycle example
- Integration process

**5. Common Tasks (Reference)**
- How to create new work item
- How to monitor progress
- How to handle failures
- How to complete sprint
- How to generate reports

**6. Next Steps**
- Deep dive links (OODATCAA_LOOP_GUIDE, RUNBOOK)
- Agent-specific guides
- Architecture documentation

**Exit Gate:** Complete onboarding guide, 15-minute quick start verified

---

#### **Step 4: Enhanced Agent Protocols (90 min)**
**Goal:** Update all `.oodatcaa/prompts/*.md` files with examples

**Agents to Enhance (10 files):**
1. negotiator.md
2. sprint-planner.md
3. planner.md
4. builder.md
5. tester.md
6. refiner.md
7. integrator.md
8. project-completion-detector.md
9. sprint-close.md
10. triage.md

**Enhancements Per Agent:**
- **Examples Section:** 2-3 concrete examples
- **Edge Cases:** 3-5 edge cases with handling
- **Common Errors:** 3-5 errors with solutions
- **Input/Output Contract:** Clear specifications
- **Related Agents:** Links to workflow connections

**Example Enhancement Template:**
   ```markdown
## Examples

### Example 1: [Scenario Name]
**Input State:**
- SPRINT_QUEUE.json: [description]
- Task status: [current state]

**Actions Taken:**
[Step-by-step what agent did]

**Output:**
[Files modified, decisions made]

**Outcome:** [Result]

## Edge Cases

### Edge Case 1: [Situation]
**Problem:** [What's unusual]
**Handling:** [How agent handles it]
**Rationale:** [Why this approach]

## Common Errors

### Error: [Error Message]
**Cause:** [Why it happens]
**Solution:** [How to fix]
**Prevention:** [How to avoid]
```

**Exit Gate:** All 10 agent prompts enhanced, examples verified

---

#### **Step 5: Architecture Documentation (60 min)**
**Goal:** Create `.oodatcaa/ARCHITECTURE.md` - System architecture

**Content:**

**1. System Overview**
- High-level architecture diagram (Mermaid)
- Component responsibilities
- Data flow overview

**2. Agent Architecture**
- Agent interaction diagram
- Coordination flow (Negotiator-centric)
- Communication patterns (file-based)

**3. Data Architecture**
- File structure diagram
- Key files and their roles
- JSON schemas (SPRINT_QUEUE.json, SPRINT_STATUS.json)

**4. Process Architecture**
- OODATCAA loop flow diagram
- Sprint lifecycle state machine
- Task state transitions

**5. Integration Points**
- P001: Daemon system integration
- P002: Log rotation integration
- P003: Sprint management integration
- P004: Documentation integration

**6. Technical Details**
- Lease mechanism
- Lock mechanism
- Baseline tagging
- Archive structure

**Diagrams (Mermaid):**
1. System architecture (components)
2. Agent coordination flow
3. OODATCAA loop (from P004)
4. Sprint lifecycle state machine
5. Task state transitions

**Exit Gate:** Architecture doc complete with 5 diagrams, all rendering correctly

---

#### **Step 6: Documentation Navigation & Integration (45 min)**
**Goal:** Improve navigation across all documentation

**Tasks:**
1. **Update `.oodatcaa/README.md`:**
   - Add navigation index to all docs
   - Categorize by purpose (getting started, operations, reference)
   - Add "See Also" sections

2. **Create Documentation Index:**
   - Add to main README.md
   - Link to all OODATCAA docs
   - Categorize by user type (new user, operator, developer)

3. **Cross-Linking:**
   - Add "Related Documentation" sections to all docs
   - Link RUNBOOK scenarios to TROUBLESHOOTING issues
   - Link agent prompts to OODATCAA_LOOP_GUIDE stages

4. **Consolidation:**
   - Review QUICK_START.md vs ONBOARDING.md for overlap
   - Merge or differentiate clearly
   - Update START_HERE.md to point to ONBOARDING.md

5. **Validation:**
   - Check all markdown links (grep for `](` and verify targets exist)
   - Verify all code examples are syntactically correct
   - Ensure consistent formatting across all docs

**Exit Gate:** All docs cross-linked, navigation clear, links validated

---

#### **Step 7: Documentation Quality & Polish (30 min)**
**Goal:** Final review and quality checks

**Tasks:**
1. **Spell Check:** Run spell checker on all new documentation
2. **Link Validation:** Verify all internal links work
3. **Command Verification:** Test all bash/make commands in examples
4. **Format Consistency:** Ensure consistent markdown style
5. **Date Stamps:** Add "Last Updated" to all modified docs
6. **Version Numbers:** Add version to new documentation files
7. **Table of Contents:** Add TOC to long documents (RUNBOOK, TROUBLESHOOTING)
8. **Final Read-Through:** Fresh eyes review for clarity

**Quality Checks:**
   ```bash
# Check all markdown links
grep -r "](\./" .oodatcaa/ docs/ | while read -r line; do
    # Verify link target exists
done

# Check code block syntax
grep -A 5 "^```" .oodatcaa/RUNBOOK.md

# Spell check
aspell check .oodatcaa/RUNBOOK.md
```

**Exit Gate:** All quality checks pass, documentation polished

---

## Task Breakdown for SPRINT_QUEUE.json

### P006-B01: Steps 1-3 - Runbook + Troubleshooting + Onboarding
**Complexity:** Large  
**Estimated Time:** 225 minutes (~3.75 hours)  
**Steps:** 1, 2, 3  
**Dependencies:** None  
**Deliverables:**
- `.oodatcaa/RUNBOOK.md` (20+ scenarios)
- `.oodatcaa/TROUBLESHOOTING.md` (30+ issues)
- `.oodatcaa/ONBOARDING.md` (complete guide)

**Branch:** `feat/P006-step-01-operational-docs`

---

### P006-B02: Steps 4-5 - Agent Protocols + Architecture
**Complexity:** Medium  
**Estimated Time:** 150 minutes (~2.5 hours)  
**Steps:** 4, 5  
**Dependencies:** P006-B01  
**Deliverables:**
- `.oodatcaa/prompts/*.md` (10 files enhanced)
- `.oodatcaa/ARCHITECTURE.md` (complete with diagrams)

**Branch:** `feat/P006-step-02-agent-protocols`

---

### P006-B03: Steps 6-7 - Navigation + Quality
**Complexity:** Small  
**Estimated Time:** 75 minutes (~1.25 hours)  
**Steps:** 6, 7  
**Dependencies:** P006-B02  
**Deliverables:**
- Updated `.oodatcaa/README.md` with navigation
- Cross-links added to all docs
- Quality checks complete

**Branch:** `feat/P006-step-03-doc-integration`

---

### P006-T01: Testing - Verify All 10 ACs
**Complexity:** Medium  
**Estimated Time:** 45 minutes  
**Dependencies:** P006-B03  
**Deliverables:**
- All 10 acceptance criteria verified
- Documentation accuracy validated
- Links and commands tested

---

## Exit Criteria Summary

This task is complete when:
1. ✅ RUNBOOK.md with 20+ operational scenarios
2. ✅ TROUBLESHOOTING.md with 30+ documented issues
3. ✅ ONBOARDING.md with 15-minute quick start
4. ✅ All 10 agent prompts enhanced with examples
5. ✅ ARCHITECTURE.md complete with 5 diagrams
6. ✅ Documentation navigation improved
7. ✅ All docs cross-linked and integrated
8. ✅ Quality checks pass (links, formatting, commands)
9. ✅ P001-P004 systems documented
10. ✅ New developer can onboard in < 30 minutes

**Unblocks:** None (final documentation task)

---

## Notes

- **Integration Focus:** Must document P001 (daemon), P002 (log rotation), P003 (sprint management), P004 (OODATCAA loop)
- **Practical Emphasis:** Runbook and troubleshooting prioritized over theoretical documentation
- **Agent-Friendly:** Documentation must be parseable by AI agents for self-improvement
- **Tiered Approach:** Quick start (15 min) → Onboarding (30 min) → Runbook (reference) → Deep dive
- **Maintenance Plan:** Date stamps, version numbers, clear ownership for updates

---

**Plan Status:** ✅ Complete  
**Ready for:** Builder (P006-B01)  
**Estimated Total Time:** 450 minutes (~7.5 hours across 3 builder tasks)
