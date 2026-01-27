# STORE — APP STORE

inherits: CANON.md

---

## Purpose

Distribution registry for CANONIC. Apps indexed by DETROS.

---

## DETROS

```
SYSTEM APPS (3)                 USER AXIOMS (3)
───────────────                 ───────────────
D → CHAT                        E → EVIDENCE/
T → EVOLUTION                   H → HOLDINGS/
R → AGENT                       S → STORE/

INFRASTRUCTURE (abstracted)
───────────────────────────
O → MACHINE
```

---

## System Apps

Platform-level apps. All users have access.

| App | Dimension | Purpose | Status |
|-----|-----------|---------|--------|
| [AGENT](../../AGENT/) | R (Relational) | Onboarding, wallet, communication | certified |
| [CHAT](../../CHAT/) | D (Declarative) | Introspection, self-governance | certified |
| [EVOLUTION](../../) | T (Temporal) | History, timeline, audit | certified |

### Architecture

```
         D          T          R
         │          │          │
         ▼          ▼          ▼
       CHAT       EVO       AGENT
         │          │          │
         └──────────┼──────────┘
                    │
                    ▼
              USER AXIOMS
         ┌──────────┼──────────┐
         │          │          │
         ▼          ▼          ▼
     EVIDENCE   HOLDINGS    STORE
         E                    S
                    │
                    ▼
                MACHINE (O)
              [abstracted]
```

---

## User Axioms

User repos provide data. Apps interface with axioms.

| Axiom | Dimension | Purpose |
|-------|-----------|---------|
| EVIDENCE/ | E (Evidential) | Proof, attestation, transcripts |
| HOLDINGS/ | — | Ownership, assets, IP |
| STORE/ | S (Structural) | Distribution, content |

### Content Types

| Type | Path | Governance |
|------|------|------------|
| BOOKS | STORE/BOOKS/ | Full DETROS |
| PAPERS | STORE/PAPERS/ | E∩T (evidential, temporal) |
| APPS | STORE/APPS/ | O∩S (operational, structural) |

---

## Domain Apps

Professional verticals. Inherit from canonic-domains/.

| Domain | Apps |
|--------|------|
| medicine | MAMMOCHAT, PSYCHCHAT |
| finance | — |
| law | — |
| government | — |
| genomics | — |
| blockchain | — |

---

## Flow

```
USER STORE ──► APP STORE ──► USERS
  (local)     (foundation)   (consumers)
```

---

## Certification

1. **Submit**: App declares DETROS dimensions
2. **Validate**: MACHINE checks constraints
3. **Certify**: Hash issued on pass
4. **Distribute**: Available to users by tier

---
