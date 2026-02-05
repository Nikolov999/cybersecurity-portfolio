from __future__ import annotations

import json
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Snapshot
from app.models.schemas import TopFixItem


def _clamp(x: int) -> int:
    return max(0, min(100, x))


def compute_top_fixes_v2(db: Session, tenant_id: int, asset_id: Optional[int], limit: int) -> List[TopFixItem]:
    limit = max(1, min(limit, 50))

    q = select(Snapshot).where(Snapshot.tenant_id == tenant_id)
    if asset_id is not None:
        q = q.where(Snapshot.asset_id == asset_id)

    # Use most recent snapshot per asset (v2 minimum viable)
    # For tenant-wide: pick the most recent N snapshots and aggregate heuristically.
    rows = db.execute(q.order_by(Snapshot.collected_at.desc()).limit(50)).scalars().all()
    if not rows:
        return [
            TopFixItem(
                score=0,
                headline="No snapshots received yet.",
                fix_action="Install and enroll the agent, then send a snapshot.",
                why_now="No endpoint telemetry exists for prioritization.",
                references=None,
            )
        ]

    # Simple aggregation based on v2 scoring principles using available fields.
    # Missing updates become the driver; signals + reboot_pending adjust.
    fixes: List[TopFixItem] = []

    for snap in rows:
        p = json.loads(snap.payload_json)
        missing = p.get("missing_updates") or []
        reboot = bool(p.get("reboot_pending") or False)
        signals = p.get("signals") or {}
        internet_facing = bool(signals.get("internet_facing", False))
        business_critical = bool(signals.get("business_critical", False))

        patch_gap = len(missing)
        patch_gap_points = min(15, int((patch_gap / 20) * 15))  # normalize to 0..15
        reboot_points = 5 if reboot else 0
        exposure_points = 25 if internet_facing else 0
        critical_points = 20 if business_critical else 0

        # Exploit/KEV signals are placeholders until you wire feeds.
        exploit_points = 0
        kev_points = 0
        auth_points = 0

        base_score = _clamp(exposure_points + auth_points + exploit_points + kev_points + critical_points + patch_gap_points + reboot_points)

        if patch_gap > 0:
            refs = []
            for mu in missing[:10]:
                kb = (mu or {}).get("kb")
                cve = (mu or {}).get("cve")
                if kb:
                    refs.append(kb)
                if cve:
                    refs.append(cve)

            fixes.append(
                TopFixItem(
                    score=base_score if base_score > 0 else min(40, 10 + patch_gap_points),
                    headline="Patch the endpoint to close known update gaps.",
                    fix_action="Apply the latest cumulative updates and any pending security updates, then reboot if required.",
                    why_now=f"{patch_gap} missing update(s) detected; reboot pending={reboot}.",
                    references=refs or None,
                )
            )

        if reboot and patch_gap == 0:
            fixes.append(
                TopFixItem(
                    score=_clamp(25 + exposure_points + critical_points),
                    headline="Complete the pending reboot to finalize security state.",
                    fix_action="Reboot the endpoint during a maintenance window.",
                    why_now="Reboot pending can leave patches partially applied and reduce confidence in posture.",
                    references=None,
                )
            )

        # Only use the most recent snapshot for that asset when asset_id specified
        if asset_id is not None:
            break

    # De-duplicate by headline for MVP
    seen = set()
    deduped: List[TopFixItem] = []
    for f in sorted(fixes, key=lambda x: x.score, reverse=True):
        if f.headline in seen:
            continue
        seen.add(f.headline)
        deduped.append(f)
        if len(deduped) >= limit:
            break

    if not deduped:
        deduped = [
            TopFixItem(
                score=5,
                headline="No immediate fixes detected from latest snapshot.",
                fix_action="Keep agents reporting snapshots on schedule.",
                why_now="Prioritization requires continuous telemetry.",
                references=None,
            )
        ]

    return deduped
