import { Shell } from "./components/layout/Shell";
import { Dashboard } from "./pages/Dashboard";
import { Assets } from "./pages/Assets";
import { Scans } from "./pages/Scans";
import { AttackSurface } from "./pages/AttackSurface";
import { Findings } from "./pages/Findings";
import { Settings } from "./pages/Settings";
import { useAppStore } from "./state/useAppStore";

export default function App() {
  const page = useAppStore((s) => s.page);

  const renderPage = () => {
    switch (page) {
      case "assets":
        return <Assets />;
      case "scans":
        return <Scans />;
      case "surface":
        return <AttackSurface />;
      case "findings":
        return <Findings />;
      case "settings":
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  return <Shell>{renderPage()}</Shell>;
}
