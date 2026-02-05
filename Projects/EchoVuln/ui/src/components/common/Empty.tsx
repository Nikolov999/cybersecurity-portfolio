export default function Empty(props: { title: string; detail?: string }) {
  return (
    <div className="empty">
      <div className="emptyTitle">{props.title}</div>
      {props.detail && <div className="emptyDetail">{props.detail}</div>}
    </div>
  );
}
