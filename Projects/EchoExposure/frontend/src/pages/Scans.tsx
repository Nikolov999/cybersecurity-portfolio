import { useEffect, useState } from "react";
import { api } from "../lib/api";
import { Scan } from "../lib/types";

export function Scans() {
  const [target, setTarget] = useState("");
  const [scans, setScans] = useState<Scan[]>([]);
  const [loading, setLoading] = useState(false);
  const [busyScanId, setBusyScanId] = useState<number | null>(null);
  const [clearing, setClearing] = useState(false);

  const load = () => api.listScans().then(setScans);

  useEffect(() => {
    load();
  }, []);

  async function run() {
    if (!target.trim()) return;
    setLoading(true);
    try {
      await api.runScan(target);
      setTarget("");
      await load();
    } finally {
      setLoading(false);
    }
  }

  async function removeScan(id: number) {
    setBusyScanId(id);
    try {
      await api.deleteScan(id);
      await load();
    } finally {
      setBusyScanId(null);
    }
  }

  async function clearAll() {
    setClearing(true);
    try {
      await api.clearScans();
      await load();
    } finally {
      setClearing(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <div className="text-sm font-medium">Run Scan</div>
            <div className="mt-1 text-xs text-white/55">Target a domain or IP.</div>
          </div>

          <button
            onClick={clearAll}
            disabled={clearing || scans.length === 0}
            className="rounded-xl bg-white/[0.06] px-4 py-2 text-xs font-medium text-white/75 ring-1 ring-white/10 hover:bg-white/[0.08] disabled:opacity-50"
          >
            {clearing ? "Clearing..." : "Clear History"}
          </button>
        </div>

        <div className="mt-4 flex gap-3">
          <input
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="example.com"
            className="flex-1 rounded-xl bg-ink-900 px-3 py-2 text-sm ring-1 ring-white/10 focus:outline-none focus:ring-neon-500/40"
          />
          <button
            onClick={run}
            disabled={loading}
            className="rounded-xl bg-gradient-to-r from-neon-500 to-neon-700 px-4 py-2 text-sm font-medium shadow-glow disabled:opacity-50"
          >
            {loading ? "Scanning..." : "Scan"}
          </button>
        </div>
      </div>

      <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10">
        <div className="text-sm font-medium">Scan History</div>

        <div className="mt-3 space-y-3 text-sm text-white/70">
          {scans.map((s) => (
            <div key={s.id} className="rounded-xl bg-ink-900/60 p-3 ring-1 ring-white/5">
              <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                <div className="min-w-0">
                  <div className="truncate text-white/90">{s.target}</div>
                  <div className="text-xs text-white/40">{new Date(s.created_at).toLocaleString()}</div>
                </div>

                <button
                  onClick={() => removeScan(s.id)}
                  disabled={busyScanId === s.id}
                  className="w-fit rounded-xl bg-rose-500/15 px-3 py-2 text-xs font-medium text-rose-200 ring-1 ring-rose-400/25 hover:bg-rose-500/20 disabled:opacity-50"
                >
                  {busyScanId === s.id ? "Deleting..." : "Delete"}
                </button>
              </div>

              <div className="mt-2 text-xs text-white/60">
                Risk: <span className="text-neon-500 font-semibold">{(s.result as any).risk_score ?? 0}/100</span>
              </div>

              <div className="mt-1 text-xs text-white/60">
                Open ports: {s.result.ports?.join(", ") || "none"}
              </div>

              {(s.result as any).resolved_ip && (
                <div className="mt-1 text-xs text-white/50">IP: {(s.result as any).resolved_ip}</div>
              )}

              {!!(s.result as any).tags?.length && (
                <div className="mt-2 flex flex-wrap gap-2">
                  {(s.result as any).tags.map((t: string) => (
                    <span
                      key={t}
                      className="rounded-lg bg-neon-500/10 px-2 py-0.5 text-[11px] text-neon-200 ring-1 ring-neon-500/20"
                    >
                      #{t}
                    </span>
                  ))}
                </div>
              )}
            </div>
          ))}

          {!scans.length && <div className="text-sm text-white/55">No scans yet.</div>}
        </div>
      </div>
    </div>
  );
}
