# STORE — Distribution Channels

inherits: CANON.md

---

## Axiom

**STORE = Distribution channels for CANONIC artifacts. Each channel has DETROS-appropriate governance.**

---

## Distribution Channels

| Channel | Path | DETROS | Index | Artifact Type |
|---------|------|--------|-------|---------------|
| **APP STORE** | STORE/APPS/ | O∩S | 3 | Software, services |
| **BOOK STORE** | STORE/BOOKS/ | D∩E∩T∩R∩O∩S | 63 | Constitutional writing |
| **PAPER STORE** | STORE/PAPERS/ | E∩T | 24 | Research, IP, patents |
| **BLOG STORE** | STORE/BLOGS/ | D∩S | 33 | Discovery narratives |

### Channel Architecture

```
                         STORE
                           │
        ┌──────────┬───────┴───────┬──────────┐
        │          │               │          │
        ▼          ▼               ▼          ▼
    APP STORE  BOOK STORE    PAPER STORE  BLOG STORE
      O∩S        #63           E∩T          D∩S
       │          │             │            │
       ▼          ▼             ▼            ▼
    Software   Books        Research     Discovery
    Services   Guides       Patents      Narratives
```

---

## Channel Requirements

### APP STORE (O∩S = 3)

Operational + Structural. Software that runs.

- MUST have operational constraints (O)
- MUST have structural form (S)
- MAY have other dimensions for higher tiers

### BOOK STORE (#63 = Full DETROS)

Constitutional writing. Published governance.

- MUST have SPINE (D∩T∩S)
- MUST have ARC (T∩S)
- MUST have REFERENCES (E)
- MUST have CHAPTERS (R)
- MUST have EXERCISES (O)
- MUST have SECTIONS (S)

### PAPER STORE (E∩T = 24)

Evidential + Temporal. Research and IP.

- MUST have evidence trail (E)
- MUST have temporal markers (T)
- Supports patent workflows

### BLOG STORE (D∩S = 33)

Declarative + Structural. Discovery narratives.

- MUST declare claims (D)
- MUST have structural form (S)
- Lighter governance for exploration

---

## DETROS Map

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

## Distribution Flow

```
AUTHOR ──► CHANNEL ──► VALIDATE ──► CERTIFY ──► DISTRIBUTE
           (STORE)     (VaaS)      (hash)      (consumers)

  ┌─────────────────────────────────────────────────────────┐
  │                                                         │
  │  USER STORE ──► APP STORE ──► USERS                     │
  │    (local)     (foundation)   (consumers)               │
  │                                                         │
  │  USER STORE ──► BOOK STORE ──► READERS                  │
  │    (local)     (foundation)   (consumers)               │
  │                                                         │
  │  USER STORE ──► PAPER STORE ──► RESEARCHERS             │
  │    (local)     (foundation)   (consumers)               │
  │                                                         │
  └─────────────────────────────────────────────────────────┘
```

---

## Certification

1. **Submit**: Artifact declares DETROS dimensions
2. **Validate**: MACHINE checks channel requirements
3. **Certify**: Hash issued on pass
4. **Distribute**: Available to consumers by tier

---

## Links

- [APP STORE](APPS/) — Software distribution
- [BOOK STORE](BOOKS/) — Constitutional writing
- [PAPER STORE](PAPERS/) — Research and IP
- [BLOG STORE](BLOGS/) — Discovery narratives

---
