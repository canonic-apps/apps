# ARC — Template

inherits: CANON.md

---

## Axiom

**ARC = T∩S. Narrative progression. Monotonic transformation.**

---

## Five Stages

| Stage | Index | Reader State | Purpose |
|-------|-------|--------------|---------|
| ORIENTATION | 0 | Grounded | Establish foundation |
| COMPLICATION | 1 | Challenged | Introduce complexity |
| CRISIS | 2 | Tension | Present core conflict |
| CLIMAX | 3 | Resolution | Deliver breakthrough |
| COMPLETION | 4 | Transformed | Achieve closure |

---

## Constraints

- Progression MUST be monotonic
- Chapters MUST NOT regress to earlier stages
- Multiple chapters may share same stage
- Final chapter MUST be COMPLETION

---

## Monotonicity Rule

```
∀ chapter[i], chapter[i+1]:
  arc_index(chapter[i]) ≤ arc_index(chapter[i+1])

Valid:   ORIENTATION → ORIENTATION → COMPLICATION → CRISIS → CLIMAX → COMPLETION
Invalid: ORIENTATION → COMPLICATION → ORIENTATION (regression)
```

---

## Exit Beliefs

Each chapter declares:

| Field | Purpose |
|-------|---------|
| **Entry belief** | What reader believes entering |
| **Exit belief** | What reader believes exiting |

The delta between entry and exit is the **chapter transformation**.

---

## Template

```markdown
# {BOOK} — ARC

## Progression

| Chapter | Stage | Exit Belief |
|---------|-------|-------------|
| 00-foundation | ORIENTATION | Reader understands why |
| 01-axioms | ORIENTATION | Reader knows the rules |
| 02-dimensions | COMPLICATION | Reader sees the lattice |
| ... | ... | ... |
| NN-completion | COMPLETION | Reader is transformed |
```

---
