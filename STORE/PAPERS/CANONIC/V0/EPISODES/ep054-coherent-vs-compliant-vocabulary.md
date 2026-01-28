# Episode 054: Coherent vs Compliant Vocabulary Discovery

**Episode:** 054  
**Date:** 2026-01-08  
**Context:** Canonbase review  
**Agent:** cline

**Type:** Unknown
**Participants:** Unknown
---

## The Discovery

During a comprehensive canonbase review, I identified that two essential governance quality descriptors were missing from the root vocabulary:

- **coherent** — describing semantic consistency of constraints
- **compliant** — describing syntactic satisfaction of requirements

These terms enable precise governance discourse about the difference between:
- Structure being correct (compliant) vs. logic being sound (coherent)

---

## The Insight

A system can be:
- **Compliant but incoherent**: All files present, triad complete, but constraints contradict each other
- **Incoherent and non-compliant**: Missing files + logical contradictions in existing rules
- **Coherent but non-compliant**: Well-reasoned rules but structural violations (missing triad)
- **Fully governed**: Both coherent AND compliant

This distinction matters because:
1. Compliance is checkable via syntactic validation (fast, deterministic)
2. Coherence requires semantic validation (LLM-powered, expensive)
3. Governance maturity = convergence from semantic to syntactic checks

---

## The Canonification

**Action taken:** Canonified both terms to root VOCAB.md in Governance Terms section

**Commit:** `Canonify coherent and compliant vocabulary definitions`

**Definition added:**

```
### coherent
The property that constraints are logically consistent with each other
and with inherited upstream constraints. A governance structure is coherent
when CANON constraints do not contradict, downstream CANONs do not
contradict upstream invariants, and VOCAB definitions are internally
consistent. Coherence is semantic—it asks whether the system makes sense
together. Contrast with compliance (syntactic structural matching).

### compliant
The property that artifacts satisfy structural requirements defined in
CANON. A system is compliant when required files exist (triad present),
file formats match specifications, references resolve correctly, and
commit patterns follow conventions. Compliance is syntactic—it asks
whether artifacts match rules. Contrast with coherence (logical constraint
alignment).

### fully governed
The property of being both coherent AND compliant simultaneously. A fully
governed system has structurally correct artifacts (compliant) that satisfy
logically consistent constraints (coherent). The ideal state of CANONIC
governance—requiring both syntactic validation (fast, deterministic) and
semantic validation (LLM-powered, expensive). Contrast with partial
governance where only one dimension is satisfied.
```

---

## The Proof

1. **Discovery**: Canonbase review revealed vocabulary gap
2. **Analysis**: Distinguished semantic (coherent) from syntactic (compliant)
3. **Canonification**: Added definitions to root VOCAB.md
4. **Documentation**: This episode captures the discovery

The governance now has precise terminology for discussing system quality across two orthogonal dimensions.

---

## Related Episodes

- Episode 031: Failed VOCAB consumption
- Episode 032: VOCAB archaeology
- Episode 053: Key principle — root CANON minimalism

---

**End Episode 054**

## The Session

Not recorded in original episode.

## Key Assets Discovered

Not recorded in original episode.

## Violations Detected and Fixed

Not recorded in original episode.

## Git Signal

Not recorded in original episode.

**Status:** Not recorded in original episode.
