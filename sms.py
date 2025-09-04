import os
from twilio.rest import Client

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUM = os.getenv("TWILIO_FROM")
TO_PHONE = os.getenv("TO_PHONE")

client = None
if ACCOUNT_SID and AUTH_TOKEN:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

def send_sms(body: str):
    if not client:
        raise RuntimeError("Twilio client not configured; check env vars.")
    if not FROM_NUM or not TO_PHONE:
        raise RuntimeError("Missing TWILIO_FROM or TO_PHONE")
    client.messages.create(from_=FROM_NUM, to=TO_PHONE, body=body)
