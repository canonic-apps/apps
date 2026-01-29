# FRONTEND

inherits: /CANONIC/

---

## Overview

FRONTEND is the browser rendering layer for the CANONVERSE.

```
CANON.md     → Specification (what)
BACKEND.md   → Coordination (how)
generator.py → Producer (build)
configs/     → Instances (who)
```

---

## Quick Start

```bash
# Generate a frontend
python3 generator.py configs/foundation.json /tmp/foundation

# Deploy
cd /tmp/foundation
git init && git add -A && git commit -m "Generated"
git remote add origin https://github.com/{org}/{org}.github.io.git
git push -u origin main
```

---

## Files

| File | Purpose |
|------|---------|
| [CANON.md](CANON.md) | FRONTEND specification |
| [BACKEND.md](BACKEND.md) | BACKEND ↔ FRONTEND coordination |
| [GITHUB.md](GITHUB.md) | GitHub Pages deployment |
| [generator.py](generator.py) | HTML generator |
| configs/*.json | Org-specific configs |

---

## Live Sites

| Site | URL |
|------|-----|
| FOUNDATION | https://canonic-foundation.github.io |
| APPS | https://canonic-apps.github.io |
| DOMAINS | https://canonic-domains.github.io |
| DEXTER | https://hadleylab-dexter.github.io |

---
