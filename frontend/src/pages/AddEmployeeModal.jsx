import { useState } from "react";
import api from "../services/api";
import "../styles/AddEmployeeModal.css";

function AddEmployeeModal({ onClose, onEmployeeAdded }) {
  const [form, setForm] = useState({
    name: "",
    email: "",
    role: "employee",
    department: "",
    status: "active",
    password: ""
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await api.post("/employees", form);
      onEmployeeAdded();  // refresh table
      onClose();          // close modal
    } catch (err) {
      console.error("Error creating employee:", err);
      alert("Failed to create employee");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-box">
        <h3>Add New Employee</h3>

        <form onSubmit={handleSubmit}>
          <input
            type="text"
            name="name"
            placeholder="Full Name"
            required
            onChange={handleChange}
          />

          <input
            type="email"
            name="email"
            placeholder="Email"
            required
            onChange={handleChange}
          />

          <input
            type="text"
            name="department"
            placeholder="Department"
            required
            onChange={handleChange}
          />

          <select name="role" onChange={handleChange}>
            <option value="employee">Employee</option>
            <option value="manager">Manager</option>
          </select>

          <select name="status" onChange={handleChange}>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>

          <input
            type="password"
            name="password"
            placeholder="Temporary Password"
            required
            onChange={handleChange}
          />

          <div className="modal-actions">
            <button type="button" onClick={onClose}>
              Cancel
            </button>

            <button type="submit" disabled={loading}>
              {loading ? "Creating..." : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default AddEmployeeModal;