export function Footer() {
  return (
    <footer className="border-t border-white/10 px-4 py-3 text-xs text-white/50 sm:px-6">
      <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
        <div>EchoExposure • Local-first exposure tracking</div>
        <div className="text-white/40">© {new Date().getFullYear()}</div>
      </div>
    </footer>
  );
}
