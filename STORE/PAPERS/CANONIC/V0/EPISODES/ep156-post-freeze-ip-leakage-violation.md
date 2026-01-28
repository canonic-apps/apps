# EPISODE - ep156

Post-freeze IP leakage violation

---

## Metadata

- Date: 2026-01-14
- Episode ID: ep156
- Type: Violation
- Participants: Dexter Hadley, Claude Opus 4.5
- Agent: Claude Code
- Model identity: claude-opus-4-5-20251101
- Channel: IDE
- Source: VSCode Claude Code extension
- Status: Resolved

---

## Context

During PDF typesetting work, post-freeze discoveries were leaking into the public
manuscript artifact. The evidence window is frozen at `stack-freeze-2026-01-12`,
but the PDF build version (`manuscript-full.md`) contained IP and discoveries
made after that freeze.

---

## Session narrative

While reverting the manuscript to recover mermaid diagrams lost during typesetting,
we compared the reverted version (447bf45) against the built PDF version and
discovered significant content expansion that violated the freeze boundary.

The PDF build version included:

1. Expanded transcript-anchored provenance methodology
2. Knowledge API / stream indexing architecture
3. Positive control markers and LFG signal detection
4. Branch-to-fixation collapse pattern
5. Full appendices A-F with proof sketches
6. Episodes ep140-ep149 references (all post-freeze)
7. Claim-to-evidence map expansion (6 claims to 16)

All of these represent discoveries made **while using the frozen OS** - they
belong to the next freeze cycle and must go through the patented canonification
process before entering the public stack.

---

## Violations encountered

- Post-freeze IP leaked into the public manuscript during PDF typesetting.
- Discoveries made during publishing workflow were added to the paper without
  going through the canonification gate.
- The freeze boundary was violated by including evidence references beyond
  the frozen window.

---

## Corrections applied

- Reverted manuscript.md to commit 447bf45 ("paper: editorial polish"), the
  last clean state with mermaid diagrams before post-freeze content injection.
- Identified the clean separation:
  - **Public paper** = frozen evidence window only (447bf45 content)
  - **Private discoveries** = everything learned during publishing/typesetting
  - **Canonification gate** = patented process controls what crosses over

---

## Discovery

This episode surfaces a meta-pattern: **the freeze is not just a version tag,
it is an IP boundary**. Work done after the freeze (typesetting, publishing,
discovery synthesis) generates new IP that must be protected until it goes
through the canonification process.

The publishing workflow itself is a discovery engine. Every session that uses
the frozen OS to produce artifacts is generating insights that belong to the
next cycle, not the current frozen release.

---

## Evidence references (LEDGER)

- paper:447bf45 - last clean manuscript with mermaids
- paper:9d1d6fb - commit where mermaids were removed and post-freeze content leaked
- stack-freeze-2026-01-12 - the evidence window boundary
- patents repo - canonification process protection

---

## Notes

This is a governance violation we caught during routine reversion. The correction
ensures the public paper contains only frozen-window evidence, and post-freeze
discoveries remain private until canonified.

---

**This file is a non-authoritative template.**
**It defines structure only and confers no governance, enforcement, or interpretive meaning.**
