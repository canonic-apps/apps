# Episode 042 – Canonbase Non-Compliance Documentation

**What went wrong:** Multiple CANON violations occurred during canonbase review.
**Date:** 2026-01-08
**Agent:** Canon Agent

**Type:** Unknown
**Participants:** Unknown
---

## Violations Detected and Fixed Identified

### 1. Wrong Episode Location
- **Violation:** Created Episode 041 in `canonic/paper/episodes/` instead of `paper/episodes/`
- **CANON Violated:** Episode alignment - episodes must be in PAPER repository
- **Evidence:** Episode 041 file exists at wrong path
- **Fix Required:** Move Episode 041 to correct location

### 2. Missing Episodes 031-032
- **Violation:** Episodes 031 and 032 were missing from sequence
- **CANON Violated:** Sequential episode numbering, never reused
- **Evidence:** Gap in episode sequence (030 → 033)
- **Fix Applied:** Restored Episodes 031 and 032 from VOCAB references

### 3. Uncanonified Terminology
- **Violation:** "canonbase" term used without VOCAB entry
- **CANON Violated:** All governance terms must be in VOCAB.md
- **Evidence:** Term appeared in paper without definition
- **Fix Applied:** Added canonbase to root VOCAB.md

### 4. Missing Episode Triad
- **Violation:** `paper/episodes/` lacked triad (CANON.md, VOCAB.md, README.md)
- **CANON Violated:** Triad requirement - all governed directories must have triad
- **Evidence:** Episodes directory had no CANON/VOCAB/README
- **Fix Applied:** Added triad to paper/episodes/

### 5. Direct Prose Generation
- **Violation:** Wrote canonbase-paper.md directly without Episode→Asset→Prose→Output FSM flow
- **CANON Violated:** WRITING machine FSM transitions must be followed
- **Evidence:** Paper generated at prose/output level without episode extraction
- **Fix Required:** Run proper PAPER machine cycle

---

## Canonification Required

1. **Move Episode 041** to `paper/episodes/` (correct location)
2. **Canonify Episode 042** as non-compliance documentation
3. **Consumer Apply** Episode 042 to all 4 repos

---

**Evidence:** Git history analysis across CANONIC, PAPER, and WRITING repos confirms violations.

## The Session

Not recorded in original episode.

## Key Assets Discovered

Not recorded in original episode.

## Git Signal

Not recorded in original episode.

## The Insight

Not recorded in original episode.

**Status:** Not recorded in original episode.
