from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from models import Event, Alert
from services.alert_service import create_alert_from_detection

def detect_brute_force(
    db: Session,
    *,
    threshold: int=10,
    window_seconds: int=60
    )-> None:

    time_limite = datetime.utcnow() - timedelta(seconds=window_seconds)

    results = (
        db.query(
            Event.ip,
            func.count(Event.id).label("attempt_count")
        )
        .filter(Event.event_type == "login_failed")
        .filter(Event.timestamp >= time_limite)
        .group_by(Event.ip)
        .having(func.count(Event.id) >= threshold)
        .all()
    )

    for ip, attempt_count in results:
        existing_alert = (
            db.query(Alert)
            .filter(
                Alert.alert_type == "brute_force",
                Alert.ip == ip,
                Alert.created_at >= time_limite
            )
            .first()
        )
        
        if existing_alert:
            continue

        create_alert_from_detection(
            db,
            alert_type="brute_force",
            ip=ip,
            count=attempt_count,
            window_seconds=window_seconds,
            severity="high"
        )
