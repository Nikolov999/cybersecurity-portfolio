import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import Card from "../../components/common/Card";
import Button from "../../components/common/Button";
import Empty from "../../components/common/Empty";
import DataTable from "../../components/tables/DataTable";
import { listAssets, Asset } from "../../api/v2/assets";
import { listAssetSnapshots, Snapshot } from "../../api/v2/snapshots";
import { computeTopFixes, TopFixItem } from "../../api/v2/topfixes";
import { fmtIso } from "../../utils/formatters/time";
import { useAppConfig } from "../../store";

export default function AssetDetail() {
  const { pushToast } = useAppConfig();
  const { id } = useParams();
  const assetId = Number(id);

  const [asset, setAsset] = useState<Asset | null>(null);
  const [snaps, setSnaps] = useState<Snapshot[]>([]);
  const [top, setTop] = useState<TopFixItem[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [rawOpen, setRawOpen] = useState<number | null>(null);

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const assets = await listAssets();
        setAsset(assets.find((a) => a.id === assetId) || null);
        setSnaps(await listAssetSnapshots(assetId, 50));
      } catch (e: any) {
        pushToast("err", "Asset load failed", e?.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [assetId, pushToast]);

  const latest = useMemo(() => snaps[0]?.payload ?? null, [snaps]);

  async function loadTopFixes() {
    try {
      setLoading(true);
      const res = await computeTopFixes(assetId, 10);
      setTop(res.items);
      pushToast("ok", "Priorities updated");
    } catch (e: any) {
      pushToast("err", "Could not load priorities", e?.message);
    } finally {
      setLoading(false);
    }
  }

  if (loading && !asset) {
    return (
      <div className="stack">
        <Card title="Loading" subtitle="Fetching asset details…">
          <div className="callout">
            <div className="strong">Please wait</div>
            <div className="muted">This usually takes a second.</div>
          </div>
        </Card>
      </div>
    );
  }

  if (!asset) {
    return (
      <Empty
        title="Asset not found"
        detail="Return to Assets and select a valid asset."
      />
    );
  }

  const agentLabel = asset.agent_id ? `Agent ID: ${asset.agent_id}` : "No agent connected";

  return (
    <div className="stack">
      <Card
        title={asset.name}
        subtitle={`${agentLabel}${asset.environment ? ` · Group: ${asset.environment}` : ""}`}
        right={
          <Button onClick={loadTopFixes} disabled={loading}>
            {loading ? "Working…" : "Update priorities"}
          </Button>
        }
      >
        {loading && (
          <div className="callout" style={{ marginBottom: 14 }}>
            <div className="strong">Refreshing</div>
            <div className="muted">Updating data from the server.</div>
          </div>
        )}

        {latest ? (
          <div className="grid3">
            <div className="callout">
              <div className="strong">Operating system</div>
              <div className="muted">{latest.os?.name || "-"}</div>
            </div>
            <div className="callout">
              <div className="strong">Restart required</div>
              <div className="muted">{Boolean(latest.reboot_pending) ? "Yes" : "No"}</div>
            </div>
            <div className="callout">
              <div className="strong">Missing updates</div>
              <div className="muted">{String((latest.missing_updates || []).length)}</div>
            </div>
          </div>
        ) : (
          <Empty title="No updates yet" detail="Connect an agent to start receiving posture data." />
        )}
      </Card>

      <Card title="Updates" subtitle="Most recent first.">
        {snaps.length === 0 ? (
          <Empty title="No updates" />
        ) : (
          <DataTable
            cols={["Collected", "Updates", "Restart", "Details"]}
            rows={snaps.map((s) => [
              <span className="mono">{fmtIso(s.collected_at_utc)}</span>,
              <span className="muted">{(s.payload?.missing_updates || []).length}</span>,
              <span className="muted">{Boolean(s.payload?.reboot_pending) ? "Yes" : "No"}</span>,
              <Button
                variant="ghost"
                onClick={() => setRawOpen(rawOpen === s.id ? null : s.id)}
              >
                {rawOpen === s.id ? "Hide" : "View"}
              </Button>,
            ])}
          />
        )}

        {rawOpen !== null && (
          <div className="rawBox">
            <div className="rawHead">
              <div className="strong">Update details</div>
              <Button variant="ghost" onClick={() => setRawOpen(null)}>
                Close
              </Button>
            </div>
            <pre className="pre">
              {JSON.stringify(snaps.find((x) => x.id === rawOpen)?.payload || {}, null, 2)}
            </pre>
          </div>
        )}
      </Card>

      <Card title="Priorities" subtitle="Recommended actions for this asset.">
        {!top || top.length === 0 ? (
          <Empty title="No priorities generated" detail="Update priorities to generate recommended actions." />
        ) : (
          <div className="stack">
            {top.map((t, idx) => (
              <div key={idx} className="fix">
                <div className="fixLeft">
                  <div className="fixScore">{t.score}</div>
                </div>
                <div className="fixBody">
                  <div className="fixHeadline">{t.headline}</div>
                  <div className="fixLine">
                    <span className="strong">Action:</span> {t.fix_action}
                  </div>
                  <div className="fixLine muted">
                    <span className="strong muted">Reason:</span> {t.why_now}
                  </div>
                  {t.references && t.references.length > 0 && (
                    <div className="fixRefs mono muted">{t.references.join(" · ")}</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
