# CANONIC GUIDE — SPINE

inherits: CANON.md

---

## Axiom

**SPINE = D∩T∩S (41). Temporal ordering. Reading order is governance.**

---

## Volumes & Chapters

### VOLUME I — FOUNDATIONS (ORIENTATION)

| # | Chapter | Dependencies | Episodes | Status |
|---|---------|--------------|----------|--------|
| 00 | genesis | — | ep000-* | planned |
| 01 | language | 00 | ep001-* | planned |
| 02 | detros | 00, 01 | ep002-* | planned |
| 03 | tiers | 02 | ep003-* | planned |

### VOLUME II — MACHINE (COMPLICATION)

| # | Chapter | Dependencies | Episodes | Status |
|---|---------|--------------|----------|--------|
| 04 | compliance | 02, 03 | ep022-* | planned |
| 05 | validators | 04 | ep023-* | planned |
| 06 | enforcement | 04, 05 | ep024-* | planned |
| 07 | certification | 05, 06 | ep025-* | planned |

### VOLUME III — ECONOMY (CRISIS)

| # | Chapter | Dependencies | Episodes | Status |
|---|---------|--------------|----------|--------|
| 08 | tokens | 03 | ep030-* | planned |
| 09 | apps | 04, 08 | ep031-* | planned |
| 10 | store | 09 | ep032-* | planned |
| 11 | pricing | 08, 10 | ep033-* | planned |

### VOLUME IV — PRACTICE (CLIMAX)

| # | Chapter | Dependencies | Episodes | Status |
|---|---------|--------------|----------|--------|
| 12 | patterns | 02, 04 | ep040-* | planned |
| 13 | domains | 12 | ep041-* | planned |
| 14 | integration | 06, 12 | ep042-* | planned |
| 15 | migration | 14 | ep043-* | planned |

### VOLUME V — MASTERY (COMPLETION)

| # | Chapter | Dependencies | Episodes | Status |
|---|---------|--------------|----------|--------|
| 16 | proofs | all | ep050-* | planned |
| 17 | governance | 16 | ep051-* | planned |
| 18 | future | 17 | ep052-* | planned |
| 19 | reference | all | — | planned |

---

## Temporal Flow

```
←─────────────────────────────────────────────────────────────────────────────→
soft BIG BANG                        NOW                       hard BIG BANG
(genesis)                          (present)                   (convergence)
    │                                                                │
    00-genesis ─────────────────────────────────────────── 19-reference

    VOLUME I        VOLUME II       VOLUME III     VOLUME IV      VOLUME V
    FOUNDATIONS     MACHINE         ECONOMY        PRACTICE       MASTERY
    [00-03]         [04-07]         [08-11]        [12-15]        [16-19]
```

---

## Dependency Graph

```
VOLUME I (FOUNDATIONS)
00-genesis
    │
    ▼
01-language
    │
    ▼
02-detros ──────────────────────────────────────────────────────────┐
    │                                                                │
    ▼                                                                │
03-tiers ─────────────────────────────────┐                         │
    │                                     │                          │
    │   VOLUME II (MACHINE)               │                          │
    │   ┌─────────────────────────────────┼──────────────────────────┤
    │   │                                 │                          │
    │   ▼                                 ▼                          │
    │  04-compliance ◄────────────────────┘                          │
    │   │                                                            │
    │   ▼                                                            │
    │  05-validators                                                 │
    │   │                                                            │
    │   ▼                                                            │
    │  06-enforcement ───────────────────────────────────────────────┤
    │   │                                                            │
    │   ▼                                                            │
    │  07-certification                                              │
    │                                                                │
    │   VOLUME III (ECONOMY)                                         │
    │   ┌────────────────────────────────────────────────────────────┤
    │   │                                                            │
    ▼   ▼                                                            │
08-tokens ◄──────────────────────────────────────────────────────────┤
    │                                                                │
    ▼                                                                │
09-apps ◄───────────────── 04-compliance                             │
    │                                                                │
    ▼                                                                │
10-store                                                             │
    │                                                                │
    ▼                                                                │
11-pricing ◄────────────── 08-tokens                                 │
                                                                     │
    VOLUME IV (PRACTICE)                                             │
    ┌────────────────────────────────────────────────────────────────┤
    │                                                                │
    ▼                                                                │
12-patterns ◄─────────────────────────────────────────────────────────┤
    │                                                                │
    ▼                                                                │
13-domains                                                           │
    │                                                                │
    ▼                                                                │
14-integration ◄────────── 06-enforcement                            │
    │                                                                │
    ▼                                                                │
15-migration                                                         │
                                                                     │
    VOLUME V (MASTERY)                                               │
    ┌────────────────────────────────────────────────────────────────┘
    │
    ▼
16-proofs ◄───────────────── ALL PRIOR CHAPTERS
    │
    ▼
17-governance
    │
    ▼
18-future
    │
    ▼
19-reference ◄───────────── ALL CHAPTERS
```

---

## Constraints

- Volumes MUST be read in order (I → V)
- Chapters MUST be read in SPINE order within volumes
- Chapter N may only reference chapters 0..N-1
- No forward references allowed
- Order MUST NOT change after CANON is frozen
- Each chapter MUST link to EVOLUTION episodes

---
