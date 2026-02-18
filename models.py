from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.sql import func
from db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    ip = Column(String, nullable=False, index=True)
    event_type = Column(String, nullable=False, index=True)
    username = Column(String, nullable=True)
    endpoint = Column(String, nullable=False, index=True)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String, nullable=False, index=True)
    ip = Column(String, nullable=False, index=True)
    count = Column(Integer, nullable=False)
    window_seconds = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class IPReputation(Base):
    __tablename__ = "ip_reputation"

    ip = Column(String, primary_key=True)
    risk_score = Column(Integer, default=0)
    last_seen = Column(DateTime(timezone=True), server_default=func.now())


Index("idx_events_ip_time", Event.ip, Event.timestamp)
Index("idx_events_type_time", Event.event_type, Event.timestamp)

