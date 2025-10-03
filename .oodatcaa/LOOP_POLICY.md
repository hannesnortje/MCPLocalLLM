# OODATCAA Loop Limit Policy

> **Purpose:** Formal policy for adaptation loop limits, warning levels, and Start-Over Gate triggers.

**Version:** 1.0  
**Effective:** 2025-10-03  
**Status:** Active

---

## Policy Statement

All OODATCAA tasks are subject to a **maximum of 3 adaptation loops** before triggering the Start-Over Gate. This policy ensures:
- **Efficiency**: Prevents infinite adaptation cycles
- **Quality**: Forces fundamental rethinking when quick fixes fail
- **Pragmatism**: Balances perfectionism with progress
- **Learning**: Documents failed approaches for future work

---

## Loop Limit Framework

### Standard Limit: 3 Adaptation Loops

```
Task → Build → Test → Check
                        ↓
                [Pass?] → Archive ✅
                        ↓
                [Fail] → Adapt → Test → Check (Loop 1)
                                          ↓
                                  [Pass?] → Archive ✅
                                          ↓
                                  [Fail] → Adapt → Test → Check (Loop 2)
                                                            ↓
                                                    [Pass?] → Archive ✅
                                                            ↓
                                                    [Fail] → Adapt → Test → Check (Loop 3)
                                                                              ↓
                                                                      [Pass?] → Archive ✅
                                                                              ↓
                                                                      [Fail] → START-OVER GATE
```

###

 Warning Levels

| Loop | Status | Action Required | Decision Authority |
|------|--------|----------------|-------------------|
| **Loop 1** | 🟢 Normal | Continue adaptation | Builder + Refiner |
| **Loop 2** | 🟡 Warning | Review decision criteria, log complexity note | Refiner + Negotiator review |
| **Loop 3** | 🟠 Escalation | Negotiator must approve continuation or trigger Start-Over | Negotiator (required) |
| **Loop 4+** | 🔴 Requires Override | User approval required, document rationale | User + Negotiator |

---

## Loop 1: Normal Operations

**Status:** 🟢 **Normal** (expected, most tasks adapt once)

**Typical Scenarios:**
- Import errors from file moves
- Type annotation corrections
- API signature mismatches
- Minor quality gate violations

**Process:**
1. Refiner analyzes test failures
2. Applies targeted fixes
3. Re-runs tests
4. Logs adaptation in `AGENT_LOG.md`

**Authority:** Refiner (autonomous)

**Sprint 1 Evidence:** 6 of 9 adaptations occurred in Loop 1 (67%)

---

## Loop 2: Warning Level

**Status:** 🟡 **Warning** (deeper issues, requires review)

**Typical Scenarios:**
- Multiple failing ACs (< 80% pass rate)
- Architectural misalignments
- Integration failures
- Persistent quality gate failures

**Process:**
1. Refiner documents issues in detail
2. Negotiator reviews decision criteria
3. Consider approach tweaks vs Start-Over
4. Log "complex task" flag in `SPRINT_QUEUE.json`
5. Apply adaptive fixes
6. Re-test with enhanced monitoring

**Authority:** Refiner + Negotiator review

**Decision Criteria Review:**
- Are we fixing symptoms or root causes?
- Is the approach fundamentally sound?
- Would Start-Over be faster than adaptation?

**Sprint 1 Evidence:** 3 of 9 adaptations reached Loop 2 (33%)

---

## Loop 3: Escalation Required

**Status:** 🟠 **Escalation** (final attempt, Negotiator decision)

**Typical Scenarios:**
- Fundamental design flaws emerging
- Scope creep beyond original plan
- Dependencies unmet after 2 loops
- Architectural dead-end

**Process:**
1. **MANDATORY:** Negotiator approval required to continue
2. Negotiator evaluates:
   - Root cause analysis
   - Alternative approaches
   - Start-Over Gate trigger conditions
   - Resource/time implications
3. **Decision:**
   - **Continue (Loop 3):** One final adaptation with clear success criteria
   - **Start-Over Gate:** Rollback and re-plan
4. Document decision + rationale in `SPRINT_LOG.md`

**Authority:** Negotiator (required), Refiner (execution)

**Sprint 1 Evidence:** 0 tasks reached Loop 3 (0%) — excellent planning!

---

## Loop 4+: User Override Required

**Status:** 🔴 **Override Required** (exceptional circumstances)

**When Needed:**
- Loop 3 failed but path forward is clear
- External factors caused failures (environment, dependencies)
- Strategic decision to continue despite policy

**Process:**
1. Negotiator requests **user approval**
2. Document:
   - Why Loop 3 failed
   - Why override is justified
   - Clear success criteria for Loop 4
   - Estimated additional time/effort
