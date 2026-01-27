# THE INHERITANCE AXIOM

*Constraints flow down. Never weaken.*

---

## Abstract

The third axiom of CANONIC establishes that constraints must flow from parent to child and can never be weakened. This paper explains monotonic constraint propagation in governance hierarchies.

---

## 1. The Problem with Weakening

Traditional governance hierarchies allow weakening:
- Exceptions override rules
- Local overrides beat global
- Subsidiaries escape parent constraints

The result: governance drift, inconsistency, exploitation.

---

## 2. The Monotonic Solution

CANONIC enforces monotonic inheritance:

```
PARENT (3 constraints)
    │
    ▼ inherits
CHILD (3 + N constraints, where N ≥ 0)
```

Children can only ADD constraints, never REMOVE.

---

## 3. How It Works

```
/CANONIC/CANON.md
├── Axiom 1: TRIAD
├── Axiom 2: INTROSPECTION
└── Axiom 3: INHERITANCE

/HOLDINGS/CANON.md (inherits: /CANONIC/)
├── [inherits all 3 axioms]
├── Constraint 4: Express governance in CANONIC LANGUAGE
├── Constraint 5: Audit to git (evidence)
└── Constraint 6: LLMs read. Humans review.

/HOLDINGS/COMPANIES/CANON.md (inherits: ../CANON.md)
├── [inherits all 6 constraints]
├── Constraint 7: All entities MUST be Foundation members
├── Constraint 8: All IP flows to Foundation
└── Constraint 9: Mission MUST NOT change
```

Each level adds. None remove.

---

## 4. The Mathematical Property

```
Let C(node) = constraint set at node
Let parent(node) = parent of node

∀ node : C(parent(node)) ⊆ C(node)

Constraints only accumulate. QED.
```

---

## 5. Why This Matters

1. **No escape** — Subsidiaries cannot bypass parent rules
2. **Audit trail** — Trace any constraint to its source
3. **Predictability** — Knowing the root tells you the floor
4. **Trust** — Foundation constraints persist through all children

---

## 6. Structure as Enforcement

With LLMs reading governance:

```
hadleylab-dexter/HOLDINGS/COMPANIES/CANON.md:
    inherits: ../CANON.md
```

The LLM:
1. Reads this file
2. Navigates to parent
3. Reads parent constraints
4. Applies all constraints
5. Validates child ⊇ parent

No code required. Structure enforces itself.

**Ledger Reference**: DISCLOSURE-TOOLING-001

---

## 7. Evidence

Inheritance appears throughout CANONVERSE:

| Level | File | Inherits |
|-------|------|----------|
| Root | /CANONIC/CANON.md | — |
| Language | /LANGUAGE/CANON.md | /CANONIC/ |
| Machine | /MACHINE/CANON.md | /CANONIC/ |
| Holdings | /HOLDINGS/CANON.md | /CANONIC/ |
| Companies | /COMPANIES/CANON.md | ../CANON.md |

35 repos, 420+ commits, one inheritance chain.

---

## Conclusion

Constraints flow down. Never weaken. This is the architecture of trust. Parent constraints persist. Children can only add. The system cannot loosen at the edges. Governance holds.

---

*AXIOMS/paper-003-inheritance | January 2026*
*Axiom 3 of 3*
