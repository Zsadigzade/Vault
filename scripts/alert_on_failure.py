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
    html = f"""<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#0f0f0f;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0f0f0f;padding:40px 0;">
    <tr><td align="center">
      <table width="560" cellpadding="0" cellspacing="0" style="background:#1a1a1a;border-radius:12px;overflow:hidden;border:1px solid #2a2a2a;">
        <tr>
          <td style="background:#ff3b30;padding:4px 24px;">
            <p style="margin:0;color:#fff;font-size:11px;font-weight:600;letter-spacing:1px;text-transform:uppercase;">Server Alert</p>
          </td>
        </tr>
        <tr>
          <td style="padding:32px 32px 8px;">
            <p style="margin:0 0 8px;font-size:11px;color:#666;letter-spacing:1px;text-transform:uppercase;">Vault Server · DO Frankfurt</p>
            <h1 style="margin:0;font-size:22px;font-weight:700;color:#fff;">⚠️ Failure Detected</h1>
          </td>
        </tr>
        <tr>
          <td style="padding:16px 32px 32px;">
            <div style="background:#111;border:1px solid #2a2a2a;border-left:3px solid #ff3b30;border-radius:8px;padding:16px 20px;margin-bottom:24px;">
              <p style="margin:0;font-size:14px;color:#e0e0e0;line-height:1.6;font-family:monospace;">{body}</p>
            </div>
            <table cellpadding="0" cellspacing="0">
              <tr>
                <td style="background:#ff3b30;border-radius:8px;padding:12px 24px;">
                  <a href="ssh://root@46.101.161.176" style="color:#fff;font-size:14px;font-weight:600;text-decoration:none;">SSH into server →</a>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr>
          <td style="padding:16px 32px;border-top:1px solid #2a2a2a;">
            <p style="margin:0;font-size:12px;color:#444;">Sent by vaultbot · bruhsocial.app</p>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""
    payload = json.dumps({
        "from": "alerts@bruhsocial.app",
        "to": [ALERT_EMAIL],
        "subject": subject,
        "html": html,
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
