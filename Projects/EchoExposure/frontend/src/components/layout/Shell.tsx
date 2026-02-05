import { ReactNode, useEffect, useState } from "react";
import { TopBar } from "./TopBar";
import { SideNav } from "./SideNav";
import { Footer } from "./Footer";
import { api } from "../../lib/api";

export function Shell({ children }: { children: ReactNode }) {
  const [apiUp, setApiUp] = useState<boolean | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        await api.health();
        if (alive) setApiUp(true);
      } catch {
        if (alive) setApiUp(false);
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  return (
    <div className="min-h-screen bg-ink-950">
      <div className="pointer-events-none fixed inset-0 bg-radial-hero" />
      <div className="relative mx-auto flex min-h-screen max-w-[1400px]">
        <SideNav />
        <div className="flex min-w-0 flex-1 flex-col">
          <TopBar apiUp={apiUp} />
          <main className="min-w-0 flex-1 px-4 pb-10 pt-4 sm:px-6">{children}</main>
          <Footer />
        </div>
      </div>
    </div>
  );
}
