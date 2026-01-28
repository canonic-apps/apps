# EPISODE - ep158

Freeze as IP boundary - public/private manuscript split

---

## Metadata

- Date: 2026-01-14
- Episode ID: ep158
- Type: Discovery
- Participants: Dexter Hadley, Claude Opus 4.5
- Agent: Claude Code
- Model identity: claude-opus-4-5-20251101
- Channel: IDE
- Source: VSCode Claude Code extension
- Status: Canonified

---

## Context

Following ep156 (IP leakage violation) and ep157 (compliance report), we
discovered that the freeze boundary is not just a version tag - it is an
IP protection boundary that separates public artifacts from private
development.

---

## Discovery

**The freeze is an IP boundary, not just a version tag.**

When we froze the stack at `stack-freeze-2026-01-12`, we created two distinct
artifact classes:

1. **Public artifacts** - everything at or before the freeze, publishable
2. **Private artifacts** - everything after the freeze, IP to be protected

The publishing workflow itself is a discovery engine. Every session that uses
the frozen OS to produce artifacts generates insights that belong to the next
cycle, not the current frozen release.

This creates a natural two-manuscript structure:

- **Public PAPER** (`paper/manuscript.md`) - v0.1, frozen window only
- **Private PAPER draft** (`patents/paper-draft/`) - v0.2+, all post-freeze IP

Post-freeze discoveries must go through the patented canonification process
before entering the public stack.

---

## Corrections applied

1. Moved post-freeze artifacts from `paper/` to `patents/paper-draft/`:
   - `figures/` (mermaid sources + renders)
   - `output/` (PDF, combined markdown)
   - `scripts/` (build tooling)
   - `supporting/` (appendices with post-freeze IP)
   - `templates/` (LaTeX headers)
   - `TYPESET.md` (typesetting governance)

2. Cleaned `paper/CANON.md` - removed post-freeze axioms:
   - Axiom 14 (Supporting materials) - removed
   - Axiom 17 (Typesetting profile) - removed
   - Axiom 18 (Build outputs) - removed
   - Renumbered remaining axioms

3. Public `paper/` now contains only:
   - Triad files (CANON, VOCAB, README)
   - PAPER.md (spec)
   - manuscript.md (v0.1 with inline mermaids)
   - LICENSE, NOTICE

---

## Canonification

This discovery is canonified as governance:

**Freeze boundaries are IP boundaries.** Work produced after a freeze belongs
to the PATENTS scope until protected via IDF and PROVISIONAL filing. Only
after IP protection can post-freeze content be released publicly in the next
version.

The pipeline is:
1. Freeze (creates IP boundary)
2. Post-freeze work (generates new IP in private scope)
3. IDF filing (discloses IP)
4. PROVISIONAL filing (protects IP)
5. Public release (v0.2+ with protected IP)

---

## Evidence references (LEDGER)

- paper:fcd5194 - v0.1 manuscript finalized
- paper:da477ea - manuscript reverted to pre-leak state
- patents/paper-draft/ - private v0.2 development scope
- ep156 - IP leakage violation
- ep157 - compliance report

---

## Notes

This episode surfaces the meta-pattern that the publishing workflow is itself
a discovery engine that must be IP-protected.

---

**This file is a non-authoritative template.**
**It defines structure only and confers no governance, enforcement, or interpretive meaning.**
