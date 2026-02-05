import { useAppStore } from "../../state/useAppStore";
import { cls } from "../../lib/utils";
import logo from "../../assets/logo.png";

type Item = {
  key: "dashboard" | "assets" | "scans" | "surface" | "findings" | "settings";
  label: string;
  hint: string;
};

const items: Item[] = [
  { key: "dashboard", label: "Dashboard", hint: "Overview + signals" },
  { key: "assets", label: "Assets", hint: "Domains / IPs tracked" },
  { key: "scans", label: "Scans", hint: "Run + history" },
  { key: "surface", label: "Attack Surface", hint: "Map + risk" },
  { key: "findings", label: "Findings", hint: "Ports + changes" },
  { key: "settings", label: "Settings", hint: "API + preferences" },
];

export function SideNav() {
  const page = useAppStore((s) => s.page);
  const setPage = useAppStore((s) => s.setPage);

  return (
    <aside className="hidden w-72 shrink-0 border-r border-white/10 bg-ink-950/60 px-4 py-5 backdrop-blur lg:block">
      <div className="mb-5 flex items-center gap-3">
        <div className="h-10 w-10 overflow-hidden rounded-2xl ring-1 ring-white/10 shadow-glow bg-gradient-to-br from-neon-500/35 to-neon-700/10 grid place-items-center">
          <img src={logo} alt="EchoExposure" className="h-8 w-auto" />
        </div>
        <div>
          <div className="text-sm font-semibold">EchoExposure</div>
          <div className="text-xs text-white/55">Minimal backend • premium UI</div>
        </div>
      </div>

      <nav className="space-y-2">
        {items.map((it) => {
          const active = page === it.key;
          return (
            <button
              key={it.key}
              onClick={() => setPage(it.key)}
              className={cls(
                "w-full rounded-2xl px-3 py-3 text-left ring-1 transition",
                active
                  ? "bg-gradient-to-r from-neon-500/20 to-neon-700/10 ring-neon-500/35 shadow-glow"
                  : "bg-white/[0.03] ring-white/10 hover:bg-white/[0.05] hover:ring-white/20"
              )}
            >
              <div className="flex items-center justify-between">
                <div className="text-sm font-medium">{it.label}</div>
                <span className={cls("text-[11px]", active ? "text-neon-500" : "text-white/40")}>
                  ↳
                </span>
              </div>
              <div className="mt-1 text-xs text-white/55">{it.hint}</div>
            </button>
          );
        })}
      </nav>

      <div className="mt-6 rounded-2xl bg-white/[0.03] p-3 ring-1 ring-white/10">
        <div className="text-xs font-medium text-white/70">Brand assets</div>
        <div className="mt-2 text-xs text-white/55 leading-relaxed">
          UI logo: <span className="text-white/80">src/assets/logo.png</span>
          <br />
          Installer icon: <span className="text-white/80">src-tauri/icons/icon.ico</span>
          <br />
          Bundle logo: <span className="text-white/80">src-tauri/icons/echopentest-logo.png</span>
        </div>
      </div>
    </aside>
  );
}
