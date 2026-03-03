"""
twilio_sms.py
-------------
Sends re-engagement SMS messages via Twilio REST API.
"""

import logging
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, SMS_TEMPLATE

log = logging.getLogger("twilio_sms")


def send_sms(name: str, phone: str) -> bool:
    """
    Send a re-engagement SMS to a single user.

    Args:
        name:  User's first name for personalization
        phone: E.164 format phone number (e.g. +15125550100)

    Returns:
        True if sent successfully, False otherwise
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=SMS_TEMPLATE.format(name=name),
            from_=TWILIO_PHONE_NUMBER,
            to=phone,
        )
        log.info(f"SMS sent to {phone} | SID: {message.sid} | Status: {message.status}")
        return True
    except Exception as e:
        log.error(f"SMS failed for {phone}: {e}")
        return False
