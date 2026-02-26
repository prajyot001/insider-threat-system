import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import "../styles/auth.css";
import logo from "../assets/icons/logo.png";
import LoaderOverlay from "../components/common/Loader";
import api from "../services/api";

function Login() {
  const navigate = useNavigate();
  const [showOverlay, setShowOverlay] = useState(false);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    console.log("BASE URL:", api.defaults.baseURL);
    console.log("FULL REQUEST URL:", `${api.defaults.baseURL}/auth/login`);
    try {
      const res = await api.post("/auth/login", formData);
      console.log("BASE URL:", api.defaults.baseURL);
      console.log("FULL REQUEST URL:", res.request.responseURL);
      console.log("ENV URL:", process.env.REACT_APP_API_URL);
      localStorage.setItem("token", res.data.access_token);
      setShowOverlay(true);
      const token = localStorage.getItem("token");

      if (!token) {
        navigate("/login");
      } else {
        setTimeout(() => {
          navigate("/dashboard");
        }, 1500);
      }
    } catch (error) {
      console.error("Login error:", error);
      alert("Invalid email or password");
      setLoading(false);
    }
  };

  if (showOverlay) return <LoaderOverlay />;
  return (
    <div className="auth-wrapper">
      <header className="top-header">
        <Link to="/" className="logo-section">
          <img src={logo} alt="Logo" className="real-logo" />
          <span className="company-name">SecureMonitor</span>
        </Link>
      </header>

      <div className="auth-container">
        <h2>Admin Login</h2>

        <form onSubmit={handleLogin} className="auth-form">
          <input
            type="email"
            name="email"
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

          <button
            type="submit"
            className={`btn-primary full-width login-btn ${loading ? "loading" : ""}`}
            disabled={loading}
          >
            <span className="btn-text">Login</span>
            <div className="btn-spinner"></div>
          </button>
        </form>

        <p className="auth-footer">
          Don’t have an account? <Link to="/signup">Sign up</Link>
        </p>
      </div>
    </div>
  );
}

export default Login;
