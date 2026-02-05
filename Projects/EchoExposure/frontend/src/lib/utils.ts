export function cls(...c: (string | undefined | false)[]) {
  return c.filter(Boolean).join(" ");
}
