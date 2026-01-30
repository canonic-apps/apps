# mCODE — Embedding Layer

inherits: /MED-CHAT/EVIDENCE/

---

## Purpose

mCODE = minimal Common Oncology Data Elements.

**Authority:** GOLD (HL7 FHIR standard)

**Role:** Precision Cancer Embedding Layer

---

## DETROS Mapping

```
mCODE = S∩E∩R (index 21)
      = STRUCTURAL + EVIDENTIAL + RELATIONAL

S — Defines cancer data structures (SCHEMA)
E — Provides evidence vocabulary (EMBEDDING)
R — Defines concept relationships (GRAPH)
```

---

## Embedding Architecture

```
GENERIC LLM EMBEDDING:
──────────────────────
Text → Transformer → Vector[1536]
                         │
                         └── No clinical semantics

mCODE PRECISION EMBEDDING:
──────────────────────────
Text → mCODE Parser → Concept[SNOMED] → Vector[mCODE]
                              │                │
                              ▼                ▼
                         Clinical ID      Semantic space
                              │
                              └── DCIS ≠ Invasive (distinct vectors)
```

**Key insight:** mCODE embeds clinical MEANING, not just text similarity.

---

## Old vs DETROS Approach

```
OLD (LLM Translator):
─────────────────────
Text → LLM → mCODE JSON
         │
         └── LLM "guesses" structure
         └── Embedding = text similarity only

DETROS (mCODE Embedding Layer):
───────────────────────────────
Text → mCODE EMBED → Vector[clinical] → ENGINE
              │              │
              ▼              ▼
        SNOMED/ICD10    Precision semantics
              │
              └── "Stage 1 DCIS" ≠ "Stage 1 Invasive"
                  (distinct embedding vectors)
```

**Key difference:**
1. LLM operates THROUGH mCODE constraints, not around them.
2. Embeddings carry clinical semantics, not just text patterns.
3. DCIS and Invasive are DISTINCT in embedding space (Minh's concern).

---

## Embedding Space

```
mCODE Embedding Dimensions:
├── Histology (DCIS | Invasive | Mixed)
├── Grade (1 | 2 | 3)
├── Stage (0 | I | II | III | IV)
├── Receptors (ER | PR | HER2)
├── Molecular (Luminal A | B | HER2+ | TNBC)
└── Treatment (Surgery | Radiation | Chemo | Endocrine | Targeted)

Query: "Stage 1 breast cancer treatment"
       │
       ▼
mCODE Embed: [?, ?, I, ?, ?, ?]  ← Incomplete vector
       │
       ▼
VALIDATOR: "Histology required for treatment recommendation"
```

---

## Core Profiles

| Profile | Description | FHIR Resource |
|---------|-------------|---------------|
| CancerPatient | Patient with cancer | Patient |
| PrimaryCancerCondition | Primary malignancy | Condition |
| TNMStageGroup | TNM staging | Observation |
| TumorMarker | Biomarkers | Observation |
| CancerRelatedProcedure | Treatments | Procedure |

---

## Breast Cancer Elements

### Primary Cancer Condition

```json
{
  "resourceType": "Condition",
  "code": {
    "coding": [{
      "system": "http://snomed.info/sct",
      "code": "254837009",
      "display": "Malignant neoplasm of breast"
    }]
  },
  "bodySite": [{
    "coding": [{
      "system": "http://snomed.info/sct",
      "code": "76752008",
      "display": "Breast structure"
    }]
  }]
}
```

### DCIS vs Invasive (Minh's concern)

```
DCIS:     SNOMED 109886000
Invasive: SNOMED 254837009

VALIDATOR MUST differentiate:
├── histology code required
├── stage interpretation differs
└── treatment recommendations differ
```

---

## Integration with ENGINE

```
READING ──► mCODE SCHEMA ──► Structured response
                │
                ▼
            Patient can export to EHR

WRITING ──► mCODE VALIDATION ──► Structured input
                │
                ▼
            Clinician contributes structured data

VALIDATING ──► mCODE CONSTRAINT CHECK
                │
                ▼
            Claims must map to mCODE vocabulary
```

---

## Citation Format

```
mCODE.STU3.Profile.Field
```

Example: `mCODE.STU3.PrimaryCancerCondition.histologyMorphologyBehavior`

---

*mCODE | S∩E∩R = Structured Evidence | FHIR-based ontology*
