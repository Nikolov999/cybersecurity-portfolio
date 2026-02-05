import React from "react";

export default function Input(props: React.InputHTMLAttributes<HTMLInputElement> & { label?: string; hint?: string }) {
  const { label, hint, ...rest } = props;
  return (
    <label className="field">
      {label && <div className="fieldLabel">{label}</div>}
      <input className="input" {...rest} />
      {hint && <div className="fieldHint">{hint}</div>}
    </label>
  );
}
