
export default function DataTable(props: { cols: string[]; rows: React.ReactNode[][] }) {
  return (
    <div className="tableWrap">
      <table className="table">
        <thead>
          <tr>
            {props.cols.map((c) => (
              <th key={c}>{c}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {props.rows.map((r, i) => (
            <tr key={i}>
              {r.map((cell, j) => (
                <td key={j}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
