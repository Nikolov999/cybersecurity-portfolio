import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import Card from "../../components/common/Card";
import Button from "../../components/common/Button";
import Modal from "../../components/common/Modal";
import Input from "../../components/common/Input";
import DataTable from "../../components/tables/DataTable";
import Empty from "../../components/common/Empty";
import StatusPill from "../../components/status/StatusPill";

import { Asset, createAsset, deleteAsset, listAssets } from "../../api/v2/assets";
import { useAppConfig } from "../../store";

function normalizeCsv(value: string): string[] {
  return value
    .split(",")
    .map((x) => x.trim())
    .filter(Boolean)
    .slice(0, 20);
}

export default function Assets() {
  const { pushToast } = useAppConfig();

  const [assets, setAssets] = useState<Asset[]>([]);
  const [loading, setLoading] = useState(false);

  const [open, setOpen] = useState(false);
  const [name, setName] = useState("");
  const [group, setGroup] = useState("endpoint");
  const [labels, setLabels] = useState("pilot");

  const connectedCount = useMemo(() => assets.filter((a) => Boolean(a.agent_id)).length, [assets]);

  async function refresh() {
    setLoading(true);
    try {
      setAssets(await listAssets());
    } catch (e: any) {
      pushToast("err", "Failed to load assets", e?.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function onCreate() {
    try {
      const tags = normalizeCsv(labels);
      await createAsset({ name: name.trim(), environment: group.trim(), tags });
      pushToast("ok", "Asset created");
      setOpen(false);
      setName("");
      setGroup("endpoint");
      setLabels("pilot");
      refresh();
    } catch (e: any) {
      pushToast("err", "Create failed", e?.message);
    }
  }

  async function onDelete(id: number) {
    if (!confirm("Delete this asset?")) return;
    try {
      await deleteAsset(id);
      pushToast("ok", "Asset deleted");
      refresh();
    } catch (e: any) {
      pushToast("err", "Delete failed", e?.message);
    }
  }

  return (
    <div className="stack">
      <Card
        title="Assets"
        subtitle={`${assets.length} total · ${connectedCount} with agents connected`}
        right={
          <div className="row">
            <StatusPill kind={loading ? "warn" : "ok"} text={loading ? "Refreshing" : "Ready"} />
            <Button onClick={() => setOpen(true)}>New asset</Button>
          </div>
        }
      >
        {assets.length === 0 ? (
          <Empty title="No assets" detail="Create an asset or connect a device to start receiving updates." />
        ) : (
          <DataTable
            cols={["Name", "Group", "Labels", "Agent ID", "Actions"]}
            rows={assets.map((a) => [
              <Link className="link" to={`/assets/${a.id}`}>
                {a.name}
              </Link>,
              <span className="muted">{a.environment || "-"}</span>,
              <span className="muted">{(a.tags || []).join(", ") || "-"}</span>,
              <span className="mono muted">{a.agent_id || "-"}</span>,
              <div className="row">
                <Link className="btn btnGhost" to={`/assets/${a.id}`}>
                  Open
                </Link>
                <Button variant="danger" onClick={() => onDelete(a.id)}>
                  Delete
                </Button>
              </div>,
            ])}
          />
        )}
      </Card>

      <Modal open={open} title="Create asset" onClose={() => setOpen(false)}>
        <div className="stack">
          <Input
            label="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="WIN11-01"
          />
          <Input
            label="Group"
            value={group}
            onChange={(e) => setGroup(e.target.value)}
            placeholder="endpoint"
          />
          <Input
            label="Labels (comma separated)"
            value={labels}
            onChange={(e) => setLabels(e.target.value)}
            placeholder="pilot,finance"
          />

          <div className="callout">
            <div className="strong">Tip</div>
            <div className="muted">Connect an agent to start receiving updates for an asset.</div>
          </div>

          <div className="rowRight">
            <Button variant="ghost" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button onClick={onCreate} disabled={!name.trim()}>
              Create
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
