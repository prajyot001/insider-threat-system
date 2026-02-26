import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/Alerts.css";

function Alerts() {
  const [alerts, setAlerts] = useState([]);

  const fetchAlerts = async () => {
    try {
      const res = await api.get("/alerts");
      setAlerts(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchAlerts();
  }, []);

  return (
    <div className="alerts-container">
      <h2>Security Alerts</h2>

      <table className="alerts-table">
        <thead>
          <tr>
            <th>Employee</th>
            <th>Severity</th>
            <th>Risk</th>
            <th>Description</th>
            <th>Status</th>
            <th>Time</th>
          </tr>
        </thead>

        <tbody>
          {alerts.length === 0 ? (
            <tr>
              <td colSpan="6">No alerts available</td>
            </tr>
          ) : (
            alerts.map((alert) => (
              
              <tr key={alert.id}>
                <td>{alert.employee_name}</td>
                <td>
                <span className={`severity ${alert.severity}`}>
                  {alert.severity}
                </span>
              </td>
              <td>{alert.risk_score}</td>
              <td>{alert.description}</td>
              <td>{alert.status}</td>
              <td>
                {new Date(alert.created_at).toLocaleString()}
              </td>
            </tr>
          )))}
        </tbody>
      </table>
    </div>
  );
}

export default Alerts;