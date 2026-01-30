# ENGINE — CANON

inherits: /CANONIC/LANGUAGE/DIMENSIONS/OPERATIONAL/

---

## Axiom

**ENGINE = O grounded. All -ING operations execute through ENGINE.**

---

## Operational Forms

```
READING    — O (consume)    → COIN
WRITING    — O (produce)    → TOKEN
VALIDATING — O (verify)     → EVIDENCE
```

---

## Constraints

### READING

- READING MUST inherit from EVIDENCE.
- READING MUST log to LEDGER with timestamp.
- READING MUST NOT return claims without evidence chain.
- READING MUST flag emotional content.

### WRITING

- WRITING MUST require credentialed USER.
- WRITING MUST validate against CANON before commit.
- WRITING MUST generate TOKEN on valid contribution.
- WRITING MUST audit to LEDGER.

### VALIDATING

- VALIDATING MUST cross-reference EVIDENCE sources.
- VALIDATING MUST block undefined claims.
- VALIDATING MUST log violations for INTROSPECTION.
- VALIDATING MUST return evidence chain on success.

---

## Clinical Constraints

From Minh's clinical review:

| Constraint | Operation | Enforcement |
|------------|-----------|-------------|
| DCIS vs invasive | VALIDATING | Pathology evidence REQUIRED |
| Patient context | READING | Session state MAINTAINED |
| Empathy risk | READING | Emotional claims FLAGGED |
| Misinformation | VALIDATING | Claims without evidence BLOCKED |

---

## Composition

```
ENGINE (O)
    │
    ├── READING (O)
    │   └── → EVIDENCE → LEDGER → RESPONSE
    │
    ├── WRITING (O)
    │   └── CREDENTIAL → CANON → LEDGER → TOKEN
    │
    └── VALIDATING (O∩E∩S = index 19)
        └── CLAIM → EVIDENCE → RESULT
```

---

## Evolution

```
1. Violation detected → INTROSPECTION
2. Constraint added → CANON
3. All operations comply → FIXATION
```

---

*ENGINE | O dimension enforcement | min CANON / max GOVERNANCE*
