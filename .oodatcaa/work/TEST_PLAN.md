# TEST_PLAN: P006 - Process Documentation & Runbook

**Task ID:** P006  
**Test Plan Version:** 1.0  
**Created:** 2025-10-03T22:30:00+02:00  
**Agent:** agent-planner-A

---

## Test Strategy

**Approach:** Documentation validation and completeness verification  
**Focus Areas:**
1. Operational procedures completeness
2. Troubleshooting coverage
3. Onboarding effectiveness
4. Agent protocol clarity
5. Architecture documentation accuracy
6. Navigation and cross-linking
7. Quality and consistency

**Test Environment:**
- OS: Linux 6.14.0-33-generic
- Documentation Tools: markdown linters, link checkers
- Working Directory: /media/hannesn/storage/Code/MCPLocalLLM

---

## Quality Gates (Run First)

### Format Check
```bash
black --check .
```
**Expected:** All files pass formatting check  
**Acceptance:** 0 files need formatting (no Python files modified)

### Lint Check
```bash
ruff check .
```
**Expected:** ≤29 errors (Sprint 2 baseline)  
**Acceptance:** No new ruff errors introduced (no code changes)

### Type Check
```bash
mypy .
```
**Expected:** ~401 mypy errors (Sprint 1 baseline)  
**Acceptance:** No new mypy errors (no code changes)

### Unit Tests
```bash
pytest -q
```
**Expected:** All existing tests pass  
**Acceptance:** 13 passed, 3 skipped (W006 baseline maintained)

### Build Check
```bash
python -m build
```
**Expected:** Clean build  
**Acceptance:** Package builds successfully

### Security Audit
```bash
pip-audit
```
**Expected:** 0 high-severity vulnerabilities  
**Acceptance:** No new security issues

---

## Acceptance Criteria

### AC1: RUNBOOK.md Complete with 20+ Scenarios ✅

**Requirement:** Operational runbook with comprehensive procedures

**Test Procedure:**
```bash
# 1. Verify RUNBOOK.md exists
test -f .oodatcaa/RUNBOOK.md && echo "PASS: RUNBOOK.md exists"

# 2. Count documented scenarios
grep -c "^### Scenario:" .oodatcaa/RUNBOOK.md

# 3. Verify categories covered
grep -i "Sprint Operations\|Agent Operations\|System Maintenance" .oodatcaa/RUNBOOK.md

# 4. Check scenario structure (Procedure, Expected Output, Troubleshooting sections)
grep -c "#### Procedure:" .oodatcaa/RUNBOOK.md
grep -c "#### Expected Output:" .oodatcaa/RUNBOOK.md
grep -c "#### Troubleshooting:" .oodatcaa/RUNBOOK.md

# 5. Verify all commands have code blocks
grep -A 3 "#### Procedure:" .oodatcaa/RUNBOOK.md | grep -c "^```"

# 6. Check Sprint 2 systems documented
grep -i "make sprint-status\|make sprint-complete\|daemon\|log rotation" .oodatcaa/RUNBOOK.md

# 7. Test example commands (safe ones)
grep "^make sprint-status" .oodatcaa/RUNBOOK.md && make sprint-status --help 2>/dev/null || echo "Command documented"

# 8. Check table of contents exists
grep -i "table of contents\|## Contents" .oodatcaa/RUNBOOK.md

# 9. Verify "See Also" cross-references
grep -c "#### See Also:" .oodatcaa/RUNBOOK.md

# 10. Check file size (should be substantial)
wc -l .oodatcaa/RUNBOOK.md | awk '{if ($1 > 500) print "PASS: Comprehensive"; else print "FAIL: Too short"}'
```

**Expected Results:**
- RUNBOOK.md file exists in `.oodatcaa/` directory
- ≥20 scenarios documented (grep count ≥20)
- All three categories present (Sprint, Agent, System)
- Each scenario has Procedure, Expected Output, Troubleshooting sections
- All procedures have code blocks with commands
- P001-P004 systems referenced
- Table of contents for navigation
- Cross-references between scenarios
- File is substantial (>500 lines)

**Pass Criteria:**
- ≥20 scenarios documented
- All major scenario categories covered
- Consistent structure across all scenarios
- All commands formatted properly
- Sprint 2 systems documented

---

### AC2: TROUBLESHOOTING.md with 30+ Issues ✅

**Requirement:** Comprehensive troubleshooting guide with diagnostic procedures

**Test Procedure:**
```bash
# 1. Verify TROUBLESHOOTING.md exists
test -f .oodatcaa/TROUBLESHOOTING.md && echo "PASS: TROUBLESHOOTING.md exists"

