# MED.ONCO.MAMMO — CANON

inherits: /MED/ONCO/

---

## Axiom

**MED.ONCO.MAMMO = Breast Oncology NODE. Mammography subspecialty.**

MAMMO is NODE. NODE inherits ONCO. ONCO inherits MED. MED inherits AGENT.

---

## Structure

```
MED/ONCO/MAMMO/         — NODE (subspecialty)
├── EVIDENCE/           — E (Evidential: breast-specific)
│   ├── NCCN/           — Treatment guidelines
│   └── BIRADS/         — Imaging classification
└── FRONTEND/           — User interface
```

---

## Evidence Sources

| Source | Authority | Scope |
|--------|-----------|-------|
| NCCN Breast | GOLD | Treatment guidelines |
| BI-RADS | GOLD | Imaging classification |
| mCODE | GOLD | Oncology data (inherited from /ONCO/) |

---

## Constraints

1. MED.ONCO.MAMMO MUST inherit from /MED/ONCO/.
2. MED.ONCO.MAMMO MUST differentiate DCIS vs Invasive.
3. MED.ONCO.MAMMO MUST cite NCCN for treatment claims.
4. MED.ONCO.MAMMO MUST use BI-RADS for imaging claims.
5. MED.ONCO.MAMMO MUST use mCODE (inherited from /ONCO/).

---

## Origin

```
Evidence: 20,000+ patient encounters
Grant: $2M Casey DeSantis Cancer Innovation (FCIF 354)
Trial: NCT06604078 (Active)
Domain: medicine/oncology/breast
```

---

*MED.ONCO.MAMMO | Breast Oncology NODE | CANONIC.MEDICINE*
