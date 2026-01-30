# MED.MAMMO — CANON

inherits: /MED/

---

## Axiom

**MED.MAMMO = Breast Oncology Domain. Medicine specialized for breast cancer.**

---

## Scope

```
MED/MAMMO/
└── CHAT/           — MED.MAMMO.CHAT = MAMMO-CHAT
```

---

## Evidence Sources

| Source | Authority | Scope |
|--------|-----------|-------|
| NCCN Breast | GOLD | Treatment guidelines |
| BI-RADS | GOLD | Imaging classification |
| mCODE | GOLD | Oncology data standard |

---

## Constraints

1. MED.MAMMO MUST inherit from /MED/.
2. MED.MAMMO MUST differentiate DCIS vs Invasive.
3. MED.MAMMO MUST use mCODE for precision embedding.
4. MED.MAMMO MUST cite NCCN for treatment claims.
5. MED.MAMMO MUST use BI-RADS for imaging claims.

---

## Origin

```
Evidence: 20,000+ patient encounters
Grant: $2M Casey DeSantis Cancer Innovation (FCIF 354)
Trial: NCT06604078 (Active)
Domain: medicine/oncology/breast
```

---

*MED.MAMMO | Breast Oncology | CANONIC.MEDICINE*
