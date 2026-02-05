from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path
from secrets import token_urlsafe

import uvicorn
from sqlalchemy import select

from app.core.security import hash_secret
from app.db.base import Base
from app.db.models import ApiKey, EnrollKey, Tenant
from app.db.session import SessionLocal, engine

ITERATIONS = int(os.getenv("ECHO_PBKDF2_ITERS", "200000"))

APP_VENDOR = "EchoPentest"
APP_NAME = "EchoVuln"


def programdata_dir() -> Path:
    pd = os.environ.get("PROGRAMDATA", r"C:\ProgramData")
    return Path(pd) / APP_VENDOR / APP_NAME / "data"


def keys_out_path() -> Path:
    return programdata_dir() / "keys.txt"


def make_key(prefix: str) -> str:
    return f"{prefix}_{token_urlsafe(20)}.{token_urlsafe(32)}"


def bootstrap_if_empty() -> None:
    Base.metadata.create_all(bind=engine)

    d = programdata_dir()
    d.mkdir(parents=True, exist_ok=True)

    db = SessionLocal()
    try:
        tenant = db.execute(select(Tenant)).scalars().first()
        if not tenant:
            tenant = Tenant(name="default")
            db.add(tenant)
            db.commit()
            db.refresh(tenant)

        has_admin = db.execute(select(ApiKey).limit(1)).first() is not None
        has_enroll = db.execute(select(EnrollKey).limit(1)).first() is not None
        if has_admin and has_enroll:
            return

        admin_key = make_key("ak")
        enroll_key = make_key("ek")

        # CHANGE 1: hash FULL compound admin key
        db.add(
            ApiKey(
                tenant_id=tenant.id,
                key_id=admin_key.split(".", 1)[0],
                key_hash=hash_secret(admin_key, iters=ITERATIONS),
                label="admin",
            )
        )

        # CHANGE 2: hash FULL compound enroll key
        db.add(
            EnrollKey(
                tenant_id=tenant.id,
                key_id=enroll_key.split(".", 1)[0],
                key_hash=hash_secret(enroll_key, iters=ITERATIONS),
                label="enroll",
            )
        )

        db.commit()

        text = (
            "================ EchoVuln Keys ================\n\n"
            f"ADMIN KEY:\n{admin_key}\n\n"
            f"ENROLL KEY:\n{enroll_key}\n\n"
            "================================================\n"
        )
        keys_out_path().write_text(text, encoding="utf-8")
    finally:
        db.close()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--host", default=os.getenv("ECHO_HOST", "127.0.0.1"))
    p.add_argument("--port", type=int, default=int(os.getenv("ECHO_PORT", "8000")))
    return p.parse_args()


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def main() -> None:
    setup_logging()
    bootstrap_if_empty()
    args = parse_args()

    config = uvicorn.Config(
        "app.main:app",
        host=args.host,
        port=args.port,
        log_config=None,
        access_log=False,
    )
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    main()
