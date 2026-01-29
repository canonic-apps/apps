# EMAIL

Governed email for CANONIC via iCloud+ Custom Email Domain.

## Status

**ACTIVE** — Passkey authentication via iCloud Keychain

## Setup

### 1. iCloud+ Custom Email Domain

Domain `canonic.org` configured with iCloud+ Custom Email Domain:
- MX records → icloud.com
- SPF, DKIM via Cloudflare DNS

### 2. Access

- **Web:** https://www.icloud.com/mail/
- **iOS/macOS:** Native Mail.app with iCloud account
- **Settings:** https://www.icloud.com/icloudplus/

### 3. Authentication

Passkey via iCloud Keychain — no passwords stored.

## Email Addresses

| User | Email |
|------|-------|
| Dexter | dexter@canonic.org |
| Fatima | fatima@canonic.org |

## Governance

All emails logged via:
- iCloud sent folder
- Native Mail.app audit trail
- Manual LEDGER entries for formal communications

## Credentials

See `~/.canonic/CREDENTIALS/ICLOUD/email-domain.md`

## Migration Note

Microsoft Graph implementation deprecated (2026-01-29).
Previous code preserved in `canonic_email.py` for reference.

---
