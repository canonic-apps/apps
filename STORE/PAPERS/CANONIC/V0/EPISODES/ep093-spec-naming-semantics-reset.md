# Episode 093: Spec Naming Semantics Reset

**Date:** 2026-01-10
**Type:** Violation
**Participants:** USER, AI
**Agent:** Codex

---

## The Session

Realigned spec naming to reflect the intended hierarchy: specs are human entry points named `00-SPECNAME`, and governed artifacts use abbreviated prefixes. Renamed specs and governed artifacts across scopes to match the rule.

## Key Assets Discovered

- machine/CANON.md
- paper/episodes/EPISODES.md

## Violations Detected and Fixed

**Violation:** Spec filenames encoded the wrong semantics (`*-00-SPEC.md`), and governed artifacts did not use spec-based abbreviations.

**SWAT**
- **Strengths:** Clear naming intent surfaced and was actionable across scopes.
- **Weaknesses:** Prior naming drifted from the intended semantic model.
- **Opportunities:** Normalize naming across specs and governed artifacts to prevent future drift.
- **Threats:** Reference drift if legacy names persist without updates.

## Git Signal

- MACHINE commit `826bf76` (Adopt 00-SPEC and abbreviation naming)
- CANONIC commit `471956f` (Adopt 00-SPEC and te naming)
- GIT commit `92d00c7` (Rename spec to 00-GIT)
- WRITING commit `73f8741` (Rename spec to 00-WRITING)
- PAPER commit `09ca2c9` (Adopt 00-SPEC and ep/te naming)

## The Insight

Spec naming encodes authority. Using `00-SPECNAME` for specs and spec-based abbreviations for governed artifacts makes the hierarchy visible and reduces naming drift.

**Status:** Recorded
