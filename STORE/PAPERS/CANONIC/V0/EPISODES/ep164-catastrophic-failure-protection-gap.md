# EPISODE - ep164

Catastrophic failure protection governance gap identified

---

## Metadata

- Date: 2026-01-14
- Episode ID: ep164
- Type: Discovery
- Participants: Dexter Hadley, Claude Opus 4.5
- Agent: Claude Code
- Model identity: claude-opus-4-5-20251101
- Channel: IDE
- Source: VSCode Claude Code extension
- Status: Documented

---

## Context

After ep163 (stack boundary violation causing workspace corruption), human asked:
> "do we have a meta-canon protecting catastrophic failure"

Investigation revealed a governance gap.

---

## Investigation

Searched for catastrophic failure, recovery, resilience, backup terms across:
- `/canonic/CANON.md` (root)
- `/stack/CANON.md`
- `/os/CANON.md`
- `/ledger/CANON.md`

**Result:** No explicit catastrophic failure protection axioms found.

---

## Current Protection (Implicit)

| Scope | Axiom | Protection |
|-------|-------|------------|
| LEDGER | Immutability | History can't be altered (but can be lost) |
| OS | Unpushed commit prohibition | Commits pushed to remote (distributed backup) |
| TRANSCRIPT | Mirroring | Fluid transcripts mirrored locally |
| STACK | Repository isolation | IDF-047, prevents cross-repo corruption |

---

## Missing Protection

1. **Multi-site backup requirement** - No axiom requiring backups beyond git remote
2. **Recovery procedures** - No canonified recovery protocol
3. **Workspace structure validation** - No axiom preventing parent-level git (ep163 root cause)
4. **Session preservation** - IDE sessions live in tool-specific caches, not governed

---

## Proposed Axioms

### Stack Repository Isolation (proposed Axiom 9)

Already discovered in ep163/IDF-047:
> Parent directories containing stack members MUST NOT have git tracking.
> Each stack member MUST be an independent git repository.

### Evidence Resilience (proposed for OS or LEDGER)

> Governed artifacts MUST be recoverable from at least two independent sources.
> - Git remote provides one source
> - Local filesystem provides second source
> - Transcript mirrors provide evidence backup

### Workspace Validation (proposed for MACHINE)

> Before session start, MACHINE SHOULD validate:
> - No parent-level .git encompassing stack members
> - All stack members have independent .git
> - Required visibility constraints (local repos have no remote)

---

## Evidence

- ep163: Stack boundary violation
- IDF-047: Stack repository isolation
- TRANSCRIPT CANON Axiom 4: Mirroring for resilience (just created)
- tx010-tx015: Transcript records for all discovered agents/models

---

## Status

Governance gap documented. Proposed axioms require human decision on scope placement:
- Repository isolation → STACK CANON Axiom 9
- Evidence resilience → OS or LEDGER
- Workspace validation → MACHINE

---
