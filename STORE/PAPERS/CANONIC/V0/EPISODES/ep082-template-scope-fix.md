# Episode 082: Template Scope Fix

**Date:** January 9, 2026
**Type:** Redo
**Participants:** Human (Governor General), AI (Codex)
**Agent:** Codex

---

## The Session

We implemented the fix for the templates scope by adding a proper triad and spec under `episodes/templates/`. The correction followed the forward-only redo pattern and avoided any edits to historical episodes.

## Key Assets Discovered

- Templates are a governed scope and require their own triad
- Fixes are documented as new episodes, not retroactive edits

## Violations Detected and Fixed

**Fix:** Added `TEMPLATES.md`, `CANON.md`, `VOCAB.md`, and `README.md` in `episodes/templates/`.

**SWAT**
- **Strengths:** The fix restored governance and preserved immutability of episode history.
- **Weaknesses:** The gap existed because canonification was treated as a reference-only step.
- **Opportunities:** Standardize the rule: every new sub-scope gets a triad immediately.
- **Threats:** Future template scopes could drift if triads aren’t created at creation time.

## Git Signal

- Commit `e8efec3` added the templates triad.

## The Insight

Canonification is complete only when the governed scope itself carries a triad and spec. Forward-only redo preserves drift evidence while restoring compliance.

**Status:** Fix recorded; scope now governed.
