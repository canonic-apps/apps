# BOOK — Governance Publishing App

inherits: /CANONIC/APPS/STORE/
tier: 63
status: coming soon

---

## Axiom

**Author books. Enforce narrative governance. Publish to STORE/BOOKS/.**

---

## Service

### What

BOOK app provides:

1. **Spine Builder** — Define temporal chapter order
2. **Arc Mapper** — Assign narrative progression
3. **Chapter Scaffolder** — Generate compliant chapter structure
4. **Section Editor** — Write within governance constraints
5. **Reference Linker** — Bind claims to evidence
6. **Certification Runner** — Validate full DETROS

### How

```bash
# Initialize a new book
canonic book init "My Book Title" --arc 5

# Add a chapter
canonic book chapter add "Foundation" --arc ORIENTATION

# Add sections
canonic book section add 00-foundation "Genesis"
canonic book section add 00-foundation "Axioms"

# Validate book structure
canonic book validate --tier 63

# Publish to STORE
canonic book publish
```

### Why

- Governance-first authoring
- Narrative progression is validated
- Claims require evidence
- Structure IS governance

---

## DETROS

| Dimension | App Function |
|-----------|--------------|
| D | SPINE definition |
| E | REFERENCE linking |
| T | ARC progression |
| R | CHAPTER scoping |
| O | EXERCISE creation |
| S | SECTION formatting |

---

## Pricing

| Tier | Books | Chapters | Price |
|------|-------|----------|-------|
| COMMUNITY | 1 | 5 | Free |
| CLOSURE | 3 | 15 | $49/mo |
| BUSINESS | 10 | 50 | $299/mo |
| ENTERPRISE | Unlimited | Unlimited | $999/mo |

---

## Validation

BOOK app validates:

1. SPINE ordering (T dimension)
2. ARC monotonicity (no regression)
3. CHAPTER inheritance (R dimension)
4. SECTION structure (S dimension)
5. REFERENCE completeness (E dimension)
6. Claim coverage (D dimension)

---

## Integration

### GitHub Action

```yaml
- uses: canonic/book-validate@v1
  with:
    token: ${{ secrets.CANONIC_TOKEN }}
    book: ./STORE/BOOKS/my-book
    tier: 63
```

### CLI

```bash
canonic book validate --book ./my-book --tier 63
```

---

## Links

- [BOOKS/CANON.md](/CANONIC/STORE/BOOKS/) — Book governance
- [VaaS](https://canonic-apps.github.io) — Validation as a Service

---
