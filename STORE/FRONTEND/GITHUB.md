# FRONTEND ← GITHUB — DEPLOYMENT

inherits: /CANONIC/STORE/FRONTEND/

---

## Axiom

**GitHub Pages is the CANONVERSE's CDN. Deploy from branch. No Actions for static content.**

---

## Repository Naming

| Pattern | Example | Purpose |
|---------|---------|---------|
| `{org}.github.io` | canonic-apps.github.io | Primary frontend |
| `{org}/{repo}` | canonic-apps/canonic | Source code |

**Constraint:** Each org has ONE `{org}.github.io` repository. It serves at `https://{org}.github.io/`.

---

## Branch Strategy

```
main ──► GitHub Pages (direct deploy)

NO secondary branches for static sites.
NO GitHub Actions for pure HTML.
```

**Why branch deploy over Actions:**
- Simpler (no workflow YAML)
- Faster (no build step)
- Debuggable (what you push is what serves)
- Cacheable (GitHub CDN handles it)

---

## Directory Structure

```
{org}.github.io/
├── .nojekyll              ← REQUIRED: disables Jekyll
├── index.html             ← / (root)
├── STORE/
│   ├── index.html         ← /STORE/
│   ├── APPS/
│   │   └── index.html     ← /STORE/APPS/
│   ├── BOOKS/
│   │   └── index.html     ← /STORE/BOOKS/
│   └── PAPERS/
│       └── index.html     ← /STORE/PAPERS/
├── CV/
│   └── index.html         ← /CV/
├── DOMAIN/
│   └── index.html         ← /DOMAIN/
└── assets/
    ├── style.css          ← Shared styles
    └── nav.js             ← Navigation script
```

**Critical:** Every navigable path MUST have an `index.html`.

---

## .nojekyll

The `.nojekyll` file MUST exist at repository root.

```bash
touch .nojekyll
```

**Why:**
- Prevents Jekyll processing
- Allows underscored directories (`_layouts` etc.)
- Faster deploy (no build)
- Predictable behavior

---

## Deployment Flow

```
LOCAL                    REMOTE                   LIVE
canonic-apps.github.io   github.com/canonic-apps  canonic-apps.github.io
      │                  canonic-apps.github.io         │
      │                         │                       │
      └── git push ────────────►│                       │
                                │                       │
                          GitHub Pages                  │
                          (auto deploy)                 │
                                │                       │
                                └───────────────────────►
```

---

## Configuration

### Repository Settings

1. **Settings → Pages**
2. **Source:** Deploy from branch
3. **Branch:** main
4. **Folder:** / (root)

```
┌─────────────────────────────────────┐
│ Build and deployment                │
├─────────────────────────────────────┤
│ Source: Deploy from a branch        │
│ Branch: main       Folder: / (root) │
└─────────────────────────────────────┘
```

### Verification

```bash
# Check live status
curl -I https://{org}.github.io/

# Check specific path
curl -I https://{org}.github.io/STORE/BOOKS/

# Expected: HTTP/2 200
# Failure:  HTTP/2 404
```

---

## Troubleshooting

### 404 on Nested Paths

| Symptom | Cause | Fix |
|---------|-------|-----|
| `/STORE/` works, `/STORE/BOOKS/` 404s | Missing index.html | Add `/STORE/BOOKS/index.html` |
| All paths 404 | Pages not enabled | Enable in Settings → Pages |
| Intermittent 404s | CDN caching | Wait 10 minutes, or add empty commit |
| 404 after Actions | Wrong source | Switch to "Deploy from branch" |

### Force Refresh

```bash
# Empty commit to force re-deploy
git commit --allow-empty -m "Force refresh"
git push

# Or touch a file
echo "<!-- $(date) -->" >> index.html
git add -A && git commit -m "Refresh" && git push
```

### Verify Files in Git

```bash
# Check files are tracked
git ls-files | grep STORE/BOOKS

# Check remote matches local
git diff origin/main
```

---

## Generator Integration

The FRONTEND generator produces GitHub-ready output:

```bash
# Generate frontend
python3 generator.py configs/apps.json /tmp/canonic-apps

# Add .nojekyll
touch /tmp/canonic-apps/.nojekyll

# Deploy
cd /tmp/canonic-apps
git init
git add -A
git commit -m "Generated frontend"
git remote add origin https://github.com/canonic-apps/canonic-apps.github.io.git
git push -u origin main --force
```

---

## Subpages

For nested paths, add `subpages` to config:

```json
{
    "title": "CANONIC Apps",
    "subpages": {
        "STORE": {
            "title": "STORE",
            "heading": "STORE",
            "sections": []
        },
        "STORE/BOOKS": {
            "title": "BOOK STORE",
            "heading": "BOOK STORE",
            "sections": []
        },
        "STORE/APPS": {
            "title": "APP STORE",
            "heading": "APP STORE",
            "sections": []
        }
    }
}
```

---

## Invariants

1. **Repository name MUST be `{org}.github.io`** for primary frontend
2. **Source MUST be "Deploy from branch"** (not Actions)
3. **`.nojekyll` MUST exist** at root
4. **Every navigable path MUST have `index.html`**
5. **No build steps** — pure static HTML/CSS/JS
6. **Branch is `main`** — no `gh-pages` branch

---

## Reserved Names

Certain directory names may cause issues with GitHub Pages CDN caching. Avoid:

| Name | Issue | Alternative |
|------|-------|-------------|
| `STORE` | Nested paths may 404 despite files existing | `CATALOG` |
| `store` | Same as STORE (case-insensitive) | `catalog` |
| `REGISTRY` | Windows Registry connotation, avoid | `CATALOG` |

**Discovery:** In January 2026, the `/STORE/BOOKS/` path on canonic-apps.github.io returned 404 despite files existing in git. Renaming to `/CATALOG/BOOKS/` resolved the issue.

---

## Red Lines

- NEVER use GitHub Actions for static HTML
- NEVER rely on Jekyll processing
- NEVER create paths without index.html
- NEVER switch between Actions/Branch deploy mid-project
- AVOID directory names that may be CDN-reserved (STORE, API, etc.)

---

## Series

- [CANON.md](CANON.md) — Design specification
- [BACKEND.md](BACKEND.md) — Generator coordination
- **GITHUB.md** — Deployment (this file)

---
