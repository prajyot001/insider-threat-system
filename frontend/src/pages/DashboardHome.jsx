import "../styles/dashboardHome.css";
import api from "../services/api";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

import { useEffect, useState } from "react";
import { useRef } from "react";

function DashboardHome() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [chartData, setChartData] = useState(null);
  const [recentAlerts, setRecentAlerts] = useState([]);
  const fetched = useRef(false);

  //chartdata = { riskTrend: [...], alertsSeverity: [...] }
  const fetchCharts = async () => {
    try {
      const res = await api.get("/dashboard/charts");
      setChartData(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  // fetch stats for summary cards

  const fetchData = async () => {
    try {
      const res = await api.get("/dashboard/overview");
      setStats(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // fetch recent alerts - for simplicity, using static data in the table section

  const fetchRecentAlerts = async () => {
    try {
      const token = localStorage.getItem("token");

      const res = await api.get("/dashboard/alerts", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setRecentAlerts(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const COLORS = ["#ff4d4d", "#f5b942", "#4caf50"];

  useEffect(() => {
    if (fetched.current) return;
    fetched.current = true;
    fetchData();
    fetchCharts();
    fetchRecentAlerts();
  }, []);

  return (
    <div className="dashboard-home">
      <div className="dashboard-header">
        <h2>Security Overview</h2>
        <p>Real-time insider threat monitoring</p>
      </div>

      {/* Summary Cards */}
      <div className="summary-grid">
        <div className="summary-card">
          <h3>{loading ? "..." : stats?.totalEmployees}</h3>
          <span>Total Employees</span>
        </div>
        <div className="summary-card">
          <h3>{loading ? "..." : stats?.activeDevices} </h3>
          <span>Active Devices</span>
        </div>
        <div className="summary-card danger">
          <h3>{loading ? "..." : stats?.openAlerts}</h3>
          <span>Open Alerts</span>
        </div>
        <div className="summary-card warning">
          <h3>{loading ? "..." : stats?.highRiskUsers}</h3>
          <span>High Risk Users</span>
        </div>
      </div>

      {/* Charts Section */}
      <div className="chart-grid">
        {/* Risk Trend Line Chart */}
        <div className="chart-box">
          <h4>Risk Trend (Weekly)</h4>
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={chartData?.riskTrend || []}>
              <XAxis dataKey="day" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="risk"
                stroke="#c9a86a"
                strokeWidth={3}
                dot={{ r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Alerts Severity Pie Chart */}
        <div className="chart-box">
          <h4>Alerts by Severity</h4>
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Pie
                data={chartData?.alertsSeverity || []}
                cx="50%"
                cy="50%"
                outerRadius={70}
                dataKey="value"
                label
              >
                {chartData?.alertsSeverity?.map((entry, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Alerts Table */}
      <div className="table-section">
        <h4>Recent Alerts</h4>
        <table>
          <thead>
            <tr>
              <th>Employee</th>
              <th>Type</th>
              <th>Severity</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {recentAlerts.length === 0 ? (
              <tr>
                <td
                  colSpan="4"
                  style={{ textAlign: "center", padding: "20px" }}
                >
                  No recent alerts
                </td>
              </tr>
            ) : (
              recentAlerts.map((alert) => (
                <tr key={alert.id}>
                  <td>{alert.employeeName}</td>
                  <td>{alert.deviceName}</td>
                  <td className={`severity-${alert.severity.toLowerCase()}`}>
                    {alert.severity}
                  </td>
                  <td>{new Date(alert.createdAt).toLocaleString()}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default DashboardHome;
