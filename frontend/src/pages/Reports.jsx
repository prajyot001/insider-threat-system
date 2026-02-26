import { useState } from "react";
import api from "../services/api";
import "../styles/Reports.css";

function Reports() {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [summary, setSummary] = useState(null);

  const fetchSummary = async () => {
    try {
      const res = await api.get("/reports/summary", {
        params: { start_date: startDate, end_date: endDate },
      });

      setSummary(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  const downloadReport = async () => {
    const response = await api.get("/reports/download", {
      params: { start_date: startDate, end_date: endDate },
      responseType: "blob",
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "security_report.pdf");
    document.body.appendChild(link);
    link.click();
  };

  return (
    <div className="reports-container">
      <h2>Security Reports</h2>

      <div className="filter-section">
        <input type="date" onChange={(e) => setStartDate(e.target.value)} />
        <input type="date" onChange={(e) => setEndDate(e.target.value)} />
        <button onClick={fetchSummary}>Generate</button>
      </div>

      {summary && (
        <div className="summary-cards">
          <div className="card">
            <h3>Total Alerts</h3>
            <p>{summary.total_alerts}</p>
          </div>

          <div className="card">
            <h3>High Risk</h3>
            <p>{summary.high_risk}</p>
          </div>

          <div className="card">
            <h3>Resolved</h3>
            <p>{summary.resolved}</p>
          </div>
        </div>
      )}

      <button className="download-btn" onClick={downloadReport}>
        Download pdf
      </button>
    </div>
  );
}

export default Reports;
