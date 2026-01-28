# Episode 120: Producer vs Consumer Commit Pattern

**Date:** 2026-01-11
**Type:** Insight
**Participants:** Human (Governor General), AI (Cline)
**Agent:** Cline

---

## The Session

Human clarified the commit pattern for CANONIC machine:

- SPEC is human input (builds machine)
- CANON is AI output (produced from SPEC)
- Episodes are human input (uses machine)
- Producer commits CANON
- Consumer commits episodes

## The Insight

**Producer/Consumer Pattern:**

| Artifact | Who Enters | Who Commits | Role |
|----------|------------|-------------|------|
| SPEC | Human | Human | Input |
| CANON | AI (from SPEC) | AI | Producer |
| Episodes | Human | Human | Consumer |
| VOCAB | AI | AI | Producer |

**No constraints, just governance:**
- Human enters SPEC → builds the machine
- AI produces CANON from SPEC → Producer commits
- Human enters episodes → uses machine
- Human commits episodes → Consumer commits

**This is the constitutional pattern:**
- Producer (AI) creates CANON from SPEC
- Consumer (Human) creates episodes to use CANON
- Both operate within governance constraints

## Git Signal

- `paper` - ep120 documents producer/consumer commit pattern (this episode)

## Status

Insight documented; pattern for canonification.
