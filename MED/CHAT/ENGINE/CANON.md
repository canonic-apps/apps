# ENGINE — CANON

inherits: /MED/CHAT/, /CANONIC/LANGUAGE/DIMENSIONS/OPERATIONAL/

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

- READING MUST inherit from domain EVIDENCE.
- READING MUST log to LEDGER with timestamp.
- READING MUST NOT return claims without evidence chain.
- READING MUST flag emotional content.
- READING MUST generate OPTS-Consent token.

### WRITING

- WRITING MUST require credentialed USER (NPI).
- WRITING MUST validate against CANON before commit.
- WRITING MUST generate OPTS-Data token on valid contribution.
- WRITING MUST audit to LEDGER.

### VALIDATING

- VALIDATING MUST cross-reference domain EVIDENCE sources.
- VALIDATING MUST block undefined claims.
- VALIDATING MUST log violations for INTROSPECTION.
- VALIDATING MUST return evidence chain on success.

---

## Composition

```
ENGINE (O)
    │
    ├── READING (O)
    │   └── QUERY → EVIDENCE → LEDGER → OPTS → RESPONSE
    │
    ├── WRITING (O)
    │   └── CREDENTIAL → CANON → LEDGER → OPTS → TOKEN
    │
    └── VALIDATING (O∩E∩S = index 19)
        └── CLAIM → EVIDENCE → OPTS → RESULT
```

---

## Evolution

```
1. Violation detected → INTROSPECTION
2. Constraint added → CANON
3. All operations comply → FIXATION
```

---

*ENGINE | O dimension | Base operational layer*
