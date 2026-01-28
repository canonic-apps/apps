# Episode 105: Spec Name Repo Match Violation

**Date:** 2026-01-11
**Type:** Violation
**Participants:** Human (Governor General), AI (Codex)
**Agent:** Codex

---

## The Session

You flagged that `00-CANONIC.md` was a misnomer after the fixed-point shift. We discovered a gap: root spec naming was not defined in CANONIC. We canonified the rule that repo specs are unnumbered and match the repo name (case-insensitive), then renamed specs across the stack and added OS enforcement.

## Key Assets Discovered

- Repo spec filenames must match repo names and be unnumbered.

## Violations Detected and Fixed

**Violation:** Spec filenames used `00-` numbering, which became non-compliant once the spec naming rule was defined.

**SWAT**
- **Strengths:** The misnomer was identified and resolved quickly across all repos.
- **Weaknesses:** The naming rule was implicit, allowing drift to persist.
- **Opportunities:** Canonify naming at CANONIC and enforce in OS to prevent recurrence.
- **Threats:** Undefined naming rules produce cross-repo ambiguity.

## Git Signal

- `canonic` – `894d2c5` Rename CANONIC spec to unnumbered
- `machine` – `3ad5aca` Rename machine specs to unnumbered
- `os` – `fb49dd1` Canonify spec naming and unnumbered specs
- `writing` – `0fe6dae` Rename writing spec to unnumbered
- `git` – `684a1ec` Rename git spec to unnumbered
- `paper` – `72eb7c0` Rename paper specs to unnumbered

## The Insight

Spec naming is constitutional. When a naming rule is undefined, drift appears as misnomers. Canonifying the rule and enforcing it in OS closes the gap.

**Status:** Fixed and canonified.
