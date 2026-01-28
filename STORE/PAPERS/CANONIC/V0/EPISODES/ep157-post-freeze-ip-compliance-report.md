# EPISODE - ep157

Post-freeze IP compliance report

---

## Metadata

- Date: 2026-01-14
- Episode ID: ep157
- Type: Compliance Report
- Participants: Dexter Hadley, Claude Opus 4.5
- Agent: Claude Code
- Model identity: claude-opus-4-5-20251101
- Channel: IDE
- Source: VSCode Claude Code extension
- Status: Active

---

## Context

Following ep156 (post-freeze IP leakage violation), this report audits the
current state of the paper repo to identify what post-freeze IP remains in
the public stack.

---

## Freeze boundary

- **Freeze tag**: `stack-freeze-2026-01-12`
- **Freeze commit (paper)**: `paper:0ee1970`
- **Files at freeze**: CANON.md, PAPER.md, README.md, VOCAB.md (+ .DS_Store)

---

## Current state (post-reversion)

### Files added after freeze

| Path | Contains post-freeze IP? | Assessment |
|------|-------------------------|------------|
| manuscript.md | **NO** (reverted to 447bf45) | Clean - frozen window only |
| TYPESET.md | YES | Publishing workflow discovery |
| LICENSE | NO | Standard file |
| NOTICE | NO | Standard file |
| .gitignore | NO | Standard file |
| figures/ | **YES** | Post-freeze discoveries |
| scripts/ | YES | Build tooling discovery |
| supporting/ | **YES** | Post-freeze proof sketches |
| templates/ | YES | LaTeX formatting discovery |
| output/ | YES | Build artifacts |

---

## IP leakage assessment

### LEAKED (still in public repo)

1. **figures/fig3a-branch-fixation.mmd** - Branch-to-fixation collapse pattern
   - Discovery: how human fixation selects admissible branches
   - Status: **POST-FREEZE IP - NOT IN FROZEN MANUSCRIPT**

2. **figures/fig5-knowledge-api.mmd** - Knowledge API architecture
   - Discovery: transcript-to-claim pipeline with inception points
   - Status: **POST-FREEZE IP - NOT IN FROZEN MANUSCRIPT**

3. **supporting/appendix-a-proofs.md** - Formal proof sketches
   - Discovery: mathematical formalization of slop inadmissibility
   - Status: **POST-FREEZE IP**

4. **supporting/appendix-b through f** - All appendices
   - Discovery: validation, transcripts, streams, methods, claim checklist
   - Status: **POST-FREEZE IP**

5. **TYPESET.md** - Typesetting governance
   - Discovery: PDF publishing workflow
   - Status: **POST-FREEZE IP**

6. **scripts/build_pdf.sh** - Build tooling
   - Discovery: mermaid-to-PDF pipeline
   - Status: **POST-FREEZE IP**

### CLEAN (no leakage)

1. **manuscript.md** - Reverted to 447bf45
   - Contains only frozen-window evidence
   - 5 inline mermaid diagrams (not external figures)
   - No appendices, no post-freeze episodes
   - Status: **COMPLIANT**

2. **CANON.md, VOCAB.md, README.md, PAPER.md**
   - Core triad files
   - Status: **COMPLIANT** (check for post-freeze edits needed)

---

## Recommendations

### Option A: Remove all post-freeze IP from public repo

Delete from paper repo:
- figures/ (entire directory)
- supporting/ (entire directory)
- scripts/ (entire directory)
- templates/ (entire directory)
- output/ (entire directory)
- TYPESET.md

Keep only:
- manuscript.md (reverted)
- CANON.md, VOCAB.md, README.md, PAPER.md
- LICENSE, NOTICE, .gitignore

### Option B: Move post-freeze IP to private scope

Create a private `publishing` or `typeset` repo to hold:
- Build scripts
- Figure sources
- Supporting materials
- PDF outputs

Public paper repo contains only the frozen manuscript.

### Option C: Declare new freeze (v0.1.1)

If the post-freeze discoveries should become public:
1. Run them through canonification process (patented)
2. Declare new freeze with expanded evidence window
3. Update manuscript to reference new evidence

---

## Verdict

**IP HAS LEAKED.** The public paper repo contains significant post-freeze
discoveries in figures/, supporting/, scripts/, and TYPESET.md.

The manuscript.md itself is now clean (reverted), but the surrounding
artifacts expose post-freeze IP that should go through canonification
before public release.

---

## Evidence references (LEDGER)

- paper:0ee1970 - freeze state (4 files)
- paper:da477ea - current HEAD after reversion
- paper:447bf45 - manuscript source for reversion
- ep156 - violation that triggered this audit

---

## Notes

The manuscript content is protected. The tooling and methodology discovered
during publishing is exposed. Decision needed on how to handle.

---

**This file is a non-authoritative template.**
**It defines structure only and confers no governance, enforcement, or interpretive meaning.**
