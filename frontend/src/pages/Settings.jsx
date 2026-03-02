import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/Settings.css";

function Settings() {
  const [form, setForm] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchSettings = async () => {
    try {
      const res = await api.get("/settings");
      setForm({
        company_name: res.data.company.company_name,
        risk_threshold: res.data.company.risk_threshold,
        email_alerts: res.data.company.email_alerts,
        name: res.data.admin.name,
        email: res.data.admin.email,
        new_password: ""
      });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value
    });
  };

  const handleSave = async () => {
    try {
      await api.put("/settings", form);
      alert("Settings Updated Successfully");
    } catch (err) {
      alert("Update Failed");
    }
  };

  if (loading) return <p>Loading...</p>;

  return (
    <div className="settings-container">
      <h2>System Settings</h2>

      <div className="settings-card">
        <h3>Company Settings</h3>
        <input
          name="company_name"
          value={form.company_name}
          onChange={handleChange}
        />

        <label>Risk Threshold: {form.risk_threshold}</label>
        <input
          type="range"
          name="risk_threshold"
          min="0"
          max="100"
          value={form.risk_threshold}
          onChange={handleChange}
        />

        <label>
          Email Alerts
          <input
            type="checkbox"
            name="email_alerts"
            checked={form.email_alerts}
            onChange={handleChange}
          />
        </label>
      </div>

      <div className="settings-card">
        <h3>Admin Profile</h3>
        <input name="name" value={form.name} onChange={handleChange} />
        <input name="email" value={form.email} onChange={handleChange} />
        <input
          type="password"
          name="new_password"
          placeholder="New Password (optional)"
          onChange={handleChange}
        />
      </div>

      <button className="save-btn" onClick={handleSave}>
        Save Changes
      </button>
    </div>
  );
}

export default Settings;