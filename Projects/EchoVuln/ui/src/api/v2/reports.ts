import { api } from "../client/http";

export type Report = {
  id: number;
  asset_id?: number | null;
  title: string;
  markdown: string;
  created_at: string;
};

export type ReportCreate = {
  asset_id?: number | null;
  title: string;
  markdown: string;
};

export async function listReports(): Promise<Report[]> {
  return api<Report[]>("/v2/reports", "GET");
}

export async function createReport(payload: ReportCreate): Promise<Report> {
  return api<Report>("/v2/reports", "POST", payload);
}

export async function getReport(id: number): Promise<Report> {
  return api<Report>(`/v2/reports/${id}`, "GET");
}

export async function deleteReport(id: number): Promise<{ ok: boolean }> {
  return api<{ ok: boolean }>(`/v2/reports/${id}`, "DELETE");
}
