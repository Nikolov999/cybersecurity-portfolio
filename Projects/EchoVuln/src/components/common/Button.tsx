import React from "react";

type Props = React.ButtonHTMLAttributes<HTMLButtonElement> & { variant?: "primary" | "ghost" | "danger" };

export default function Button({ variant = "primary", ...rest }: Props) {
  const cls =
    variant === "primary" ? "btn" : variant === "danger" ? "btn btnDanger" : "btn btnGhost";
  return <button className={cls} {...rest} />;
}
