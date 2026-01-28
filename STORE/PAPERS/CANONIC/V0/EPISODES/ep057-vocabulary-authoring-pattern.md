# Episode 057: Vocabulary Authoring Pattern

**Episode:** 057  
**Date:** 2026-01-08  
**Context:** Canonbase review correction  
**Agent:** cline

**Type:** Unknown
**Participants:** Unknown
---

## The Problem

I polluted the root CANON with newly discovered vocabulary constraints.

**What I did wrong:**
- Added vocabulary consumption rules to CANON.md
- Added multi-repo synchronization constraints to CANON.md
- Added vocabulary completeness requirements to CANON.md

**Why it's wrong:**
- CANON must remain minimal (constitutional law)
- CANON contains invariants, not detailed procedural patterns
- New vocabulary belongs in VOCAB
- New patterns requiring human guidance belong in CANONIC.md

---

## The Insight

**CANON is constitution. CANONIC.md is specification.**

| Document | Purpose | Updated By |
|----------|---------|------------|
| CANON.md | Constitutional invariants (minimal, stable) | LLM only |
| CANONIC.md | Human-iterated specification (explains paradigm) | Human only |
| VOCAB.md | Term definitions (evolves with machine) | LLM only |

**Discovery flow:**

1. Canonbase review reveals missing vocabulary → Episode documents
2. New terms added to VOCAB.md (LLM-generated)
3. If pattern requires human guidance → Add to CANONIC.md (human-iterated)
4. New terms consumed by downstream VOCABs (consumer commits)

**CANON minimality rule:**

- If it defines what must ALWAYS be true → CANON
- If it requires human explanation → CANONIC.md
- If it defines what terms MEAN → VOCAB
- If it's reusable across contexts → PROTOCOLS.md

---

## The Correction

**Reverted from CANON.md:**
- ❌ VOCAB terminology consumption constraint
- ❌ Multi-repo synchronization constraint
- ❌ Governance vocabulary completeness constraint

**Added to CANONIC.md (specification):**
- ✅ "Vocabulary Authoring Pattern" section explaining where new vocabulary goes
- ✅ Clear rules for what belongs in CANON vs VOCAB vs CANONIC.md

**New pattern documented:**

```
Discovery → Episode → VOCAB addition → CANONIC.md update (if needed) → Consumption
```

---

## The Proof

1. **Violation**: Root CANON accumulated detailed procedural constraints
2. **Correction**: Reverted pollution, added authoring pattern to specification
3. **Documentation**: Episode 057 captures the lesson
4. **Canonification**: New pattern in CANONIC.md explains correct authoring

CANON remains pure. Vocabulary evolves in VOCAB. Patterns are documented in CANONIC.md.

---

**End Episode 057**

## The Session

Not recorded in original episode.

## Key Assets Discovered

Not recorded in original episode.

## Violations Detected and Fixed

Not recorded in original episode.

## Git Signal

Not recorded in original episode.

**Status:** Not recorded in original episode.
