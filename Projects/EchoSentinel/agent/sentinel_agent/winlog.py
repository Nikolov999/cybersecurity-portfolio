from __future__ import annotations

import win32evtlog  # type: ignore
import win32evtlogutil  # type: ignore
import win32con  # type: ignore

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import List


@dataclass
class RawWinEvent:
    channel: str
    record_id: int
    event_id: int
    time_created: datetime
    source_name: str
    strings: list[str]  # rendered strings (varies by provider)
    message: str        # formatted message best-effort


def _to_utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def read_events_since_record(
    channel: str,
    min_record_id: int,
    max_events: int = 250,
) -> List[RawWinEvent]:
    """
    Reads forward from the newest and returns events with record_id > min_record_id.
    Uses backwards read then reverses to preserve chronological order.
    """
    try:
        handle = win32evtlog.OpenEventLog(None, channel)
    except Exception:
        return []

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ

    out: list[RawWinEvent] = []
    total = 0

    while total < max_events:
        try:
            events = win32evtlog.ReadEventLog(handle, flags, 0)
        except Exception:
            break

        if not events:
            break

        for e in events:
            rid = int(e.RecordNumber)
            if rid <= min_record_id:
                # since reading backwards, we can stop once we reach old records
                try:
                    win32evtlog.CloseEventLog(handle)
                except Exception:
                    pass
                out.reverse()
                return out

            event_id = int(e.EventID & 0xFFFF)
            t = _to_utc(e.TimeGenerated)
            src = str(e.SourceName)
            strings = list(e.StringInserts or [])
            try:
                msg = win32evtlogutil.SafeFormatMessage(e, channel)
            except Exception:
                msg = " ".join(strings) if strings else src

            out.append(
                RawWinEvent(
                    channel=channel,
                    record_id=rid,
                    event_id=event_id,
                    time_created=t,
                    source_name=src,
                    strings=strings,
                    message=msg,
                )
            )
            total += 1
            if total >= max_events:
                break

    try:
        win32evtlog.CloseEventLog(handle)
    except Exception:
        pass
    out.reverse()
    return out