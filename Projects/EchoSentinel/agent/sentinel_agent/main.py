from __future__ import annotations

import logging
import time
from typing import Dict

from .config import load_config
from .state import load_state, save_state, get_or_create_agent_id
from .utils import setup_logging, hostname
from .winlog import read_events_since_record
from .parse import parse_event
from .transport import BackendClient

log = logging.getLogger("echosentinel.agent")


def main():
    setup_logging()
    cfg = load_config()
    client = BackendClient(cfg.backend_url, cfg.api_key)

    host = hostname()
    agent_id = get_or_create_agent_id(cfg.state_dir)
    state: Dict[str, int] = load_state(cfg.state_dir)

    log.info("Agent started host=%s agent_id=%s backend=%s channels=%s event_ids=%s state_dir=%s",
             host, agent_id, cfg.backend_url, cfg.channels, sorted(cfg.event_ids), cfg.state_dir)

    while True:
        try:
            any_sent = 0
            for ch in cfg.channels:
                last = int(state.get(ch, 0))
                raw_events = read_events_since_record(channel=ch, min_record_id=last, max_events=300)

                max_rid = last
                for ev in raw_events:
                    if ev.event_id not in cfg.event_ids:
                        max_rid = max(max_rid, ev.record_id)
                        continue

                    parsed = parse_event(ev)
                    payload = {
                        "agent_id": agent_id,
                        "hostname": host,
                        "event_id": parsed.event_id,
                        "timestamp": parsed.timestamp,
                        "username": parsed.username,
                        "source_ip": parsed.source_ip,
                        "channel": ch,
                        "record_id": ev.record_id,
                        "raw": parsed.raw,
                    }

                    ok = client.ingest_event(payload)
                    if ok:
                        any_sent += 1
                        max_rid = max(max_rid, ev.record_id)
                    else:
                        # stop advancing record_id on failure to avoid gaps
                        log.warning("Ingest failed channel=%s record_id=%s event_id=%s", ch, ev.record_id, ev.event_id)
                        break

                if max_rid != last:
                    state[ch] = max_rid
                    save_state(cfg.state_dir, state)

            if any_sent:
                log.info("Sent %d events", any_sent)

        except Exception as e:
            log.exception("Loop error: %s", e)

        time.sleep(cfg.poll_seconds)


if __name__ == "__main__":
    main()