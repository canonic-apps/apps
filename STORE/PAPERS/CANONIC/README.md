# PAPER (/paper/)

Academic manuscript governance for evidence-bounded epistemic claims.

---

## Purpose

PAPER governs the creation and publication of academic manuscripts within CANONIC.

PAPER is epistemic-only: it records knowledge but does not enforce behavior. All claims trace to LEDGER evidence and are bounded by declared evidence windows.

---

## Scope

### In Scope

- Academic manuscript production (manuscript.md)
- PDF generation and typesetting
- Evidence-bounded claim validation
- Freeze sequence management (IP → publish → ledger)
- Supplemental material organization

### Out of Scope

- Governance enforcement (see CANON)
- Evidence storage (see LEDGER)
- Typesetting rules (see PAPER.md spec)

---

## Quickstart

```bash
# Build manuscript PDF
cd paper
pandoc manuscript.md -o manuscript.pdf

# Validate claims trace to evidence
python validators/paper/validate.py

# Check freeze status
grep "freeze:" PAPER.md
```

---

## Artifacts

| File | Purpose |
|------|---------|
| manuscript.md | Source manuscript in Markdown |
| manuscript.pdf | Generated PDF output |
| PAPER.md | Spec governing typesetting |
| SUPPLEMENTAL.md | Supplemental material index |

---

## References

- [CANON.md](CANON.md) — Normative axioms (5 axioms)
- [VOCAB.md](VOCAB.md) — Term definitions
- [PAPER.md](PAPER.md) — Typesetting specification
- [SUPPLEMENTAL.md](SUPPLEMENTAL.md) — Supplemental material

---

*Governed by: CANON.md*

---
