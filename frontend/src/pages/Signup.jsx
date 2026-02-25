import { useState } from "react";
import axios from "axios";
import "../styles/auth.css";
import logo from "../assets/icons/logo.png";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
function Signup() {
  const [step, setStep] = useState(1);
  const [otp, setOtp] = useState("");
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    companyName: "",
    companyEmail: "",
    adminName: "",
    adminEmail: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const sendOtp = async (e) => {
    e.preventDefault();

    try {
      await axios.post("http://127.0.0.1:8000/auth/signup", formData);
      setStep(2);
    } catch (error) {
      alert("Failed to send OTP");
    }
  };

  const verifyOtp = async (e) => {
    e.preventDefault();

    try {
      await axios.post("http://127.0.0.1:8000/auth/verify-otp", {
        adminEmail: formData.adminEmail,
        otp: otp,
      });

      alert("Signup Successful!");
      // redirect to login
      setTimeout(() => {
        navigate("/login");
      }, 1500);
    } catch (error) {
      alert("Invalid OTP");
    }
  };

  return (
    <div className="auth-wrapper">
      <header className="top-header">
        <Link to="/" className="logo-section">
          <img src={logo} alt="Logo" className="real-logo" />
          <span className="company-name">SecureMonitor</span>
        </Link>
      </header>

      <div className="auth-container">
        {step === 1 && (
          <>
            <h2>Create Company Account</h2>
            <form onSubmit={sendOtp} className="auth-form">
              <input
                type="text"
                name="companyName"
                placeholder="Company Name"
                required
                onChange={handleChange}
              />
              <input
                type="email"
                name="companyEmail"
                placeholder="Company Email"
                required
                onChange={handleChange}
              />
              <input
                type="text"
                name="adminName"
                placeholder="Admin Name"
                required
                onChange={handleChange}
              />
              <input
                type="email"
                name="adminEmail"
                placeholder="Admin Email"
                required
                onChange={handleChange}
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                required
                onChange={handleChange}
              />
              <button type="submit" className="btn-primary full-width">
                Send OTP
              </button>
            </form>
          </>
        )}

        {step === 2 && (
          <>
            <h2>Verify OTP</h2>
            <form onSubmit={verifyOtp} className="auth-form">
              <input
                type="text"
                placeholder="Enter OTP"
                value={otp}
                required
                onChange={(e) => setOtp(e.target.value)}
              />
              <button type="submit" className="btn-primary full-width">
                Verify OTP
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}

export default Signup;
