# twilio-whatsapp-reengagement

**Automated customer re-engagement using Twilio SMS and WhatsApp API**

Built for [JoGo.Team](https://jogo.team) — a two-sided SaaS marketplace with 1,500+ users across four continents.

---

## The Problem

On a two-sided marketplace, user drop-off is silent. There's no sales team to notice. No CSM sending manual emails. If a host stops scheduling or a participant stops showing up, churn happens invisibly — unless you build something to catch it.

This system monitors user engagement health scores, detects at-risk signals, and automatically triggers personalized re-engagement messages via SMS and WhatsApp through Twilio.

**Result:** 80%+ of dormant users converted back to active participation.

---

## How It Works
```
User Activity Tracked
        ↓
Health Score Calculated (last login, sessions attended, bookings made)
        ↓
At-Risk Threshold Triggered (score drops below threshold)
        ↓
Twilio Sends Personalized SMS or WhatsApp Message
        ↓
Engagement Response Logged → Score Updated
```

---

## Features

- **Health scoring engine** — tracks engagement signals (logins, sessions, bookings) and calculates a composite score per user
- **At-risk detection** — flags users below configurable thresholds before they fully churn
- **Twilio SMS** — sends re-engagement nudges via SMS for high-priority at-risk users
- **WhatsApp API** — sends richer re-engagement messages with session info via WhatsApp Business API
- **Personalization** — messages include user name, last activity, and a direct re-engagement CTA
- **Response tracking** — logs delivery status and reply signals back to health score

---

## Tech Stack

- **Python 3.10+**
- **Twilio REST API** (SMS + WhatsApp)
- **Twilio Messaging Services**
- **Cloudflare Workers** (webhook handling)
- **JSON / CSV** (user health score data layer)

---

## Setup
```bash
git clone https://github.com/jeypnet/twilio-whatsapp-reengagement.git
cd twilio-whatsapp-reengagement
pip install -r requirements.txt
```

Create a `.env` file:
```env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1xxxxxxxxxx
WHATSAPP_FROM=whatsapp:+14155238886
HEALTH_SCORE_THRESHOLD=40
```

Run the re-engagement job:
```bash
python reengagement.py
```

---

## File Structure
```
twilio-whatsapp-reengagement/
├── reengagement.py          # Main script — detects at-risk users and triggers messages
├── health_score.py          # Calculates composite engagement score per user
├── twilio_sms.py            # Twilio SMS send logic
├── twilio_whatsapp.py       # WhatsApp Business API send logic
├── users_sample.csv         # Sample user data structure (anonymized)
├── config.py                # Threshold and message template config
├── requirements.txt
└── README.md
```

---

## Business Context

This wasn't a side project — it ran in production for a live SaaS platform. The health scoring logic was modeled after enterprise CSM tools like Gainsight, adapted for a lean startup stack. The re-engagement sequences ran on a daily cron job and were the primary driver of quarter-over-quarter engagement growth.

---

## Related Skills Demonstrated

- Customer health scoring and churn signal detection
- Automated lifecycle messaging at scale
- Twilio SMS + WhatsApp API integration
- Python scripting for CS operations
- Production SaaS platform management

---

*Part of the [jeypnet](https://github.com/jeypnet) project portfolio — tools built while running JoGo.Team.*# twilio-whatsapp-reengagement
