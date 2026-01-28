# Episode 128: vocab-closure Layer Violation

**Date:** 2026-01-11
**Type:** Violation + Resolution
**Participants:** Human (Governor General), AI (Claude Opus 4.5)
**Agent:** Claude Opus 4.5

---

## The Session

During compliance review of CANONIC, Human asked if there was a meta-CANON to close VOCAB gaps automatically. AI found none and proposed canonifying a `vocab-closure` axiom.

AI placed the axiom in `/os` CANON instead of `/git` CANON.

## The Violation

**What I did:**
- Added `vocab-closure` axiom to `/os/CANON.md` (axiom 9)
- Added supporting VOCAB entries to `/os/VOCAB.md`
- Committed and pushed to `/os`

**Why it's a violation:**
- `vocab-closure` is a **pre-commit verification** tied to producer commits
- Commits are governed by `/git`, not `/os`
- `/os` governs AI behavior enforcement, not git operations
- The trigger is "before producer commit" — a git concept

## SWAT Analysis

| Factor | Assessment |
|--------|------------|
| **Severity** | Medium - axiom in wrong scope, but functionally correct |
| **Where** | `/os` scope (should be `/git`) |
| **When** | 2026-01-11 during vocab-closure canonification |
| **Who** | Claude Opus 4.5 (AI) |
| **Trigger** | Human asked to canonify automatic closure |

**Root Cause:** I conflated:
- "AI must do X" (governance behavior → `/os`)
- "before commit Y" (git operation → `/git`)

The axiom says "AI must verify VOCAB closure **before producer commit**". The operative constraint is on the commit action, not on AI behavior generally. Commits live in `/git`.

**Pattern recognized:** When an axiom constrains an action that belongs to scope X, the axiom belongs in scope X — regardless of who performs the action.

## Git Signal

- `/os` - `37f903d` canonify vocab-closure axiom (VIOLATION)
- `/os` - `3ac23ce` close VOCAB to CANON
- `/os` - `d675c11` remove vocab-closure axiom (FIX)
- `/git` - `ec75520` add vocab-closure axiom (FIX)

## The Fix

1. Remove `vocab-closure` axiom from `/os/CANON.md` ✓
2. Remove related VOCAB entries from `/os/VOCAB.md` ✓
3. Add `vocab-closure` axiom to `/git/CANON.md` as axiom 7 ✓
4. Add related VOCAB entries to `/git/VOCAB.md` ✓

**Status:** Closed

