from __future__ import annotations

from pathlib import Path
from secrets import token_urlsafe

from sqlalchemy import select

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.db.models import ApiKey, EnrollKey, Tenant
from app.core.security import hash_secret

ITERATIONS = 200_000

APP_VENDOR = "EchoPentest"
APP_NAME = "EchoVuln"


def programdata_dir() -> Path:
    return Path(r"C:\ProgramData") / APP_VENDOR / APP_NAME / "data"


def keys_out_path() -> Path:
    d = programdata_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d / "keys.txt"


def make_key(prefix: str) -> str:
    return f"{prefix}_{token_urlsafe(20)}.{token_urlsafe(32)}"


def main() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        tenant = db.execute(select(Tenant)).scalars().first()
        if not tenant:
            tenant = Tenant(name="default")
            db.add(tenant)
            db.commit()
            db.refresh(tenant)

        # wipe old keys
        db.query(ApiKey).delete()
        db.query(EnrollKey).delete()
        db.commit()

        admin_key = make_key("ak")
        enroll_key = make_key("ek")

        admin_key_id = admin_key.split(".", 1)[0]
        enroll_key_id = enroll_key.split(".", 1)[0]

        # IMPORTANT: hash the FULL compound key (matches auth.py verification)
        admin = ApiKey(
            tenant_id=tenant.id,
            key_id=admin_key_id,
            key_hash=hash_secret(admin_key, iters=ITERATIONS),
            label="admin",
        )

        enroll = EnrollKey(
            tenant_id=tenant.id,
            key_id=enroll_key_id,
            key_hash=hash_secret(enroll_key, iters=ITERATIONS),
            label="enroll",
        )

        db.add(admin)
        db.add(enroll)
        db.commit()

        text = (
            "================ EchoVuln Keys ================\n\n"
            f"ADMIN KEY:\n{admin_key}\n\n"
            f"ENROLL KEY:\n{enroll_key}\n\n"
            "==============================================\n"
        )
        keys_out_path().write_text(text, encoding="utf-8")
        print(text)
        print(f"Saved to: {keys_out_path()}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
