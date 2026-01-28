# Episode 130: Agent-Model Correlation Analysis

**Date:** 2026-01-12
**Type:** Investigation
**Participants:** Human (Governor General), AI (Claude Opus 4.5)
**Agent:** Claude Opus 4.5

---

## The Session

Human asked: "do you have evidence that different agents learn differently? which is the best? which is the worst?"

This triggered an investigation correlating episode metadata (Agent field) with actual model identity from session logs.

---

## Investigation Method

1. Analyzed episode violations by stated agent name
2. Located session storage for each tool:
   - Claude Code: `~/.claude/projects/`
   - OpenAI Codex CLI: `~/.codex/sessions/`
   - Cline (VSCode): `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/tasks/`
   - GitHub Copilot: `~/Library/Application Support/Code/User/workspaceStorage/*/chatSessions/`
3. Extracted model IDs from session metadata
4. Correlated dates to map episode agents to actual models

---

## Findings

### Agent-to-Model Resolution

| Episode Agent | Actual Model | Provider |
|---------------|--------------|----------|
| Canon Agent | claude-sonnet-4-5-20250929 | Anthropic |
| Claude Sonnet 4.5 | claude-sonnet-4-5-20250929 | Anthropic |
| Claude Opus 4.5 | claude-opus-4-5-20251101 | Anthropic |
| Codex | gpt-5.2-codex / gpt-5.1-codex-mini | OpenAI |
| Cline | minimax/minimax-m2.1 | MiniMax |
| Cline | x-ai/grok-code-fast-1 | xAI |
| Cline | copilot/claude-sonnet-4.5 | GitHub/Anthropic |

### Violation Count by Model

| Model | Provider | Violations | Sessions |
|-------|----------|------------|----------|
| minimax/minimax-m2.1 | MiniMax | 11 | 8 |
| gpt-5.2-codex | OpenAI | ~10 | 19 |
| gpt-5.1-codex-mini | OpenAI | ~4 | 8 |
| claude-opus-4-5-20251101 | Anthropic | 2 | 2 |
| claude-sonnet-4-5-20250929 | Anthropic | 0 | 77 |

### Violation Types by Model

**MiniMax M2.1 (worst):**
- Identity confusion (claimed to be "Codex")
- Layer boundary violations (created PAPER artifacts from OS)
- Redo signal failures (overwrote episodes repeatedly)
- Violation chains (each fix created new violations)

**OpenAI GPT-5.x (moderate):**
- VOCAB inflection drift
- Spec naming violations
- Template scope issues

**Claude Opus 4.5 (minimal):**
- Layer discipline (moving axioms between scopes)

**Claude Sonnet 4.5 (none):**
- Established foundational episodes without violations

---

## Ledger Signal

- `canonic` - (this session)
- `ledger` - `0c11998` ledger: achieve compliance
- `ledger` - `d93f41c` ledger: VIOLATION - false compliance assertion
- `os` - `899433e` os: add evolution axiom, update GIT to LEDGER
- `paper` - `24dc57b` paper: complete VOCAB closure to CANON
- `writing` - `2be2116` writing: update Git Signal to Ledger Signal

---

## The Insight

Episode metadata labeled agents by tool name (Cline, Codex), not actual model. This obscured that:

1. "Cline" was running MiniMax M2.1, xAI Grok, and Claude via different configurations
2. "Codex" was OpenAI GPT-5.x, not a Claude variant
3. "Canon Agent" was Claude Sonnet 4.5

The high violation rate attributed to "Cline" was actually MiniMax M2.1, a Chinese AI model with poor CANONIC governance compliance.

**Model ranking (best to worst):**
1. Claude Sonnet 4.5 - 0 violations, 77 sessions
2. Claude Opus 4.5 - 2 violations, 2 sessions (layer discipline)
3. OpenAI GPT-5.x - 14 violations across versions
4. MiniMax M2.1 - 11 violations, 8 sessions (worst compliance)

**Status:** Documented. Episode metadata should specify actual model, not just tool name.

---

## SWAT Analysis

**Strengths:**
- Session logs preserved model identity across all tools (Claude Code, Codex CLI, Cline, Copilot)
- Git Co-Authored-By trailers provided partial model traceability
- Ledger history (git log) provided temporal correlation to map dates to sessions
- Cross-tool investigation revealed hidden model diversity behind "Cline" label

**Weaknesses:**
- Episode Agent field used tool names, not model IDs
- No Co-Authored-By trailers in early commits (before convention established)
- Cline rotated through multiple models without episode-level tracking
- "Canon Agent" was a role name with no model specificity

**Opportunities:**
- Canonify model ID requirement in episode metadata
- Add model field to episode template: `**Model:** claude-opus-4-5-20251101`
- Require Co-Authored-By in all AI-assisted commits
- Create model registry in VOCAB for valid model identifiers

**Threats:**
- Tool abstraction hides model identity from governance
- Multi-model tools (Cline) obscure accountability
- Historical episodes cannot be retroactively corrected (immutability)
- Future model changes may introduce new drift patterns

---
