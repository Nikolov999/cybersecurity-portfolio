import { api } from "../client/http";

export type Asset = {
  id: number;
  name: string;
  description?: string | null;
  environment?: string | null;
  tags?: string[] | null;
  agent_id?: string | null;
  created_at: string;
};

export type AssetCreate = {
  name: string;
  description?: string | null;
  environment?: string | null;
  tags?: string[] | null;
  agent_id?: string | null;
};

export async function listAssets(): Promise<Asset[]> {
  return api<Asset[]>("/v2/assets", "GET");
}

export async function createAsset(payload: AssetCreate): Promise<Asset> {
  return api<Asset>("/v2/assets", "POST", payload);
}

export async function deleteAsset(id: number): Promise<{ ok: boolean }> {
  return api<{ ok: boolean }>(`/v2/assets/${id}`, "DELETE");
}
