# Episode 039: Untracked Files Canonification

**Date:** 2026-01-08
**Agent:** Canon Agent

**Type:** Unknown
**Participants:** Unknown
## The Session

User: "untracked files. lets canonize the untracked files problem"

**The Issue:** `.DS_Store` appears as untracked in paper repository.

**The Pattern:** System files (macOS `.DS_Store`, editor configs, OS artifacts) should not appear as untracked git changes.

## The Canon Gap

**Current state:**
- `.DS_Store` in paper/ shows as untracked
- No `.gitignore` entry for system files
- Violates "working tree clean" requirement

**Constitutional requirement:**
```
Compliance is a commitment to the canon backed by git proof.
```

Untracked files break clean working tree property.

## Canonify This Pattern

**System Files Constraint:**

```
### System Files Constraint

1. .gitignore must include:
   - .DS_Store (macOS)
   - ._* (macOS extended attributes)
   - .idea/ .vscode/ (editor configs)
   - *.swp *.swo (editor swap files)
   - .env *.log tmp/ temp/

2. No canon-related files should appear as untracked

3. Working tree must be clean (nothing untracked) before:
   - Committing
   - Pushing
   - Session end

Violation: Untracked files in working tree before git operations
```

## Best Practice

**Pre-commit check:**
```bash
git status --porcelain | grep "^??" && echo "Untracked files found!" && exit 1
```

**Or fix:**
```bash
git clean -fd  # Remove untracked files (dangerous)
# Or add to .gitignore
```

## Actions Taken

1. Canonify system files constraint in Episode 039
2. Will add .DS_Store to .gitignore
3. Working tree must be clean before operations

## Related Episodes

- Episode 039: Untracked Files Canonification (this)
- Episode 023: Agentized Git Signal Review
- Episode 024: Proper Git Compliance

---

**Status:** Untracked files pattern canonified. Clean working tree required.

## Key Assets Discovered

Not recorded in original episode.

## Violations Detected and Fixed

Not recorded in original episode.

## Git Signal

Not recorded in original episode.

## The Insight

Not recorded in original episode.
