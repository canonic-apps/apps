# Episode 088: Episode Insights Canonification Review

**Date:** 2026-01-09
**Type:** Analysis
**Participants:** Human (Governor General), AI (Codex)
**Agent:** Codex

---

## The Session

I reviewed the full episode archive to identify insights that appear in episode records but are not yet canonified in `paper/CANON.md`. The review uses explicit “The Insight” sections where present and flags gaps where early episodes lacked an insight section. Findings are grouped into: (1) already canonified, (2) candidates for canonification, and (3) conflicts with current canon language.

## Key Assets Discovered

**Already canonified (no further action):**
- Autocommit after canon changes and explicit USER override (Episode 086).
- Canonification approval requirement and commit+push coupling (Episode 087).
- Episodes governed for template compliance (recent CANON update).

**Candidates for canonification (in episodes, not explicit in CANON):**
- **VOCAB-first principle** — VOCAB should be read/defined before CANON/README (Episode 011).
- **Episode→Asset→Prose→Output FSM detail** — Episodes are unprocessed capture; Prose is processed episodes (Episode 016).
- **Redo commit specificity** — Redo commits should reference episode number, agent role, and violation (Episode 024).
- **Coherence vs compliance distinction** — Governance requires both semantic coherence and structural compliance (Episode 054).
- **VOCAB self-governance recursion** — VOCAB defines “fully governed” and must satisfy it (Episode 055).
- **CANON / CANONIC / VOCAB roles** — CANON minimal invariants; CANONIC as human spec; VOCAB as definitions (Episode 057).
- **Minimal machine primitives** — Enforcement belongs in MACHINE, not CANONIC (Episode 058).
- **SPEC primacy with CANON+VOCAB co-equal** (Episode 059).
- **Literal introspection + minimal axioms** — VOCAB defines terms across CANON/SPEC/README/self (Episode 060).
- **Forward-only standardization** — Episodes immutable; corrections via new episodes (Episodes 079–082).
- **Template vocab locality** — Template VOCAB must stay locally scoped (Episode 083).
- **Reversal narrative requirement** — Reversals need full causal narrative in episodes (Episode 085).

**Conflicts to resolve:**
- `paper/CANON.md` still says “Episodes are ungoverned input,” which conflicts with the newly canonified template governance requirement.

**Coverage gaps:**
- Many early episodes (001–009, 012–015, etc.) lack explicit “The Insight” sections, so their canon candidates are not extractable without interpretation.

## Violations Detected and Fixed

None.

## Git Signal

- Add Episode 088 (this review) to record candidate canonifications and conflicts.

## The Insight

A large share of episode-derived insights remain implicit rather than canonified. A targeted canonification pass should focus on the candidate list above and resolve the “ungoverned episodes” conflict, while preserving early episodes as evidence rather than retrofitting them.

**Status:** Review complete; canonification candidates identified.
