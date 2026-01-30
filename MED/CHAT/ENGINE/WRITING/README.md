# WRITING — Operation

inherits: /MED/CHAT/ENGINE/

---

## Purpose

WRITING = Clinician validates/adds clinical knowledge.

---

## Flow

```
CREDENTIAL → INPUT → VALIDATE → CANON → OPTS → LEDGER → TOKEN
```

---

## Constraints

1. WRITING MUST require NPI-credentialed USER.
2. WRITING MUST validate against EVIDENCE before commit.
3. WRITING MUST audit to LEDGER with clinician identity.
4. WRITING MUST generate OPTS-Data token on valid contribution.
5. WRITING MUST NOT bypass VALIDATING.

---

## Credentialing

```
USER ──► NPI ──► CANONIC/CREDENTIALING-APP
  │        │            │
  ▼        ▼            ▼
name    1234567890    VERIFIED
```

| Credential | Authority | Scope |
|------------|-----------|-------|
| MD/DO | Full write | All content |
| PA/NP | Limited write | Non-diagnostic |
| RN | Annotate only | Patient guidance |
| PATIENT | Read only | No write |

---

## Token Generation

```
VALID_WRITE ──► CANON ──► LEDGER ──► OPTS-Data ──► TOKEN
                           │                         │
                           ▼                         ▼
                     audit trail              market value
```

---

*WRITING | Clinician knowledge input | O dimension*
