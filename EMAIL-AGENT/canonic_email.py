#!/usr/bin/env python3
"""
CANONIC EMAIL — CANON compliant

inherits: /CANONIC/APPS/EMAIL-AGENT/CANON.md
tier: 63

Governed email via Microsoft Graph.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import msal
import requests

# PATHS
HOME: Path = Path.home()
CANONIC: Path = HOME / ".canonic"
CREDS: Path = CANONIC / "credentials" / "microsoft"
SCRIPT_DIR: Path = Path(__file__).parent
TEMPLATES: Path = SCRIPT_DIR / "templates"
SENT: Path = SCRIPT_DIR / "sent"

# CONFIG
CONFIG: Path = CREDS / "azure-app.json"
CACHE: Path = CREDS / "token-cache.json"
GRAPH: str = "https://graph.microsoft.com/v1.0"


def load_config() -> dict[str, Any]:
    """Load Azure AD config from credential store."""
    with open(CONFIG) as f:
        return json.load(f)


def load_cache() -> msal.SerializableTokenCache:
    """Load MSAL token cache from credential store."""
    cache = msal.SerializableTokenCache()
    if CACHE.exists():
        cache.deserialize(CACHE.read_text())
    return cache


def save_cache(cache: msal.SerializableTokenCache) -> None:
    """Save MSAL token cache to credential store."""
    if cache.has_state_changed:
        CACHE.write_text(cache.serialize())


def get_token(config: dict[str, Any], cache: msal.SerializableTokenCache) -> str:
    """Get access token. Refresh silently or initiate device flow."""
    app = msal.PublicClientApplication(
        config["client_id"],
        authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        token_cache=cache
    )

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(
            ["Mail.Send", "Mail.ReadWrite", "User.Read"],
            account=accounts[0]
        )
        if result and "access_token" in result:
            save_cache(cache)
            return result["access_token"]

    flow = app.initiate_device_flow(["Mail.Send", "Mail.ReadWrite", "User.Read"])
    print(flow["message"])
    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        save_cache(cache)
        return result["access_token"]

    print(f"AUTH FAILED: {result.get('error_description')}")
    sys.exit(1)


def whoami(token: str) -> dict[str, Any]:
    """Get current user info from Graph API."""
    r = requests.get(f"{GRAPH}/me", headers={"Authorization": f"Bearer {token}"})
    return r.json()


def send(token: str, to: str, subject: str, body: str, html: bool = False, sender: Optional[str] = None, verbose: bool = False) -> bool:
    """Send email via Microsoft Graph API. Optionally set from address."""
    message: dict[str, Any] = {
        "subject": subject,
        "body": {"contentType": "HTML" if html else "Text", "content": body},
        "toRecipients": [{"emailAddress": {"address": to}}]
    }

    # Set custom from address if provided (supports "Name <email>" format)
    if sender:
        if "<" in sender and ">" in sender:
            name = sender.split("<")[0].strip()
            addr = sender.split("<")[1].split(">")[0].strip()
            message["from"] = {"emailAddress": {"name": name, "address": addr}}
        else:
            message["from"] = {"emailAddress": {"address": sender}}

    r = requests.post(
        f"{GRAPH}/me/sendMail",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"message": message, "saveToSentItems": True}
    )
    if verbose and r.status_code != 202:
        print(f"Error {r.status_code}: {r.text}")
    return r.status_code == 202


def log_send(to: str, subject: str, template: Optional[str] = None) -> None:
    """Log sent email to LEDGER."""
    SENT.mkdir(exist_ok=True)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "to": to,
        "subject": subject,
        "template": template
    }
    log = SENT / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    with open(log, "a") as f:
        f.write(json.dumps(entry) + "\n")


def load_template(name: str) -> tuple[str, str, bool]:
    """Load email template. Returns (subject, body, is_html)."""
    # Check for HTML template first
    html_path = TEMPLATES / f"{name}.html"
    md_path = TEMPLATES / f"{name}.md"

    if html_path.exists():
        body = html_path.read_text()
        # Extract subject from md file if exists
        subject = f"CANONIC — {name.title()}"
        if md_path.exists():
            for line in md_path.read_text().split("\n"):
                if line.startswith("Subject:"):
                    subject = line[8:].strip()
                    break
        return subject, body, True

    if not md_path.exists():
        print(f"TEMPLATE NOT FOUND: {name}")
        sys.exit(1)

    lines = md_path.read_text().strip().split("\n")
    subject: Optional[str] = None
    body_start = 0

    for i, line in enumerate(lines):
        if line.startswith("Subject:"):
            subject = line[8:].strip()
            body_start = i + 1
            break

    if subject is None:
        print(f"NO SUBJECT: {md_path}")
        sys.exit(1)

    body = "\n".join(lines[body_start:]).strip()
    return subject, body, False


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("canonic_email.py <cmd>")
        print("  whoami")
        print("  send <to> <template>")
        print("  templates")
        print("  log")
        sys.exit(1)

    cmd = sys.argv[1]
    config = load_config()
    cache = load_cache()

    if cmd == "whoami":
        token = get_token(config, cache)
        user = whoami(token)
        print(f"User: {user.get('displayName')}")
        print(f"Email: {user.get('mail') or user.get('userPrincipalName')}")

    elif cmd == "send":
        if len(sys.argv) < 4:
            print("send <to> <template>")
            sys.exit(1)

        to = sys.argv[2]
        template = sys.argv[3]

        token = get_token(config, cache)
        user = whoami(token)
        subject, body, is_html = load_template(template)

        print(f"From: {user.get('mail') or user.get('userPrincipalName')}")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Format: {'HTML' if is_html else 'Text'}")
        print("---")

        if send(token, to, subject, body, html=is_html):
            log_send(to, subject, template)
            print("SENT")
        else:
            print("FAILED")
            sys.exit(1)

    elif cmd == "templates":
        for t in TEMPLATES.glob("*.md"):
            print(f"  {t.stem}")

    elif cmd == "send-raw":
        if len(sys.argv) < 5:
            print("send-raw <to> <subject> <body> [--from sender@domain.org]")
            sys.exit(1)

        to = sys.argv[2]
        subject = sys.argv[3]
        body = sys.argv[4]
        sender = None

        if "--from" in sys.argv:
            idx = sys.argv.index("--from")
            sender = sys.argv[idx + 1] if idx + 1 < len(sys.argv) else None

        token = get_token(config, cache)

        if send(token, to, subject, body, html=False, sender=sender, verbose=True):
            log_send(to, subject, "raw")
            print(f"SENT from {sender or 'me'}")
        else:
            print("FAILED")
            sys.exit(1)

    elif cmd == "log":
        if not SENT.exists():
            print("No sent")
        else:
            for f in sorted(SENT.glob("*.jsonl")):
                print(f"\n=== {f.stem} ===")
                for line in open(f):
                    e = json.loads(line)
                    print(f"  {e['timestamp']} -> {e['to']}: {e['subject']}")

    else:
        print(f"Unknown: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
