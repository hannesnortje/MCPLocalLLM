# OODATCAA Agent Prompts — Autonomous Mode

## 🚀 Quick Start (Autonomous Workflow)

**You only need to edit ONE file:** `.oodatcaa/objectives/OBJECTIVE.md`

Then launch agents and they'll self-organize!

### Step 1: Define Your Objective
Edit `.oodatcaa/objectives/OBJECTIVE.md` with:
- Vision (what problem you're solving)
- Outcome (what success looks like)
- Success criteria (how agents know when done)
- Constraints (technical requirements)

### Step 2: Launch the Negotiator (Coordinator)
Open a Cursor chat:
```
Load @Cursor Rules and @Project Rules. 
Run the prompt in .oodatcaa/prompts/negotiator.md exactly. 
Return only file diffs.
```
Click **Run in Background** and let it run continuously (every 15-30 min).

### Step 3: Launch Other Agents As Requested
**The Negotiator will tell you when to launch other agents!**

It will output messages like:
```
⚠️ LAUNCH AGENT: Sprint Planner
- Reason: No sprint goal exists yet
- Command: Load @Cursor Rules and @Project Rules. 
           Run .oodatcaa/prompts/sprint-planner.md exactly.
```

Copy the command, paste in a new Cursor chat, and run.

**Typical sequence:**
1. Negotiator → requests Sprint Planner
2. Sprint Planner runs (once) → creates sprint goal
3. Negotiator → requests Planner
4. Planner runs (background) → creates detailed plans
5. Negotiator → requests Builder(s)
6. Builder(s) run (background) → implement code
7. Negotiator → requests Tester
8. Tester runs (background) → validates acceptance
9. Negotiator → coordinates Integrator
10. Integrator runs (background) → merges PRs

**See `../AGENT_MANAGEMENT.md` for complete guide.**

---

## 🤖 Agent Roles

### Autonomous Coordination
- **negotiator.md** — Control plane; manages sprint lifecycle, coordinates all other agents
- **sprint-planner.md** — Generates sprint goals from OBJECTIVE.md; decides when project is complete
- **project-completion-detector.md** — Evaluates if objective achieved; generates completion report

### Development Workflow
- **planner.md** — Observe/Orient/Decide; creates detailed plans for work items
- **builder.md** — Act; implements code changes on feature branches
- **tester.md** — Test/Check; validates acceptance criteria
- **refiner.md** — Adapt; decides quick fixes vs rollbacks
- **integrator.md** — Archive; merges PRs, tags releases, updates docs

### Utilities
- **sprint-close.md** — Sprint retrospective and summary
- **release.md** — Release finalization (RC → GA)
- **triage.md** — Bug triage to work items

---

## 🎛 Manual Mode (Optional)

If you want more control, you can launch agents individually:

```
Load @Cursor Rules and @Project Rules. 
Run the prompt in .oodatcaa/prompts/<role>.md exactly.
```

Roles: sprint-planner, planner, builder, tester, refiner, integrator, negotiator

Owner tags (optional): Add `OWNER_TAG: agent-builder-A` to label leases for parallel work.

---

## 📊 Monitoring Progress

Watch these files (auto-updated by agents):
- `.oodatcaa/objectives/SPRINT_GOAL.md` — Current sprint goal & progress
- `.oodatcaa/work/SPRINT_QUEUE.json` — Task status
- `.oodatcaa/work/AGENT_LOG.md` — Detailed execution log
- `.oodatcaa/work/SPRINT_LOG.md` — Sprint summaries & decisions

