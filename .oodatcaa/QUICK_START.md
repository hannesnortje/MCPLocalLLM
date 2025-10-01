# 🚀 OODATCAA Quick Start Guide

## 📋 What You Need to Know

**The OODATCAA system is file-based autonomous development** where agents coordinate through files, not through background processes.

### Key Principle:
- Agents write to files → You run Negotiator → It reads files → Tells you what's next
- **On-demand coordination** (not background due to Cursor limitations)

---

## 🎯 How to Use the System

### **Step 1: Run Negotiator to Check Status**

```
Load @Cursor Rules and @Project Rules. 
Run .oodatcaa/prompts/negotiator.md exactly.
CRITICAL: Follow the MANDATORY output format from @Cursor Rules.
Return only file diffs.
```

**Run as:** Once (not in background)

### **Step 2: Follow the Instructions**

Negotiator will output:

```markdown
## 🎯 NEXT ACTION REQUIRED

**LAUNCH AGENT: <Agent Name>**

**COPY-PASTE THIS COMMAND:**
```
Load @Cursor Rules and @Project Rules. 
Run .oodatcaa/prompts/<agent>.md exactly.
```

**Run as:** Once (not in background)
```

### **Step 3: Run That Agent**

Copy the command and run it in a new chat.

### **Step 4: Repeat**

After the agent completes, go back to Step 1 (run Negotiator again).

---

## 🔄 Complete Workflow

```
1. Run Negotiator → "Launch Sprint Planner"
2. Run Sprint Planner → Creates Sprint 1
3. Run Negotiator → "Launch Planner"
4. Run Planner → Creates detailed plans
5. Run Negotiator → "Launch Builder"
6. Run Builder → Implements code
7. Run Negotiator → "Launch Tester"
8. Run Tester → Validates work
9. Run Negotiator → Next cycle...
```

---

## 🎯 Current Status

Check these files to understand current state:
- `.oodatcaa/objectives/SPRINT_GOAL.md` - Current sprint and progress
- `.oodatcaa/work/SPRINT_QUEUE.json` - Task statuses
- `.oodatcaa/work/AGENT_LOG.md` - Recent agent activity

---

## 📚 Documentation

- `README.md` - Overview and setup
- `AGENT_MANAGEMENT.md` - Agent details and commands
- `PARALLEL_AGENTS_GUIDE.md` - Running multiple builders
- `WORKFLOW_ANALYSIS.md` - How the system works

---

## ❓ FAQ

**Q: Why not background mode?**
A: Cursor background agents cache files and don't detect changes. On-demand is more reliable.

**Q: How do I know what's next?**
A: Run the Negotiator - it always tells you exactly what to do.

**Q: Can I run multiple agents?**
A: Yes! See `PARALLEL_AGENTS_GUIDE.md` for details on parallel builders.

**Q: Where do I start?**
A: Run the Negotiator command (Step 1 above).

---

**That's it!** The system tells you exactly what to do at each step. Just follow the commands.

