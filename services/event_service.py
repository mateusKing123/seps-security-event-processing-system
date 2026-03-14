from datetime import datetime, timezone
from models import Event


def create_event(db, event_data: dict) -> Event:
    timestamp = datetime.fromisoformat(event_data["timestamp"]).replace(tzinfo=timezone.utc)
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    event = Event(
        timestamp = timestamp,
        ip = event_data["ip"],
        event_type = event_data["event_type"],
        username = event_data.get("username"),
        endpoint = event_data["endpoint"]
    )
    
    db.add(event)
    db.commit()
    db.refresh(event)

    return event
