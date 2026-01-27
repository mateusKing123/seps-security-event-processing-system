from sqlalchemy.orm import Session
from datetime import datetime, timezone

from models import Alert, IPReputation

def create_alert_from_detection(
        db: Session,
        *,
        alert_type: str,
        ip: str,
        count: int,
        window_seconds: int,
        risk_increment: int = 10
) -> Alert:
    alert = Alert(
        alert_type = alert_type,
        ip = ip,
        count = count,
        window_seconds = window_seconds,
        created_at = datetime.now(timezone.utc)
    )

    db.add(alert)

    reputation = db.get(IPReputation, ip)
    
    if reputation is None:
        reputation = IPReputation(
            ip=ip,
            risk_score = risk_increment,
            last_seen = datetime.now(timezone.utc)
        )
        db.add(reputation)
    else:
        reputation.risk_score += risk_increment
        reputation.last_seen = datetime.now(timezone.utc)

    db.commit()
    db.refresh(alert)

    return alert