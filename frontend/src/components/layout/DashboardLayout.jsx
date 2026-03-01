import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useState } from "react";
import "../../styles/dashboard.css";

function DashboardLayout() {
  const navigate = useNavigate();
  const [collapsed, setCollapsed] = useState(false);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  return (
    <div className={`dashboard-wrapper ${collapsed ? "collapsed" : ""}`}>
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo-section">{collapsed ? "SM" : "SecureMonitor"}</div>

        <nav className="nav-links">
          <NavLink to="/dashboard" end>
            <span>🏠</span>
            {!collapsed && " Dashboard"}
          </NavLink>

          <NavLink to="/dashboard/employees">
            <span>👤</span>
            {!collapsed && " Employees"}
          </NavLink>

          <NavLink to="/dashboard/devices">
            <span>💻</span>
            {!collapsed && " Devices"}
          </NavLink>

          <NavLink to="/dashboard/alerts">
            <span>🚨</span>
            {!collapsed && " Alerts"}
          </NavLink>

          <NavLink to="/dashboard/logs">
            <span>📊</span>
            {!collapsed && " Logs"}
          </NavLink>

          <NavLink to="/dashboard/reports">
            <span>📈</span>
            {!collapsed && " Reports"}
          </NavLink>

          <NavLink to="/dashboard/settings">
            <span>⚙️</span>
            {!collapsed && " Settings"}
          </NavLink>

          <button className="logout-btn" onClick={handleLogout}>
            {!collapsed ? "➡️ Logout" : "➡️"}
          </button>
        </nav>
      </aside>

      {/* Main Area */}
      <div className="main-content">
        <div className="sidebar-header">

          <button
            className="toggle-btn"
            onClick={() => setCollapsed(!collapsed)}
          >
            {collapsed ? "➤" : "◀"}
          </button>
        </div>

        <div className="page-content">
          <Outlet />
        </div>
      </div>
    </div>
  );
}

export default DashboardLayout;
