import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/Employees.css";
import AddEmployeeModal from "./AddEmployeeModal.jsx";
import GenerateTokenModal from "../components/layout/GenerateTokenModal.jsx";

function Employees() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [selectedEmployee, setSelectedEmployee] = useState(null);

  const fetchEmployees = async () => {
    try {
      const res = await api.get("/employees");
      setEmployees(res.data);
    } catch (err) {
      console.error("Error fetching employees:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, []);

  return (
    <div className="employees-container">
      <div className="employees-header">
        <h2>Employee Management</h2>
        <button className="add-btn" onClick={() => setShowModal(true)}>
          + Add Employee
        </button>
      </div>
      {loading ? (
        <p>Loading employees...</p>
      ) : (
        <table className="employee-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Department</th>
              <th>Risk</th>
              <th>Device</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>

          <tbody>
            {employees.length === 0 ? (
              <tr>
                <td colSpan="8">No employees found</td>
              </tr>
            ) : (
              employees.map((emp) => (
                <tr key={emp.employee_id}>
                  <td>{emp.name}</td>
                  <td>{emp.email}</td>
                  <td>{emp.role}</td>
                  <td>{emp.department}</td>
                  <td>
                    <span className="risk-badge">{emp.risk_score ?? 0}</span>
                  </td>
                  <td>
                    {emp.device_registered ? "Registered" : "Not Registered"}
                  </td>
                  <td>
                    <span className={`status ${emp.status}`}>{emp.status}</span>
                  </td>
                  <td>
                    <button
                      className="action-btn"
                      onClick={() => setSelectedEmployee(emp.employee_id)}
                    >
                      Generate Token
                    </button>
                    <button className="danger-btn">Disable</button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      )}
      {showModal && (
        <AddEmployeeModal
          onClose={() => setShowModal(false)}
          onEmployeeAdded={fetchEmployees}
        />
      )}
      {selectedEmployee && (
        <GenerateTokenModal
          employeeId={selectedEmployee}
          onClose={() => setSelectedEmployee(null)}
        />
      )}
    </div>
  );
}

export default Employees;
