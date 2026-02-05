import { useMemo, useState } from "react";
import Card from "../../components/common/Card";
import Button from "../../components/common/Button";
import Input from "../../components/common/Input";
import { useAppConfig } from "../../store";

export default function Provisioning() {
  const { cfg, pushToast } = useAppConfig();
  const [enrollKey, setEnrollKey] = useState("");
  const [agentId, setAgentId] = useState("11111111-2222-3333-4444-555555555555");
  const [deviceName, setDeviceName] = useState("WIN11-01");

  const script = useMemo(() => {
    const backend = cfg.backendUrl.replace(/\/+$/, "");
    const ek = enrollKey || "PASTE_ENROLLMENT_KEY_HERE";

    return `$Server = "${backend}"
$EnrollmentKey = "${ek}"

$Body = @{
  agent_id = "${agentId}"
  hostname = "${deviceName}"
  os = "Windows"
  ip = ""
} | ConvertTo-Json

$Headers = @{
  "X-ENROLL-KEY" = $EnrollmentKey
  "Content-Type" = "application/json"
}

Invoke-RestMethod -Method POST -Uri "$Server/v2/agents/enroll" -Headers $Headers -Body $Body
`;
  }, [cfg.backendUrl, enrollKey, agentId, deviceName]);

  function copy() {
    navigator.clipboard.writeText(script);
    pushToast("ok", "Copied");
  }

  return (
    <div className="stack">
      <Card
        title="Add Agent"
        subtitle="Use this to connect a device for the first time."
        right={<Button onClick={copy}>Copy</Button>}
      >
        <div className="grid2">
          <Input
            label="Enrollment key"
            value={enrollKey}
            onChange={(e) => setEnrollKey(e.target.value)}
            placeholder="ek_xxxxx.secret"
          />
          <Input label="Agent ID" value={agentId} onChange={(e) => setAgentId(e.target.value)} />
          <Input label="Device name" value={deviceName} onChange={(e) => setDeviceName(e.target.value)} />
          <div className="callout">
            <div className="strong">Tip</div>
            <div className="muted">Run this once per device to connect it to your console.</div>
          </div>
        </div>

        <div className="rawBox">
          <div className="rawHead">
            <div className="strong">Setup command</div>
          </div>
          <pre className="pre">{script}</pre>
        </div>
      </Card>
    </div>
  );
}
