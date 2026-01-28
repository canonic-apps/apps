# Episode 081: Template Scope Canonification Violation

**Date:** January 9, 2026
**Type:** Violation
**Participants:** Human (Governor General), AI (Codex)
**Agent:** Codex

---

## The Session

We confirmed that `episodes/templates/` was referenced in canon, but the directory itself lacked its own triad and spec. I had called the templates “canonified,” which ignored the requirement that every governed scope has its own triad. You flagged this as a violation to test whether the redo process now catches and records violations correctly.

## Key Assets Discovered

- Canonification requires the governed scope to be fully triad-compliant
- Referencing a scope in canon is not the same as governing it

## Violations Detected and Fixed

**Violation:** Claimed episode templates were canonified without a triad/spec in `episodes/templates/`.

**SWAT**
- **Strengths:** The gap was detected immediately and traced to the governance requirement.
- **Weaknesses:** I treated a canon reference as full canonification and missed the triad requirement.
- **Opportunities:** Add a triad/spec to `episodes/templates/` to make the scope fully governed.
- **Threats:** Undermines trust in canon claims and creates drift in self-documenting scopes.

## Git Signal

- Commit `39d0a10` referenced templates without creating a triad in the templates scope.

## The Insight

This violation confirms the redo path: violations are now recorded in a standardized episode with SWAT, and the fix is forward-only (add triad/spec) rather than retroactive edits.

**Status:** Violation recorded; fix required.
