# VALIDATING — Operation

inherits: /MED/CHAT/ENGINE/

---

## Purpose

VALIDATING = Claims verified against EVIDENCE.

**Index:** E∩O∩S = 19 (Validator)

---

## Flow

```
CLAIM → PARSE → EVIDENCE → OPTS → VERDICT → LOG
```

---

## Constraints

1. VALIDATING MUST cross-reference domain EVIDENCE sources.
2. VALIDATING MUST block claims without evidence chain.
3. VALIDATING MUST log violations for INTROSPECTION.
4. VALIDATING MUST return evidence chain on success.
5. VALIDATING MUST generate OPTS token for audit trail.

---

## Validation Levels

| Level | Source | Authority |
|-------|--------|-----------|
| GOLD | Guidelines (NCCN, AHA, etc.) | Highest |
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
    ├── timestamp: ISO8601
    └── action: BLOCKED
         │
         ▼
    LEDGER records for evolution
```

---

## Evolution Cycle

```
1. Claim fails validation → INTROSPECTION
2. Pattern detected → CANON constraint proposed
3. Constraint approved → CANON updated
4. Future claims comply → FIXATION
```

---

*VALIDATING | E∩O∩S = Validator | Base claim verification*
