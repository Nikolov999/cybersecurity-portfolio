import React from "react";

export default function Card(props: { title?: string; subtitle?: string; right?: React.ReactNode; children: React.ReactNode }) {
  return (
    <div className="card">
      {(props.title || props.subtitle || props.right) && (
        <div className="cardHead">
          <div>
            {props.title && <div className="cardTitle">{props.title}</div>}
            {props.subtitle && <div className="cardSub">{props.subtitle}</div>}
          </div>
          {props.right ? <div className="cardRight">{props.right}</div> : null}
        </div>
      )}
      <div className="cardBody">{props.children}</div>
    </div>
  );
}
