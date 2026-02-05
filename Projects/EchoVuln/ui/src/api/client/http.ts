import { getConfig } from "../../store";

export type HttpMethod = "GET" | "POST" | "DELETE";

export class ApiError extends Error {
  status: number;
  body?: any;
  constructor(status: number, message: string, body?: any) {
    super(message);
    this.status = status;
    this.body = body;
  }
}

export async function api<T>(
  path: string,
  method: HttpMethod = "GET",
  body?: any,
  headers?: Record<string, string>
): Promise<T> {
  const cfg = getConfig();
  const base = cfg.backendUrl.replace(/\/+$/, "");
  const url = `${base}${path}`;

  const h: Record<string, string> = {
    "Content-Type": "application/json",
    ...(headers || {}),
  };

  // Admin UI uses X-API-Key
  if (cfg.adminKey) {
    h["X-API-Key"] = cfg.adminKey;
  }

  const res = await fetch(url, {
    method,
    headers: h,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  const text = await res.text();
  const data = text ? safeJson(text) : null;

  if (!res.ok) {
    throw new ApiError(res.status, data?.detail || `HTTP ${res.status}`, data);
  }

  return data as T;
}

function safeJson(s: string) {
  try {
    return JSON.parse(s);
  } catch {
    return { raw: s };
  }
}
