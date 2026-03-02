import { Outlet, NavLink, useNavigate } from "react-router-dom";
import { useState } from "react";
import logo from "../../assets/icons/logo.png";
import {
  LayoutDashboard,
  Users,
  Monitor,
  AlertTriangle,
  FileText,
  BarChart3,
  Settings,
  LogOut,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

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
        <div className="logo-section">
          <img src={logo} alt="Logo" className="real-logo" />
          {!collapsed && <span className="logo-text">SecureMonitor</span>}
        </div>

        <nav className="nav-links">
          <NavLink
            to="/dashboard"
            end
            className={({ isActive }) =>
              isActive ? "nav-item active" : "nav-item"
            }
          >
            <LayoutDashboard size={18} />
            {!collapsed && <span>Dashboard</span>}
            {collapsed && <span className="tooltip">Dashboard</span>}
          </NavLink>

          <NavLink to="/dashboard/employees" className={({ isActive }) =>
    isActive ? "nav-item active" : "nav-item"
  }>
            <Users size={18} />
            {!collapsed && <span>Employees</span>}
            {collapsed && <span className="tooltip">Employees</span>}
          </NavLink>

          <NavLink to="/dashboard/devices" className={({ isActive }) =>
    isActive ? "nav-item active" : "nav-item"
  }>
            <Monitor size={18} />
            {!collapsed && <span>Devices</span>}
            {collapsed && <span className="tooltip">Devices</span>}
          </NavLink>

          <NavLink to="/dashboard/alerts" className={({ isActive }) =>
    isActive ? "nav-item active" : "nav-item"
  }>
            <AlertTriangle size={18} / >
            {!collapsed && <span>Alerts</span>}
            {collapsed && <span className="tooltip">Alerts</span>}
          </NavLink>

          <NavLink to="/dashboard/logs" className={({ isActive }) =>
    isActive ? "nav-item active" : "nav-item"
  }>
            <FileText size={18} />
            {!collapsed && <span>Logs</span>}
            {collapsed && <span className="tooltip">Logs</span>}
          </NavLink>

          <NavLink to="/dashboard/reports" className={({ isActive }) =>
    isActive ? "nav-item active" : "nav-item"
  }>
            <BarChart3 size={18} />
            {!collapsed && <span>Reports</span>}
            {collapsed && <span className="tooltip">Reports</span>}
          </NavLink>

          <NavLink to="/dashboard/settings" className={({ isActive }) =>
    isActive ? "nav-item active" : "nav-item"
  }>
            <Settings size={18} />
            {!collapsed && <span>Settings</span>}
            {collapsed && <span className="tooltip">Settings</span>}
          </NavLink>

          <button className="logout-btn" onClick={handleLogout}>
            <LogOut size={18} />
            {!collapsed && <span>Logout</span>}
            {collapsed && <span className="tooltip">Logout</span>}
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
            {collapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
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
