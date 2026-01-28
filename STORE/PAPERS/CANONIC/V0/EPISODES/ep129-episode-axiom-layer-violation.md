# Episode 129: Episode Axiom Layer Violation

**Date:** 2026-01-11
**Type:** Violation + Resolution
**Participants:** Human (Governor General), AI (Claude Opus 4.5)
**Agent:** Claude Opus 4.5

---

## The Session

After canonifying `layer-discipline` in `/os`, Human observed: "WRITING introduces episodes, not PAPER."

This revealed a layer violation in `/os` CANON axiom 5.

## The Violation

**Current state in `/os/CANON.md`:**
```
5. episode:
   OS produce compliant PAPER episodes only when documenting violations
   episode must include complete Git Signal trace
   episode must follow canonical template structure
   correction requires canonification of fix, not episode overwrite
```

**Why it's a violation:**

1. **Episodes are a WRITING concept** — session records for prose production
2. **PAPER is a use case of WRITING** — not the introducer of episodes
3. **OS governs AI behavior** — not application-layer artifacts
4. The axiom conflates:
   - OS (behavior enforcement)
   - WRITING (application layer that introduces episodes)
   - PAPER (specific artifact type)

**Layer-discipline violation:** The operative action is "produce episodes" — that's a WRITING operation, not an OS behavior.

## SWAT Analysis

| Factor | Assessment |
|--------|------------|
| **Severity** | Medium - axiom in wrong scope |
| **Where** | `/os` CANON axiom 5 (should be `/writing`) |
| **When** | Pre-existing, discovered 2026-01-11 |
| **Who** | Historical (prior AI sessions) |
| **Trigger** | Human insight after layer-discipline canonification |

**Root Cause:** Episodes were introduced in the context of PAPER writing, so they were placed near the governance layer (OS). But episodes are an application concept — they belong where prose artifacts are governed.

**Correct abstraction:**
- `/writing` introduces episodes as session records
- `/paper` inherits episode structure and adds paper-specific constraints
- `/os` should not mention episodes at all

## Git Signal

- `/os` - `e0a8173` canonify layer-discipline (exposed this violation)
- `/os` - `6e4ef7b` remove episode axiom (FIX)
- `/writing` - `b778f00` add episode axiom (FIX)

## The Fix

1. Remove episode axiom from `/os/CANON.md` ✓
2. Remove episode-related VOCAB entries from `/os/VOCAB.md` ✓
3. Add episode axiom to `/writing/CANON.md` as axiom 1 ✓
4. Add episode VOCAB entries to `/writing/VOCAB.md` ✓
5. Update `/os` layer-discipline axiom: "episode axioms belong in WRITING" ✓

**Status:** Closed

