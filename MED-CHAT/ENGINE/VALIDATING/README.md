# VALIDATING — Operation

inherits: /MED-CHAT/ENGINE/

---

## Purpose

VALIDATING = Claims verified against EVIDENCE.

**Index:** E∩O∩S = 19 (Validator)

---

## Flow

```
CLAIM → PARSE → EVIDENCE → VERDICT → LOG
```

---

## Constraints

1. VALIDATING MUST cross-reference EVIDENCE sources.
2. VALIDATING MUST block claims without evidence chain.
3. VALIDATING MUST log violations for INTROSPECTION.
4. VALIDATING MUST return evidence chain on success.
5. VALIDATING MUST differentiate clinical nuances (DCIS vs invasive).

---

## Minh's Clinical Concerns

### DCIS vs Invasive

```
CLAIM: "Stage 1 breast cancer treatment"
       │
       ▼
VALIDATOR asks: DCIS or invasive?
       │
       ├── DCIS → different treatment pathway
       │          (may not require chemo)
       │
       └── Invasive → standard staging applies
                      (chemo may be indicated)
```

**Constraint:** DCIS claims MUST specify pathology.

### Misinformation Prevention

```
CLAIM: "Vitamin C cures breast cancer"
       │
       ▼
VALIDATOR checks: EVIDENCE/NCCN/
       │
       └── NOT FOUND → BLOCKED
           │
           ▼
       "No evidence supports this claim"
```

---

## Validation Levels

| Level | Source | Authority |
|-------|--------|-----------|
| GOLD | NCCN Guidelines | Highest |
| SILVER | Peer-reviewed | High |
| BRONZE | Expert consensus | Medium |
| NONE | Unverified | BLOCKED |

---

## Violation Logging (INTROSPECTION)

```
VIOLATION DETECTED
    │
    ├── claim: "X cures Y"
    ├── evidence: NONE
    ├── timestamp: 2026-01-29T...
    └── action: BLOCKED
         │
         ▼
    LEDGER records for evolution
```

Violations inform CANON evolution.

---

## Evolution Cycle

```
1. Claim fails validation → INTROSPECTION
2. Pattern detected → CANON constraint proposed
3. Constraint approved → CANON updated
4. Future claims comply → FIXATION
```

---

*VALIDATING | E∩O∩S = Validator | min CANON / max GOVERNANCE*
