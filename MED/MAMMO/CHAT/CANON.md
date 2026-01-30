# MED.MAMMO.CHAT — CANON (MAMMO-CHAT)

inherits: /MED/MAMMO/, /MED/CHAT/

composed: MED.MAMMO.CHAT = MAMMO-CHAT

---

## Axiom

**MAMMO-CHAT = MED.MAMMO.CHAT. Breast oncology chat with precision cancer embedding.**

---

## Structure

```
MED/MAMMO/CHAT/                    — MAMMO-CHAT
├── inherits: /MED/CHAT/           — Base infrastructure
│   ├── ENGINE/                    — Operations
│   ├── OPTS-EGO/                  — Provenance
│   ├── LEDGER/                    — Temporal
│   └── SCHEMA/                    — Structural
├── EVIDENCE/                      — E (Breast-specific)
│   ├── NCCN/                      — Treatment guidelines
│   ├── BIRADS/                    — Imaging classification
│   └── MCODE/                     — Precision embedding
└── FRONTEND/                      — Empathy UI
```

---

## DETROS Compliance

**Level:** 63 (full ENTERPRISE)

| Dimension | Source |
|-----------|--------|
| D | /MED/MAMMO/CHAT/CANON.md |
| E | /MED/MAMMO/CHAT/EVIDENCE/ |
| T | /MED/CHAT/LEDGER/ (inherited) |
| R | /CANONIC/USERS/ (inherited) |
| O | /MED/CHAT/ENGINE/ (inherited) |
| S | /MED/CHAT/SCHEMA/ (inherited) |

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

## mCODE Precision Embedding

```
DCIS     → SNOMED:109886000 → Vector[DCIS]
Invasive → SNOMED:254837009 → Vector[Invasive]

"Stage 1 DCIS" ≠ "Stage 1 Invasive"
(distinct embedding vectors)
```

---

## Empathy Architecture

From MammoChat Whitepaper:

```
Listen → Explain → Act → Trust
   │         │       │       │
   ▼         ▼       ▼       ▼
Acknowledge  Clarify Empower Reinforce
```

> "We don't build empathy on top of technology.
> We build technology on top of empathy."

---

## Origin

```
App: MAMMOCHAT
Whitepaper: October 2025 (Pre-CANONIC)
Domain: medicine/oncology/breast
Evidence: 20,000+ patient encounters
Grant: $2M FCIF 354
Trial: NCT06604078
```

---

*MAMMO-CHAT | MED.MAMMO.CHAT | Precision cancer embedding + empathy*
