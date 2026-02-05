import { useEffect, useState } from "react";
import { api } from "../lib/api";
import { Scan } from "../lib/types";
import { SeverityBadge } from "../components/ui/SeverityBadge";

export function AttackSurface() {
  const [scans, setScans] = useState<Scan[]>([]);

  useEffect(() => {
    api.listScans().then(setScans);
  }, []);

  return (
    <div className="space-y-6">
      {scans.map((s) => (
        <div
          key={s.id}
          className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10 shadow-glow"
        >
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div className="text-sm font-medium">{s.target}</div>
            <div className="text-xs text-white/60">
              Risk Score{" "}
              <span className="text-neon-500 font-semibold">{s.result.risk_score}/100</span>
            </div>
          </div>

          <div className="mt-1 text-xs text-white/55">
            IP: <span className="text-white/75">{s.result.resolved_ip || "unknown"}</span>
          </div>

          <div className="mt-4 grid gap-2 md:grid-cols-2">
            {s.result.services?.map((svc, i) => (
              <div
                key={i}
                className="flex items-center justify-between rounded-xl bg-ink-900/60 px-3 py-2 ring-1 ring-white/5"
              >
                <div className="text-sm text-white/80">
                  <span className="text-white">{svc.service}</span>
                  <span className="text-white/50"> :</span> {svc.port}
                </div>
                <SeverityBadge level={svc.severity} />
              </div>
            ))}
            {!s.result.services?.length && (
              <div className="text-sm text-white/55">No services recorded for this scan.</div>
            )}
          </div>

          {!!s.result.tags?.length && (
            <div className="mt-3 flex flex-wrap gap-2">
              {s.result.tags.map((t) => (
                <span
                  key={t}
                  className="rounded-lg bg-neon-500/10 px-2 py-1 text-xs text-neon-200 ring-1 ring-neon-500/20"
                >
                  #{t}
                </span>
              ))}
            </div>
          )}
        </div>
      ))}
      {!scans.length && (
        <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10 text-sm text-white/60">
          No scans yet. Run a scan first.
        </div>
      )}
    </div>
  );
}
