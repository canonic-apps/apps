# Episode 166: SPEC Naming Convention Violation

**Date:** 2026-01-15
**Type:** Violation
**Participants:** USER, AI
**Agent:** Claude Opus 4.5

---

## The Session

While drafting strategic specifications for the CANONIC Foundation and OncoNex, the AI agent created files named `SPEC.md` instead of following the established naming convention where the SPEC artifact is named after the scope (e.g., `FOUNDATION.md`, `ONCONEX.md`, `US.md`, `MT.md`).

## The Violation

The AI created:
- `/companies/foundation/SPEC.md` (should be `FOUNDATION.md`)
- `/companies/onconex/SPEC.md` (should be `ONCONEX.md`)

This violated the established pattern visible in:
- `/companies/onconex/us/US.md`
- `/companies/onconex/mt/MT.md`

## Root Cause

The AI followed the template filename (`te003-spec-template.md`) literally rather than recognizing that `SPEC` is a variable that should be replaced with the scope name in uppercase.

## Key Assets Affected

- `/companies/foundation/FOUNDATION.md` (renamed from SPEC.md)
- `/companies/onconex/ONCONEX.md` (renamed from SPEC.md)

## SWAT Analysis

**Strengths**
- User immediately caught the violation
- Files were quickly renamed to correct convention
- Episode documented the violation pattern

**Weaknesses**
- AI failed to recognize SPEC as a variable
- Template naming created ambiguity
- No validator exists for SPEC file naming

**Opportunities**
- Clarify SPEC naming convention in VOCAB
- Add SPEC naming to template documentation
- Consider a SPEC-naming validator

**Threats**
- Future AI sessions may repeat this violation
- Inconsistent SPEC naming across scopes
- Template ambiguity may persist

## Correction Applied

```bash
mv companies/foundation/SPEC.md companies/foundation/FOUNDATION.md
mv companies/onconex/SPEC.md companies/onconex/ONCONEX.md
```

## The Insight

SPEC is not a literal filename—it is a variable that should be replaced with the scope name in uppercase. The pattern is:
- Scope `/companies/foundation/` → SPEC file `FOUNDATION.md`
- Scope `/companies/onconex/` → SPEC file `ONCONEX.md`
- Scope `/companies/onconex/us/` → SPEC file `US.md`

This convention makes the strategic planning artifact immediately identifiable by scope name.

## Related Episodes

- ep092-spec-naming-violation.md
- ep093-spec-naming-semantics-reset.md

## IDF Potential

IDF-071: SPEC Naming Convention Enforcement — A validator that checks SPEC files are named after their containing scope.

---

**Status:** Recorded

---
