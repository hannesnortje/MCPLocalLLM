# Agent Management Guide — When to Launch Agents

## 🚀 Startup Strategy (Recommended)

### Phase 1: Launch Just the Negotiator
**At project start, launch ONLY:**
1. **Negotiator** (coordinator) — Run in background continuously

That's it! The Negotiator will coordinate everything and tell you when to launch other agents.

---

## 🤖 How the Negotiator Signals You

The Negotiator will include instructions in its output when more agents are needed:

### Example Negotiator Output:
```markdown
## Coordination Status — Sprint 1

### Actions Needed:
⚠️ LAUNCH AGENT: Sprint Planner
- Reason: No sprint goal exists yet
- Command: Load @Cursor Rules and @Project Rules. 
           Run .oodatcaa/prompts/sprint-planner.md exactly.
- Run: Once (not background)

### Current State:
- Sprint status: none (need Sprint Planner)
- Tasks ready: 0
- WIP limits: OK
```

### When Negotiator Detects Work:
```markdown
## Coordination Status — Sprint 1

### Actions Needed:
⚠️ LAUNCH AGENT: Builder (1st instance)
- Reason: 3 tasks ready, no builders active
- Command: Load @Cursor Rules and @Project Rules. 
           Run .oodatcaa/prompts/builder.md exactly.
- Run: In background
- OWNER_TAG: agent-builder-A

✅ Planner: Active (working on W001)
📊 WIP: 0/3 builders, 0/2 testers
```

---

## 🔄 Progressive Agent Launch (As Needed)

### Typical Launch Sequence:

**T+0 min: Project Start**
```
YOU: Edit OBJECTIVE.md
YOU: Launch Negotiator (background)
```

**T+1 min: Negotiator's first run**
```
NEGOTIATOR OUTPUT: "⚠️ LAUNCH AGENT: Sprint Planner (no sprint exists)"
YOU: Launch Sprint Planner (one-time)
```

**T+2 min: Sprint Planner generates Sprint 1**
```
SPRINT PLANNER OUTPUT: Sprint 1 created with 4 tasks
NEGOTIATOR OUTPUT (next run): "⚠️ LAUNCH AGENT: Planner (tasks need detailed plans)"
YOU: Launch Planner (background)
```

**T+10 min: Planner completes plans**
```
PLANNER OUTPUT: AGENT_PLAN.md created for task W001
NEGOTIATOR OUTPUT: "⚠️ LAUNCH AGENT: Builder #1 (3 tasks ready)"
YOU: Launch Builder-A (background)
```

**T+60 min: Builder finishes first task**
```
BUILDER OUTPUT: Task W001 complete, awaiting test
NEGOTIATOR OUTPUT: "⚠️ LAUNCH AGENT: Tester (1 task awaiting test)"
YOU: Launch Tester (background)
```

**T+90 min: More work available**
```
NEGOTIATOR OUTPUT: "⚠️ SCALE UP: Launch Builder #2 (WIP 1/3, 2 tasks queued)"
YOU: Launch Builder-B (background) with OWNER_TAG: agent-builder-B
```

---

## 📊 Recommended Agent Scaling

### Minimal (Solo Dev Mode)
```
1 Negotiator (background, continuous)
1 Planner (background, on-demand)
1 Builder (background)
1 Tester (background)
```
**Total: 4 concurrent Cursor chats**

### Standard (Team Mode)
```
1 Negotiator (background, continuous)
1 Planner (background)
2-3 Builders (background, parallel work)
1-2 Testers (background)
1 Integrator (background)
```
**Total: 6-8 concurrent Cursor chats**

### Heavy (Fast Development)
```
1 Negotiator (background, continuous)
1 Sprint Planner (on-demand)
1 Planner (background)
3 Builders (background, max parallelism)
2 Testers (background)
1 Refiner (background)
1 Integrator (background)
```
**Total: 9-10 concurrent Cursor chats**

---

## 🎯 Agent Lifecycle Management

### Always Running (Background)
- **Negotiator** — Coordination loop (runs every 15-30 min)

### Launch on Demand (Background)
These agents should run continuously once launched:
- **Planner** — Waits for tasks marked "needs_plan"
- **Builder(s)** — Waits for tasks marked "ready"
- **Tester** — Waits for tasks marked "awaiting_test"
- **Refiner** — Waits for tasks marked "needs_adapt"
- **Integrator** — Waits for tasks marked "ready_for_integrator"

### One-Time Execution (Not Background)
These agents run once when needed:
- **Sprint Planner** — Called by Negotiator at sprint boundaries
- **Sprint Close** — Called at end of sprint
- **Release** — Called for release finalization
- **Triage** — Called for bug triage

---

## 🚦 Detecting When Agents Are Idle

### Check SPRINT_QUEUE.json
```json
{
  "tasks": [
    {"id": "W001", "status": "ready"},      // ← Builder needed!
    {"id": "W002", "status": "needs_plan"}, // ← Planner needed!
    {"id": "W003", "status": "awaiting_test"} // ← Tester needed!
  ]
}
```

