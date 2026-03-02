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
  ChevronRight
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

          <NavLink to="/dashboard" end>
            <LayoutDashboard size={18} />
            {!collapsed && <span>Dashboard</span>}
          </NavLink>

          <NavLink to="/dashboard/employees">
            <Users size={18} />
            {!collapsed && <span>Employees</span>}
          </NavLink>

          <NavLink to="/dashboard/devices">
            <Monitor size={18} />
            {!collapsed && <span>Devices</span>}
          </NavLink>

          <NavLink to="/dashboard/alerts">
            <AlertTriangle size={18} />
            {!collapsed && <span>Alerts</span>}
          </NavLink>

          <NavLink to="/dashboard/logs">
            <FileText size={18} />
            {!collapsed && <span>Logs</span>}
          </NavLink>

          <NavLink to="/dashboard/reports">
            <BarChart3 size={18} />
            {!collapsed && <span>Reports</span>}
          </NavLink>

          <NavLink to="/dashboard/settings">
            <Settings size={18} />
            {!collapsed && <span>Settings</span>}
          </NavLink>

          <button className="logout-btn" onClick={handleLogout}>
            <LogOut size={18} />
            {!collapsed && <span>Logout</span>}
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