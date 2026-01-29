#!/usr/bin/env python3
"""
CANONIC GMAIL READER — Read emails from Gmail accounts
Usage: python gmail_read.py auth <account>   # Authenticate
       python gmail_read.py read <account>   # Read inbox
"""

import json
import sys
import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
CREDS_DIR = Path.home() / ".canonic" / "credentials" / "GOOGLE"
CLIENT_SECRET = CREDS_DIR / "gmail-oauth.json"

def get_token_path(account: str) -> Path:
    return CREDS_DIR / f"gmail-token-{account}.json"

def authenticate(account: str):
    """Run OAuth flow for a Gmail account."""
    token_path = get_token_path(account)
    creds = None

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            print(f"\nAuthenticating for: {account}")
            print("A browser window will open. Sign in with the Gmail account.")
            creds = flow.run_local_server(port=0)

        token_path.write_text(creds.to_json())
        print(f"Token saved to: {token_path}")

    return creds

def read_inbox(account: str, max_results: int = 10):
    """Read recent emails from inbox."""
    creds = authenticate(account)
    service = build('gmail', 'v1', credentials=creds)

    # Get profile
    profile = service.users().getProfile(userId='me').execute()
    print(f"\n=== {profile['emailAddress']} ===\n")

    # Get messages
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])

    for msg in messages:
        full = service.users().messages().get(userId='me', id=msg['id'], format='metadata').execute()
        headers = {h['name']: h['value'] for h in full['payload']['headers']}

        print(f"From: {headers.get('From', 'Unknown')}")
        print(f"Subject: {headers.get('Subject', '(no subject)')}")
        print(f"Date: {headers.get('Date', '')}")
        print("-" * 60)

def search_emails(account: str, query: str, max_results: int = 10):
    """Search emails."""
    creds = authenticate(account)
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().messages().list(
        userId='me',
        q=query,
        maxResults=max_results
    ).execute()

    messages = results.get('messages', [])
    print(f"\n=== Search: {query} ({len(messages)} results) ===\n")

    for msg in messages:
        full = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = {h['name']: h['value'] for h in full['payload']['headers']}

        print(f"From: {headers.get('From', 'Unknown')}")
        print(f"Subject: {headers.get('Subject', '(no subject)')}")
        print(f"Date: {headers.get('Date', '')}")

        # Get snippet
        print(f"Preview: {full.get('snippet', '')[:200]}...")
        print("-" * 60)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python gmail_read.py auth <account>      # hadleylab or mammochat")
        print("  python gmail_read.py read <account>")
        print("  python gmail_read.py search <account> <query>")
        sys.exit(1)

    cmd = sys.argv[1]
    account = sys.argv[2]

    if cmd == "auth":
        authenticate(account)
        print("Authentication complete.")
    elif cmd == "read":
        read_inbox(account)
    elif cmd == "search":
        query = sys.argv[3] if len(sys.argv) > 3 else "is:unread"
        search_emails(account, query)
    else:
        print(f"Unknown command: {cmd}")
