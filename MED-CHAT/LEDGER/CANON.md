# LEDGER — CANON

inherits: /CANONIC/LANGUAGE/DIMENSIONS/TEMPORAL/

---

## Axiom

**LEDGER = T∩O grounded. All operations log with temporal integrity.**

---

## Purpose

LEDGER records all MammoChat interactions for:
1. Audit trail
2. Evolution (INTROSPECTION)
3. Patient context continuity
4. Compliance verification

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
  "input": "query or claim",
  "output": "response or verdict",
  "evidence_chain": ["NCCN.2024.3.2", "BIRADS.5ed.4"],
  "validation": {
    "status": "VALID | BLOCKED | FLAGGED",
    "reason": "string"
  },
  "session": {
    "id": "session_uuid",
    "context": {
      "diagnosis": "DCIS | invasive | unknown",
      "phase": "screening | diagnosis | treatment | survivorship"
    }
  }
}
```

---

## Constraints

1. LEDGER entries MUST be immutable (append-only).
2. LEDGER MUST include timestamp with timezone.
3. LEDGER MUST hash patient identifiers (privacy).
4. LEDGER MUST retain for compliance period (7 years).
5. LEDGER MUST support INTROSPECTION queries.

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

## Evolution Feed

LEDGER violations feed INTROSPECTION:

```
VIOLATION_PATTERN
    │
    ├── frequency > threshold
    ├── impact: HIGH
    └── proposal: new CANON constraint
         │
         ▼
    EVOLUTION
```

---

*LEDGER | T∩O = Temporal Operations | Audit + Evolution*
