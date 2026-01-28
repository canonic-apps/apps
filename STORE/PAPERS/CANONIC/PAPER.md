# PAPER SPEC

---

## 1. Purpose

Define the PAPER scope: the CANONIC academic paper governing epistemic claims bounded by LEDGER evidence.

---

## 2. Governance Path

```
/ (ROOT)
└── /canonic-foundation/LANGUAGE/ (LANGUAGE CANON)
    └── /canonic-hadley/CANONIC-PAPER/ (THIS SCOPE)
```

| Field | Value |
| --- | --- |
| Path | `/canonic-hadley/CANONIC-PAPER/` |
| Inherits | `/canonic-foundation/LANGUAGE/` |
| Closes | CANON.md |

---

## 3. Normative Language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are
to be interpreted as described in RFC 2119.

---

## 4. Manuscript Structure

| Order | Section | Description |
| --- | --- | --- |
| 00 | Abstract | Problem, solution, contribution |
| 01 | Introduction | CANONIC paradigm motivation |
| 02 | Background | Related work, prior art |
| 03 | CANONIC LANGUAGE | Formal specification |
| 04 | Implementation | VALIDATORS, MACHINE, OS, LEDGER |
| 05 | Evaluation | Empirical validation |
| 06 | Discussion | Implications, limitations |
| 07 | Conclusion | Summary, future work |
| 08 | Supplemental | GitHub as proof archive |

---

## 5. Lifecycle

| Phase | Status | Description |
|-------|--------|-------------|
| v0 draft | ✓ Complete | CANONIC PAPER drafted |
| v0 freeze | ✓ Complete | IP boundary: January 23, 2026 |
| v0 open-source | ✓ Complete | Archive: github.com/canonic-machine |
| v0 patents | Pending | File HADLEY-PROV-001/002/003 |
| v0 publish | Ready | arXiv submission ready |
| v0 comments | Pending | Post-publication errata |
| v1 build | Active | canonic-foundation era begins |
| v1 publish | Planned | LANGUAGE + DETROS formalization |

---

## 6. Freeze Sequence

Per CANON Axiom 4:

```
IP freeze → Publish freeze → Ledger freeze
```

| Freeze | Effect | Reversible |
|--------|--------|------------|
| IP freeze | Public/private boundary marked | Yes (content editable) |
| Publish freeze | Submitted to external archive | No (content locked) |
| Ledger freeze | Versioned on chain | No (immutable) |

---

## 7. Supplemental Separation

Per CANON Axiom 5:

Main PAPER **MUST NOT** contain supplemental material.

| Type | Location | Content |
|------|----------|---------|
| Appendix | GitHub | Math proofs, formal derivations |
| Supplemental | GitHub | Full v0 closure (drift episodes, IDFs, validators) |

**GitHub IS the supplemental archive. The OS proves the PAPER.**

---

## 8. Publication Targets

| Target | Priority | Status |
|--------|----------|--------|
| arXiv | P0 | Ready (v0 manuscript.pdf) |
| ACL/EMNLP | P1 | Planned 2026 |
| Nature Machine Intelligence | P2 | Planned 2027 |

---

## 9. Core Assets

| File | Purpose |
|------|---------|
| manuscript.md | Source manuscript |
| manuscript.pdf | Generated PDF |
| SUPPLEMENTAL.md | Supplemental material index |

---

## 10. Validation

```
VALIDITY = triad(scope) ∧ inheritance(scope) ∧ introspection(scope)
```

PAPER validity requires:
- CANON.md, VOCAB.md, README.md present
- Inherits from /canonic-foundation/LANGUAGE/
- All CANON concepts defined in VOCAB

---

This SPEC closes CANON. Governance is defined exclusively by CANON.

---
