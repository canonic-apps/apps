# FRONTEND ← BACKEND — COORDINATION

inherits: /CANONIC/LANGUAGE/TEMPLATES/

---

## Axiom

**FRONTEND consumes BACKEND. BACKEND produces FRONTEND.**

```
BACKEND (generator.py)  →  CONFIG (*.json)  →  FRONTEND (index.html)
     ↓                          ↓                    ↓
  Producer               Specification            Consumer
```

---

## Flow

```
canonic-apps/STORE/FRONTEND/
├── CANON.md              ← FRONTEND spec
├── BACKEND.md            ← this file (coordination)
├── generator.py          ← BACKEND producer
├── configs/
│   ├── foundation.json   ← org config
│   ├── apps.json
│   ├── domains.json
│   └── dexter.json
└── README.md
         ↓
    python3 generator.py configs/{org}.json /tmp/{org}-frontend
         ↓
    {org}.github.io/index.html  ← FRONTEND consumer
```

---

## Contracts

### BACKEND → FRONTEND

| BACKEND Produces | FRONTEND Consumes |
|------------------|-------------------|
| `index.html` | Pages |
| Design tokens in HTML | Styling via style.css |
| nav.js script tag | Navigation |
| Logo URL | Hero image |

### CONFIG → BOTH

| Field | Type | Required |
|-------|------|----------|
| title | string | yes |
| heading | string | yes |
| tagline | string | yes |
| badge | string | yes |
| sections | array | yes |
| sections[].title | string | yes |
| sections[].subtitle | string | no |
| sections[].type | grid\|timeline\|flow | yes |
| sections[].items | array | yes |
| footer_links | array | yes |

---

## Deployment

```bash
# 1. Edit config
vim configs/{org}.json

# 2. Generate
python3 generator.py configs/{org}.json /tmp/{org}-frontend

# 3. Push
cd /tmp/{org}-frontend
git add -A && git commit -m "Regenerated" && git push
```

---

## Assets

FRONTEND depends on Foundation assets:

| Asset | URL | Source |
|-------|-----|--------|
| style.css | canonic-foundation.github.io/assets/style.css | FRONTEND CANON tokens |
| nav.js | canonic-foundation.github.io/assets/nav.js | BACKEND navigation |
| logo | raw.githubusercontent.com/.../logo-business.svg | TIERS assets |

---

## Invariants

- BACKEND MUST NOT modify FRONTEND spec.
- FRONTEND MUST inherit from Foundation assets.
- CONFIG MUST validate against CANON.
- Generator MUST be idempotent.

---
