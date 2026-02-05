import React from "react";
import Button from "./Button";

export default function Modal(props: { open: boolean; title: string; children: React.ReactNode; onClose: () => void }) {
  if (!props.open) return null;
  return (
    <div className="modalOverlay" onMouseDown={props.onClose}>
      <div className="modal" onMouseDown={(e) => e.stopPropagation()}>
        <div className="modalHead">
          <div className="modalTitle">{props.title}</div>
          <Button variant="ghost" onClick={props.onClose}>Close</Button>
        </div>
        <div className="modalBody">{props.children}</div>
      </div>
    </div>
  );
}
