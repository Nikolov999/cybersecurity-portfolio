import { useEffect, useMemo, useState } from "react";
import Card from "../../components/common/Card";
import Kpi from "../../components/common/Kpi";
import StatusPill from "../../components/status/StatusPill";
import Empty from "../../components/common/Empty";
import DataTable from "../../components/tables/DataTable";
import { listAssets, Asset } from "../../api/v2/assets";
import { computeTopFixes } from "../../api/v2/topfixes";
import { useAppConfig } from "../../store";

export default function Dashboard() {
  const { pushToast } = useAppConfig();
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(false);
  const [top, setTop] = useState<any[] | null>(null);
  const [topLoading, setTopLoading] = useState(false);

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const a = await listAssets();
        setAssets(a);
      } catch (e: any) {
        pushToast("err", "Failed to load assets", e?.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [pushToast]);

  const connectedAgents = useMemo(() => assets.filter((a) => Boolean(a.agent_id)).length, [assets]);
  const unassigned = useMemo(() => Math.max(0, assets.length - connectedAgents), [assets.length, connectedAgents]);

  async function loadTopFixes() {
    setTopLoading(true);
    try {
      const res = await computeTopFixes(undefined, 10);
      setTop(res.items);
      pushToast("ok", "Priorities updated");
    } catch (e: any) {
      pushToast("err", "Could not load priorities", e?.message);
    } finally {
      setTopLoading(false);
    }
  }

  return (
    <div className="grid2">
      <Card
        title="Overview"
        subtitle="Live view of your environment."
        right={<StatusPill kind={loading ? "warn" : "ok"} text={loading ? "Refreshing" : "Live"} />}
      >
        <div className="kpiRow">
          <Kpi label="Assets" value={String(assets.length)} hint="Registered devices and services" />
          <Kpi label="Agents connected" value={String(connectedAgents)} hint="Reporting devices" />
          <Kpi label="Unassigned" value={String(unassigned)} hint="Missing agent link" />
        </div>
      </Card>

      <Card
        title="Priorities"
        subtitle="Actionable items ranked by impact."
        right={
          <button className="btn" onClick={loadTopFixes} disabled={topLoading}>
            {topLoading ? "Updating..." : "Update"}
          </button>
        }
      >
        {!top || top.length === 0 ? (
          <Empty title="No priorities yet" detail="Update to generate tenant-wide actions." />
        ) : (
          <DataTable
            cols={["Score", "Action", "Reason"]}
            rows={top.map((t) => [
              <span className="mono">{t.score}</span>,
              <div>
                <div className="strong">{t.headline}</div>
                <div className="muted">{t.fix_action}</div>
              </div>,
              <span className="muted">{t.why_now}</span>,
            ])}
          />
        )}
      </Card>

      <Card title="Getting started" subtitle="Connect agents, then review priorities and reports.">
        <div className="callout">
          <div className="strong">Next step</div>
          <div className="muted">Use “Add Agent” to connect a device. Then return here to see live posture.</div>
        </div>
      </Card>

      <Card title="Notes" subtitle="Keep this console client-facing.">
        <div className="muted">
          Recommended workflow:
          <ul className="bullets">
            <li>Connect devices</li>
            <li>Review priorities</li>
            <li>Create a report</li>
            <li>Re-check after remediation</li>
          </ul>
        </div>
      </Card>
    </div>
  );
}
