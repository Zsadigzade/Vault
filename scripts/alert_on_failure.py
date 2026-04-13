#!/usr/bin/env python3
"""Send Resend email alert — called directly on failure with a message."""

import os
import sys
import json
import urllib.request

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
ALERT_EMAIL = os.environ.get("ALERT_EMAIL", "")


def send_alert(subject: str, body: str):
    if not RESEND_API_KEY or not ALERT_EMAIL:
        print("Missing RESEND_API_KEY or ALERT_EMAIL")
        sys.exit(1)
    payload = json.dumps({
        "from": "vaultbot@bruhsocial.app",
        "to": [ALERT_EMAIL],
        "subject": subject,
        "text": body,
    }).encode()
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=payload,
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"Alert sent: {resp.status}")
    except Exception as e:
        print(f"Failed to send alert: {e}")
        sys.exit(1)


if __name__ == "__main__":
    message = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Unknown failure"
    send_alert(
        subject=f"⚠️ Vault server failure: {message[:60]}",
        body=f"Vault server reported a failure:\n\n{message}\n\nSSH in to investigate:\nssh root@46.101.161.176",
    )
