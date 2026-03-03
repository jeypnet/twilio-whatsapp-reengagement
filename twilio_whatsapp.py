"""
twilio_whatsapp.py
------------------
Sends re-engagement messages via WhatsApp Business API through Twilio.
"""

import logging
from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, WHATSAPP_FROM, WHATSAPP_TEMPLATE

log = logging.getLogger("twilio_whatsapp")


def send_whatsapp(name: str, phone: str) -> bool:
    """
    Send a re-engagement WhatsApp message to a single user.

    Args:
        name:  User's first name for personalization
        phone: E.164 format phone number (e.g. +15125550100)
                Will be prefixed with 'whatsapp:' automatically

    Returns:
        True if sent successfully, False otherwise
    """
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        to = f"whatsapp:{phone}" if not phone.startswith("whatsapp:") else phone
        message = client.messages.create(
            body=WHATSAPP_TEMPLATE.format(name=name),
            from_=WHATSAPP_FROM,
            to=to,
        )
        log.info(f"WhatsApp sent to {phone} | SID: {message.sid} | Status: {message.status}")
        return True
    except Exception as e:
        log.error(f"WhatsApp failed for {phone}: {e}")
        return False
