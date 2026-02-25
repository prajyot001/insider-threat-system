import "../styles/dashboardHome.css";
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
import axios from "axios";
import { useEffect, useState } from "react";

function DashboardHome() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [chartData, setChartData] = useState(null);
  const fetchCharts = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/dashboard/charts");
      setChartData(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  fetchCharts();
  

  const COLORS = ["#ff4d4d", "#f5b942", "#4caf50"];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/dashboard/overview");
        setStats(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
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
            <tr>
              <td>John Doe</td>
              <td>USB Access</td>
              <td className="severity-high">High</td>
              <td>2 min ago</td>
            </tr>
            <tr>
              <td>Sarah Smith</td>
              <td>File Download</td>
              <td className="severity-medium">Medium</td>
              <td>10 min ago</td>
            </tr>
            <tr>
              <td>Alex Johnson</td>
              <td>Login Attempt</td>
              <td className="severity-low">Low</td>
              <td>25 min ago</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default DashboardHome;
