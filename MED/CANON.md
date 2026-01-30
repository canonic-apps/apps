# MED — CANON

inherits: /AGENT/

---

## Axiom

**MED = Medical NODE. Healthcare governance through DETROS.**

MED is NODE. NODE is AGENT. AGENT = EVO + CHAT + SHOP.

---

## Structure

```
MED/                    — NODE (inherits AGENT)
├── ENGINE/             — O (Operational)
│   ├── READING/        — Patient queries
│   ├── WRITING/        — Clinician input
│   └── VALIDATING/     — Claim verification
├── EVIDENCE/           — E (Evidential: pan-MED ontologies)
│   ├── SNOMED/         — Diagnoses, procedures, body sites
│   ├── ICD/            — Classifications (ICD-10-CM)
│   ├── LOINC/          — Labs, vitals
│   ├── RXNORM/         — Medications
│   └── CPT/            — Procedures
├── COIN/           — Token + provenance
├── LEDGER/             — T (Temporal)
├── SCHEMA/             — S (Structural)
└── ONCO/               — NODE (specialty)
    └── MAMMO/          — NODE (subspecialty)
```

---

## Pan-MED Ontologies

| Ontology | Scope | Authority |
|----------|-------|-----------|
| SNOMED CT | Clinical terms | IHTSDO |
| ICD-10-CM | Diagnoses | WHO/CMS |
| LOINC | Labs + vitals | Regenstrief |
| RxNorm | Medications | NLM |
| CPT | Procedures | AMA |

All MED specialties inherit these. Compose, don't duplicate.

---

## DETROS Mapping

| Dimension | Component |
|-----------|-----------|
| D (Declarative) | CANON.md |
| E (Evidential) | EVIDENCE/ (pan-MED + specialty) |
| T (Temporal) | LEDGER/ |
| R (Relational) | USERS/ |
| O (Operational) | ENGINE/ |
| S (Structural) | SCHEMA/ |

---

## Constraints

1. MED MUST inherit AGENT (EVO + CHAT + SHOP).
2. MED MUST implement COIN for provenance.
3. MED MUST audit to LEDGER with HIPAA compliance.
4. MED MUST credential operators via NPI.
5. MED MUST maintain 7-year audit retention.
6. All operations MUST route through ENGINE.
7. All tokens MUST comply with COIN.

---

## Compliance

| Standard | Requirement |
|----------|-------------|
| HIPAA | Privacy + Security |
| HITECH | Breach notification |
| 21st Century Cures | No information blocking |
| FHIR R4 | Interoperability |
| TEFCA/USCDI | Data exchange |

---

*MED | Medical NODE | CANONIC.MEDICINE*