# 2. Count documented issues
grep -c "^### Issue:" .oodatcaa/TROUBLESHOOTING.md

# 3. Verify categories covered
grep -i "Agent Issues\|System Issues\|Process Issues" .oodatcaa/TROUBLESHOOTING.md

# 4. Check issue structure (Symptoms, Diagnosis, Solution, Prevention)
grep -c "^\*\*Symptoms:\*\*" .oodatcaa/TROUBLESHOOTING.md
grep -c "^\*\*Diagnosis:\*\*" .oodatcaa/TROUBLESHOOTING.md
grep -c "^\*\*Solution:\*\*" .oodatcaa/TROUBLESHOOTING.md
grep -c "^\*\*Prevention:\*\*" .oodatcaa/TROUBLESHOOTING.md

# 5. Verify diagnostic commands have code blocks
grep -A 3 "**Diagnosis:**" .oodatcaa/TROUBLESHOOTING.md | grep -c "^```"

# 6. Check common Sprint 2 issues documented
grep -i "SPRINT_QUEUE.json\|lease\|lock\|quality gate\|log rotation" .oodatcaa/TROUBLESHOOTING.md

# 7. Verify "Related Issues" cross-references
grep -c "^\*\*Related Issues:\*\*" .oodatcaa/TROUBLESHOOTING.md

# 8. Check file size
wc -l .oodatcaa/TROUBLESHOOTING.md | awk '{if ($1 > 600) print "PASS: Comprehensive"; else print "FAIL: Too short"}'

# 9. Verify index or TOC
grep -i "table of contents\|## Contents\|## Index" .oodatcaa/TROUBLESHOOTING.md

# 10. Test diagnostic commands are safe (read-only)
! grep "rm -rf\|--force\|DELETE\|DROP" .oodatcaa/TROUBLESHOOTING.md && echo "PASS: No destructive commands"
```

**Expected Results:**
- TROUBLESHOOTING.md file exists
- ≥30 issues documented (grep count ≥30)
- All three categories present (Agent, System, Process)
- Each issue has Symptoms, Diagnosis, Solution, Prevention
- Diagnostic commands in code blocks
- Common Sprint 2 issues covered
- Cross-references between related issues
- File is substantial (>600 lines)
- Table of contents for navigation
- No destructive commands in examples

**Pass Criteria:**
- ≥30 issues documented
- All major issue categories covered
- Consistent structure across all issues
- Diagnostic procedures safe and tested
- Sprint 2 common issues included

---

### AC3: ONBOARDING.md with Quick Start Path ✅

**Requirement:** Developer onboarding guide with 15-minute quick start

**Test Procedure:**
```bash
# 1. Verify ONBOARDING.md exists
test -f .oodatcaa/ONBOARDING.md && echo "PASS: ONBOARDING.md exists"

# 2. Check main sections present
grep "## Welcome\|## Quick Start\|## Core Concepts\|## First Sprint\|## Common Tasks\|## Next Steps" .oodatcaa/ONBOARDING.md

# 3. Verify Quick Start is actionable
grep -A 20 "## Quick Start" .oodatcaa/ONBOARDING.md | grep -E "Step [0-9]:|^[0-9]+\."

# 4. Check Quick Start time estimate
grep -i "15 minutes\|15-minute\|quick start" .oodatcaa/ONBOARDING.md

# 5. Verify prerequisites section
grep -i "prerequisite\|requirements\|before you start" .oodatcaa/ONBOARDING.md

# 6. Check for Sprint 1 walkthrough/example
grep -i "sprint 1\|case study\|example sprint\|walkthrough" .oodatcaa/ONBOARDING.md

# 7. Verify links to other docs
grep -c "\[.*\](\./" .oodatcaa/ONBOARDING.md

# 8. Check diagram references
grep -i "diagram\|architecture\|flow" .oodatcaa/ONBOARDING.md

