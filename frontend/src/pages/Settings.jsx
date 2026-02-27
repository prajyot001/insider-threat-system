import { useState } from "react";
import "../styles/Settings.css";

function Settings() {
  const [formData, setFormData] = useState({
    companyName: "SecureMonitor Inc.",
    adminEmail: "admin@company.com",
    newPassword: "",
    confirmPassword: "",
  });

  const [settings, setSettings] = useState({
    emailAlerts: true,
    autoRefresh: false,
    darkMode: true,
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleToggle = (e) => {
    setSettings({
      ...settings,
      [e.target.name]: e.target.checked,
    });
  };

  const handleSave = () => {
    alert("Settings saved (UI only for now)");
  };

  return (
    <div className="settings-container">
      <h2>System Settings</h2>

      {/* Profile Section */}
      <div className="settings-card">
        <h3>Profile Information</h3>
        <input
          type="text"
          name="companyName"
          value={formData.companyName}
          onChange={handleChange}
          placeholder="Company Name"
        />
        <input
          type="email"
          name="adminEmail"
          value={formData.adminEmail}
          onChange={handleChange}
          placeholder="Admin Email"
        />
      </div>

      {/* Password Section */}
      <div className="settings-card">
        <h3>Change Password</h3>
        <input
          type="password"
          name="newPassword"
          placeholder="New Password"
          onChange={handleChange}
        />
        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          onChange={handleChange}
        />
      </div>

      {/* System Preferences */}
      <div className="settings-card">
        <h3>Preferences</h3>

        <label className="toggle-row">
          <span>Email Alerts</span>
          <input
            type="checkbox"
            name="emailAlerts"
            checked={settings.emailAlerts}
            onChange={handleToggle}
          />
        </label>

        <label className="toggle-row">
          <span>Auto Refresh Dashboard</span>
          <input
            type="checkbox"
            name="autoRefresh"
            checked={settings.autoRefresh}
            onChange={handleToggle}
          />
        </label>

        <label className="toggle-row">
          <span>Dark Mode</span>
          <input
            type="checkbox"
            name="darkMode"
            checked={settings.darkMode}
            onChange={handleToggle}
          />
        </label>
      </div>

      <button className="save-btn" onClick={handleSave}>
        Save Settings
      </button>
    </div>
  );
}

export default Settings;