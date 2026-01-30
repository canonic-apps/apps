# MED.CHAT — CANON

inherits: /MED/

---

## Axiom

**MED.CHAT = Medical chat infrastructure. Base for all domain chats.**

---

## Composition

```
Compose: MED.CHAT
Extend:  MED.MAMMO.CHAT = MAMMO-CHAT
         MED.CARDIO.CHAT = CARDIO-CHAT
         MED.DERM.CHAT = DERM-CHAT
```

---

## Structure

```
MED/CHAT/
├── ENGINE/         — O (Operational)
│   ├── READING/    — Patient queries
│   ├── WRITING/    — Clinician input
│   └── VALIDATING/ — Claim verification
├── OPTS-EGO/       — Token + provenance
├── LEDGER/         — T (Temporal)
└── SCHEMA/         — S (Structural)
```

---

## DETROS Mapping

| Dimension | Component |
|-----------|-----------|
| D (Declarative) | CANON.md |
| E (Evidential) | Domain-specific (inherited) |
| T (Temporal) | LEDGER/ |
| R (Relational) | USERS/ (inherited) |
| O (Operational) | ENGINE/ |
| S (Structural) | SCHEMA/ |

---

## Constraints

1. MED.CHAT provides infrastructure. Domains add EVIDENCE.
2. All operations MUST route through ENGINE.
3. All interactions MUST log to LEDGER.
4. All tokens MUST comply with OPTS-EGO.

---

*MED.CHAT | Base medical chat infrastructure*
