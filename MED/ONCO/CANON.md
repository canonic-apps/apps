# MED.ONCO — CANON

inherits: /MED/

---

## Axiom

**MED.ONCO = Oncology NODE. Cancer medicine via mCODE composition.**

ONCO is NODE. NODE inherits MED. MED inherits AGENT.

---

## mCODE Composition

```
mCODE = PATIENT + LAB + DISEASE + GENOMICS + TREATMENT + OUTCOME
```

| Domain | Profiles | Inherits | Adds |
|--------|----------|----------|------|
| PATIENT | CancerPatient | /MED/ | — |
| LAB | TumorMarker | /MED/LOINC/ | — |
| DISEASE | PrimaryCancer | /MED/SNOMED/, /MED/ICD/ | ICD-O-3, TNM |
| GENOMICS | GenomicsReport | — | HGVS, HGNC |
| TREATMENT | CancerTreatment | /MED/RXNORM/, /MED/CPT/ | — |
| OUTCOME | DiseaseStatus | /MED/SNOMED/ | — |

mCODE = 6 domains × 23 profiles × ~90 data elements.

---

## Structure

```
MED/ONCO/               — NODE (specialty, inherits /MED/)
├── EVIDENCE/           — E (Evidential: pan-ONCO)
│   ├── MCODE/          — mCODE (composes from /MED/EVIDENCE/)
│   ├── TNM/            — Staging (pan-ONCO)
│   └── HGVS/           — Genomics (pan-ONCO)
└── MAMMO/              — NODE (subspecialty: breast)
    └── EVIDENCE/       — E (Evidential: breast-specific)
        ├── NCCN/       — Treatment guidelines
        └── BIRADS/     — Imaging classification
```

Inherits from /MED/: SNOMED, ICD, LOINC, RXNORM, CPT
Adds pan-ONCO: TNM, HGVS, ICD-O-3

---

## Subspecialties

| Node | Domain | Status |
|------|--------|--------|
| MAMMO | Breast | Active |
| LUNG | Lung | Future |
| COLON | Colorectal | Future |
| PROSTATE | Prostate | Future |

---

## Constraints

1. MED.ONCO MUST inherit MED.
2. MED.ONCO MUST compose mCODE (6 domains).
3. MED.ONCO subspecialties MUST define domain-specific EVIDENCE.
4. MED.ONCO MUST cite guidelines for treatment claims.
5. MED.ONCO MUST embed via SNOMED CT, ICD-O-3, LOINC, RxNorm, TNM.

---

*MED.ONCO | Oncology NODE | mCODE composition | CANONIC.MEDICINE*
