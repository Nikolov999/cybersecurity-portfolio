from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional
from .winlog import RawWinEvent

# IPv4 + IPv6 (best-effort)
_IPV4_RE = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")
_IPV6_RE = re.compile(r"\b(?:[A-F0-9]{1,4}:){2,7}[A-F0-9]{1,4}\b", re.IGNORECASE)

# Prefer Security-event labels when present
_RE_SRC_ADDR = re.compile(r"Source\s+Network\s+Address:\s*([^\r\n]+)", re.IGNORECASE)
_RE_IP_GENERIC = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
_RE_ACCOUNT_NAME = re.compile(r"Account\s+Name:\s*([^\r\n]+)", re.IGNORECASE)
_RE_SUBJECT_ACCOUNT = re.compile(r"Subject:\s*(?:\r?\n)+\s*Security\s+ID:\s*[^\r\n]+(?:\r?\n)+\s*Account\s+Name:\s*([^\r\n]+)", re.IGNORECASE)
_RE_TARGET_ACCOUNT = re.compile(r"Target\s+Account:\s*(?:\r?\n)+\s*Security\s+ID:\s*[^\r\n]+(?:\r?\n)+\s*Account\s+Name:\s*([^\r\n]+)", re.IGNORECASE)
_RE_NEW_ACCOUNT = re.compile(r"New\s+Account:\s*(?:\r?\n)+\s*Security\s+ID:\s*[^\r\n]+(?:\r?\n)+\s*Account\s+Name:\s*([^\r\n]+)", re.IGNORECASE)
_RE_MEMBER_NAME = re.compile(r"Member:\s*(?:\r?\n)+\s*Security\s+ID:\s*[^\r\n]+(?:\r?\n)+\s*Account\s+Name:\s*([^\r\n]+)", re.IGNORECASE)

# Exclude common non-user placeholders
_BAD_USERS = {"-", "n/a", "system", "localhost", "null"}


@dataclass
class ParsedEvent:
    event_id: int
    timestamp: str  # ISO UTC
    username: Optional[str]
    source_ip: Optional[str]
    raw: str


def _clean_user(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    v = s.strip()
    if not v:
        return None
    if v.lower() in _BAD_USERS:
        return None
    if v.startswith("S-1-5-"):
        return None
    return v


def _extract_source_ip(msg: str) -> Optional[str]:
    if not msg:
        return None

    # Best signal for Security 4624/4625 etc
    m = _RE_SRC_ADDR.search(msg)
    if m:
        v = (m.group(1) or "").strip()
        if v and v != "-" and v.lower() != "::1":
            # v can be "127.0.0.1" or "::1" or "-"
            if _IPV4_RE.search(v):
                ip = _IPV4_RE.search(v).group(0)
                if ip not in ("127.0.0.1", "0.0.0.0"):
                    return ip
            if _IPV6_RE.search(v):
                ip6 = _IPV6_RE.search(v).group(0)
                if ip6.lower() not in ("::1",):
                    return ip6

    # Fallback: first non-loopback ipv4 in message
    for m in _RE_IP_GENERIC.finditer(msg):
        ip = m.group(0)
        if ip in ("127.0.0.1", "0.0.0.0"):
            continue
        return ip

    # IPv6 fallback
    m6 = _IPV6_RE.search(msg)
    if m6:
        ip6 = m6.group(0)
        if ip6.lower() not in ("::1",):
            return ip6

    return None


def _extract_username_from_message(event_id: int, msg: str) -> Optional[str]:
    if not msg:
        return None

    # Prefer event-specific “Target/New/Member” fields when available:
    if event_id in (4624, 4625, 4648, 4672):
        # For logons, "Account Name" appears in Subject and New Logon.
        # Prefer Target Account block if present, else Subject.
        m = _RE_TARGET_ACCOUNT.search(msg)
        if m:
            u = _clean_user(m.group(1))
            if u:
                return u
        m = _RE_SUBJECT_ACCOUNT.search(msg)
        if m:
            u = _clean_user(m.group(1))
            if u:
                return u

    if event_id in (4720, 4722):
        # New Account block is usually the created/enabled account.
        m = _RE_NEW_ACCOUNT.search(msg)
        if m:
            u = _clean_user(m.group(1))
            if u:
                return u

    if event_id in (4732, 4733):
        # Member block is usually the account added/removed.
        m = _RE_MEMBER_NAME.search(msg)
        if m:
            u = _clean_user(m.group(1))
            if u:
                return u

    # Generic first "Account Name:" (best-effort)
    m = _RE_ACCOUNT_NAME.search(msg)
    if m:
        u = _clean_user(m.group(1))
        if u:
            return u

    return None


def _extract_username_fallback(strings: list[str]) -> Optional[str]:
    for s in strings:
        s = (s or "").strip()
        if not s:
            continue
        if s.startswith("S-1-5-"):
            continue
        if s.lower() in _BAD_USERS:
            continue
        if len(s) > 2 and "\\" in s:
            return s
        if len(s) > 2:
            return s
    return None


def parse_event(e: RawWinEvent) -> ParsedEvent:
    msg = e.message or ""
    source_ip = _extract_source_ip(msg)

    username = _extract_username_from_message(e.event_id, msg)
    if not username:
        username = _extract_username_fallback(e.strings)

    return ParsedEvent(
        event_id=e.event_id,
        timestamp=e.time_created.isoformat(),
        username=username,
        source_ip=source_ip,
        raw=msg,
    )