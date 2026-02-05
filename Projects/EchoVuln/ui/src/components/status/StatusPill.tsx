
export default function StatusPill(props: { kind: "ok" | "warn" | "err"; text: string }) {
  const cls = props.kind === "ok" ? "pill pillOk" : props.kind === "warn" ? "pill pillWarn" : "pill pillErr";
  return <span className={cls}>{props.text}</span>;
}
