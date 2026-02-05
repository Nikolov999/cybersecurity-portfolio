import React from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import MainLayout from "./layouts/main/MainLayout";

import Dashboard from "./pages/dashboard/Dashboard";
import Assets from "./pages/assets/Assets";
import AssetDetail from "./pages/asset-detail/AssetDetail";
import Agents from "./pages/agents/Agents";
import Provisioning from "./pages/provisioning/Provisioning";
import Reports from "./pages/reports/Reports";
import Settings from "./pages/settings/Settings";
import About from "./pages/about/About";

import { useAppConfig } from "./store";

function RequireConfig(props: { children: React.ReactNode }) {
  const { isConfigured } = useAppConfig();
  if (!isConfigured) return <Navigate to="/settings" replace />;
  return <>{props.children}</>;
}

export default function App() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route
          path="/"
          element={
            <RequireConfig>
              <Dashboard />
            </RequireConfig>
          }
        />
        <Route
          path="/assets"
          element={
            <RequireConfig>
              <Assets />
            </RequireConfig>
          }
        />
        <Route
          path="/assets/:id"
          element={
            <RequireConfig>
              <AssetDetail />
            </RequireConfig>
          }
        />
        <Route
          path="/agents"
          element={
            <RequireConfig>
              <Agents />
            </RequireConfig>
          }
        />
        <Route
          path="/provisioning"
          element={
            <RequireConfig>
              <Provisioning />
            </RequireConfig>
          }
        />
        <Route
          path="/reports"
          element={
            <RequireConfig>
              <Reports />
            </RequireConfig>
          }
        />

        <Route path="/settings" element={<Settings />} />
        <Route path="/about" element={<About />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
