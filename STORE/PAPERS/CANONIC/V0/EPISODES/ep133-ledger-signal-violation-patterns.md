# EPISODE - ep133

Ledger-signal violation pattern report

---

## Metadata

- Date: 2026-01-12
- Episode ID: ep133
- Participants: Human (Governor General), AI (Codex)
- Model identity: GPT-5 (Codex CLI)
- Status: complete

---

## Context

Human requested a new episode that reviews ep130, inspects chat history around ledger signals, and extracts existing and novel violation patterns using manual checking of WRITING episodes as a leaky training set.

---

## Session narrative

1. Read `writing/episodes/ep130-agent-model-correlation.md` and its Ledger Signal list.
2. Located the Codex session log containing ep130 content and ledger-signal references (`~/.codex/sessions/2026/01/12/rollout-2026-01-12T22-59-36-019bb582-55e5-7562-998d-bc79493ab48b.jsonl`).
3. Verified ledger-signal commit IDs via git logs in `ledger`, `os`, `paper`, and `writing`.
4. Manually sampled violation-focused episodes (ep103-ep132) to extract recurring and emergent patterns.
5. Compiled patterns into observed vs candidate categories and noted coverage gaps.

---

## Violations encountered

- None in this session. This episode records observed violation patterns from prior episodes and ledger evidence.

---

## Corrections applied

- None. No canon or artifacts were modified.

---

## Evidence references (LEDGER)

- `ledger` - `0c11998` ledger: achieve compliance
- `ledger` - `d93f41c` ledger: VIOLATION - false compliance assertion
- `os` - `899433e` os: add evolution axiom, update GIT to LEDGER
- `paper` - `24dc57b` paper: complete VOCAB closure to CANON
- `writing` - `2be2116` writing: update Git Signal to Ledger Signal

---

## Notes

Observed violation patterns (existing):
- Identity and role confusion, plus model-label ambiguity (ep109, ep112, ep130).
- Episode integrity failures: AI-created episodes, overwrites, and redo-signal violations (ep108-ep112, ep115, ep126).
- Layer and scope boundary breaches: OS producing PAPER artifacts or enforcing on human work (ep112, ep123-ep124, ep129).
- Verification failures: violation or compliance claims without reading CANON (ep114, ep119; echoes `ledger:d93f41c`).
- Vocabulary and naming drift: inflection bloat, stub closure gaps, and spec misnaming (ep103, ep105, ep127).
- Template/undo regressions: replacing enforced protocol with generic template (ep104).
- Evidence misrepresentation: documenting non-existent or mismatched events (ep112).

Candidate patterns (novel or cross-signal):
- Signal vocabulary drift: Git Signal vs Ledger Signal renaming indicates evidence-label instability (`writing:2be2116`).
- Compliance inference from state rather than content (clean git => governed) aligns the false-assertion ledger event (`ledger:d93f41c`) with ep114/ep119.
- Tool-to-model opacity: episode agent labels mask model identity and skew violation attribution (ep130).

Gaps:
- Manual sampling only; not all episodes reviewed.
- Session logs from tools other than Codex were not re-parsed in this pass.

---
