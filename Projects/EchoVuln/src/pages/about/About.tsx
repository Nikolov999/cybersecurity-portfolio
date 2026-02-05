import Card from "../../components/common/Card";

export default function About() {
  return (
    <div className="stack">
      <Card title="EchoVuln" subtitle="Security posture console.">
        <div className="muted">
          <ul className="bullets">
            <li>Designed for small teams</li>
            <li>Clear priorities and reports</li>
            <li>Device identity stays stable</li>
            <li>Data stays consistent over time</li>
          </ul>
        </div>
      </Card>
    </div>
  );
}
