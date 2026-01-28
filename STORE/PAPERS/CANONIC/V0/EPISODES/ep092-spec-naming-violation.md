# Episode 092: Spec Naming Violation

**Date:** 2026-01-10
**Type:** Violation
**Participants:** USER, AI
**Agent:** Codex

---

## The Session

Detected that spec artifacts were named `*-000_spec.md` instead of the intended `*-00-SPEC.md`. Updated nomenclature rules and renamed specs across scopes to align with the intended semantic pattern.

## Key Assets Discovered

- machine/CANON.md
- paper/episodes/EPISODES.md

## Violations Detected and Fixed

Strengths
- Clear intent for spec naming emerged from the episode review.

Weaknesses
- Spec filenames used `*-000_spec.md`, contradicting the intended `00-SPEC` form.

Opportunities
- Canonified a single spec naming rule and aligned all specs to it.

Threats
- Naming drift across scopes if spec filenames diverge again.

## Git Signal

- MACHINE commit `bf64db2` (Rename specs to 00-SPEC)
- CANONIC commit `cf637bf` (Rename specs to 00-SPEC)
- WRITING commit `321beb5` (Rename spec to 00-SPEC)
- GIT commit `61e5a79` (Rename spec to 00-SPEC)
- PAPER commit `a3a2e39` (Rename specs to 00-SPEC)

## The Insight

Spec filenames encode semantic intent; keeping the `00-SPEC` form consistent across scopes prevents drift and makes the spec artifact visually unambiguous.

**Status:** Recorded
