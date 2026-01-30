# READING — Operation

inherits: /MED/CHAT/ENGINE/

---

## Purpose

READING = Patient consumes clinical guidance.

---

## Flow

```
QUERY → CONTEXT → EVIDENCE → VALIDATE → OPTS → RESPONSE → LEDGER
```

---

## Constraints

1. READING MUST maintain patient context (session state).
2. READING MUST cite evidence for all clinical claims.
3. READING MUST flag emotional/empathetic content.
4. READING MUST log to LEDGER with timestamp.
5. READING MUST NOT hallucinate medical facts.
6. READING MUST generate OPTS-Consent token.

---

## Context Awareness

```
Session State:
├── patient_id (anonymous hash)
├── diagnosis_context (domain-specific)
├── treatment_phase (domain-specific)
└── conversation_history (temporal chain)
```

---

## Evidence Chain

```
CLAIM ──► EVIDENCE_SOURCE ──► CITATION
  │           │                   │
  ▼           ▼                   ▼
claim     SOURCE.YEAR         "Citation text"
```

---

## Emotional Flagging

```
RESPONSE TYPE:
├── CLINICAL  (evidence-backed)
├── GUIDANCE  (procedural)
├── EMOTIONAL (flagged, not medical advice)
└── UNKNOWN   (escalate to clinician)
```

---

*READING | Patient query handler | O dimension*
