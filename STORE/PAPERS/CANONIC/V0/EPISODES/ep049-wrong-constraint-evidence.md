# Episode 049 – Wrong Constraint Evidence (Preserved)

**Evidence of layer violation:** What the wrong constraint looked like before reset.
**Date:** 2026-01-08
**Agent:** Canon Agent

**Type:** Unknown
**Participants:** Unknown
---

## The Wrong Constraint

This was added to CANONIC/CANON.md (root paradigm) before being caught and removed:

```markdown
### AI/USER commit separation
**AI must never commit on USER's behalf. USER commits their own work.**

When USER performs work (external agent interaction, specification edits, etc.):
1. AI documents the work in an episode
2. AI leaves changes unstaged
3. AI asks USER to commit with their own message

**Violation:** AI committing USER's work with AI-constructed message.
```

**Why this was wrong:**
- CANONIC (root) = pure paradigm
- Contains fundamental governance principles only
- Git workflow patterns belong in MACHINE (implementation layer)

---

## The Wrong Commit

```
4c0939d Episode 048 – Canonify layer violation reset
1 file changed, 20 insertions(+), 2 deletions(-)
```

This commit was then RESET to remove the violation.

**Why reset was appropriate here:**
- Reset to UNDERSTAND the violation
- NOT to fix it (that requires a new commit)
- Evidence trail preserved in Episode 048 and 049

---

## What We Learned

1. **Paradigm ≠ Implementation**
   - CANONIC: What (fundamental principles)
   - MACHINE: How (git workflow, validation)

2. **Reset for Understanding**
   - Use reset to remove wrong constraint
   - Follow with commit explaining why
   - Preserve evidence as episodes

3. **Correct Location**
   - AI/USER separation is now in MACHINE/CANON.md
   - Git interface belongs in implementation layer

---

## Evidence Preservation

This episode preserves:
- The wrong constraint text
- The commit hash that added it (4c0939d)
- The reset that removed it
- The correct constraint in MACHINE/CANON.md

All evidence traces to git history.

## The Session

Not recorded in original episode.

## Key Assets Discovered

Not recorded in original episode.

## Violations Detected and Fixed

Not recorded in original episode.

## Git Signal

Not recorded in original episode.

## The Insight

Not recorded in original episode.

**Status:** Not recorded in original episode.
