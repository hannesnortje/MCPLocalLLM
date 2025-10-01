# 🔄 Running Multiple Agents in Parallel

## 🎯 When You Need Multiple Builders

The Negotiator will tell you when to launch multiple builders. For example:

```markdown
## 🎯 NEXT ACTION REQUIRED

**LAUNCH AGENT: Builder #1**

**COPY-PASTE THIS COMMAND:**
```
Load @Cursor Rules and @Project Rules. 
Run .oodatcaa/prompts/builder.md exactly.
```

**Run as:** Once (not background)

**Why:** Tasks W001 and W002 are ready and independent
**What it will do:** Implement W001 (MCP Server File Migration)

---

**ALSO LAUNCH: Builder #2 (if you want parallel work)**

**COPY-PASTE THIS COMMAND:**
```
OWNER_TAG: builder-B
Load @Cursor Rules and @Project Rules. 
Run .oodatcaa/prompts/builder.md exactly.
```

**Run as:** Once (not background)

**Why:** Task W002 is independent and can run in parallel
**What it will do:** Implement W002 (Dependency Consolidation)
```

## 📋 How Multiple Agents Work

### **Key Concept: OWNER_TAG**

Each agent instance needs a unique identifier:

- **Builder A**: No OWNER_TAG needed (or `OWNER_TAG: builder-A`)
- **Builder B**: `OWNER_TAG: builder-B`
- **Builder C**: `OWNER_TAG: builder-C`

### **WIP Limits (from SPRINT_QUEUE.json)**

```json
{
  "wip_limits": {
    "planner": 1,    // Only 1 planner at a time
    "builder": 3,    // Up to 3 builders in parallel
    "tester": 2,     // Up to 2 testers in parallel
    "integrator": 1  // Only 1 integrator at a time
  }
}
```

## 🚀 Launching Multiple Builders

### **Example: 2 Builders in Parallel**

**Chat 1 - Builder A:**
```
Load @Cursor Rules and @Project Rules. 
Run .oodatcaa/prompts/builder.md exactly.
```

**Chat 2 - Builder B:**
```
OWNER_TAG: builder-B
Load @Cursor Rules and @Project Rules. 
Run .oodatcaa/prompts/builder.md exactly.
```

### **Both builders will:**
1. Read SPRINT_QUEUE.json
2. Find tasks with status `ready`
3. Pick different tasks (using leases to avoid conflicts)
4. Work independently
5. Commit their changes
6. Update task status to `awaiting_test`

## 🔐 Lease System Prevents Conflicts

When Builder A starts:
1. Reads SPRINT_QUEUE.json
2. Finds W001 with status `ready`
3. Creates lease: `.leases/W001-builder-A.json`
4. Works on W001

When Builder B starts:
1. Reads SPRINT_QUEUE.json  
2. Sees W001 has active lease (Builder A)
3. Finds W002 with status `ready`
4. Creates lease: `.leases/W002-builder-B.json`
5. Works on W002

**No conflicts!** Each builder works on different tasks.

## 📊 Workflow with Multiple Builders

### **Step-by-Step:**

1. **Run Negotiator** (once) → Detects 3 ready tasks

   Output:
   ```
   3 tasks ready: W001, W002, W003
   WIP: 0/3 builders available
   
   Launch up to 3 builders for parallel work!
   ```

2. **Launch Builder #1** (Chat 1)
   ```
   Load @Cursor Rules and @Project Rules. 
   Run .oodatcaa/prompts/builder.md exactly.
   ```

3. **Launch Builder #2** (Chat 2)
   ```
   OWNER_TAG: builder-B
   Load @Cursor Rules and @Project Rules. 
   Run .oodatcaa/prompts/builder.md exactly.
   ```

4. **Launch Builder #3** (Chat 3 - optional)
   ```
   OWNER_TAG: builder-C
   Load @Cursor Rules and @Project Rules. 
   Run .oodatcaa/prompts/builder.md exactly.
   ```

5. **Wait for builders to complete** (each commits independently)

6. **Run Negotiator** (once) → Checks what's next

   Output:
   ```
   3 tasks now: awaiting_test
   Launch Tester to validate
   ```

7. **Launch Tester** (once)

## ⏱️ Timing

**Sequential (1 builder):**
- W001: 30 minutes
- W002: 45 minutes  
- W003: 60 minutes
- **Total: 135 minutes** (2h 15m)

**Parallel (3 builders):**
- W001, W002, W003 all at once
- **Total: 60 minutes** (longest task)
- **Speedup: 2.25x faster!**

## 🎯 When to Use Multiple Builders

**Use multiple builders when:**
- ✅ Multiple tasks have status `ready`
- ✅ Tasks are independent (no dependencies)
- ✅ You want faster completion
- ✅ Tasks are substantial enough to warrant parallelism

**Use single builder when:**
- ❌ Only 1 task is `ready`
- ❌ Tasks have dependencies
- ❌ Tasks are quick (< 10 minutes)
- ❌ Resources are limited

## 📋 Negotiator Will Tell You

The Negotiator's output will indicate:

```markdown
**Ready Tasks:** 3 (W001, W002, W003)
**WIP Status:** builder 0/3 available

**RECOMMENDATION:** Launch 2-3 builders for parallel work
```

Then it provides commands for each builder with unique OWNER_TAGs.

## 🔄 After Parallel Work

All builders complete independently:

```
Builder A: W001 → awaiting_test ✅
Builder B: W002 → awaiting_test ✅  
Builder C: W003 → awaiting_test ✅
```

Then run Negotiator:

```
3 tasks awaiting test
Launch 1-2 testers (WIP limit: 2)
```

You can launch multiple Testers the same way!

## 💡 Best Practices

1. **Start with 1 builder** to understand the flow
2. **Add more builders** when you see multiple ready tasks
3. **Don't exceed WIP limits** (check SPRINT_QUEUE.json)
4. **Use unique OWNER_TAGs** (builder-A, builder-B, builder-C)
5. **Let agents complete** before running Negotiator again
6. **Check lease files** (`.leases/`) to see active work

## 📁 File Structure with Multiple Agents

```
.leases/
├── W001-builder-A.json     ← Builder A working on W001
├── W002-builder-B.json     ← Builder B working on W002
└── W003-builder-C.json     ← Builder C working on W003

.oodatcaa/work/
├── SPRINT_QUEUE.json       ← All tasks and their status
├── AGENT_LOG.md            ← All agent activity logged here
└── SPRINT_LOG.md           ← Sprint-level coordination
```

## 🎯 Summary

**Multiple agents = Parallel work = Faster completion!**

The Negotiator coordinates everything:
- Tells you when to launch multiple agents
- Provides unique commands with OWNER_TAGs
- Agents use leases to avoid conflicts
- Each agent works independently
- All progress tracked in shared files

**Just follow the Negotiator's instructions** - it will tell you when and how to launch multiple agents!

---

**Example Command Structure:**

```
# Builder A (first builder)
Load @Cursor Rules and @Project Rules. 
Run .oodatcaa/prompts/builder.md exactly.

# Builder B (second builder)
OWNER_TAG: builder-B
Load @Cursor Rules and @Project Rules. 
Run .oodatcaa/prompts/builder.md exactly.

# Builder C (third builder)
OWNER_TAG: builder-C
Load @Cursor Rules and @Project Rules. 
Run .oodatcaa/prompts/builder.md exactly.
```

That's it! The system handles the rest through file-based coordination and leases.

