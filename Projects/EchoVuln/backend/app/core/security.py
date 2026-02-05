from __future__ import annotations

import base64
import hashlib
import hmac
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class HashRecord:
    algo: str
    salt_b64: str
    iters: int
    dklen: int
    hash_b64: str

    def to_string(self) -> str:
        # algo$salt$iters$dklen$hash
        return f"{self.algo}${self.salt_b64}${self.iters}${self.dklen}${self.hash_b64}"

    @staticmethod
    def from_string(s: str) -> "HashRecord":
        parts = s.split("$")
        if len(parts) != 5:
            raise ValueError("Invalid hash record format")
        algo, salt_b64, iters, dklen, hash_b64 = parts
        return HashRecord(algo=algo, salt_b64=salt_b64, iters=int(iters), dklen=int(dklen), hash_b64=hash_b64)


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).decode("utf-8").rstrip("=")


def _b64d(s: str) -> bytes:
    pad = "=" * (-len(s) % 4)
    return base64.urlsafe_b64decode((s + pad).encode("utf-8"))


def hash_secret(secret: str, *, iters: int, dklen: int = 32) -> str:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", secret.encode("utf-8"), salt, iters, dklen=dklen)
    rec = HashRecord(algo="pbkdf2_sha256", salt_b64=_b64(salt), iters=iters, dklen=dklen, hash_b64=_b64(dk))
    return rec.to_string()


def verify_secret(secret: str, stored: str) -> bool:
    try:
        rec = HashRecord.from_string(stored)
        if rec.algo != "pbkdf2_sha256":
            return False
        salt = _b64d(rec.salt_b64)
        expected = _b64d(rec.hash_b64)
        dk = hashlib.pbkdf2_hmac("sha256", secret.encode("utf-8"), salt, rec.iters, dklen=rec.dklen)
        return hmac.compare_digest(dk, expected)
    except Exception:
        return False


def mint_token(nbytes: int) -> str:
    # URL-safe token without padding
    return _b64(os.urandom(nbytes))
