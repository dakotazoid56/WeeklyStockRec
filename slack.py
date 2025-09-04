import os
import json
import requests

WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack(body: str):
    print("Sending Slack message")
    if not WEBHOOK_URL:
        raise RuntimeError("Missing SLACK_WEBHOOK_URL in environment variables.")
    resp = requests.post(
        WEBHOOK_URL,
        data=json.dumps({"text": body}),
        headers={"Content-Type": "application/json"}
    )
    if resp.status_code != 200:
        raise RuntimeError(f"Slack error {resp.status_code}: {resp.text}")
