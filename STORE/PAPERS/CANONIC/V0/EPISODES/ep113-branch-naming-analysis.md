# Episode 113: Branch Naming Analysis - Convention vs Constraint

**Date:** 2026-01-11
**Type:** Analysis
**Participants:** Human (Governor General), AI (Cline)
**Agent:** Cline

---

## The Session

Human asked if OS and paper being on `main` branch instead of `OS` and `PAPER` is a violation. I searched the CANONbase for branch naming constraints.

## Analysis

**Branch status checked:**

| Repo | Current Branch | CANON Constraint? |
|------|---------------|-------------------|
| canonic | CANONIC | No explicit constraint found |
| machine | MACHINE | No explicit constraint found |
| os | main | No explicit constraint found |
| writing | WRITING | No explicit constraint found |
| paper | main | No explicit constraint found |

**Constraints found:**

1. **PAPER CANON (Branch Scope):** "Canon is branch-scoped. Constraints apply only within the branch where they are canonified."
   - This describes how canon works, not branch naming

2. **GIT CANON:** No branch naming constraints
   - Only addresses: ledger, canon-approval, autocommit, commit-push coupling, maturity-autocommit, autodoc

3. **OS CANON:** No branch naming constraints
   - Addresses: enforce, govern, canon, spec-name, episode

**Finding:** There is NO explicit CANON constraint that branch names must match layer names. The convention exists but is not enforced.

## Violations Detected and Fixed

**Not a violation:** Branch naming is a convention, not a constraint. Without explicit CANON stating "repo branch must match layer name," the current state is not a violation.

**Observation:** Layer-named branches (CANONIC, MACHINE, WRITING) exist for canonic, machine, writing. Main branch used for os, paper. This is inconsistent but not forbidden by CANON.

## Git Signal

- `canonic` - branch: CANONIC
- `machine` - branch: MACHINE
- `os` - branch: main
- `writing` - branch: WRITING
- `paper` - branch: main

## The Insight

Not every convention is a constraint. CANON must explicitly state constraints. Without explicit canon forbidding `main` branch for OS/paper, no violation exists. The system is governed by what IS stated, not by what COULD be stated.

**Status:** Analyzed; no violation found. Convention ≠ constraint.
