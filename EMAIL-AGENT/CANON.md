# EMAIL — CANON

inherits: /CANONIC/

---

## Axiom

**EMAIL = O∩E∩T grounded. Governed communications via iCloud+ Custom Email Domain.**

---

## Axioms

- All email operations via iCloud+ native apps (Mail.app, icloud.com).
- Every sent email MUST be logged to LEDGER with timestamp.
- Email templates MUST be stored in templates/ and versioned.
- Authentication via Passkey (iCloud Keychain).
- DNS managed via Cloudflare (MX, SPF, DKIM).
- App MUST be Git-native. Validators are GitHub Actions.
- Validators MUST be black-box. Opaque, signed, tamper-proof.

---

## Constraints

- Provider: iCloud+ Custom Email Domain.
- Auth: Passkey via iCloud Keychain.
- DNS: Cloudflare (MX → icloud.com, SPF, DKIM).
- Domain: canonic.org.
- Native-first interface (Mail.app, web).

---

## Validators

| Validator | Enforces | Trigger |
|-----------|----------|---------|
| email.audit | Audit Trail | Before send |
| email.template | Template Governance | On template load |
| email.credential | Credential Security | On token access |
| email.recipient | Domain allowlist | Before send |
| email.ratelimit | Abuse prevention | Before send |

---
