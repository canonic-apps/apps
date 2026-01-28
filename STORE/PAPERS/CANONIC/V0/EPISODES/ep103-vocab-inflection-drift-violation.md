# Episode 103: VOCAB Inflection Drift Violation

**Date:** 2026-01-10
**Type:** Violation
**Participants:** Human (Governor General), AI (Codex)
**Agent:** Codex

---

## The Session

After the OS VOCAB was regenerated, inflected variants (enforce/enforces/enforcement, machine(s), scope(s), output(s), report(s)) were added to satisfy literal introspection. This reintroduced vocabulary bloat and drifted from the concept-only principle. We corrected the vocabularies across CANONIC, MACHINE, OS, WRITING, GIT, and PAPER, normalized CANON verb forms where needed, and canonified the concept-only rule in the CANONIC spec and templates.

## Key Assets Discovered

- Concept-only VOCAB: one concept per heading; grammatical variants do not create new entries.
- Base-verb CANON phrasing reduces inflection drift.

## Violations Detected and Fixed

**Violation:** VOCAB entries expanded into inflected variants (e.g., enforce/enforces/enforcement, machine(s), scope(s), output(s), report(s)) instead of single concept stems, repeating the bloat drift noted in Episodes 061 and 083 and contradicting the CANON-closed vocabulary pattern (Episode 062).

**SWAT**
- **Strengths:** Drift was caught quickly and corrected across the stack with atomic commits.
- **Weaknesses:** Literal introspection was interpreted as word-form coverage; templates lacked an explicit concept-only guard.
- **Opportunities:** Encode concept-only vocabulary in CANONIC SPEC/templates and normalize CANON phrasing to base verbs.
- **Threats:** Regeneration can reintroduce inflection bloat and cause cross-repo drift.

## Git Signal

- `canonic` – `2b370f0` Canonify concept-only vocab
- `os` – `1644e8c` Redo OS vocab to concept-only
- `machine` – `14e39f8` Redo machine vocab to concept-only
- `git` – `a3d451a` Redo git vocab to concept-only
- `writing` – `7040e7d` Redo writing vocab to concept-only
- `paper` – `de5fed3` Redo paper vocab to concept-only

## The Insight

VOCAB defines concepts, not word forms. Inflected variants are not new concepts and must not appear as separate entries. Canonical templates and specs must state this explicitly to prevent regeneration drift.

**Status:** Fixed and canonified.
