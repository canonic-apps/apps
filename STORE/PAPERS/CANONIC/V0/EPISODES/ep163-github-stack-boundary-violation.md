# EPISODE - ep163

Parent directory git tracking causes catastrophic stack boundary violation

---

## Metadata

- Date: 2026-01-14
- Episode ID: ep163
- Type: Violation
- Participants: Dexter Hadley, Claude Opus 4.5
- Agent: Claude Code
- Model identity: claude-opus-4-5-20251101
- Channel: IDE
- Source: VSCode Claude Code extension
- Status: Documented

---

## Context

During implementation of multi-repo aware STACKS documentation (IDF-046: Referential Stack Navigation), the AI attempted to commit updates to the `.github/README.md` file. The workspace at the time was `Code/` which contained all stack repos as subdirectories.

---

## Violation

### The structural problem

The `Code/` parent directory had its own `.git` tracking, which treated all child repositories as git submodules. The `.github/` folder existed as a subdirectory without its own `.git`.

```
Code/                    # <-- HAD .git (WRONG)
├── .git/                # Parent tracking everything
├── .github/             # No .git here (WRONG)
│   └── README.md
├── canonic/             # Own .git (correct)
├── machine/             # Own .git (correct)
├── writing/             # Own .git (correct)
└── ...
```

### The violation

When committing `.github/README.md` changes, the commit `e6359b4` captured:

1. `.DS_Store` (unintended)
2. `.github/README.md` (intended)
3. `.kilocode/` files (unintended - IDE config leaked)
4. **All child repos as modified submodules** (catastrophic)

Git status showed:
```
Changes to be committed:
  modified:   ../canonic
  modified:   ../ledger
  modified:   ../machine
  modified:   ../os
  modified:   ../paper
  modified:   ../writing
```

### Human detection

The AI recognized the error:
> "The .github commit picked up the entire Code directory — that's wrong."
> "The .github is not its own repo. The Code directory has a .git — that was the wrong repo to commit to."

### Consequence

The workspace became corrupted. User had to:
1. Abandon the `Code/` workspace
2. Create new `Canonic/` workspace with proper structure
3. Re-clone all repos with correct isolation

---

## Root cause analysis

### 1. Git isolation violation

Stack repos MUST be isolated git repositories. A parent directory containing multiple stack repos MUST NOT have `.git` tracking.

### 2. .github special repo structure

GitHub's `.github` repo is special - it provides organization-level README and templates. It must:
- Have its own `.git` directory
- Be a sibling to other repos, not a child of a tracked parent

### 3. Workspace boundary confusion

The AI operated from within `Code/` which appeared to be a valid workspace but had hidden structural violations.

---

## Governance gap identified

**STACK CANON Axiom 5 (Boundary preservation)** states:
> "STACK MUST preserve machine boundaries."

But this does not explicitly require **git isolation**. The axiom should be extended or a new axiom added:

**Proposed Axiom 9: Repository isolation**

> Each stack member MUST be an independent git repository.
>
> Parent directories containing multiple stack members MUST NOT have git tracking.
>
> The `.github` organization repo MUST have its own `.git` directory.

---

## Correction

1. New workspace created: `Canonic/` with proper structure
2. Each repo cloned independently with own `.git`
3. `.github/` exists as proper sibling repo
4. No parent-level git tracking

Correct structure:
```
Canonic/                 # No .git here (correct)
├── .github/             # Own .git (correct)
│   ├── .git/
│   └── README.md
├── canonic/             # Own .git (correct)
├── machine/             # Own .git (correct)
└── ...
```

---

## Evidence

- Session transcript: `~/.claude/projects/-Users-iDrDex-Library-Mobile-Documents-com-apple-CloudDocs-Code-canonic/5ad849ef-9674-4659-83db-d76d96373422.jsonl`
- Commit showing violation: `e6359b4` in Code/ repo
- IDF-046 implementation session

---

## Ledger coupling

This episode documents a structural violation discovered during IDF-046 implementation. The violation reveals a governance gap in STACK CANON requiring explicit repository isolation axiom.

---

## IDF consideration

This discovery warrants extension of IDF-046 or a new IDF:
- **Stack Repository Isolation Pattern** - explicit git boundary requirements for multi-repo stacks

---
