import os
from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

APP_DIR_NAME = "EchoExposure"


def get_data_dir() -> Path:
    # 1) Explicit override (best for NSSM/Windows service)
    override = os.environ.get("ECHOEXPOSURE_DATA_DIR")
    if override:
        p = Path(override)
        p.mkdir(parents=True, exist_ok=True)
        return p

    # 2) Service-safe default (ProgramData)
    programdata = os.environ.get("PROGRAMDATA")
    if programdata:
        p = Path(programdata) / "EchoPentest" / APP_DIR_NAME
        p.mkdir(parents=True, exist_ok=True)
        return p

    # 3) User-mode fallback (LOCALAPPDATA / home)
    base = os.environ.get("LOCALAPPDATA") or str(Path.home())
    p = Path(base) / APP_DIR_NAME
    p.mkdir(parents=True, exist_ok=True)
    return p


DB_PATH = get_data_dir() / "echoexposure.db"
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH.as_posix()}"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Base(DeclarativeBase):
    pass


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
