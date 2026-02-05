import { NavLink, Outlet } from "react-router-dom";
import { useAppConfig } from "../../store";
import Toast from "../../components/status/Toast";

import logo from "../../assets/echopentest-logo.png";

const nav = [
  { to: "/", label: "Dashboard" },
  { to: "/assets", label: "Assets" },
  { to: "/agents", label: "Agents" },
  { to: "/provisioning", label: "Add Agent" },
  { to: "/reports", label: "Reports" },
  { to: "/settings", label: "Settings" },
  { to: "/about", label: "About" },
];

function cleanUrl(url: string) {
  if (!url) return "-";
  return url.replace(/^https?:\/\//, "").replace(/\/+$/, "");
}

export default function MainLayout() {
  const { cfg, toasts, isConfigured } = useAppConfig();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <img className="brandLogo" src={logo} alt="EchoVuln" />
          <div className="brandText">
            <div className="brandTitle">EchoVuln</div>
            <div className="brandSub">Console</div>
          </div>
        </div>

        <div className="sidebarMeta">
          <div className="metaRow">
            <span className="metaKey">Server</span>
            <span className="metaVal">{cleanUrl(cfg.backendUrl)}</span>
          </div>
          <div className="metaRow">
            <span className="metaKey">Status</span>
            <span className={"metaVal " + (isConfigured ? "okText" : "warnText")}>
              {isConfigured ? "Configured" : "Not configured"}
            </span>
          </div>
        </div>

        <nav className="nav">
          {nav.map((n) => (
            <NavLink
              key={n.to}
              to={n.to}
              className={({ isActive }) => "navItem" + (isActive ? " navItemActive" : "")}
            >
              {n.label}
            </NavLink>
          ))}
        </nav>

        <div className="sidebarFooter">
          <div className="muted">v2</div>
        </div>
      </aside>

      <main className="main">
        <div className="topbar">
          <div className="topbarTitle">EchoVuln</div>
          <div className="topbarRight">
            <span className={"chip " + (isConfigured ? "chipOk" : "chipWarn")}>
              {isConfigured ? "Connected" : "Setup required"}
            </span>
          </div>
        </div>

        <div className="content">
          <Outlet />
        </div>
      </main>

      <Toast toasts={toasts} />
    </div>
  );
}
