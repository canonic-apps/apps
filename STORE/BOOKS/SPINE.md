# SPINE — Template

inherits: CANON.md

---

## Axiom

**SPINE = D∩T∩S. Temporal ordering of chapters. Reading order is governance.**

---

## Structure

```
00-{chapter}/    ← Genesis (soft BIG BANG)
01-{chapter}/
02-{chapter}/
...
NN-{chapter}/    ← Convergence (hard BIG BANG)
```

---

## Constraints

- Chapters MUST be numbered sequentially (00, 01, 02, ...)
- Chapter order MUST NOT change after CANON is frozen
- Reading order = SPINE order = governance order
- Dependencies flow forward (chapter N may reference 0..N-1)

---

## Temporal Flow

```
←────────────────────────────────────────────────────────→
soft BIG BANG         NOW              hard BIG BANG
(genesis)           (present)          (convergence)
    │                                       │
    00-foundation                    NN-completion
```

---

## Template

```markdown
# {BOOK} — SPINE

## Chapters

| # | Name | Dependencies | Status |
|---|------|--------------|--------|
| 00 | {foundation} | — | {status} |
| 01 | {chapter} | 00 | {status} |
| 02 | {chapter} | 00, 01 | {status} |
```

---
