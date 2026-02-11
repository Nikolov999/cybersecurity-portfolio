from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class IngestEvent(BaseModel):
    hostname: str = Field(..., min_length=1, max_length=255)
    event_id: int = Field(..., ge=1)
    timestamp: datetime
    username: Optional[str] = Field(default=None, max_length=255)
    source_ip: Optional[str] = Field(default=None, max_length=64)
    channel: Optional[str] = Field(default=None, max_length=64)
    record_id: Optional[int] = Field(default=None, ge=0)
    raw: str = Field(..., min_length=1)


class EventOut(BaseModel):
    id: int
    timestamp: datetime
    hostname: str
    event_id: int
    username: Optional[str]
    source_ip: Optional[str]
    channel: Optional[str]
    record_id: Optional[int]
    raw: str

    class Config:
        from_attributes = True


class EndpointOut(BaseModel):
    hostname: str
    last_seen: datetime
    channels_seen: List[str] = []
    sysmon_present: bool
    event_rate: float  # events per hour over lookback window


class AlertOut(BaseModel):
    id: int
    rule_name: str
    severity: str
    timestamp: datetime
    hostname: str
    event_id: Optional[int]
    username: Optional[str]
    source_ip: Optional[str]
    details: str

    class Config:
        from_attributes = True


class IngestResponse(BaseModel):
    stored_event_id: int
    alerts_created: int
    alert_ids: List[int] = []