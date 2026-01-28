# Episode 025: Failed Canon Consumption and Corrective Action

**Date:** 2026-01-08
**Agent:** Canon Agent

**Type:** Unknown
**Participants:** Unknown
## The Session

User asked: "is git compliant? I see changes. why dont you follow the canon?" This followed a commit where I added Episode 021 definition and episode timeline to VOCAB.md without first consuming the existing canon.

## Investigation

**What went wrong:**
1. Modified VOCAB.md with fresh content
2. Committed as "Canonify Episode 021..."
3. Violation: Episode 021 was already canonified in HEAD~1

**Evidence:**
```bash
cd /Users/iDrDex/Code/paper
git show HEAD~1:VOCAB.md | grep -A5 "Episode 021"
# Episode 021 was already there!
```

**The existing canon already had:**
- Episode 019 definition
- Episode 021 definition  
- Episode Timeline (partial)
- Multi-Repo Locations
- Violations Documented

## Canon Pattern Violation

**Producer vs Consumer commit misuse:**
- My commit: "Canonify Episode 021 multi-repo disconnect correction" (producer)
- Correct action: "Apply Episode 021 canonification" (consumer)

**Rule violated:** Canonify = discovering NEW patterns. Apply = enforcing EXISTING constraints.

Since Episode 021 was already in the canon, this should have been a consumer commit (Apply), not producer (Canonify).

## Root Cause

Failed to consume existing canon before committing:
1. `git show HEAD:VOCAB.md` (read existing canon) - SKIPPED
2. Identify gaps - SKIPPED
3. Add only missing content - SKIPPED
4. Commit as "Apply" (consumer) - SKIPPED

## Corrective Action

1. **Document as Episode 025** - Preserve violation as evidence
2. **Reset VOCAB.md** - `git checkout HEAD -- VOCAB.md`
3. **Consume existing canon** - `git show HEAD:VOCAB.md`
4. **Apply only missing pieces** - Identify what's new vs existing
5. **Commit as Apply** - "Apply Episode 025 canonification pattern"

## The Pattern

**Failed Canon Consumption:**
- Write fresh content without reading existing canon
- Producer commit for already-canonified content
- No consumption step before production

**Correct Canon Consumption:**
1. READ: `git show HEAD:VOCAB.md`
2. ANALYZE: What exists? What's missing?
3. PRODUCE: Only add genuinely new content
4. CONSUME: Commit as "Apply [existing canon]" not "Canonify [already there]"

## Why This Matters

Canonification is about discovering NEW patterns, not re-stating existing ones. If content is already canonified:
- Don't "canonify" it again
- "Apply" the existing canon
- Only produce when genuinely NEW patterns emerge

The git signal shows the violation clearly: my commit duplicated existing canon content.

---

**Status:** Episode documented, reset and correction pending

## Key Assets Discovered

Not recorded in original episode.

## Violations Detected and Fixed

Not recorded in original episode.

## Git Signal

Not recorded in original episode.

## The Insight

Not recorded in original episode.
