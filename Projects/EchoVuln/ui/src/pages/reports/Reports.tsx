import { useEffect, useMemo, useState } from "react";
import Card from "../../components/common/Card";
import Button from "../../components/common/Button";
import Modal from "../../components/common/Modal";
import Input from "../../components/common/Input";
import Empty from "../../components/common/Empty";
import { createReport, deleteReport, listReports, Report } from "../../api/v2/reports";
import { useAppConfig } from "../../store";
import { marked } from "marked";
import { fmtIso } from "../../utils/formatters/time";

export default function Reports() {
  const { pushToast } = useAppConfig();
  const [reports, setReports] = useState<Report[]>([]);
  const [selected, setSelected] = useState<Report | null>(null);

  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("EchoVuln Report");
  const [markdown, setMarkdown] = useState(`# Summary
- ...

# Findings
- ...

# Priorities
- ...
`);

  async function refresh() {
    try {
      const r = await listReports();
      setReports(r);
      if (selected) {
        const s = r.find((x) => x.id === selected.id) || null;
        setSelected(s);
      }
    } catch (e: any) {
      pushToast("err", "Failed to load reports", e?.message);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  const html = useMemo(() => {
    return selected ? marked.parse(selected.markdown || "") : "";
  }, [selected]);

  async function onCreate() {
    try {
      const r = await createReport({ title, markdown, asset_id: null });
      pushToast("ok", "Report created");
      setOpen(false);
      await refresh();
      setSelected(r);
    } catch (e: any) {
      pushToast("err", "Create failed", e?.message);
    }
  }

  async function onDelete(id: number) {
    if (!confirm("Delete this report?")) return;
    try {
      await deleteReport(id);
      pushToast("ok", "Report deleted");
      setSelected(null);
      refresh();
    } catch (e: any) {
      pushToast("err", "Delete failed", e?.message);
    }
  }

  return (
    <div className="grid2">
      <Card title="Reports" subtitle="Create and store client-ready writeups." right={<Button onClick={() => setOpen(true)}>New report</Button>}>
        {reports.length === 0 ? (
          <Empty title="No reports" detail="Create one from findings and priorities." />
        ) : (
          <div className="stack">
            {reports.map((r) => (
              <div key={r.id} className={"listItem" + (selected?.id === r.id ? " listItemActive" : "")}>
                <button className="listBtn" onClick={() => setSelected(r)}>
                  <div className="strong">{r.title}</div>
                  <div className="muted">Created: {fmtIso(r.created_at)}</div>
                </button>
                <Button variant="danger" onClick={() => onDelete(r.id)}>
                  Delete
                </Button>
              </div>
            ))}
          </div>
        )}
      </Card>

      <Card title={selected ? selected.title : "Preview"} subtitle={selected ? `Created: ${fmtIso(selected.created_at)}` : "Select a report"}>
        {!selected ? <Empty title="No report selected" /> : <div className="md" dangerouslySetInnerHTML={{ __html: html }} />}
      </Card>

      <Modal open={open} title="Create report" onClose={() => setOpen(false)}>
        <div className="stack">
          <Input label="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
          <label className="field">
            <div className="fieldLabel">Content</div>
            <textarea className="textarea" value={markdown} onChange={(e) => setMarkdown(e.target.value)} rows={12} />
          </label>
          <div className="rowRight">
            <Button variant="ghost" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button onClick={onCreate}>Create</Button>
          </div>
        </div>
      </Modal>
    </div>
  );
}
