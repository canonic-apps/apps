# Episode 104: OS Protocol Template Undo Violation

**Date:** 2026-01-11
**Type:** Violation
**Participants:** Human (Governor General), AI (Codex)
**Agent:** Codex

---

## The Session

You asked for generic OS-level protocols. I replaced the existing OS canon-only protocol with a generic template, which functionally undid an enforced OS axiom. You called it out as an undo git signal and a violation. We reverted the change to restore the canon-only protocol.

## Key Assets Discovered

- OS protocols must enforce OS CANON, not erase it.

## Violations Detected and Fixed

**Violation:** I removed the OS canon-only protocol and replaced it with a generic template, which reversed an enforceable OS axiom and created drift.

**SWAT**
- **Strengths:** The undo was caught immediately.
- **Weaknesses:** I treated "generic" as "empty," removing enforcement.
- **Opportunities:** Keep protocols generic in structure but specific to OS axioms.
- **Threats:** Template substitutions can silently disable enforcement.

## Git Signal

- `os` – `f3cf2ee` Revert "Replace canon-only protocol with generic template"

## The Insight

Generic protocol structure is fine, but OS protocols must remain tied to OS axioms. Replacing enforcement with a blank template is an undo, not a refactor.

**Status:** Fixed via revert.
