import { api } from "../client/http";

export type Snapshot = {
  id: number;
  asset_id: number;
  agent_id: string;
  collected_at_utc: string;
  payload: any;
};

export async function listAssetSnapshots(assetId: number, limit = 50): Promise<Snapshot[]> {
  return api<Snapshot[]>(`/v2/assets/${assetId}/snapshots?limit=${limit}`, "GET");
}
