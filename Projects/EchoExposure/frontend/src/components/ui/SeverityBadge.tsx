export function SeverityBadge({ level }: { level: "low" | "medium" | "high" }) {
  const styles =
    level === "high"
      ? "bg-rose-500/15 text-rose-200 ring-rose-400/30"
      : level === "medium"
      ? "bg-amber-500/15 text-amber-200 ring-amber-400/30"
      : "bg-emerald-500/15 text-emerald-200 ring-emerald-400/30";

  return (
    <span className={`rounded-full px-2 py-0.5 text-xs font-medium ring-1 ${styles}`}>
      {level.toUpperCase()}
    </span>
  );
}
