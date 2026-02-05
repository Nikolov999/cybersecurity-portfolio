import { api } from "../client/http";

export type TopFixItem = {
  score: number;
  headline: string;
  fix_action: string;
  why_now: string;
  references?: string[] | null;
};

export type TopFixesResponse = { items: TopFixItem[] };

export async function computeTopFixes(assetId?: number, limit = 10): Promise<TopFixesResponse> {
  return api<TopFixesResponse>("/v2/top-fixes", "POST", { asset_id: assetId ?? null, limit });
}
