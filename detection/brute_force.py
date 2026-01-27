from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from models import Event

def detect_brute_force(
    db: Session,
    *,
    max_attempts: int=10,
    window_seconds: int=60
    )-> list[dict]:

    window_start = datetime.now(timezone.utc) - timedelta(seconds=window_seconds)

    results = (
        db.query(
            Event.ip,
            func.count(Event.id).label("attempts")
        )
        .filter(Event.event_type == "login_failed")
        .filter(Event.timestamp >= window_start)
        .group_by(Event.ip)
        .having(func.count(Event.id) >= max_attempts)
        .all()
    )

    detections = []

    for ip, attempts in results:
        detections.append({
            "ip": ip,
            "attempts": attempts,
            "window_seconds": window_seconds,
            "detected_at": datetime.now(timezone.utc)
        })

    return detections
