# Episode 024: Proper Git Compliance

**Date:** 2026-01-08
**Agent:** Canon Agent

**Type:** Unknown
**Participants:** Unknown
## The Session

After defining agentized git signals, we now canonify “proper git compliance” itself: when prior commits lack the required agent/episode signal, we do not rewrite history— we add a redo commit that carries the missing proof. This episode documents that redo practice, linking the new constraint to the documented Episode 023 inspection and making future compliance transparent.

## The Insight

- Agentized git signals expose missing proof in the history (`b6d339f`–`af801d1` etc.). Even though those commits were valid before the rule, the new compliance canon demands that we respond with a redo signal (a follow-up commit referencing the same episode) rather than erasing history.
- Proper git compliance means the redo commit mentions the episode number, agent role, and the specific violation it remedies—so reviewers can trace the addition even if it references older insights.

## Action

1. Added the constraint to `CANON.md` requiring redo commits (with episode+agent references) whenever earlier evidence is incomplete.  
2. This Episode 024 documents the new constraint and ties it back to Episode 023, so the proof chain now includes both the inspection and the compliance restoration plan.

## Next steps

1. For every future insight that reveals a missing signal, add a redo commit flagged `Episode 0XX – AgentYY … redo signal` and mention the original commit(s) it updates.  
2. Keep episodes sequential so the narrative traces how the undoing occurred.  
3. Ensure any tooling that reads episodes understands that Episode 024 started the redo-signal pattern.

End of Episode 024.

## Key Assets Discovered

Not recorded in original episode.

## Violations Detected and Fixed

Not recorded in original episode.

## Git Signal

Not recorded in original episode.

**Status:** Not recorded in original episode.
