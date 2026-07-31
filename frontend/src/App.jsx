// Main application shell. It defines navigation and page routes.
import { NavLink, Route, Routes } from "react-router-dom";
import { Activity, BarChart3, History, LayoutDashboard, ScanSearch, ShieldQuestion } from "lucide-react";
import Dashboard from "./pages/Dashboard.jsx";
import URLScanner from "./pages/URLScanner.jsx";
import ScanHistory from "./pages/ScanHistory.jsx";
import Analytics from "./pages/Analytics.jsx";
import Explainability from "./pages/Explainability.jsx";

const navigationItems = [
  { path: "/", label: "Dashboard", icon: LayoutDashboard },
  { path: "/scanner", label: "URL Scanner", icon: ScanSearch },
  { path: "/history", label: "Scan History", icon: History },
  { path: "/analytics", label: "Analytics", icon: BarChart3 },
  { path: "/explainability", label: "Explainability", icon: ShieldQuestion },
];

function App() {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <Activity size={26} aria-hidden="true" />
          <span>Phishing Guard</span>
        </div>
        <nav className="nav-list" aria-label="Primary navigation">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink key={item.path} to={item.path} end={item.path === "/"} className="nav-link">
                <Icon size={18} aria-hidden="true" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </aside>

      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/scanner" element={<URLScanner />} />
          <Route path="/history" element={<ScanHistory />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/explainability" element={<Explainability />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
