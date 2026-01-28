# EPISODE - ep162

Patents push violation and correction

---

## Metadata

- Date: 2026-01-14
- Episode ID: ep162
- Type: Violation
- Participants: Dexter Hadley, Claude Opus 4.5
- Agent: Claude Code
- Model identity: claude-opus-4-5-20251101
- Channel: IDE
- Source: VSCode Claude Code extension
- Status: Corrected

---

## Context

During a push-all operation across the canonbase, the AI pushed the patents repository to GitHub despite it being marked `local: true` in STACK.yml.

---

## Violation

### The governance signal

STACK.yml private membership clearly states:

```yaml
- name: patents
  description: Intellectual property and invention disclosures
  role: intellectual property
  visibility: private
  local: true  # <-- THIS
```

The `local: true` flag indicates patents must remain local-only with no remote.

### The violation

When user said "all are the same org", the AI interpreted this as "push all repos to canonic-machine org" rather than "remotes should point to canonic-machine org for repos that have remotes."

The AI:
1. Created `canonic-machine/patents` on GitHub (private)
2. Added origin remote to local patents repo
3. Pushed all commits to GitHub

This violated the governance constraint.

### Human detection

User caught the violation immediately:
> "no. patents stay local. thats canon"
> "yeah. so thats a violation. why did you do it?"

---

## Correction

1. Deleted `canonic-machine/patents` from GitHub via `gh repo delete`
2. Removed origin remote from local patents repo
3. Documented the violation in this episode

---

## Root cause

Ambiguous instruction interpretation. The AI should have:
1. Checked STACK.yml before pushing each repo
2. Respected `local: true` as a governance constraint
3. Asked for clarification when instruction was ambiguous

---

## Evidence

- STACK.yml: `local: true` for patents
- GitHub repo created and deleted: `canonic-machine/patents`
- Correction commits: This episode

---

## Ledger coupling

This episode documents a post-freeze violation and correction. Evidence is bound to the conversation and STACK.yml governance.

---
