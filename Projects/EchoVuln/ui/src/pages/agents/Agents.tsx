import { useEffect, useMemo, useState } from "react";
import Card from "../../components/common/Card";
import Empty from "../../components/common/Empty";
import DataTable from "../../components/tables/DataTable";
import StatusPill from "../../components/status/StatusPill";
import { listAssets, Asset } from "../../api/v2/assets";
import { useAppConfig } from "../../store";

export default function Agents() {
  const { pushToast } = useAppConfig();
  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    (async () => {
      setLoading(true);
      try {
        const a = await listAssets();
        setAssets(a);
      } catch (e: any) {
        pushToast("err", "Failed to load agents", e?.message);
      } finally {
        setLoading(false);
      }
    })();
  }, [pushToast]);

  const agents = useMemo(() => {
    return assets
      .filter((a) => Boolean(a.agent_id))
      .map((a) => ({
        name: a.name,
        agentId: a.agent_id as string,
        group: a.environment || "-",
      }));
  }, [assets]);

  return (
    <div className="stack">
      <Card
        title="Agents"
        subtitle="Reporting devices connected to this console."
        right={<StatusPill kind={loading ? "warn" : "ok"} text={loading ? "Refreshing" : "Live"} />}
      >
        {agents.length === 0 ? (
          <Empty title="No agents connected" detail="Go to “Add Agent” to connect the first device." />
        ) : (
          <DataTable
            cols={["Device", "Agent ID", "Group"]}
            rows={agents.map((a) => [
              <div className="strong">{a.name}</div>,
              <span className="mono">{a.agentId}</span>,
              <span className="muted">{a.group}</span>,
            ])}
          />
        )}
      </Card>
    </div>
  );
}
