from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime

from app.core.db import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    target = Column(String, index=True)
    type = Column(String)  # domain, ip, range
    created_at = Column(DateTime, default=datetime.utcnow)


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    target = Column(String)
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
