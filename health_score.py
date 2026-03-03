"""
health_score.py
---------------
User engagement health scoring engine for JoGo.Team.

Calculates a composite health score (0-100) per user based on:
- Days since last login
- Sessions attended
- Bookings made
- Profile completeness

Users below the threshold are flagged as at-risk for re-engagement.
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional
import csv
import logging

log = logging.getLogger("health_score")

# ── Scoring Weights ────────────────────────────────────────────────────────────
WEIGHT_LAST_LOGIN     = 0.40
WEIGHT_SESSIONS       = 0.30
WEIGHT_BOOKINGS       = 0.20
WEIGHT_PROFILE        = 0.10

AT_RISK_THRESHOLD     = 40  # Score below this = at-risk


# ── User Model ─────────────────────────────────────────────────────────────────
@dataclass
class User:
    user_id: str
    name: str
    phone: str
    email: str
    last_login: Optional[datetime]
    sessions_attended: int
    bookings_made: int
    profile_complete: bool
    health_score: float = 0.0
    at_risk: bool = False


# ── Scoring Logic ──────────────────────────────────────────────────────────────

def score_last_login(last_login: Optional[datetime]) -> float:
    """Score based on recency of last login. Max score if logged in today."""
    if not last_login:
        return 0.0
    days_ago = (datetime.now() - last_login).days
    if days_ago <= 1:
        return 100.0
    elif days_ago <= 7:
        return 80.0
    elif days_ago <= 14:
        return 60.0
    elif days_ago <= 30:
        return 30.0
    else:
        return 0.0


def score_sessions(sessions: int) -> float:
    """Score based on total sessions attended."""
    if sessions >= 10:
        return 100.0
    elif sessions >= 5:
        return 75.0
    elif sessions >= 2:
        return 50.0
    elif sessions == 1:
        return 25.0
    else:
        return 0.0


def score_bookings(bookings: int) -> float:
    """Score based on total bookings made."""
    if bookings >= 5:
        return 100.0
    elif bookings >= 3:
        return 75.0
    elif bookings >= 1:
        return 50.0
    else:
        return 0.0


def score_profile(complete: bool) -> float:
    """Score based on profile completeness."""
    return 100.0 if complete else 0.0


def calculate_health_score(user: User) -> User:
    """Calculate composite health score and flag at-risk users."""
    score = (
        score_last_login(user.last_login)   * WEIGHT_LAST_LOGIN +
        score_sessions(user.sessions_attended) * WEIGHT_SESSIONS +
        score_bookings(user.bookings_made)   * WEIGHT_BOOKINGS +
        score_profile(user.profile_complete) * WEIGHT_PROFILE
    )
    user.health_score = round(score, 2)
    user.at_risk = user.health_score < AT_RISK_THRESHOLD
    return user


# ── CSV Loader ─────────────────────────────────────────────────────────────────

def load_users_from_csv(filepath: str) -> list[User]:
    """Load users from a CSV file and calculate health scores."""
    users = []
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            last_login = None
            if row.get("last_login"):
                try:
                    last_login = datetime.fromisoformat(row["last_login"])
                except ValueError:
                    pass

            user = User(
                user_id=row["user_id"],
                name=row["name"],
                phone=row["phone"],
                email=row.get("email", ""),
                last_login=last_login,
                sessions_attended=int(row.get("sessions_attended", 0)),
                bookings_made=int(row.get("bookings_made", 0)),
                profile_complete=row.get("profile_complete", "false").lower() == "true",
            )
            calculate_health_score(user)
            users.append(user)

    log.info(f"Loaded {len(users)} users. At-risk: {sum(1 for u in users if u.at_risk)}")
    return users


def get_at_risk_users(users: list[User]) -> list[User]:
    """Return only users flagged as at-risk."""
    return [u for u in users if u.at_risk]
