# PYTHON — Code Governance SaaS

inherits: /CANONIC/APPS/STORE/BYOL
tier: 63

---

## Axiom

**Python compliance without a repo. Define. Submit. Validate.**

---

## Service

### API

```bash
# Validate Python code against constraints
curl -X POST https://api.canonic.dev/python/validate \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "code": "def foo(): pass",
    "constraints": [
      "Functions MUST have docstrings",
      "Functions MUST have type hints"
    ]
  }'
```

### Response

```json
{
  "status": "FAIL",
  "tier": 63,
  "violations": [
    {"line": 1, "rule": "Functions MUST have docstrings", "found": "def foo(): pass"},
    {"line": 1, "rule": "Functions MUST have type hints", "found": "def foo(): pass"}
  ],
  "passed": 0,
  "failed": 2
}
```

---

## Default Constraints

ENTERPRISE tier includes:

```markdown
- Functions MUST have docstrings
- Functions MUST have type hints
- Classes MUST have __init__ docstring
- Imports MUST be at top of file
- No hardcoded credentials
- No eval() or exec()
- Exception handlers MUST NOT be bare
```

---

## Custom Constraints

Add your own:

```json
{
  "constraints": [
    "Functions MUST NOT exceed 50 lines",
    "Variables MUST use snake_case",
    "Constants MUST use UPPER_CASE"
  ]
}
```

---

## Pricing

| Tier | Validations/mo | Custom Rules | Price |
|------|----------------|--------------|-------|
| COMMUNITY | 100 | 0 | Free |
| CLOSURE | 1,000 | 5 | $29/mo |
| BUSINESS | 10,000 | 25 | $199/mo |
| ENTERPRISE | Unlimited | Unlimited | $999/mo |

---

## Integration

### GitHub Action

```yaml
- uses: canonic/python-validate@v1
  with:
    token: ${{ secrets.CANONIC_TOKEN }}
    tier: 63
```

### Pre-commit Hook

```yaml
- repo: https://github.com/canonic-apps/python
  hooks:
    - id: canonic-python
```

### CLI

```bash
canonic python validate --file main.py --tier 63
```

---

## Links

- [BYOL](BYOL.md) — Bring Your Own Language
- [VaaS](https://canonic-apps.github.io) — Validation as a Service
- [API Docs](https://api.canonic.dev/docs) — Full API reference

---
