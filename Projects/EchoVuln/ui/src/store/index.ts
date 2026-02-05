import { useEffect, useMemo, useState } from "react";

type AppConfig = {
  backendUrl: string;
  adminKey: string;
};

const KEY = "echovuln.config.v1";

let _cfg: AppConfig = load();

function load(): AppConfig {
  try {
    const raw = localStorage.getItem(KEY);
    if (!raw) return { backendUrl: "http://127.0.0.1:8000", adminKey: "" };
    const parsed = JSON.parse(raw);
    return {
      backendUrl: typeof parsed.backendUrl === "string" ? parsed.backendUrl : "http://127.0.0.1:8000",
      adminKey: typeof parsed.adminKey === "string" ? parsed.adminKey : "",
    };
  } catch {
    return { backendUrl: "http://127.0.0.1:8000", adminKey: "" };
  }
}

function save(cfg: AppConfig) {
  _cfg = cfg;
  localStorage.setItem(KEY, JSON.stringify(cfg));
}

export function getConfig(): AppConfig {
  return _cfg;
}

type Toast = { id: string; kind: "ok" | "warn" | "err"; title: string; detail?: string };

const toastKey = "echovuln.toast.seq";

export function useAppConfig() {
  const [cfg, setCfg] = useState<AppConfig>(() => getConfig());
  const [toasts, setToasts] = useState<Toast[]>([]);

  useEffect(() => {
    const onStorage = () => setCfg(getConfig());
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  const isConfigured = useMemo(() => {
    return Boolean(cfg.backendUrl && cfg.adminKey);
  }, [cfg.backendUrl, cfg.adminKey]);

  function update(next: AppConfig) {
    save(next);
    setCfg(next);
  }

  function pushToast(kind: Toast["kind"], title: string, detail?: string) {
    const seq = (Number(localStorage.getItem(toastKey) || "0") + 1).toString();
    localStorage.setItem(toastKey, seq);
    const id = `t_${Date.now()}_${seq}`;
    const t: Toast = { id, kind, title, detail };
    setToasts((p) => [t, ...p].slice(0, 5));
    setTimeout(() => setToasts((p) => p.filter((x) => x.id !== id)), 3500);
  }

  return { cfg, isConfigured, update, toasts, pushToast };
}