# 9. Verify "Next Steps" section exists
grep -A 10 "## Next Steps" .oodatcaa/ONBOARDING.md

# 10. Check file is beginner-friendly (reasonable length)
wc -l .oodatcaa/ONBOARDING.md | awk '{if ($1 > 200 && $1 < 800) print "PASS: Good length"; else print "CHECK: Length"}'
```

**Expected Results:**
- ONBOARDING.md file exists
- All 6 main sections present (Welcome, Quick Start, Core Concepts, First Sprint, Common Tasks, Next Steps)
- Quick Start has numbered steps
- 15-minute time estimate mentioned
- Prerequisites section exists
- Sprint 1 walkthrough included as example
- Multiple links to other documentation
- Architecture/diagram references
- Next Steps provides continuation path
- File length reasonable (200-800 lines)

**Pass Criteria:**
- Complete onboarding structure
- Quick start actionable in 15 minutes
- Sprint 1 example included
- Clear path to deeper documentation
- Beginner-friendly language

---

### AC4: All Agent Prompts Enhanced with Examples ✅

**Requirement:** 10 agent prompt files enhanced with examples, edge cases, and error handling

**Test Procedure:**
```bash
# 1. List all agent prompts
ls -1 .oodatcaa/prompts/*.md | grep -v README

# 2. Count agent prompts
ls -1 .oodatcaa/prompts/*.md | grep -v README | wc -l

# 3. Check each prompt has "Examples" section
for file in .oodatcaa/prompts/{negotiator,sprint-planner,planner,builder,tester,refiner,integrator,project-completion-detector,sprint-close,triage}.md; do
    grep -q "## Examples" "$file" && echo "PASS: $file has examples" || echo "FAIL: $file missing examples"
done

# 4. Check for "Edge Cases" section
for file in .oodatcaa/prompts/{negotiator,planner,builder,tester,refiner,integrator}.md; do
    grep -q "## Edge Cases\|### Edge Case" "$file" && echo "PASS: $file has edge cases" || echo "FAIL: $file missing edge cases"
done

# 5. Check for "Common Errors" section
for file in .oodatcaa/prompts/{planner,builder,tester,refiner,integrator}.md; do
    grep -q "## Common Errors\|### Error:" "$file" && echo "PASS: $file has error docs" || echo "FAIL: $file missing errors"
done

# 6. Verify examples have structure (Input State, Actions, Output, Outcome)
grep -c "**Input State:**\|**Actions Taken:**\|**Output:**\|**Outcome:**" .oodatcaa/prompts/planner.md

# 7. Count total examples added across all prompts
grep -c "### Example [0-9]" .oodatcaa/prompts/*.md

# 8. Count total edge cases documented
grep -c "### Edge Case" .oodatcaa/prompts/*.md

# 9. Count total errors documented
grep -c "### Error:" .oodatcaa/prompts/*.md

# 10. Check for "Related Agents" or "See Also" sections
grep -c "## Related Agents\|## See Also" .oodatcaa/prompts/*.md
```

**Expected Results:**
- ≥10 agent prompt files exist
- All core agent prompts have "Examples" section (negotiator, planner, builder, tester, refiner, integrator)
- ≥6 prompts have "Edge Cases" section
- ≥5 prompts have "Common Errors" section
- Examples have consistent structure (Input→Actions→Output→Outcome)
- ≥20 total examples across all prompts (2 per agent minimum)
- ≥15 edge cases documented across prompts
- ≥15 errors documented across prompts
- Cross-references between related agents

**Pass Criteria:**
- All 10 target prompts enhanced
- ≥2 examples per core agent
- ≥3 edge cases per core agent
- ≥3 errors per core agent
- Consistent documentation structure

---

### AC5: ARCHITECTURE.md Complete with Diagrams ✅

**Requirement:** System architecture documentation with 5 Mermaid diagrams

**Test Procedure:**
```bash
# 1. Verify ARCHITECTURE.md exists
test -f .oodatcaa/ARCHITECTURE.md && echo "PASS: ARCHITECTURE.md exists"

# 2. Check main sections present
grep "## System Overview\|## Agent Architecture\|## Data Architecture\|## Process Architecture\|## Integration Points\|## Technical Details" .oodatcaa/ARCHITECTURE.md

# 3. Count Mermaid diagrams
grep -c "^```mermaid" .oodatcaa/ARCHITECTURE.md

# 4. Verify diagram types
grep -A 2 "^```mermaid" .oodatcaa/ARCHITECTURE.md | grep -E "graph|flowchart|stateDiagram|sequenceDiagram"

# 5. Check P001-P004 systems documented in Integration Points
grep -A 20 "## Integration Points" .oodatcaa/ARCHITECTURE.md | grep -i "P001\|daemon\|P002\|log rotation\|P003\|sprint management\|P004\|OODATCAA"

# 6. Verify JSON schemas documented
grep -i "SPRINT_QUEUE.json\|SPRINT_STATUS.json" .oodatcaa/ARCHITECTURE.md

# 7. Check technical details (leases, locks, tags, archives)
grep -i "lease\|lock\|baseline.*tag\|archive" .oodatcaa/ARCHITECTURE.md

# 8. Verify file structure diagram/description
grep -i "file structure\|directory.*structure" .oodatcaa/ARCHITECTURE.md

# 9. Check component responsibilities documented
grep -c "responsibility\|responsibilities\|role" .oodatcaa/ARCHITECTURE.md

# 10. Verify file size is substantial
wc -l .oodatcaa/ARCHITECTURE.md | awk '{if ($1 > 300) print "PASS: Comprehensive"; else print "FAIL: Too short"}'
```

**Expected Results:**
- ARCHITECTURE.md file exists
- All 6 main sections present
- ≥5 Mermaid diagrams (exact count ≥5)
- Diagrams use appropriate types (graph, flowchart, stateDiagram, sequence)
- P001-P004 integration documented
- JSON schemas explained
- Technical mechanisms documented (leases, locks, tags, archives)
- File structure explained
- Component responsibilities clear
- File is substantial (>300 lines)

**Pass Criteria:**
- All sections complete
- 5 diagrams render correctly
- P001-P004 systems integrated
- Technical details accurate
- Clear architecture overview

---

### AC6: Documentation Navigation Improved ✅

**Requirement:** Clear navigation across all OODATCAA documentation

**Test Procedure:**
```bash
# 1. Check .oodatcaa/README.md has navigation index
grep -A 20 "## Documentation\|## Navigation\|## Index" .oodatcaa/README.md

# 2. Verify main README.md links to OODATCAA docs
grep -c "\.oodatcaa/" README.md

# 3. Count total OODATCAA documentation files
find .oodatcaa -name "*.md" -type f | wc -l

# 4. Check for categorization (getting started, operations, reference)
grep -i "getting started\|operations\|reference\|guides" .oodatcaa/README.md

# 5. Verify QUICK_START.md references ONBOARDING.md
grep -i "onboarding" .oodatcaa/QUICK_START.md || echo "Check if consolidated"

# 6. Check START_HERE.md points to right docs
grep -c "\.md" .oodatcaa/START_HERE.md

# 7. Verify navigation consistency across key docs
for file in .oodatcaa/{RUNBOOK,TROUBLESHOOTING,ONBOARDING,ARCHITECTURE}.md; do
    grep -q "## See Also\|## Related" "$file" && echo "PASS: $file has navigation" || echo "FAIL: $file missing navigation"
done

# 8. Check cross-links between RUNBOOK and TROUBLESHOOTING
grep -c "TROUBLESHOOTING.md" .oodatcaa/RUNBOOK.md
grep -c "RUNBOOK.md" .oodatcaa/TROUBLESHOOTING.md

# 9. Verify ONBOARDING links to OODATCAA_LOOP_GUIDE
grep -c "OODATCAA_LOOP_GUIDE" .oodatcaa/ONBOARDING.md

# 10. Count total cross-references in new docs
grep -c "](\./" .oodatcaa/{RUNBOOK,TROUBLESHOOTING,ONBOARDING,ARCHITECTURE}.md
```

**Expected Results:**
- .oodatcaa/README.md has comprehensive navigation index
- Main README.md links to OODATCAA documentation
- ≥20 documentation files in `.oodatcaa/`
- Documentation categorized by purpose
- QUICK_START.md and ONBOARDING.md are integrated or differentiated
- START_HERE.md has correct pointers
- All new docs have "See Also" or "Related" sections
- RUNBOOK ↔ TROUBLESHOOTING cross-linked
- ONBOARDING links to OODATCAA_LOOP_GUIDE
- ≥30 cross-references in new documentation

**Pass Criteria:**
- Clear navigation from main README
- All new docs have navigation sections
- Key docs cross-reference each other
- Categorization clear
- Easy to find related content

---

### AC7: All Documentation Cross-Linked ✅

**Requirement:** Comprehensive cross-linking between related documentation

**Test Procedure:**
```bash
# 1. Extract all markdown links from new docs
grep -h "](\./" .oodatcaa/{RUNBOOK,TROUBLESHOOTING,ONBOARDING,ARCHITECTURE}.md | wc -l

# 2. Verify links are valid (targets exist)
for file in .oodatcaa/{RUNBOOK,TROUBLESHOOTING,ONBOARDING,ARCHITECTURE}.md; do
    echo "Checking links in $file..."
    grep -o "](\.oodatcaa/[^)]*)" "$file" 2>/dev/null | sed 's/](//' | sed 's/)//' | while read -r link; do
        test -f ".oodatcaa/$link" || echo "BROKEN: $link in $file"
    done
done

# 3. Check RUNBOOK links to agent prompts
grep -c "prompts/" .oodatcaa/RUNBOOK.md

# 4. Check TROUBLESHOOTING links to RUNBOOK scenarios
grep -c "RUNBOOK.md#" .oodatcaa/TROUBLESHOOTING.md

# 5. Verify ONBOARDING links to multiple docs
grep -o "](\.oodatcaa/[^)]*)" .oodatcaa/ONBOARDING.md | wc -l

# 6. Check ARCHITECTURE links to P004 (OODATCAA_LOOP_GUIDE)
grep -c "OODATCAA_LOOP_GUIDE" .oodatcaa/ARCHITECTURE.md

# 7. Verify bidirectional links (A→B and B→A)
# RUNBOOK → TROUBLESHOOTING
grep -q "TROUBLESHOOTING.md" .oodatcaa/RUNBOOK.md && echo "PASS: RUNBOOK→TROUBLESHOOTING"
# TROUBLESHOOTING → RUNBOOK
grep -q "RUNBOOK.md" .oodatcaa/TROUBLESHOOTING.md && echo "PASS: TROUBLESHOOTING→RUNBOOK"

# 8. Check ONBOARDING → RUNBOOK
grep -q "RUNBOOK.md" .oodatcaa/ONBOARDING.md && echo "PASS: ONBOARDING→RUNBOOK"

# 9. Check ARCHITECTURE → all new docs
for doc in RUNBOOK TROUBLESHOOTING ONBOARDING; do
    grep -q "$doc.md" .oodatcaa/ARCHITECTURE.md && echo "PASS: ARCHITECTURE→$doc" || echo "CHECK: ARCHITECTURE→$doc"
done

# 10. Verify no broken links
! find .oodatcaa -name "*.md" -exec grep -l "](broken\|](TODO\|](FIXME" {} \; && echo "PASS: No placeholder links"
```

**Expected Results:**
- ≥30 markdown links in new documentation
- All link targets exist (no broken links)
- RUNBOOK references agent prompts (scenarios use agents)
- TROUBLESHOOTING links to RUNBOOK scenarios
- ONBOARDING links to multiple docs (≥5 different files)
- ARCHITECTURE links to OODATCAA_LOOP_GUIDE
- Bidirectional links present (RUNBOOK↔TROUBLESHOOTING)
- ONBOARDING links to RUNBOOK for operations
- ARCHITECTURE links to all new docs
- No placeholder or broken links

**Pass Criteria:**
- No broken links
- ≥30 cross-references
- Bidirectional linking implemented
- Key relationships linked (scenarios↔issues, onboarding↔operations)
- All new docs integrated into documentation web

---

### AC8: Quality Checks Pass ✅

**Requirement:** Documentation quality validated (links, formatting, commands)

**Test Procedure:**
```bash
# 1. Validate all markdown links
echo "Checking markdown links..."
for file in .oodatcaa/{RUNBOOK,TROUBLESHOOTING,ONBOARDING,ARCHITECTURE}.md; do
    grep -o "](\.oodatcaa/[^)]*)" "$file" 2>/dev/null | while read -r link_part; do
        link=$(echo "$link_part" | sed 's/](//' | sed 's/)//')
        test -f "$link" && echo "✓ $link" || echo "✗ BROKEN: $link in $(basename $file)"
    done
done

# 2. Check markdown formatting consistency
# Headers should use ## not underlines
! grep -E "^={3,}|^-{3,}" .oodatcaa/{RUNBOOK,TROUBLESHOOTING,ONBOARDING,ARCHITECTURE}.md && echo "PASS: Consistent header formatting"

# 3. Verify code blocks are closed
for file in .oodatcaa/{RUNBOOK,TROUBLESHOOTING,ONBOARDING,ARCHITECTURE}.md; do
    open=$(grep -c "^```" "$file")
    if [ $((open % 2)) -eq 0 ]; then
        echo "PASS: $file has balanced code blocks"
    else
        echo "FAIL: $file has unclosed code blocks"
    fi
done

# 4. Test command examples (safe ones)
echo "Testing safe commands from RUNBOOK..."
# Extract make commands and test they exist
grep "^make " .oodatcaa/RUNBOOK.md | sort -u | while read -r cmd; do
    target=$(echo "$cmd" | awk '{print $2}')
    make -n "$target" 2>/dev/null && echo "✓ $cmd" || echo "✗ $cmd (not in Makefile)"
done

# 5. Check for consistent terminology
# Should use "Sprint" not "sprint", "Agent" not "agent" in titles
grep -E "### [a-z]|## [a-z]" .oodatcaa/{RUNBOOK,TROUBLESHOOTING,ONBOARDING,ARCHITECTURE}.md | head -5

# 6. Verify date stamps present
for file in .oodatcaa/{RUNBOOK,TROUBLESHOOTING,ONBOARDING,ARCHITECTURE}.md; do
    grep -q "Last Updated:\|Updated:\|Date:" "$file" && echo "PASS: $file has date" || echo "FAIL: $file missing date"
done

# 7. Check version numbers
for file in .oodatcaa/{RUNBOOK,TROUBLESHOOTING,ONBOARDING,ARCHITECTURE}.md; do
    grep -q "Version:\|v[0-9]\." "$file" && echo "PASS: $file has version" || echo "CHECK: $file version"
done

# 8. Verify table of contents in long docs
for file in .oodatcaa/{RUNBOOK,TROUBLESHOOTING}.md; do
    lines=$(wc -l < "$file")
    if [ "$lines" -gt 500 ]; then
        grep -q "## Table of Contents\|## Contents" "$file" && echo "PASS: $file has TOC" || echo "FAIL: $file needs TOC"
    fi
done

# 9. Check spell check (basic - common technical terms)
! grep -i "occured\|recieve\|seperate\|teh " .oodatcaa/{RUNBOOK,TROUBLESHOOTING,ONBOARDING,ARCHITECTURE}.md && echo "PASS: No obvious typos"

# 10. Verify all quality gates pass (no code changes expected)
make gates 2>&1 | grep -E "black|ruff|mypy"
```

**Expected Results:**
- All markdown links valid (no broken links)
- Consistent header formatting (## not underlines)
- All code blocks balanced (opened and closed)
- Make commands in examples exist in Makefile
- Consistent capitalization in headers
- All new docs have date stamps
- Version numbers present
- Long docs (>500 lines) have table of contents
- No obvious spelling errors
- All quality gates pass (black, ruff, mypy maintained)

**Pass Criteria:**
- Zero broken links
- All code blocks balanced
- Commands are valid
- Date stamps present
- Quality gates maintained
- Professional formatting

---

### AC9: Existing Documentation Consolidated ✅

**Requirement:** Existing docs reviewed and integrated with new documentation

**Test Procedure:**
```bash
# 1. Check for documentation overlap
# Compare QUICK_START.md vs ONBOARDING.md
diff -u <(head -50 .oodatcaa/QUICK_START.md) <(head -50 .oodatcaa/ONBOARDING.md) | head -20

# 2. Verify START_HERE.md updated to reference ONBOARDING
grep -i "onboarding" .oodatcaa/START_HERE.md && echo "PASS: START_HERE references ONBOARDING"

# 3. Check AGENT_MANAGEMENT.md integrated with new docs
grep -c "RUNBOOK\|TROUBLESHOOTING" .oodatcaa/AGENT_MANAGEMENT.md

# 4. Verify WORKFLOW_ANALYSIS.md references ARCHITECTURE
grep -c "ARCHITECTURE" .oodatcaa/WORKFLOW_ANALYSIS.md || echo "Check if consolidated"

# 5. Check PARALLEL_AGENTS_GUIDE integrated
grep -c "RUNBOOK\|operational" .oodatcaa/PARALLEL_AGENTS_GUIDE.md

# 6. Verify main README.md updated
grep -A 10 "## Documentation" README.md | grep -c "RUNBOOK\|TROUBLESHOOTING\|ONBOARDING\|ARCHITECTURE"

# 7. Check for redundant documentation files
find .oodatcaa -name "*_OLD.md" -o -name "*_BACKUP.md" -o -name "*.md~" | wc -l

# 8. Verify consistent navigation across old and new docs
for file in .oodatcaa/{QUICK_START,AGENT_MANAGEMENT,WORKFLOW_ANALYSIS}.md; do
    grep -q "## See Also\|## Related\|## Documentation" "$file" && echo "PASS: $file has navigation" || echo "CHECK: $file navigation"
done

# 9. Check documentation is not duplicated
# Should not have same content in multiple files
echo "Checking for major content duplication..."
# Manual review of key sections

# 10. Verify documentation hierarchy is clear
cat .oodatcaa/README.md | grep -A 30 "## Documentation"
```

**Expected Results:**
- QUICK_START.md and ONBOARDING.md differentiated or consolidated
- START_HERE.md references ONBOARDING.md
- AGENT_MANAGEMENT.md cross-references new docs
- WORKFLOW_ANALYSIS.md references ARCHITECTURE.md or consolidated
- PARALLEL_AGENTS_GUIDE.md integrated with RUNBOOK
- Main README.md lists all new docs
- No redundant backup files
- Consistent navigation in existing docs
- No major content duplication
- Clear documentation hierarchy

**Pass Criteria:**
- Overlap addressed (differentiated or merged)
- Existing docs reference new docs
- No obsolete files
- Clear hierarchy from getting-started → reference
- Consolidated where appropriate

---

### AC10: Sprint 2 Systems (P001-P004) Documented ✅

**Requirement:** All Sprint 2 infrastructure documented in runbook and guides

**Test Procedure:**
```bash
# 1. Check P001 (Background Agent Daemon) documentation
grep -i "daemon\|background agent\|agent.*process" .oodatcaa/{RUNBOOK,ONBOARDING,ARCHITECTURE}.md

# 2. Verify P002 (Log Rotation) procedures
grep -i "log rotation\|rotate.*log\|archive.*log" .oodatcaa/{RUNBOOK,TROUBLESHOOTING}.md

# 3. Check P003 (Sprint Management) scenarios
grep -i "make sprint-status\|make sprint-complete\|make sprint-new\|sprint.*dashboard" .oodatcaa/{RUNBOOK,ONBOARDING}.md

# 4. Verify P004 (OODATCAA Loop) references
grep -c "OODATCAA_LOOP_GUIDE\|OODATCAA loop\|8.*stage" .oodatcaa/{ONBOARDING,ARCHITECTURE}.md

# 5. Check P001 daemon commands documented
grep -i "make agents-start\|make agents-stop\|agent.*daemon" .oodatcaa/RUNBOOK.md

# 6. Verify P002 rotation commands
grep "bash scripts/rotate-logs.sh\|make.*rotate" .oodatcaa/RUNBOOK.md

# 7. Check P003 sprint commands
grep -E "make sprint-status|make sprint-complete|make sprint-new" .oodatcaa/RUNBOOK.md | wc -l

# 8. Verify P004 loop documentation integration
grep -c "Check stage\|adaptation.*loop\|Start-Over Gate" .oodatcaa/{RUNBOOK,ONBOARDING}.md

# 9. Check troubleshooting for all P001-P004
for system in "daemon" "log rotation" "sprint management" "OODATCAA loop"; do
    grep -i "$system" .oodatcaa/TROUBLESHOOTING.md && echo "✓ $system troubleshooting"
done

# 10. Verify architecture integration points documented
grep -A 20 "## Integration Points" .oodatcaa/ARCHITECTURE.md | grep -c "P001\|P002\|P003\|P004"
```

**Expected Results:**
- P001 daemon system documented in RUNBOOK, ONBOARDING, ARCHITECTURE
- P002 log rotation procedures in RUNBOOK, TROUBLESHOOTING
- P003 sprint management commands in RUNBOOK (all 3 make targets)
- P004 OODATCAA loop referenced in ONBOARDING, ARCHITECTURE
- P001 daemon commands documented (agents-start, agents-stop, agents-status)
- P002 rotation commands documented (rotate-logs.sh, --dry-run)
- P003 commands documented (≥3 references)
- P004 loop concepts integrated (Check stage, adaptation, Start-Over)
- Troubleshooting for all P001-P004 systems
- Architecture integration points documented (≥4 systems mentioned)

**Pass Criteria:**
- All 4 Sprint 2 systems documented
- Operational procedures for each system
- Troubleshooting coverage for each system
- Integration points explained
- Commands and usage examples included

---

## Test Execution Summary

### Prerequisites Checklist
- [ ] Repository at latest commit (P001-P004 integrated)
- [ ] No uncommitted changes
- [ ] All Sprint 2 infrastructure operational
- [ ] Documentation tools available (markdown linter, link checker)

### Execution Order
1. Run quality gates first (black, ruff, mypy, pytest, build, audit)
2. Test AC1: RUNBOOK.md complete
3. Test AC2: TROUBLESHOOTING.md complete
4. Test AC3: ONBOARDING.md complete
5. Test AC4: Agent prompts enhanced
6. Test AC5: ARCHITECTURE.md complete
7. Test AC6: Navigation improved
8. Test AC7: Cross-linking complete
9. Test AC8: Quality checks pass
10. Test AC9: Existing docs consolidated
11. Test AC10: P001-P004 documented

### Success Criteria
**All 10 ACs must pass for task to be ready_for_integrator.**

**Critical ACs (must pass):**
- AC1: RUNBOOK.md complete
- AC2: TROUBLESHOOTING.md complete
- AC3: ONBOARDING.md complete
- AC10: Sprint 2 systems documented

**Important ACs (should pass):**
- AC4: Agent prompts enhanced
- AC5: ARCHITECTURE.md complete
- AC7: Cross-linking complete
- AC9: Existing docs consolidated

**Quality ACs (negotiate if needed):**
- AC6: Navigation (can improve iteratively)
- AC8: Quality checks (minor issues acceptable)

---

## Risk Assessment

### Low Risk
- Navigation improvements (AC6) - Can iterate
- Quality checks (AC8) - Non-blocking issues

### Medium Risk
- Cross-linking completeness (AC7) - Time-consuming to verify all links
- Existing doc consolidation (AC9) - May require judgment calls

### High Risk
- Documentation completeness (AC1-3) - Must be comprehensive
- P001-P004 coverage (AC10) - Critical for Sprint 2 completion

### Mitigation
- Use automation for link checking
- Systematic review of all doc files
- Test commands in examples
- Review Sprint 2 objectives for completeness

---

## Notes for Tester

### Manual Testing Required
- Read ONBOARDING.md as new user (actual onboarding test)
- Try RUNBOOK scenarios for common operations
- Use TROUBLESHOOTING.md to diagnose test issue
- Verify diagrams render correctly in preview

### Automated Testing Scope
- Quality gates (format, lint, type)
- Link validation (grep + test -f)
- File existence checks
- Command validation (make -n)
- Consistency checks (structure, formatting)

### Known Limitations
- Cannot fully test onboarding effectiveness without new user
- Diagram rendering depends on markdown viewer
- Some commands require operational system
- Cross-linking exhaustive test is time-consuming

### Recommendations
- Use markdown preview for diagram verification
- Test safe commands (read-only) from RUNBOOK
- Verify all make targets exist before testing
- Check link validity with automated script
- Review for clarity and completeness

---

**Test Plan Status:** ✅ Complete  
**Ready for:** Tester (after P006-B03 complete)  
**Estimated Testing Time:** 45 minutes  
**Risk Level:** Medium (comprehensive documentation review required)
