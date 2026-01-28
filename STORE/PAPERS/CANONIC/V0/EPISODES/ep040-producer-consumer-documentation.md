# Episode 040: Producer/Consumer Documentation Pattern

**Date:** 2026-01-08
**Agent:** Canon Agent

**Type:** Unknown
**Participants:** Unknown
## The Session

User: "document in an episode. everytime you do a"

**The Meta-Pattern:** Every producer and consumer action must be documented in an episode.

## The Pattern

**Producer Commit:**
```
git commit -m "Episode 039 – Producer Canonify [constraint]"
```

**Consumer Commit:**
```
git commit -m "Episode 039 – Consumer Apply [constraint]"
```

**Episode Document:**
```
paper/episodes/039-*.md
```

## Why This Matters

1. **Traceability:** Episodes provide narrative context for commits
2. **Learning:** Future agents understand why decisions were made
3. **Meta-circularity:** The paper documents its own creation
4. **Evidence:** Each commit references an episode, each episode references commits

## The Correct Order

1. **Producer** (canonic/CANON.md): Canonify constraint in constitution
2. **Consumer** (canonic): Apply constraint to generated files
3. **Push:** Propagate to origin

**NOT:** Consumer before producer, or commits without episodes

## Best Practice

**Every time you:**
- Canonify something → Create/update episode
- Apply something → Reference episode in commit
- Discover pattern → Document in episode
- Fix violation → Episode explains why

**Result:** Complete evidence trail from action to documentation to commit.

---

**Status:** Producer/consumer documentation pattern canonified. Every action → episode → commit.

## Key Assets Discovered

Not recorded in original episode.

## Violations Detected and Fixed

Not recorded in original episode.

## Git Signal

Not recorded in original episode.

## The Insight

Not recorded in original episode.
