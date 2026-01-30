# ATOM CREDENTIALING — CANON

inherits: /CANONIC/

owner: ATOM Advantage (avinash@canonic.org)

---

## Domain

Constitutional AI governance for healthcare provider credentialing.

```
ATOM CREDENTIALING
═══════════════════════════════════════════════════════════════
Every credential verified.
Every verification logged.
Every decision traceable.
```

---

## Axioms

### 1. Primary Source Verification

All credentials MUST be verified against primary sources.

```
CREDENTIAL → PRIMARY SOURCE → VERIFICATION → LEDGER
```

| Credential | Primary Source |
|------------|----------------|
| NPI | NPPES Registry |
| State License | State Medical Board |
| DEA | DEA CSOS |
| Board Certification | ABMS/AOA |
| Exclusions | OIG LEIE, SAM.gov |

### 2. Continuous Monitoring

Credentials MUST be monitored for:
- Expiration (30/60/90 day alerts)
- Status changes
- Sanctions list updates
- License actions

### 3. Audit Trail

Every verification MUST be logged to immutable ledger:
- Timestamp
- Source checked
- Result
- Verifier identity

### 4. Delegation Authority

Credentialing decisions MAY be delegated with:
- Explicit scope
- Audit trail
- Revocation capability

---

## Constraints

- Credentials without primary source verification are INVALID.
- Expired credentials MUST trigger alerts.
- Excluded providers MUST be flagged immediately.
- All verifications MUST complete within 24 hours.

---

## Validators

| Validator | Function | Status |
|-----------|----------|--------|
| `npi-verify.py` | NPPES lookup | Active |
| `license-check.py` | State board verification | Active |
| `exclusion-scan.py` | OIG/SAM screening | Active |
| `expiry-monitor.py` | Expiration tracking | Active |

---

## Integration

```
ATOM PLATFORM
    │
    └── CREDENTIALING API
            │
            ├── /verify/{npi}
            ├── /status/{provider}
            ├── /alerts
            └── /audit/{provider}
```

---

*ATOM CREDENTIALING | Governed by CANONIC | Built for ATOM Advantage*