3. User approves or rejects
4. If approved: Log override in `SPRINT_LOG.md` and add to Sprint retrospective

**Authority:** User (required), Negotiator (execution)

**Sprint 1 Evidence:** 0 overrides needed (0%)

---

## Start-Over Gate

### Trigger Conditions

**Automatic Triggers:**
1. **Loop 3 completes** and < 60% ACs pass
2. **Fundamental approach wrong** (Planner + Refiner consensus)
3. **No clear path forward** (adaptation not improving outcomes)
4. **Scope creep** (work exceeds 2x original estimate)
5. **Architectural dead-end** (requires major redesign)

**Manual Triggers:**
- Negotiator determination
- User request
- Resource/time constraints

### Start-Over Process

```bash
# 1. Create baseline tag (if not exists)
git tag "pre/<TASK_ID>-step-<N>-$(date -u +%Y%m%dT%H%M%S)"
git push --tags

# 2. Rollback to baseline
git reset --hard <baseline_tag>
git push --force-with-lease origin <branch>

# 3. Release lease
rm .leases/<TASK_ID>.json

# 4. Update queue
#    status: in_progress → needs_plan
#    agent: null
#    Add: rollback_reason, rollback_count

# 5. Document in logs
#    - SPRINT_LOG.md: Start-Over Gate trigger + rationale
#    - AGENT_LOG.md: Failed approach + lessons learned
```

### Documentation Requirements

**Mandatory Entries:**
1. **SPRINT_LOG.md**
   - Trigger condition (which rule)
   - Rationale (why Start-Over chosen over Loop 4)
   - Failed approach summary
   - Lessons learned

2. **AGENT_LOG.md**
   - Detailed timeline of adaptation attempts
   - What was tried, what failed
   - Root cause analysis
   - Recommended new approach

3. **SPRINT_QUEUE.json**
   - Update task status: `needs_plan`
   - Add: `rollback_count`, `rollback_reason`, `rollback_at`
   - Increment: `adaptation_attempts` counter

### Lessons Learned

**Capture:**
- What assumptions were wrong?
- What should Planner have considered?
- What patterns to avoid?
- What worked despite failure?

**Apply:**
- Update agent prompts if systemic issue
- Add to planning checklist
- Document in OODATCAA_LOOP_GUIDE.md

---

## Metrics & Monitoring

### Key Metrics

1. **Average loops per task**
   - Target: ≤ 1.5 loops
   - Sprint 1: 1.5 loops (excellent!)

2. **Adaptation success rate (Loop 1)**
   - Target: ≥ 60%
   - Sprint 1: 67% (above target!)

3. **Loop 3 frequency**
   - Target: < 10% of tasks
   - Sprint 1: 0% (perfect!)

4. **Start-Over Gate triggers**
   - Target: < 5% of tasks
   - Sprint 1: 0% (no rollbacks!)

### Dashboard

View current metrics:
```bash
make loop-metrics
```

Track trends over time in `ROTATION_STATS.md` and Sprint retrospectives.

---

## Exceptions & Special Cases

### Exception 1: External Dependencies

If failure caused by external factors (network, API changes, environment), adaptation doesn't count toward loop limit.

**Example:** Third-party API change requires code update → Loop 1 (external) not counted.

### Exception 2: Test Infrastructure Issues

If test failures are due to test infrastructure (not code quality), fix test infrastructure first, then re-test.

**Example:** Flaky test causing false negative → Fix test, re-run (doesn't count).

### Exception 3: Documentation Tasks

Documentation-only tasks (no code) use simplified criteria:
- Loop 1-2: Normal review/revision
- Loop 3+: Only if fundamental restructuring needed

---

## Policy Review

**Review Frequency:** Every sprint retrospective

**Review Criteria:**
- Are loop limits appropriate?
- Are warning levels triggering correctly?
- Is Start-Over Gate threshold right?
- Sprint metrics vs targets

**Adjustment Process:**
1. Propose change in Sprint retrospective
2. Document rationale
3. Update this policy (version +1)
4. Announce to all agents

---

## References

- **OODATCAA Loop Guide:** `.oodatcaa/OODATCAA_LOOP_GUIDE.md`
- **Agent Prompts:** `.oodatcaa/prompts/` (negotiator.md, refiner.md)
- **Sprint Planning:** `.oodatcaa/objectives/SPRINT_GOAL.md`
- **Metrics Dashboard:** `make loop-metrics`

---

**Policy Owner:** Negotiator  
**Last Review:** 2025-10-03  
**Next Review:** Sprint 2 Retrospective  
**Version:** 1.0

---

