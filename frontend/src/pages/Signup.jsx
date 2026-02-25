import { useState } from "react";
import { Link } from "react-router-dom";
import logo from "../assets/icons/logo.png";
import "../styles/auth.css";

function Signup() {
  const [formData, setFormData] = useState({
    companyName: "",
    companyEmail: "",
    adminName: "",
    adminEmail: "",
    password: "",
    confirmPassword: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);
    // Later connect to backend
  };

  return (
    <div className="auth-wrapper">
      {/* Header */}
      <header className="top-header">
        <div className="logo-section">
          <Link to="/">
            <img src={logo} alt="Logo" className="real-logo" />
          </Link>
          <span className="company-name">SecureMonitor</span>
        </div>
      </header>

      {/* Signup Form */}
      <div className="auth-container">
        <h2>Create Company Account</h2>

        <form onSubmit={handleSubmit} className="auth-form">
          <h4>Company Information</h4>
          <input
            type="text"
            name="companyName"
            placeholder="Company Name"
            onChange={handleChange}
            required
          />

          <input
            type="email"
            name="companyEmail"
            placeholder="Company Email"
            onChange={handleChange}
            required
          />

          <h4>Admin Information</h4>
          <input
            type="text"
            name="adminName"
            placeholder="Admin Name"
            onChange={handleChange}
            required
          />

          <input
            type="email"
            name="adminEmail"
            placeholder="Admin Email"
            onChange={handleChange}
            required
          />

          <input
            type="password"
            name="password"
            placeholder="Password"
            onChange={handleChange}
            required
          />

          <input
            type="password"
            name="confirmPassword"
            placeholder="Confirm Password"
            onChange={handleChange}
            required
          />

          <button type="submit" className="btn-primary full-width">
            Create Account
          </button>
        </form>

        <p className="auth-switch">
          Already have an account? <Link to="/login">Sign In</Link>
        </p>
      </div>
    </div>
  );
}

export default Signup;
