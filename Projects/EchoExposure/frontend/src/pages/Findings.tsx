import { useEffect, useMemo, useState } from "react";
import { api } from "../lib/api";
import { Scan } from "../lib/types";
import { SeverityBadge } from "../components/ui/SeverityBadge";

export function Findings() {
  const [scans, setScans] = useState<Scan[]>([]);

  useEffect(() => {
    api.listScans().then(setScans);
  }, []);

  const rows = useMemo(() => {
    return scans.flatMap((s) =>
      (s.result.services || []).map((svc) => ({
        target: s.target,
        port: svc.port,
        service: svc.service,
        severity: svc.severity,
        time: s.created_at,
        risk: s.result.risk_score,
      }))
    );
  }, [scans]);

  return (
    <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10">
      <div className="text-sm font-medium">Exposure Findings</div>
      <div className="mt-3 space-y-2 text-sm text-white/70">
        {rows.map((r, i) => (
          <div key={i} className="flex flex-col gap-1 border-b border-white/5 py-2 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center gap-2">
              <span className="text-white/85">
                {r.target} : {r.port}
              </span>
              <span className="text-xs text-white/45">{r.service}</span>
              <SeverityBadge level={r.severity} />
            </div>
            <div className="text-xs text-white/45">
              Risk <span className="text-neon-500 font-semibold">{r.risk}/100</span> •{" "}
              {new Date(r.time).toLocaleString()}
            </div>
          </div>
        ))}
        {!rows.length && <div className="text-sm text-white/55">No findings yet. Run a scan.</div>}
      </div>
    </div>
  );
}
