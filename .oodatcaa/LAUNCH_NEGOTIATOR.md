# 🚀 LAUNCH THE NEGOTIATOR

## Copy-Paste This EXACT Command:

```
Load @Cursor Rules and @Project Rules. 
Run .oodatcaa/prompts/negotiator.md exactly.
IMPORTANT: You MUST end your response with the MANDATORY output format defined in @Cursor Rules (python.mdc).
Return only file diffs.
```

## Then Click: "Run in Background" ✨

---

## What to Expect:

The Negotiator will analyze the current state and output:

```markdown
---

## 🎯 NEXT ACTION REQUIRED

**LAUNCH AGENT: Sprint Planner**

**COPY-PASTE THIS COMMAND:**
```
Load @Cursor Rules and @Project Rules. 
Run .oodatcaa/prompts/sprint-planner.md exactly.
```

**Run as:** Once (not in background)

**Why:** No sprint exists - need to create Sprint 1
**What it will do:** Analyze OBJECTIVE.md and create Sprint 1
```

## If You DON'T See This Format:

The agent isn't following the mandatory format. Try this enhanced command:

```
Load @Cursor Rules and @Project Rules.
Read the MANDATORY output format section in @Cursor Rules (python.mdc).
Run .oodatcaa/prompts/negotiator.md exactly.
Your response MUST end with the exact format from python.mdc showing "🎯 NEXT ACTION REQUIRED" with a copy-paste code block.
Return only file diffs.
```

---

## The Format MUST Include:

✅ Section header: "## 🎯 NEXT ACTION REQUIRED"
✅ Agent name clearly stated
✅ Code block with exact command to copy-paste
✅ "Run as: Background" or "Once (not in background)"
✅ Brief explanation of why and what

**Without this format, the agent is not following the rules correctly.**

