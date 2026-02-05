import { ReactNode } from "react";
import { cls } from "../../lib/utils";

type Tone = "muted" | "success" | "danger";

export function Badge({ children, tone = "muted" }: { children: ReactNode; tone?: Tone }) {
  const styles =
    tone === "success"
      ? "bg-emerald-500/10 text-emerald-200 ring-emerald-400/20"
      : tone === "danger"
      ? "bg-rose-500/10 text-rose-200 ring-rose-400/20"
      : "bg-white/5 text-white/70 ring-white/10";

  return (
    <span
      className={cls(
        "inline-flex items-center rounded-full px-3 py-1 text-[11px] font-medium ring-1",
        styles
      )}
    >
      {children}
    </span>
  );
}
