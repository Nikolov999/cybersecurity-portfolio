from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.sql import func
from .db import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    hostname = Column(String(255), nullable=False, index=True)
    event_id = Column(Integer, nullable=False, index=True)
    username = Column(String(255), nullable=True, index=True)
    source_ip = Column(String(64), nullable=True, index=True)
    channel = Column(String(64), nullable=True, index=True)
    record_id = Column(Integer, nullable=True, index=True)
    raw = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    rule_name = Column(String(255), nullable=False, index=True)
    severity = Column(String(32), nullable=False, index=True)  # low/medium/high
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    hostname = Column(String(255), nullable=False, index=True)
    event_id = Column(Integer, nullable=True, index=True)
    username = Column(String(255), nullable=True, index=True)
    source_ip = Column(String(64), nullable=True, index=True)
    details = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


Index("ix_events_host_time", Event.hostname, Event.timestamp)
Index("ix_events_user_time", Event.username, Event.timestamp)
Index("ix_alerts_host_time", Alert.hostname, Alert.timestamp)