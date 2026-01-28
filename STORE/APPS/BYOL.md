# BYOL — Bring Your Own Language

inherits: /CANONIC/APPS/STORE/

status: active
tier: ENTERPRISE

---

## Axiom

**Define your language. CANONIC enforces. Universal code governance.**

---

## Service

### What

BYOL lets you define code governance for ANY programming language using declarative CANON specs.

### How

1. Create `LANGUAGE/MACHINE/{LANG}.md`
2. Define constraints (`MUST`, `MUST NOT`)
3. Define patterns (what to detect)
4. Run VaaS — P validator enforces

### Why

- One governance system for polyglot codebases
- Self-documenting constraints (in markdown)
- Self-validating tooling (P validates itself)
- Extensible to any language

---

## Pricing

| Tier | Languages | Orgs | Price |
|------|-----------|------|-------|
| COMMUNITY | 1 | 1 | Free |
| CLOSURE | 3 | 1 | $99/mo |
| BUSINESS | 10 | 5 | $499/mo |
| ENTERPRISE | Unlimited | Unlimited | Contact |

---

## Supported Languages

Out of the box:
- Python (PYTHON.md)

Add your own:
- Go (GO.md)
- TypeScript (TYPESCRIPT.md)
- Rust (RUST.md)
- Any language you define

---

## Get Started

```bash
# 1. Create your language spec
cat > LANGUAGE/MACHINE/GO.md << 'EOF'
# GO — Code Governance

inherits: /CANONIC/LANGUAGE/MACHINE/

## Constraints
- Functions MUST have error returns
- Packages MUST have doc.go

## Patterns
func {name}(  →  signature
EOF

# 2. Run VaaS
python3 canonic_validate.py --tier 64

# 3. See violations
[PASS] P
  [!] Function missing error return: main()
```

---

## Links

- [LANGUAGE/MACHINE/PYTHON.md](/LANGUAGE/MACHINE/PYTHON.md) — Python spec
- [VaaS](/VALIDATORS/) — Validation as a Service
- [LanguageReader](/MACHINE/core.py) — Abstraction layer

---
