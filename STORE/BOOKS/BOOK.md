# BOOK — Pattern Specification

inherits: CANON.md

status: active

---

## Axiom

**BOOK = Constitutional writing. Full DETROS closure. Published governance.**

A BOOK is not content — it is **governance made readable**. CANONIC itself emerged from book governance patterns. This specification formalizes that origin.

---

## DETROS Requirements

BOOKS require ALL six dimensions. This is the key constraint.

| Dimension | Weight | Book Component | Purpose |
|-----------|--------|----------------|---------|
| D (Declarative) | 32 | SPINE | What the book claims |
| E (Evidential) | 16 | REFERENCES | How claims are proven |
| T (Temporal) | 8 | ARC | Narrative progression |
| R (Relational) | 4 | CHAPTERS | Scope boundaries |
| O (Operational) | 2 | EXERCISES | Reader enforcement |
| S (Structural) | 1 | SECTIONS | Physical form |

**BOOK = D∩E∩T∩R∩O∩S = 63** (Full ENTERPRISE)

---

## SPINE Definition (T-Dimension)

The SPINE is the **temporal skeleton**. It defines invariant order of conceptual progression.

```
SPINE/
├── 00-foundation/    ← Genesis (soft BIG BANG)
├── 01-axioms/        ← Core claims
├── 02-dimensions/    ← DETROS expansion
├── ...
└── NN-convergence/   ← Completion (hard BIG BANG)
```

**Temporal Flow:**
```
BACKWARDS ← soft BIG BANG ← NOW → hard BIG BANG → FORWARDS
(genesis)                  (present)            (convergence)
```

**SPINE Rule**: Book MUST progress from genesis to convergence. Reading order is governance.

---

## ARC Definition (Narrative Progression)

The ARC overlays emotional/conceptual trajectory onto SPINE. Defines **exit beliefs** at chapter boundaries.

| Stage | Index | Reader State |
|-------|-------|--------------|
| ORIENTATION | 0 | Grounded |
| COMPLICATION | 1 | Challenged |
| CRISIS | 2 | Tension |
| CLIMAX | 3 | Resolution |
| COMPLETION | 4 | Transformed |

**ARC Rule**: Progression MUST be monotonic. No regression to earlier states.

```
ARC_MONOTONIC :=
  ∀ chapter[i], chapter[i+1]:
    arc_index(chapter[i]) ≤ arc_index(chapter[i+1])
```

---

## Structure

```
BOOK/
├── CANON.md           ← Book constitution
├── BOOK.md            ← This specification
├── SPINE.md           ← Temporal ordering
├── ARC.md             ← Narrative progression
├── VOCAB.md           ← Book-specific vocabulary
├── README.md          ← Human guide
├── COVERAGE.md        ← Completion tracking
├── ROADMAP.md         ← Future additions
│
├── 00-{chapter}/      ← R-dimension: scope boundary
│   ├── CANON.md       ← Chapter constitution
│   ├── CHAPTER.md     ← Chapter specification
│   ├── 00-{section}.md ← S-dimension: form
│   ├── 01-{section}.md
│   └── EXERCISES/     ← O-dimension: enforcement
│
├── 01-{chapter}/
│   └── ...
│
└── REFERENCES/        ← E-dimension: evidence
    ├── CANON.md
    └── *.md           ← Citation entries
```

---

## DETROS Formulas

| Component | Formula | Index | Meaning |
|-----------|---------|-------|---------|
| SPINE | D∩T∩S | 41 | Declared temporal structure |
| ARC | T∩S | 9 | Temporal form (history) |
| CHAPTER | D∩R∩S | 37 | Declared scoped structure |
| SECTION | S | 1 | Pure structure |
| REFERENCE | E∩T∩S | 25 | Proven temporal artifact |
| EXERCISE | O∩S | 3 | Operational structure |
| BOOK | D∩E∩T∩R∩O∩S | 63 | Complete governance |

---

## Chapter CANON.md Template

```markdown
# {CHAPTER} — CHAPTER CANON

inherits: ../{BOOK}/CANON.md
arc: {ORIENTATION|COMPLICATION|CRISIS|CLIMAX|COMPLETION}
spine: {00-NN}

---

## Contract

**Entry belief:** {What reader believes entering}
**Exit belief:** {What reader believes exiting}

---

## Red Lines

- {Invariant that MUST NOT be violated}

---

## Sections

| # | Title | Concept | Status |
|---|-------|---------|--------|
| 00 | {name} | {concept} | {draft|review|frozen} |
```

---

## Validation Rules

### Book-Level

```
BOOK_VALID :=
  HAS(CANON.md) ∧
  HAS(SPINE.md) ∧
  HAS(ARC.md) ∧
  INHERITS(/CANONIC/STORE/BOOKS/) ∧
  DETROS_COMPLETE
```

### Chapter-Level

```
CHAPTER_VALID :=
  HAS(CANON.md) ∧
  INHERITS(../CANON.md) ∧
  DECLARES(arc) ∧
  DECLARES(spine) ∧
  arc ∈ {ORIENTATION, COMPLICATION, CRISIS, CLIMAX, COMPLETION}
```

### Arc Monotonicity

```
ARC_MONOTONIC :=
  ∀ chapter[i], chapter[i+1]:
    arc_index(chapter[i]) ≤ arc_index(chapter[i+1])
```

---

## Certification

Books are certified when:

1. All DETROS dimensions present
2. SPINE validated (temporal ordering)
3. ARC monotonic (no regression)
4. All chapters inherit correctly
5. VaaS passes at declared tier

---

## Links

- [BOOKS/CANON.md](CANON.md) — Book governance
- [STORE.md](../STORE.md) — Distribution registry

---
