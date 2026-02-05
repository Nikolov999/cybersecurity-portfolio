export const API_BASE = "http://127.0.0.1:9000";

async function request(path: string, options?: RequestInit) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "API error");
  }

  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) return res.json();
  return null;
}

export const api = {
  health: () => request("/api/health"),

  listAssets: () => request("/api/assets"),
  addAsset: (target: string, type = "domain") =>
    request(`/api/assets?target=${encodeURIComponent(target)}&type=${type}`, { method: "POST" }),
  deleteAsset: (id: number) => request(`/api/assets/${id}`, { method: "DELETE" }),

  listScans: () => request("/api/scan"),
  runScan: (target: string) =>
    request(`/api/scan?target=${encodeURIComponent(target)}`, { method: "POST" }),
  deleteScan: (id: number) => request(`/api/scan/${id}`, { method: "DELETE" }),
  clearScans: () => request(`/api/scan`, { method: "DELETE" }),
};
