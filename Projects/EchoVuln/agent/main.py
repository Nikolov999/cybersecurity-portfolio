from __future__ import annotations

import sys
import time
import traceback
from datetime import datetime

from agent.config import load_settings
from agent.http_client import Http
from agent.identity import load_state, save_state
from agent.enroll import enroll_if_needed
from agent.heartbeat import send_heartbeat
from agent.snapshot import build_snapshot_payload, send_snapshot

def _log(msg: str) -> None:
    ts = datetime.utcnow().isoformat(timespec="seconds")
    print(f"[{ts}Z] {msg}", flush=True)

def run() -> int:
    s = load_settings(sys.argv[1:])
    http = Http(base_url=s.backend_url, verify_tls=s.verify_tls, timeout_seconds=s.timeout_seconds)

    st = load_state(s.state_path)

    # Enroll if needed
    token, new_asset_id = enroll_if_needed(http, enroll_key=s.enroll_key, agent_id=st.agent_id, existing_token=st.agent_token)
    st.agent_token = token
    if new_asset_id is not None:
        st.asset_id = new_asset_id
    save_state(s.state_path, st)

    _log(f"agent_id={st.agent_id} asset_id={st.asset_id} enrolled=1")

    next_hb = 0.0
    next_snap = 0.0

    while True:
        now = time.time()

        try:
            if now >= next_hb:
                send_heartbeat(http, st.agent_token)
                next_hb = now + s.heartbeat_seconds
                _log("heartbeat ok")

            if now >= next_snap:
                payload = build_snapshot_payload(
                    agent_id=st.agent_id,
                    asset_id=st.asset_id,
                    signal_internet_facing=s.signal_internet_facing,
                    signal_business_critical=s.signal_business_critical,
                )
                sid = send_snapshot(http, st.agent_token, payload)
                next_snap = now + s.snapshot_seconds
                _log(f"snapshot ok id={sid}")

        except Exception as e:
            _log(f"error: {e}")
            _log(traceback.format_exc())

            # If bearer token was revoked/invalid, force re-enroll on next loop.
            msg = str(e)
            if "401" in msg or "Invalid agent token" in msg:
                st.agent_token = None
                save_state(s.state_path, st)
                _log("token invalid -> cleared; will re-enroll if enroll_key present")

            time.sleep(5)

        time.sleep(1)

def main() -> None:
    try:
        raise SystemExit(run())
    except KeyboardInterrupt:
        raise SystemExit(0)

if __name__ == "__main__":
    main()
