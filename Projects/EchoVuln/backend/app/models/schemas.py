from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


# ---------- Common ----------
class ApiOk(BaseModel):
    ok: bool = True


# ---------- Enrollment ----------
class EnrollRequest(BaseModel):
    agent_id: str = Field(..., min_length=8, max_length=64)
    hostname: Optional[str] = None
    os: Optional[str] = None
    ip: Optional[str] = None


class EnrollResponse(BaseModel):
    agent_token: str
    asset_id: int


# ---------- Assets ----------
class AssetCreate(BaseModel):
    name: str
    description: Optional[str] = None
    environment: Optional[str] = None
    tags: Optional[List[str]] = None
    agent_id: Optional[str] = None


class AssetOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    environment: Optional[str] = None
    tags: Optional[List[str]] = None
    agent_id: Optional[str] = None
    created_at: datetime


# ---------- Snapshot ingest v2 ----------
class SnapshotOS(BaseModel):
    name: Optional[str] = None
    build: Optional[str] = None
    release: Optional[str] = None


class SnapshotHotfix(BaseModel):
    installed_count: Optional[int] = None
    last_installed_on: Optional[str] = None


class SnapshotSignals(BaseModel):
    internet_facing: bool = False
    business_critical: bool = False


class MissingUpdate(BaseModel):
    kb: Optional[str] = None
    cve: Optional[str] = None


class SnapshotIngestV2(BaseModel):
    schema_version: Literal[2]
    agent_id: str
    asset_id: Optional[int] = None
    collected_at_utc: datetime

    os: Optional[SnapshotOS] = None
    reboot_pending: bool = False
    missing_updates: List[MissingUpdate] = []
    hotfix: Optional[SnapshotHotfix] = None
    signals: Optional[SnapshotSignals] = None

    # forward-compatible raw extras (agent can add more without breaking server)
    extras: Dict[str, Any] = {}


class SnapshotOut(BaseModel):
    id: int
    asset_id: int
    agent_id: str
    collected_at_utc: datetime
    payload: Dict[str, Any]


# ---------- Top fixes ----------
class TopFixItem(BaseModel):
    score: int = Field(..., ge=0, le=100)
    headline: str
    fix_action: str
    why_now: str
    references: Optional[List[str]] = None


class TopFixesRequest(BaseModel):
    asset_id: Optional[int] = None
    limit: int = Field(10, ge=1, le=50)


class TopFixesResponse(BaseModel):
    items: List[TopFixItem]


# ---------- Reports ----------
class ReportCreate(BaseModel):
    asset_id: Optional[int] = None
    title: str
    markdown: str


class ReportOut(BaseModel):
    id: int
    asset_id: Optional[int] = None
    title: str
    markdown: str
    created_at: datetime
