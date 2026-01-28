# EPISODE - ep144

Stream model identity gap

---

## Metadata

- Date: 2026-01-13
- Episode ID: ep144
- Type: Violation
- Participants: Dexter Hadley, Codex (GPT-5)
- Model identity: gpt-5 (Codex CLI)
- Status: Resolved

---

## Context

Stream indexes listed episode agents but omitted model identities, even though
agent-to-model mapping is now established (ep130). This created a traceability
gap in WRITING stream indexes.

---

## Session narrative

The user flagged missing model identity fields in stream README tables. We
confirmed the gap and chose to regenerate all stream indexes from episodes,
forward-filling model identities from known agent-to-model mapping without
editing immutable episode files.

---

## Violations encountered

- Stream indexes omitted model identity despite available mapping evidence.

---

## Corrections applied

- Regenerated all stream README tables from episodes.
- Forward-filled model identity using known agent-to-model mapping.

---

## Evidence references (LEDGER)

- writing: working tree (stream index regeneration)

---

## Notes

Episode immutability is preserved; stream indexes carry the forward-filled
identity mapping.

---

**This file is a non-authoritative template.**  
**It defines structure only and confers no governance, enforcement, or interpretive meaning.**
