export default function Kpi(props: { label: string; value: string; hint?: string }) {
  return (
    <div className="kpi">
      <div className="kpiLabel">{props.label}</div>
      <div className="kpiValue">{props.value}</div>
      {props.hint && <div className="kpiHint">{props.hint}</div>}
    </div>
  );
}
