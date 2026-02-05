import { useEffect, useState } from "react";
import Card from "../../components/common/Card";
import Button from "../../components/common/Button";
import Input from "../../components/common/Input";
import StatusPill from "../../components/status/StatusPill";
import { useAppConfig } from "../../store";
import { listAssets } from "../../api/v2/assets";

type KeyKind = "admin" | "enroll";

type KeyRow = {
  kind: KeyKind;
  key_id: string;
  label: string | null;
  created_at: string;
  revoked_at: string | null;
};

export default function Settings() {
  const { cfg, update, pushToast, isConfigured } = useAppConfig();
  const [backendUrl, setBackendUrl] = useState(cfg.backendUrl);
  const [adminKey, setAdminKey] = useState(cfg.adminKey);
  const [testing, setTesting] = useState(false);
  const [testMsg, setTestMsg] = useState<string | null>(null);
  const [testOk, setTestOk] = useState<boolean | null>(null);

  // --- keys UI state ---
  const [keyLabel, setKeyLabel] = useState("");
  const [keysLoading, setKeysLoading] = useState(false);
  const [keysErr, setKeysErr] = useState<string | null>(null);
  const [keys, setKeys] = useState<KeyRow[]>([]);
  const [creatingKind, setCreatingKind] = useState<KeyKind | null>(null);
  const [revokingId, setRevokingId] = useState<string | null>(null);
  const [lastCreatedKey, setLastCreatedKey] = useState<string | null>(null);

  useEffect(() => {
    setBackendUrl(cfg.backendUrl);
    setAdminKey(cfg.adminKey);
  }, [cfg.backendUrl, cfg.adminKey]);

  function apiBase() {
    return backendUrl.trim().replace(/\/+$/, "");
  }

  async function apiFetch(path: string, init?: RequestInit) {
    const url = `${apiBase()}${path}`;
    const headers: Record<string, string> = {
      "X-API-Key": adminKey.trim(),
      ...(init?.headers as any),
    };
    if (!(init?.body instanceof FormData)) {
      headers["Content-Type"] = headers["Content-Type"] || "application/json";
    }
    const res = await fetch(url, { ...init, headers });
    return res;
  }

  async function loadKeys() {
    if (!backendUrl.trim() || !adminKey.trim()) return;
    setKeysLoading(true);
    setKeysErr(null);
    try {
      const res = await apiFetch("/v2/keys", { method: "GET" });
      if (!res.ok) {
        const t = await res.text().catch(() => "");
        throw new Error(`Keys fetch failed (${res.status}) ${t || ""}`.trim());
      }
      const data = (await res.json()) as { keys: KeyRow[] };
      setKeys(Array.isArray(data.keys) ? data.keys : []);
    } catch (e: any) {
      const msg = e?.message || "Failed to load keys";
      setKeysErr(msg);
      pushToast("err", "Keys load failed", msg);
    } finally {
      setKeysLoading(false);
    }
  }

  async function createKey(kind: KeyKind) {
    if (!backendUrl.trim() || !adminKey.trim()) return;
    setCreatingKind(kind);
    setLastCreatedKey(null);
    try {
      const label = keyLabel.trim() ? keyLabel.trim() : null;
      const res = await apiFetch("/v2/keys", {
        method: "POST",
        body: JSON.stringify({ kind, label }),
      });
      const t = await res.text().catch(() => "");
      if (!res.ok) throw new Error(`Create failed (${res.status}) ${t || ""}`.trim());

      const out = JSON.parse(t) as { kind: KeyKind; key_id: string; key: string };
      setLastCreatedKey(out.key);
      pushToast("ok", "Key created");
      await loadKeys();
    } catch (e: any) {
      pushToast("err", "Create key failed", e?.message);
    } finally {
      setCreatingKind(null);
    }
  }

  async function revokeKey(kind: KeyKind, key_id: string) {
    if (!backendUrl.trim() || !adminKey.trim()) return;
    setRevokingId(`${kind}:${key_id}`);
    try {
      const res = await apiFetch(`/v2/keys/${kind}/${key_id}`, { method: "DELETE" });
      if (!res.ok) {
        const t = await res.text().catch(() => "");
        throw new Error(`Revoke failed (${res.status}) ${t || ""}`.trim());
      }
      pushToast("ok", "Key revoked");
      await loadKeys();
    } catch (e: any) {
      pushToast("err", "Revoke failed", e?.message);
    } finally {
      setRevokingId(null);
    }
  }

  async function copy(s: string) {
    try {
      await navigator.clipboard.writeText(s);
      pushToast("ok", "Copied");
    } catch {
      pushToast("err", "Copy failed");
    }
  }

  async function testConn() {
    setTesting(true);
    setTestMsg(null);
    setTestOk(null);
    try {
      update({ backendUrl, adminKey });
      await listAssets();
      setTestOk(true);
      setTestMsg("Backend reachable. Admin key accepted.");
      pushToast("ok", "Connection OK");
      await loadKeys();
    } catch (e: any) {
      setTestOk(false);
      setTestMsg(e?.message || "Connection failed");
      pushToast("err", "Connection failed", e?.message);
    } finally {
      setTesting(false);
    }
  }

  function save() {
    update({ backendUrl, adminKey });
    pushToast("ok", "Settings saved");
  }

  const adminKeys = keys.filter((k) => k.kind === "admin");
  const enrollKeys = keys.filter((k) => k.kind === "enroll");

  return (
    <div className="setupGrid">
      <div className="setupHero">
        <div className="setupBadge">EchoVuln Console</div>
        <div className="setupTitle">Console Setup</div>
        <div className="setupSub">
          UI uses <span className="mono">X-API-Key</span>. Agents never use this key. Agents enroll with{" "}
          <span className="mono">X-ENROLL-KEY</span> and run on per-agent bearer tokens.
        </div>

        <div className="setupSteps">
          <div className="step">
            <div className="stepNum">1</div>
            <div className="stepBody">
              <div className="strong">Paste backend URL</div>
              <div className="muted">Local dev: http://127.0.0.1:8000</div>
            </div>
          </div>
          <div className="step">
            <div className="stepNum">2</div>
            <div className="stepBody">
              <div className="strong">Paste admin key</div>
              <div className="muted">Seeded by backend console output (ak_*.secret)</div>
            </div>
          </div>
          <div className="step">
            <div className="stepNum">3</div>
            <div className="stepBody">
              <div className="strong">Test connection</div>
              <div className="muted">Verifies tenant auth + API routing</div>
            </div>
          </div>
        </div>
      </div>

      <Card
        title="Connection"
        subtitle="These values are stored locally on this machine."
        right={<StatusPill kind={isConfigured ? "ok" : "warn"} text={isConfigured ? "Configured" : "Not configured"} />}
      >
        <div className="stack">
          <Input
            label="Backend URL"
            value={backendUrl}
            onChange={(e) => setBackendUrl(e.target.value)}
            placeholder="http://127.0.0.1:8000"
          />
          <Input
            label="Admin key (ak_*.secret)"
            value={adminKey}
            onChange={(e) => setAdminKey(e.target.value)}
            placeholder="ak_xxxxx.secret"
          />

          <div className="row">
            <Button onClick={save} disabled={!backendUrl.trim() || !adminKey.trim()}>
              Save
            </Button>
            <Button variant="ghost" onClick={testConn} disabled={!backendUrl.trim() || !adminKey.trim() || testing}>
              {testing ? "Testing..." : "Test connection"}
            </Button>
            {testMsg && <StatusPill kind={testOk ? "ok" : "err"} text={testMsg} />}
          </div>

          <div className="callout">
            <div className="strong">Hard rule</div>
            <div className="muted">Admin key stays in the console. Endpoint agents never receive it.</div>
          </div>
        </div>
      </Card>

      {/* FULL-WIDTH bottom row */}
      <div style={{ gridColumn: "1 / -1" }}>
        <Card
          title="API Keys"
          subtitle="Create and revoke admin/enrollment keys. Newly created key secrets are shown once."
          right={
            keysLoading ? (
              <StatusPill kind="warn" text="Loading..." />
            ) : keysErr ? (
              <StatusPill kind="err" text="Error" />
            ) : (
              <StatusPill kind="ok" text={`${keys.length} keys`} />
            )
          }
        >
          <div className="stack">
            <Input
              label="Optional label"
              value={keyLabel}
              onChange={(e) => setKeyLabel(e.target.value)}
              placeholder="e.g. Client A / Office laptop"
            />

            <div className="row">
              <Button
                variant="ghost"
                onClick={loadKeys}
                disabled={!backendUrl.trim() || !adminKey.trim() || keysLoading}
              >
                {keysLoading ? "Refreshing..." : "Refresh"}
              </Button>

              <Button
                onClick={() => createKey("admin")}
                disabled={!backendUrl.trim() || !adminKey.trim() || creatingKind !== null}
              >
                {creatingKind === "admin" ? "Creating..." : "Create admin key"}
              </Button>

              <Button
                onClick={() => createKey("enroll")}
                disabled={!backendUrl.trim() || !adminKey.trim() || creatingKind !== null}
              >
                {creatingKind === "enroll" ? "Creating..." : "Create enroll key"}
              </Button>
            </div>

            {lastCreatedKey && (
              <div className="callout">
                <div className="strong">Created key</div>
                <div className="muted mono" style={{ wordBreak: "break-all" }}>
                  {lastCreatedKey}
                </div>
                <div className="row">
                  <Button variant="ghost" onClick={() => copy(lastCreatedKey)}>
                    Copy
                  </Button>
                </div>
              </div>
            )}

            {keysErr && (
              <div className="callout">
                <div className="strong">Error</div>
                <div className="muted">{keysErr}</div>
              </div>
            )}

            {/* two-table layout on wide screens */}
            <div className="stack" style={{ gap: 16 }}>
              <div style={{ display: "grid", gap: 16, gridTemplateColumns: "1fr" as any }}>
                <div className="strong" style={{ marginBottom: 0 }}>
                  Keys
                </div>
                <div
                  style={{
                    display: "grid",
                    gap: 16,
                    gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
                  }}
                >
                  <div>
                    <div className="strong" style={{ marginBottom: 8 }}>
                      Admin keys
                    </div>
                    <div className="tableWrap">
                      <table className="table">
                        <thead>
                          <tr>
                            <th>key_id</th>
                            <th>label</th>
                            <th>created</th>
                            <th>status</th>
                            <th />
                          </tr>
                        </thead>
                        <tbody>
                          {adminKeys.length === 0 ? (
                            <tr>
                              <td className="muted" colSpan={5}>
                                No admin keys found.
                              </td>
                            </tr>
                          ) : (
                            adminKeys.map((k) => {
                              const busy = revokingId === `admin:${k.key_id}`;
                              const active = !k.revoked_at;
                              return (
                                <tr key={`admin-${k.key_id}`}>
                                  <td className="mono">{k.key_id}</td>
                                  <td>{k.label || <span className="muted">—</span>}</td>
                                  <td className="mono">{k.created_at}</td>
                                  <td>
                                    <StatusPill kind={active ? "ok" : "warn"} text={active ? "active" : "revoked"} />
                                  </td>
                                  <td style={{ textAlign: "right" }}>
                                    <Button
                                      variant="ghost"
                                      onClick={() => revokeKey("admin", k.key_id)}
                                      disabled={!active || busy}
                                    >
                                      {busy ? "Revoking..." : "Revoke"}
                                    </Button>
                                  </td>
                                </tr>
                              );
                            })
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <div>
                    <div className="strong" style={{ marginBottom: 8 }}>
                      Enrollment keys
                    </div>
                    <div className="tableWrap">
                      <table className="table">
                        <thead>
                          <tr>
                            <th>key_id</th>
                            <th>label</th>
                            <th>created</th>
                            <th>status</th>
                            <th />
                          </tr>
                        </thead>
                        <tbody>
                          {enrollKeys.length === 0 ? (
                            <tr>
                              <td className="muted" colSpan={5}>
                                No enrollment keys found.
                              </td>
                            </tr>
                          ) : (
                            enrollKeys.map((k) => {
                              const busy = revokingId === `enroll:${k.key_id}`;
                              const active = !k.revoked_at;
                              return (
                                <tr key={`enroll-${k.key_id}`}>
                                  <td className="mono">{k.key_id}</td>
                                  <td>{k.label || <span className="muted">—</span>}</td>
                                  <td className="mono">{k.created_at}</td>
                                  <td>
                                    <StatusPill kind={active ? "ok" : "warn"} text={active ? "active" : "revoked"} />
                                  </td>
                                  <td style={{ textAlign: "right" }}>
                                    <Button
                                      variant="ghost"
                                      onClick={() => revokeKey("enroll", k.key_id)}
                                      disabled={!active || busy}
                                    >
                                      {busy ? "Revoking..." : "Revoke"}
                                    </Button>
                                  </td>
                                </tr>
                              );
                            })
                          )}
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div className="callout">
              <div className="strong">Notes</div>
              <div className="muted">
                Enrollment keys are safe to hand to a client for one-time agent enrollment. Revoke them if leaked.
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