### Check AGENT_LOG.md (Recent Activity)
```markdown
2025-10-01T10:45Z - builder-A - W001 - gates PASS - awaiting_test
2025-10-01T10:30Z - planner-A - W002 - plan created - ready
# If no recent entries → agents may be idle or stuck
```

### Negotiator Heartbeats (SPRINT_LOG.md)
```markdown
2025-10-01T10:50Z - Heartbeat - WIP: builder 1/3, tester 0/2
⚠️ Tester idle but 1 task awaiting_test → LAUNCH TESTER
```

---

## 🛠️ Practical Launch Commands

### Copy-Paste Ready

**Negotiator (START HERE):**
```
Load @Cursor Rules and @Project Rules. 
Run the prompt in .oodatcaa/prompts/negotiator.md exactly. 
Return only file diffs.
```
➜ Run in **Background** ✅

**Sprint Planner (when Negotiator requests):**
```
Load @Cursor Rules and @Project Rules. 
Run the prompt in .oodatcaa/prompts/sprint-planner.md exactly. 
Return only file diffs.
```
➜ Run **Once** (not background)

**Planner:**
```
Load @Cursor Rules and @Project Rules. 
Run the prompt in .oodatcaa/prompts/planner.md exactly. 
Return only file diffs.
```
➜ Run in **Background** ✅

**Builder #1:**
```
Load @Cursor Rules and @Project Rules. 
Run the prompt in .oodatcaa/prompts/builder.md exactly. 
Return only file diffs.
```
➜ Run in **Background** ✅
➜ Optional: Add first line `OWNER_TAG: agent-builder-A` to the prompt

**Builder #2 (if scaling up):**
```
OWNER_TAG: agent-builder-B
Load @Cursor Rules and @Project Rules. 
Run the prompt in .oodatcaa/prompts/builder.md exactly. 
Return only file diffs.
```
➜ Run in **Background** ✅

**Tester:**
```
Load @Cursor Rules and @Project Rules. 
Run the prompt in .oodatcaa/prompts/tester.md exactly. 
Return only file diffs.
```
➜ Run in **Background** ✅

**Integrator:**
```
Load @Cursor Rules and @Project Rules. 
Run the prompt in .oodatcaa/prompts/integrator.md exactly. 
Return only file diffs.
```
➜ Run in **Background** ✅

---

## 🔍 Monitoring Agent Activity

### Cursor UI
- Each background agent runs in its own chat
- Look for "Agent X is running in background" indicator
- Check recent messages for activity

### File Watching
Watch these files for changes (use `watch` or file watcher):
```bash
# Terminal 1: Watch queue changes
watch -n 10 cat .oodatcaa/work/SPRINT_QUEUE.json

# Terminal 2: Tail agent log
tail -f .oodatcaa/work/AGENT_LOG.md

# Terminal 3: Watch sprint progress
watch -n 30 cat .oodatcaa/objectives/SPRINT_GOAL.md
```

### Check Leases
```bash
# See which agents are active
ls -la .leases/
# Shows: W001-builder-A.json, W002-planner-A.json, etc.

# Check specific lease
cat .leases/W001-builder-A.json
# Shows: heartbeat timestamp, ttl
```

---

## ⚠️ Troubleshooting

### "No agents are doing anything"
1. Check if Negotiator is running (background chat active?)
2. Check SPRINT_QUEUE.json — are there tasks marked "ready"?
3. Launch agents as Negotiator suggests

### "Too many agents running, things are slow"
1. Stop extra builders (keep 1-2)
2. Stop refiner if no "needs_adapt" tasks
3. Keep only: Negotiator + Planner + 1-2 Builders + 1 Tester

### "Agent seems stuck"
1. Check .leases/ — is there a stale lease?
2. Negotiator will auto-detect stale leases (>10min) and reset
3. Or manually delete lease file and restart agent

### "Don't know which agents to launch"
**Just follow Negotiator's instructions!** It will tell you exactly which agents to launch and when.

---

## 💡 Best Practices

### ✅ DO:
- Start with just Negotiator
- Launch agents as Negotiator requests
- Run most agents in background
- Use OWNER_TAG for multiple instances (builder-A, builder-B)
- Monitor Negotiator output for instructions

### ❌ DON'T:
- Launch all agents at startup (wasteful)
- Run Negotiator without background mode (it needs to loop)
- Launch multiple Planners (only 1 needed)
- Ignore Negotiator's launch requests (work will stall)
- Run Sprint Planner in background (it's one-time per sprint)

---

## 🎯 TL;DR — Simple Startup

**Step 1:** Edit OBJECTIVE.md
**Step 2:** Launch Negotiator (background)
**Step 3:** Wait for Negotiator to tell you which agents to launch
**Step 4:** Launch agents as requested
**Step 5:** Watch agents work! ✨

The Negotiator is your guide — it will coordinate everything and tell you exactly when to scale up or down.

