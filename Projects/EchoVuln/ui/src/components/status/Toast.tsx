
export default function Toast(props: { toasts: Array<{ id: string; kind: "ok" | "warn" | "err"; title: string; detail?: string }> }) {
  return (
    <div className="toastStack">
      {props.toasts.map((t) => (
        <div key={t.id} className={"toast " + (t.kind === "ok" ? "toastOk" : t.kind === "warn" ? "toastWarn" : "toastErr")}>
          <div className="toastTitle">{t.title}</div>
          {t.detail && <div className="toastDetail">{t.detail}</div>}
        </div>
      ))}
    </div>
  );
}
