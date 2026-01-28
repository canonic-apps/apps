# Episode 106: Canon Maturity and Autocommit Threshold

**Date:** 2026-01-11
**Type:** Analysis
**Participants:** Human (Governor General), AI (Codex)
**Agent:** Codex

---

## The Session

You clarified that CANON requires explicit approval for canon commits and said to keep that until the machine canon stabilizes by git signal. We analyzed producer vs consumer signals across repos as a maturity proxy.

## Key Assets Discovered

- Producer/consumer ratios can indicate canon maturity and readiness for autocommit.

## Violations Detected and Fixed

None.

## Git Signal

Producer and consumer proxies (commit message keywords):
- Producer = "Canonify"
- Consumer = "Apply" and "Redo"

Counts by repo (total | canonify | apply | redo | episode):
- canonic: 133 | 71 | 10 | 2 | 15
- machine: 77 | 24 | 27 | 1 | 2
- os: 11 | 4 | 0 | 1 | 0
- writing: 42 | 11 | 9 | 1 | 3
- git: 11 | 3 | 0 | 1 | 0
- paper: 136 | 48 | 32 | 4 | 53

## The Insight

Autocommit should be enabled only after sustained consumer-dominant signals. Current ratios show producer-heavy activity in several repos (canonic, os, git), so approval remains required until stabilization is evident in git signal.

**Status:** Recorded.
