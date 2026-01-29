# CANONIC APPS

![CANONIC](https://img.shields.io/badge/CANONIC-ENTERPRISE-00ff88?style=flat-square)
![Validators](https://img.shields.io/badge/VaaS-ENTERPRISE-00ff88?style=flat-square)

Governed utilities for the CANONIC ecosystem. ENTERPRISE compliance via VaaS (VITAE as a Service).

## Structure

```
canonic-apps/
├── CANON.md          ← App axioms (FROZEN)
├── VOCAB.md          ← Term definitions
├── README.md         ← This file
├── OFFICE/           ← Business productivity
│   └── EMAIL/        ← Governed email
├── KNOWLEDGE/        ← Discovery apps
│   ├── HEXAD/        ← Six-element patterns
│   ├── LATTICE/      ← Formula composition
│   └── TRANSCRIPT/   ← Evidence queries
├── SHOP/             ← App distribution (SHOP, not STORE/CATALOG)
├── EVOLUTION/        ← EVO = grounded evolution
├── MAMMOCHAT/        ← Oncology support
├── PSYCHCHAT/        ← Mental health
├── SELFCHAT/         ← AI introspection
├── YOUCHAT/          ← Personal governance
├── TUTORCHAT/        ← Education
├── INVESTORCHAT/     ← Token economics
└── TRANSCRIPTCHAT/   ← Ledger interface
```

## Usage

```bash
# Install
git clone https://github.com/canonic/apps

# Run
canonic office email send --to x@y.com
canonic knowledge search --query "governance"
```

## Axioms

1. Git-Native — every app is a repo
2. Black Box Validators — opaque, signed
3. Composable — apps call apps
4. One Namespace — `canonic {domain} {app} {cmd}`
5. Audit Everything — git log is truth
6. EVO — grounded evolution. All change is ledger-derived.

---
