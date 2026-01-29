# CANONIC GUIDE — ARC

inherits: CANON.md

---

## Axiom

**ARC = T∩S (9). Narrative progression. Monotonic transformation.**

---

## Stages

| Stage | Index | Reader State |
|-------|-------|--------------|
| ORIENTATION | 0 | Grounded |
| COMPLICATION | 1 | Challenged |
| CRISIS | 2 | Tension |
| CLIMAX | 3 | Resolution |
| COMPLETION | 4 | Transformed |

---

## Progression

| Chapter | Stage | Entry Belief | Exit Belief |
|---------|-------|--------------|-------------|
| 00-genesis | ORIENTATION | I don't know CANONIC | I understand CANONIC's origin |
| 01-language | ORIENTATION | I don't know the syntax | I can read/write CANON.md |
| 02-detros | COMPLICATION | Governance seems arbitrary | I see the 64-point lattice |
| 03-tiers | COMPLICATION | Tiers are confusing | I know CLOSURE/COMMUNITY/BUSINESS/ENTERPRISE |
| 04-compliance | CRISIS | Validation seems complex | I understand VaaS as a product |
| 05-machine | CRISIS | Enforcement is unclear | I see pure machine validation |
| 06-economy | CLIMAX | Economics are opaque | I understand TOKEN economy |
| 07-apps | CLIMAX | App store is unclear | I see the distribution model |
| 08-proofs | COMPLETION | It's just documentation | I accept CANONIC=WORK=GIT |
| 09-governance | COMPLETION | I'm a user | I'm a practitioner |

---

## Monotonicity Check

```
00 (0) ≤ 01 (0) ≤ 02 (1) ≤ 03 (1) ≤ 04 (2) ≤ 05 (2) ≤ 06 (3) ≤ 07 (3) ≤ 08 (4) ≤ 09 (4)
✓ VALID: Monotonically non-decreasing
```

---

## Transformation

```
READER STATE MACHINE:

    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │  UNINFORMED ──► GROUNDED ──► CHALLENGED ──► TENSIONED ──►  │
    │      │              │             │              │          │
    │      │              │             │              │          │
    │      ▼              ▼             ▼              ▼          │
    │    entry        ORIENTATION   COMPLICATION    CRISIS       │
    │                  00, 01         02, 03        04, 05       │
    │                                                             │
    │  ──► RESOLVED ──► TRANSFORMED ──► exit                     │
    │         │              │                                    │
    │         │              │                                    │
    │         ▼              ▼                                    │
    │      CLIMAX       COMPLETION                                │
    │      06, 07         08, 09                                  │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

---

## Constraints

- Progression MUST be monotonic (no regression)
- Each chapter declares ARC position
- Final chapter MUST be COMPLETION
- Entry/exit beliefs MUST differ (transformation required)

---

## Era Mapping

The GUIDE ARC maps to CANONIC eras:

| ARC Stage | Era | Stack Layer | Exit State |
|-----------|-----|-------------|------------|
| ORIENTATION | v0 ORIGIN | GIT | Understand Git as foundation |
| COMPLICATION | v1 MACHINE | EVO | See LEDGER + TRANSCRIPTS |
| CRISIS | v1→v2 | AGENT | Grasp CHAT + EVO |
| CLIMAX | v2 FOUNDATION | APP | Understand AGENT + VERIFY |
| COMPLETION | v3 DISTRIBUTED | CANONVERSE | See the full network |

**Parallel:** The reader's transformation mirrors CANONIC's evolution.

---

## Stack Derivation Through ARC

```
ORIENTATION:    GIT exists (foundation)
                     ↓
COMPLICATION:   GIT → EVO (formalization)
                     ↓
CRISIS:         EVO → AGENT (interface)
                     ↓
CLIMAX:         AGENT → APP (validation)
                     ↓
COMPLETION:     APP → CANONVERSE (distribution)
```

---
