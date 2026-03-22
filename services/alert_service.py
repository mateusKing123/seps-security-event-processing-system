from sqlalchemy.orm import Session
from datetime import datetime, timezone

from models import Alert, IPReputation

SEVERity_RISK_MAP = {
    "low": 5,
    "medium": 10,
    "high": 20,
    "critical": 40
}

def create_alert_from_detection(
        db: Session,
        *,
        alert_type: str,
        ip: str,
        count: int,
        window_seconds: int,
        risk_increment: int | None = None,
        severity: str = "medium"
) -> Alert:
    alert = Alert(
        alert_type = alert_type,
        ip = ip,
        count = count,
        window_seconds = window_seconds,
        created_at = datetime.utcnow(),
        severity = severity
    )

    db.add(alert)

    if risk_increment is None:
        risk_increment = SEVERity_RISK_MAP.get(severity, 10)

    reputation = db.get(IPReputation, ip)
    
    if reputation is None:
        reputation = IPReputation(
            ip=ip,
            risk_score = risk_increment,
            last_seen = datetime.utcnow()
        )
        db.add(reputation)
    else:
        reputation.risk_score += risk_increment
        reputation.last_seen = datetime.utcnow()

    db.commit()
    db.refresh(alert)

    return alert