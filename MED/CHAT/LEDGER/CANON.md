# LEDGER — CANON

inherits: /MED/CHAT/, /CANONIC/LANGUAGE/DIMENSIONS/TEMPORAL/

---

## Axiom

**LEDGER = T∩O grounded. All operations log with temporal integrity.**

---

## Purpose

LEDGER records all MED.CHAT interactions for:
1. Audit trail (HIPAA compliance)
2. Evolution (INTROSPECTION)
3. Patient context continuity
4. OPTS-EGO token provenance

---

## Entry Schema

```json
{
  "id": "uuid",
  "timestamp": "ISO8601",
  "operation": "READING | WRITING | VALIDATING",
  "actor": {
    "type": "PATIENT | CLINICIAN | SYSTEM",
    "id": "hash | NPI | system"
  },
  "opts_token": {
    "type": "OPTS-Data | OPTS-Consent | OPTS-Credential",
    "hash": "sha256"
  },
  "input": "query or claim",
  "output": "response or verdict",
  "evidence_chain": ["SOURCE.YEAR.SECTION"],
  "validation": {
    "status": "VALID | BLOCKED | FLAGGED",
    "reason": "string"
  },
  "session": {
    "id": "session_uuid",
    "context": {}
  }
}
```

---

## Constraints

1. LEDGER entries MUST be immutable (append-only).
2. LEDGER MUST include timestamp with timezone.
3. LEDGER MUST hash patient identifiers (privacy).
4. LEDGER MUST retain for 7 years (HIPAA).
5. LEDGER MUST support INTROSPECTION queries.
6. LEDGER MUST link to OPTS-EGO tokens.

---

## Temporal Integrity

```
T₀ ──► T₁ ──► T₂ ──► T₃
│      │      │      │
▼      ▼      ▼      ▼
query  resp   claim  blocked
       │             │
       └─────────────┴──► INTROSPECTION
                          (pattern detection)
```

---

*LEDGER | T∩O = Temporal Operations | Audit + Evolution*
