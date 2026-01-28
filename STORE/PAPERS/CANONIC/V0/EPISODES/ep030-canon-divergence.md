# Episode 030: CANON Divergence - Wrong Pattern Applied

**Date:** 2026-01-08
**Agent:** Canon Agent

**Type:** Unknown
**Participants:** Unknown
## The Session

User: "hold on. why are you making an episode. this is the CANON for paper. why did you diverge from the CANON?"

**The Violation:**

Created episodes using wrong pattern:
- Episode format: Direct narrative
- Commit format: Free text
- Repo coordination: PAPER only

**The Correct Pattern (from CANON.md):**

1. **Episode Alignment Constraint:**
   > "Every commit message must mention the agent... and the same episode number referenced in the linked episode file."
   > Format: `Episode 0XX – Agent [role] …`

2. **Cross-Repo Atomic Coordination:**
   > "Ensure each repo records its own commit referencing the same episode"

3. **Proper Git Compliance:**
   > "Issue a redo commit (never rewriting history) when earlier evidence lacks the required agent/episode signal"

## What I Did Wrong

| CANON Requirement | What I Did |
|-------------------|------------|
| Episode 0XX format | Just "Episode 030" without proper header |
| `Episode 0XX – Agent [role] …` commit | Used free-text commit message |
| Cross-repo commits | Only touched PAPER repo |
| Agent role mentioned | Only mentioned "USER" in body |
| Episode number in all repos | No commits in canonic/machine/writing |

## The Correct Pattern

**Commit format:**
```
Episode 030 – Agent USER Canonify agent-model evaluation constraint

- Canonify: evaluate best AGENT for CANONIC MACHINE WRITING PAPER
- Criteria: Canon compliance, git signal quality, VOCAB discipline
- Format: Episode 0XX – Agent [role] …
```

**Cross-repo coordination:**
```
canonic: Episode 030 – Producer Canonify evaluation criteria
machine: Episode 030 – Consumer Apply evaluation framework
writing: Episode 030 – Consumer Apply evaluation criteria  
paper: Episode 030 – Agent USER Document episode and criteria
```

## Corrective Action

1. **Don't rewrite history** - Redo commits only
2. **Follow format**: `Episode 0XX – Agent [role] …`
3. **Coordinate across repos** - Each affected repo must commit
4. **Include agent role** - Producer, Consumer, USER

---

**Status:** CANON divergence documented, redo pattern canonified

## Key Assets Discovered

Not recorded in original episode.

## Violations Detected and Fixed

Not recorded in original episode.

## Git Signal

Not recorded in original episode.

## The Insight

Not recorded in original episode.
