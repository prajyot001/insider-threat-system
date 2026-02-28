import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/logs.css";

function Logs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchLogs = async () => {
    try {
      const res = await api.get("/logs");
      setLogs(res.data);
    } catch (err) {
      console.error("Error fetching logs:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  return (
    <div className="logs-container">
      <div className="logs-header">
        <h2>System Activity Logs</h2>
        <button onClick={fetchLogs}>Refresh</button>
      </div>

      {loading ? (
        <p>Loading logs...</p>
      ) : (
        <table className="logs-table">
          <thead>
            <tr>
              <th>Employee</th>
              <th>Device</th>
              <th>Action</th>
              <th>Risk</th>
              <th>Status</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {logs.length === 0 ? (
              <tr>
                <td colSpan="6">No logs found</td>
              </tr>
            ) : (
              logs.map((log, index) => (
                <tr key={index}>
                  <td>{log.employee?.name}</td>
                  <td>{log.device_name}</td>
                  <td>{log.event_type}</td>
                  <td>
                    <span className="risk-badge">{log.risk_score}</span>
                  </td>
                  <td>
                    <span className={`status ${log.status}`}>
                      {log.status}
                    </span>
                  </td>
                  <td>{new Date(log.created_at).toLocaleString()}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default Logs;