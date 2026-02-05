from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


def utcnow() -> datetime:
    return datetime.utcnow()


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)


class ApiKey(Base):
    __tablename__ = "api_keys"
    __table_args__ = (
        UniqueConstraint("tenant_id", "key_id", name="uq_api_keys_tenant_keyid"),
        Index("ix_api_keys_key_id", "key_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)

    key_id: Mapped[str] = mapped_column(String(32), nullable=False)  # ak_xxx
    key_hash: Mapped[str] = mapped_column(Text, nullable=False)
    label: Mapped[str] = mapped_column(String(200), default="admin", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    tenant: Mapped["Tenant"] = relationship()


class EnrollKey(Base):
    __tablename__ = "enroll_keys"
    __table_args__ = (
        UniqueConstraint("tenant_id", "key_id", name="uq_enroll_keys_tenant_keyid"),
        Index("ix_enroll_keys_key_id", "key_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)

    key_id: Mapped[str] = mapped_column(String(32), nullable=False)  # ek_xxx
    key_hash: Mapped[str] = mapped_column(Text, nullable=False)
    label: Mapped[str] = mapped_column(String(200), default="enroll", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    tenant: Mapped["Tenant"] = relationship()


class Asset(Base):
    __tablename__ = "assets"
    __table_args__ = (
        Index("ix_assets_tenant_agent", "tenant_id", "agent_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)

    name: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    environment: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)
    tags_json: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    agent_id: Mapped[Optional[str]] = mapped_column(String(64), index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    tenant: Mapped["Tenant"] = relationship()


class Agent(Base):
    __tablename__ = "agents"
    __table_args__ = (
        UniqueConstraint("tenant_id", "agent_id", name="uq_agents_tenant_agentid"),
        UniqueConstraint("tenant_id", "token_id", name="uq_agents_tenant_tokenid"),
        Index("ix_agents_token_id", "token_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)

    agent_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), index=True, nullable=False)

    token_id: Mapped[str] = mapped_column(String(32), nullable=False)  # at_xxx
    token_hash: Mapped[str] = mapped_column(Text, nullable=False)
    last_seen_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    tenant: Mapped["Tenant"] = relationship()
    asset: Mapped["Asset"] = relationship()


class Snapshot(Base):
    __tablename__ = "snapshots"
    __table_args__ = (
        Index("ix_snapshots_tenant_asset_collected", "tenant_id", "asset_id", "collected_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)

    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), index=True, nullable=False)
    agent_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)

    collected_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)

    payload_json: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    tenant: Mapped["Tenant"] = relationship()
    asset: Mapped["Asset"] = relationship()


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[int] = mapped_column(ForeignKey("tenants.id"), index=True, nullable=False)

    asset_id: Mapped[Optional[int]] = mapped_column(ForeignKey("assets.id"), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    markdown: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=utcnow, nullable=False)

    tenant: Mapped["Tenant"] = relationship()
    asset: Mapped[Optional["Asset"]] = relationship()
