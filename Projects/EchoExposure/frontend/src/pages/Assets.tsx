import { useEffect, useState } from "react";
import { api } from "../lib/api";
import { Asset } from "../lib/types";

export function Assets() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [target, setTarget] = useState("");
  const [busyId, setBusyId] = useState<number | null>(null);

  const load = () => api.listAssets().then(setAssets);

  useEffect(() => {
    load();
  }, []);

  async function add() {
    if (!target.trim()) return;
    await api.addAsset(target);
    setTarget("");
    load();
  }

  async function remove(id: number) {
    setBusyId(id);
    try {
      await api.deleteAsset(id);
      await load();
    } finally {
      setBusyId(null);
    }
  }

  return (
    <div className="space-y-6">
      <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10">
        <div className="text-sm font-medium">Add Asset</div>
        <div className="mt-3 flex gap-3">
          <input
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            placeholder="example.com"
            className="flex-1 rounded-xl bg-ink-900 px-3 py-2 text-sm ring-1 ring-white/10 focus:outline-none focus:ring-neon-500/40"
          />
          <button
            onClick={add}
            className="rounded-xl bg-gradient-to-r from-neon-500 to-neon-700 px-4 py-2 text-sm font-medium shadow-glow"
          >
            Add
          </button>
        </div>
      </div>

      <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10">
        <div className="text-sm font-medium">Tracked Assets</div>

        <div className="mt-3 space-y-2 text-sm text-white/70">
          {assets.map((a) => (
            <div
              key={a.id}
              className="flex items-center justify-between gap-3 rounded-xl bg-ink-900/40 px-3 py-2 ring-1 ring-white/5"
            >
              <div className="min-w-0">
                <div className="truncate text-white/90">{a.target}</div>
                <div className="text-xs text-white/45">{a.type}</div>
              </div>

              <button
                onClick={() => remove(a.id)}
                disabled={busyId === a.id}
                className="shrink-0 rounded-xl bg-rose-500/15 px-3 py-2 text-xs font-medium text-rose-200 ring-1 ring-rose-400/25 hover:bg-rose-500/20 disabled:opacity-50"
              >
                {busyId === a.id ? "Deleting..." : "Delete"}
              </button>
            </div>
          ))}

          {!assets.length && <div className="text-sm text-white/55">No assets yet.</div>}
        </div>
      </div>
    </div>
  );
}
