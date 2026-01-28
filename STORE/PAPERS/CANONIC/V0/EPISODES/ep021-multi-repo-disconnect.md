# Episode 021: Multi-Repo Disconnect

**Date:** 2026-01-08
**Agent:** Canon Agent

**Type:** Unknown
**Participants:** Unknown
## The Session

User requested: “all need atomic commits. intelligent. why the disconnect? investigate and document in paper episode. follow the canons.” The request came after reviewing all four repositories (`canonic`, `machine`, `writing`, `paper`) and noticing inconsistent states across them. This episode captures that investigation, which starts from the PAPER specification and works backward through the rest of the stack.

## Investigation

We treated git status as the primary sensor. Running `git status -sb` in each repo showed:

- `canonic`: clean working tree, branch ahead of `origin/main` by four commits (latest: `17ff36b Revert "Canonify vocabulary references"`). No local edits to stage.
- `machine`: local modifications in `MACHINE.md`, `01-AGENTS.md`, `02-PROTOCOLS.md`, `04-LEARNINGS.md`, `CANON.md`, `README.md`, and the entire `tools/` subtree (`CANON.md`, `README.md`, `canonic_validator.py`, `fsm_status.py`, `trace_asset.py`). Branch ahead by four commits (`0c6214f`, `e17ac8f`, `75bd024`, `828551a`), pointing to ongoing governance and tooling refinements.
- `writing`: single tracked modification in `WRITING.md` plus a commit history that raised the SPEC (`5337a02 Canonify WRITING.md as human-iterated SPEC` at the head). Branch ahead by five commits, signalling continued work on the writing FSM and tools.
- `paper`: branch ahead by 25 commits, with an untracked episode `episodes/020-canon-bloat-canonical-locality.md`. The new episode documents the canonical locality refactor and the agent self-check violation discussed earlier.

Running `git log` in each repository confirmed the divergence in focus: `canonic` stabilizing, `machine` expanding agent behavior and tooling, `writing` refreshing its SPEC, and `paper` chronicling episodes. Yet the working-tree inconsistencies (modifications only in three of the four repos plus `paper`’s untracked episode) created the “disconnect” the user reported—there is no single atomic action that touches every repo simultaneously, so each repo drifts at its own pace unless we coordinate.

## Findings

1. **Asymmetric drift**: `canonic` has no pending edits while the others do, so simply running `git add -A` from the CANONIC repo does nothing—source of the user’s “why the disconnect?” observation.
2. **Incomplete staging**: `paper` contained an untracked episode because documentation is still being written; it never made it into `git add -A` when the user ran it from `canonic` (the command scopes to the current repo).
3. **Cross-repo coordination gap**: The producer/consumer rhythm (Canonify → Apply/Fix) spans several repositories, but there was no simultaneous commit signal linking the outstanding work in `machine`, `writing`, and `paper`. This makes the stack look disconnected even though each repo individually follows its canonical plan.

## Why This Matters

The PAPER specification demands that every claim still traces to git history. When the working trees are misaligned, the evidence trail splits: you cannot point to a single atomic change that spans the stack. That is the disconnect. Documenting it here preserves the “why” for future episodes, fulfilling the metacircular requirement (“The paper discovers best practices by analyzing its own writing”) while also reminding future agents to coordinate atomic commits across repos.

## Next Steps

1. **Canonical checklist per repo**: Run `git status` and `git log -n 3 --oneline` in each repository to verify whether the work in progress belongs to the current producer/consumer cycle.
2. **Episode linking**: Reference this episode number when making future commits that stitch those repositories together, e.g., include “Episode 021” in the commit message or PR description so reviewers know this work is a cross-repo investigation.
3. **Atomic commits**: When ready to push, create targeted commits per repository using the correct prefix (`Canonify …` for governance updates in `canonic`/`machine`, `Apply …` or `Fix …` for implementation changes in `writing`/`paper`). Document how each commit addresses the disconnect.

End of Episode 021.

## Key Assets Discovered

Not recorded in original episode.

## Violations Detected and Fixed

Not recorded in original episode.

## Git Signal

Not recorded in original episode.

## The Insight

Not recorded in original episode.

**Status:** Not recorded in original episode.
