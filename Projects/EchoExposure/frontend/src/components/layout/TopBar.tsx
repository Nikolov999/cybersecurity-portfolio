import { Badge } from "../ui/Badge";
import logo from "../../assets/logo.png";

export function TopBar({ apiUp }: { apiUp: boolean | null }) {
  const status =
    apiUp === null
      ? { label: "Checking API", tone: "muted" as const }
      : apiUp
      ? { label: "API Online", tone: "success" as const }
      : { label: "API Offline", tone: "danger" as const };

  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-ink-950/70 backdrop-blur">
      <div className="flex items-center justify-between px-4 py-3 sm:px-6">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-br from-neon-500/30 to-neon-700/10 ring-1 ring-white/10 shadow-glow grid place-items-center overflow-hidden">
            <img src={logo} alt="EchoExposure" className="h-7 w-auto" />
          </div>
          <div className="leading-tight">
            <div className="text-sm font-semibold">EchoExposure</div>
            <div className="text-xs text-white/60">
              External exposure inventory • change tracking
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Badge tone={status.tone}>{status.label}</Badge>
          <div className="hidden sm:block text-xs text-white/55">
            API: <span className="text-white/80">127.0.0.1:9000</span>
          </div>
        </div>
      </div>
    </header>
  );
}
