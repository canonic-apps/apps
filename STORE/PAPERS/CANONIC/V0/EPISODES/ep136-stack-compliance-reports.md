# EPISODE — ep136

Stack compliance reports recorded outside PAPER

---

## Metadata

- Date: 2026-01-13
- Episode ID: ep136
- Participants: USER, Agent
- Model identity: OpenAI Codex (GPT-5)
- Status: complete

---

## Context

Derived compliance reports were stored in the PAPER scope. To keep PAPER minimal,
we recorded those reports in WRITING and removed the redundant artifacts from
PAPER.

---

## Session narrative

1. Reviewed PAPER artifacts and identified compliance reports.
2. Chose to preserve report content as an episode.
3. Anchored the report to the freeze tag for evidence alignment.

---

## Evidence references (LEDGER)

- tag `stack-freeze-2026-01-12`
- writing commit `f8acf128` (freeze commit)

---

## Report A — Triad compliance (freeze snapshot)

Tag: `stack-freeze-2026-01-12`

Note: `publishing` was created post-freeze and is intentionally excluded from
this snapshot.

This report lists directories that contain `CANON.md`, `VOCAB.md`, and
`README.md` at the tag.

### Summary

| Repo | Triad scopes |
| --- | --- |
| canonic | 2 |
| machine | 1 |
| os | 1 |
| ledger | 1 |
| writing | 3 |
| paper | 1 |
| stack | 1 |
| validators | 1 |
| patents | 1 |

Total triad scopes: **12**

### Details

#### canonic

Triad scopes (2):

- .
- templates

#### machine

Triad scopes (1):

- .

#### os

Triad scopes (1):

- .

#### ledger

Triad scopes (1):

- .

#### writing

Triad scopes (3):

- .
- episodes
- episodes/templates

#### paper

Triad scopes (1):

- .

#### stack

Triad scopes (1):

- .

#### validators

Triad scopes (1):

- .

#### patents

Triad scopes (1):

- .

---

## Report B — Repository root metadata compliance

Assessment time (UTC): 2026-01-13T12:55:29Z

Criteria: each git repository root scope must include `LICENSE` and `NOTICE`.
Source: `/canonic/CANON.md` (Repository licensing axiom).

### Summary

| Repo | Git repo | LICENSE | NOTICE | Status |
| --- | --- | --- | --- | --- |
| canonic | yes | yes | yes | compliant |
| machine | yes | yes | yes | compliant |
| os | yes | yes | yes | compliant |
| ledger | yes | yes | yes | compliant |
| writing | yes | yes | yes | compliant |
| paper | yes | yes | yes | compliant |
| stack | yes | yes | yes | compliant |
| validators | yes | yes | yes | compliant |
| patents | yes | yes | yes | compliant |
| publishing | yes | yes | yes | compliant |
| agents | no | yes | yes | not a git repo (excluded) |

### Notes

- Only git repository roots are evaluated for compliance.
- Non-repository directories are excluded from the requirement.

---
