# EPISODE - ep159

Auto-attribution discovery for PAPER v0.2

---

## Metadata

- Date: 2026-01-14
- Episode ID: ep159
- Type: Discovery
- Participants: Dexter Hadley, Fatima Boukrim, Claude Opus 4.5
- Agent: Claude Code
- Model identity: claude-opus-4-5-20251101
- Channel: IDE
- Source: VSCode Claude Code extension
- Status: Documented (v0.2 scope)

---

## Context

While adding Fatima Boukrim's contribution to the Acknowledgments section,
we discovered a pattern: cross-human injection surfaces insights that should
be attributed, and the attribution itself follows a traceable pattern.

---

## Discovery

**Auto-attribution for PAPER**: The ledger already contains the information
needed to generate acknowledgments automatically.

For v0.2, PAPER could:

1. Parse commit co-author lines to extract AI model identities
2. Parse episode metadata to extract human participants
3. Parse transcript records to identify cross-human injections
4. Generate an Acknowledgments section from ledger evidence

This makes attribution verifiable—not a courtesy section, but a computed
artifact from the evidence trail.

The pattern is:
- Human contributions → episode participant metadata
- AI contributions → commit co-author lines + model identity
- Cross-human injections → transcript timestamps + episode references

---

## v0.1 implementation (manual)

For v0.1, we added a manual Acknowledgments section:

- Fatima Boukrim: asked "Help me understand what this is for" → led to
  "Why Should You Care?" section
- AI agents: Claude Opus 4.5, Claude Sonnet 4.5, GPT-5 → recorded in ledger

---

## v0.2 scope (deferred)

Auto-attribution requires:
- Transcript-ledger alignment (post-freeze IP)
- Participant extraction from episode metadata
- Model identity aggregation from commits
- Cross-human injection detection

This is deferred to v0.2 after IDF and PROVISIONAL filing.

---

## Evidence references (LEDGER)

- paper:9d7f5bf - Fatima attribution commit (amended)
- This episode documents the discovery for v0.2

---

## Notes

Cross-human injection is a discovery pattern: a non-expert question surfaces
a gap in the narrative that experts miss. The question becomes content.

---

**This file is a non-authoritative template.**
**It defines structure only and confers no governance, enforcement, or interpretive meaning.**
