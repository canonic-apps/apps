# CANONIC APPS

Governed utilities for the CANONIC ecosystem.

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
├── STORE/            ← App distribution
├── EVOLUTION/        ← System evolution
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

---
