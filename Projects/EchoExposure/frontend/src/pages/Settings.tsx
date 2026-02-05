export function Settings() {
  return (
    <div className="space-y-6">
      <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10">
        <div className="text-sm font-medium">API Configuration</div>
        <div className="mt-2 text-xs text-white/60">Current API endpoint:</div>
        <div className="mt-2 rounded-xl bg-ink-900 px-3 py-2 text-sm ring-1 ring-white/10">
          http://127.0.0.1:9000
        </div>
      </div>

      <div className="rounded-2xl bg-white/[0.03] p-5 ring-1 ring-white/10">
        <div className="text-sm font-medium">EchoExposure</div>
        <div className="mt-2 text-xs text-white/60 leading-relaxed">
          Minimal backend. High-signal exposure tracking. Built for EchoPentest.
        </div>
      </div>
    </div>
  );
}
