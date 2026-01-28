# EPISODE — ep135

Model identity disclosure gap (historical)

---

## Metadata

- Date: 2026-01-13
- Episode ID: ep135
- Type: Investigation
- Participants: Human (Governor General), AI (Codex)
- Model identity: gpt-5.2-codex
- Status: complete

---

## Context

WRITING requires every episode to disclose model identity. A stack-wide review
showed many historical episodes lack a model identity field, which weakens
model x agent analysis and violates current WRITING CANON for historical data.

---

## Session narrative

1. Scanned `writing/episodes/` for model identity disclosure fields.
2. Counted episodes missing model identity labels.
3. Cross-referenced the alignment report to preserve model attribution where
   session logs exist.
4. Documented the historical gap and the correction approach (do not edit old
   episodes; record the limitation and use alignment mapping for analysis).

---

## Violations encountered

- Historical episodes missing model identity disclosure (legacy noncompliance).

---

## Corrections applied

- No edits to historical episodes (immutability preserved).
- Documented the limitation and alignment mapping approach for analysis.

---

## Evidence references (LEDGER)

- `writing` - `stack-freeze-2026-01-12` evidence window
- `writing` - `2c57e73` alignment report baseline

---

## Notes

- Missing model identity is treated as a historical limitation.
- Model attribution uses `writing/WRITING_MODEL_ALIGNMENT.md` when evidence
  exists; otherwise episodes remain un-attributed.

---
