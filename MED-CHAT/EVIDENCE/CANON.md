# EVIDENCE — CANON

inherits: /CANONIC/LANGUAGE/DIMENSIONS/EVIDENTIAL/

---

## Axiom

**EVIDENCE = E grounded. All claims require evidence chain.**

---

## Sources

```
EVIDENCE/
├── NCCN/      — National Comprehensive Cancer Network
├── BIRADS/    — Breast Imaging Reporting and Data System
└── TRIALS/    — Clinical trial data
```

---

## Authority Hierarchy

| Source | Weight | Update Cycle |
|--------|--------|--------------|
| NCCN Guidelines | 1.0 | Annual |
| BIRADS Atlas | 0.9 | ~10 years |
| Phase 3 Trials | 0.8 | As published |
| Phase 2 Trials | 0.6 | As published |
| Expert Consensus | 0.5 | Variable |
| Case Reports | 0.3 | Variable |

---

## Constraints

1. EVIDENCE MUST have provenance (source + date).
2. EVIDENCE MUST be versioned.
3. EVIDENCE MUST NOT contradict higher-authority sources.
4. EVIDENCE MUST be machine-readable.

---

## Evidence Chain

```
CLAIM ──► requires ──► EVIDENCE ──► cites ──► SOURCE
  │                        │                     │
  ▼                        ▼                     ▼
"ER+ responds to       NCCN.Breast.2024     "NCCN Guidelines
 endocrine therapy"    Section 3.2           Version 2.2024"
```

---

*EVIDENCE | E dimension | Clinical truth grounding*
