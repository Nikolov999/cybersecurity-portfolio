import { useEffect, useState } from "react";
import { api } from "../lib/api";
import { Asset, Scan } from "../lib/types";

export function Dashboard() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [scans, setScans] = useState<Scan[]>([]);

  useEffect(() => {
    api.listAssets().then(setAssets);
    api.listScans().then(setScans);
  }, []);

  const openPorts = scans.reduce((acc, s) => acc + (s.result.ports?.length || 0), 0);
  const avgRisk =
    scans.length === 0
      ? 0
      : Math.round(scans.reduce((a, s) => a + (s.result.risk_score || 0), 0) / scans.length);

  return (
    <div className="grid gap-6 md:grid-cols-4">
      <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10 shadow-glow">
        <div className="text-xs text-white/60">Tracked Assets</div>
        <div className="mt-2 text-3xl font-semibold">{assets.length}</div>
      </div>

      <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10 shadow-glow">
        <div className="text-xs text-white/60">Scans Executed</div>
        <div className="mt-2 text-3xl font-semibold">{scans.length}</div>
      </div>

      <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10 shadow-glow">
        <div className="text-xs text-white/60">Open Ports Found</div>
        <div className="mt-2 text-3xl font-semibold">{openPorts}</div>
      </div>

      <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10 shadow-glow">
        <div className="text-xs text-white/60">Average Risk</div>
        <div className="mt-2 text-3xl font-semibold text-neon-500">{avgRisk}/100</div>
      </div>

      <div className="md:col-span-4 rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10">
        <div className="text-sm font-medium">Latest Scans</div>
        <div className="mt-3 space-y-2 text-sm text-white/70">
          {scans.slice(0, 6).map((s) => (
            <div key={s.id} className="flex flex-col gap-1 border-b border-white/5 py-2 sm:flex-row sm:items-center sm:justify-between">
              <span className="text-white/85">{s.target}</span>
              <span className="text-xs text-white/55">
                Risk <span className="text-neon-500 font-semibold">{s.result.risk_score}/100</span>{" "}
                • Ports: {s.result.ports?.join(", ") || "none"}
              </span>
            </div>
          ))}
          {!scans.length && <div className="text-sm text-white/55">No scans yet.</div>}
        </div>
      </div>
    </div>
  );
}
