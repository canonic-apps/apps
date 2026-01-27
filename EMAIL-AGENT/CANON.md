# EMAIL — CANON

inherits: /CANONIC/

---

## Axiom

**EMAIL = O∩E∩T grounded. Governed communications via Microsoft Graph.**

---

## Axioms

- All email operations MUST use Microsoft Graph API.
- Every sent email MUST be logged to LEDGER with timestamp.
- Email templates MUST be stored in templates/ and versioned.
- Direct API calls only. No third-party email services.
- OAuth tokens MUST be stored securely, never in plaintext.
- App MUST be Git-native. Validators are GitHub Actions.
- Validators MUST be black-box. Opaque, signed, tamper-proof.

---

## Constraints

- Provider: Microsoft 365 / Azure AD.
- API: Microsoft Graph.
- Scopes: Mail.Send, Mail.ReadWrite, User.Read.
- CLI-first interface.
- Zero configuration (auto-detect from git config).

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
