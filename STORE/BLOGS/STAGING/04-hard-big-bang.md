# The Hard Big Bang

*From monolithic to distributed in one commit*

---

**Markets:** v0 (MACHINE Era)
**Ledger:** Commit `9ec7cc9`, January 23, 2026

---

## Before

```
CANONIC (monolithic)
└── Everything in one repo
```

One repo. Growing fast. 100 commits in 14 days.

Too big. Too coupled. Too fragile.

---

## The Explosion

January 23, 2026. Commit `9ec7cc9`.

One repo becomes four orgs:

```
canonic-machine    → Governance kernel (immutable)
canonic-domains    → Professional domain axioms
canonic-hadley     → Instance applications
canonic-apps       → Certified app registry
```

---

## Why Four

```
KERNEL (canonic-machine)
    │
    └── Never changes. The constitution.

DOMAINS (canonic-domains)
    │
    └── Professional verticals. Inherits kernel.

INSTANCES (canonic-hadley)
    │
    └── Actual apps. Inherits domains.

REGISTRY (canonic-apps)
    │
    └── Certified apps. Validates instances.
```

Each layer has one job.

---

## The Property

Governance isolation.

```
canonic-machine is IMMUTABLE

Lower layers cannot mutate parent axioms.
Inheritance flows DOWN.
Never weakens.
```

The kernel is protected by architecture.

---

## The Timeline

```
2026-01-10: SOFT BIG BANG (genesis)
     │
     ├── 14 days of building
     ├── 100 commits
     └── System bloats
     │
2026-01-23: HARD BIG BANG (distribution)
     │
     └── Four orgs. Isolated. Governed.
```

Compression then explosion. Like a real big bang.

---

## The Insight

Monolithic governance doesn't scale.

Distributed governance with inheritance does.

Same constitution. Independent implementations.

---

*STAGING/005 | January 2026*
*Ledger: canonic-machine*
