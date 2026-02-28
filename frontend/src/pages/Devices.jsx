import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/Devices.css";

function Devices() {
  const [devices, setDevices] = useState([]);

  const fetchDevices = async () => {
    try {
      const res = await api.get("/devices");
      setDevices(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchDevices();
  }, []);

  return (
    <div className="devices-container">
      <h2>Registered Devices</h2>

      <table className="devices-table">
        <thead>
          <tr>
            <th>Employee</th>
            <th>Device</th>
            <th>OS</th>
            <th>IP</th>
            <th>Status</th>
            <th>Last Active</th>
          </tr>
        </thead>

        <tbody>
          {devices.length === 0 ? (
            <tr>
              <td colSpan="6">No devices registered</td>
            </tr>
          ) : (
            devices.map((device) => (
              <tr key={device.id}>
                <td>{device.employee?.name}</td>
                <td>{device.device_name}</td>
                <td>{device.os_type}</td>
              <td>{device.ip_address}</td>
              <td>
                <span className={`status ${device.status}`}>
                  {device.status}
                </span>
              </td>
              <td>
                {device.last_active
                  ? new Date(device.last_active).toLocaleString()
                  : "Never"}
              </td>
            </tr>
          )))}
        </tbody>
      </table>
    </div>
  );
}

export default Devices;