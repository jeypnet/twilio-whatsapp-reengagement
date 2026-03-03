"""
reengagement.py
---------------
Main re-engagement job for JoGo.Team.

Loads users from CSV, calculates health scores,
identifies at-risk users, and sends re-engagement
messages via SMS and WhatsApp through Twilio.

Run daily via cron:
    0 9 * * * python reengagement.py
"""

import logging
import time
from health_score import load_users_from_csv, get_at_risk_users
from twilio_sms import send_sms
from twilio_whatsapp import send_whatsapp
from config import USERS_CSV_PATH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger("reengagement")

# ── Channel Assignment ─────────────────────────────────────────────────────────
# Users with score < 20 get SMS (urgent)
# Users with score 20-40 get WhatsApp (softer touch)
SMS_THRESHOLD = 20


def run():
    log.info("Starting re-engagement job...")

    users = load_users_from_csv(USERS_CSV_PATH)
    at_risk = get_at_risk_users(users)

    if not at_risk:
        log.info("No at-risk users found. All good!")
        return

    log.info(f"Found {len(at_risk)} at-risk users. Starting outreach...")

    sms_sent = 0
    wa_sent = 0
    failed = 0

    for user in at_risk:
        log.info(f"Processing {user.name} | Score: {user.health_score} | Phone: {user.phone}")

        if user.health_score < SMS_THRESHOLD:
            success = send_sms(user.name, user.phone)
            channel = "SMS"
        else:
            success = send_whatsapp(user.name, user.phone)
            channel = "WhatsApp"

        if success:
            if channel == "SMS":
                sms_sent += 1
            else:
                wa_sent += 1
        else:
            failed += 1

        time.sleep(0.5)  # Rate limiting — be kind to the Twilio API

    log.info("── Re-engagement job complete ──")
    log.info(f"  SMS sent:       {sms_sent}")
    log.info(f"  WhatsApp sent:  {wa_sent}")
    log.info(f"  Failed:         {failed}")
    log.info(f"  Total reached:  {sms_sent + wa_sent} / {len(at_risk)}")


if __name__ == "__main__":
    run()
