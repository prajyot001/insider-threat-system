import { Link ,NavLink} from "react-router-dom";
import "../styles/global.css";
import { motion } from "framer-motion";
import logo from "../assets/icons/logo.png";

function Home() {
  return (
    
    <div className="home-wrapper">

       {/* Top Header */}
      <header className="top-header">
        <div className="logo-section">
          <NavLink to="/" className="logo-section">
          <img src={logo} alt="Logo" className="real-logo" />
          <span className="company-name">SecureMonitor</span>
        </NavLink>
        </div>
      </header>

      {/* Hero Section */}
      <div className="home-wrapper">
        <motion.section
          className="hero"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 0.8 }}
          >
            Employee Monitoring & Insider Threat Detection
          </motion.h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.8 }}
          >
            Real-time activity tracking, intelligent risk scoring, and secure
            administrative control.
          </motion.p>

          <motion.div
            className="hero-buttons"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6, duration: 0.8 }}
          >
            <Link to="/login" className="btn-primary">
              Sign In
            </Link>
            <Link to="/signup" className="btn-outline">
              Sign Up
            </Link>
          </motion.div>
        </motion.section>
      </div>

      {/* Features Section */}
      <section className="features">
        <h2>Core Features</h2>

        <div className="feature-grid">
          <div className="feature-card">
            <h3>Real-Time Monitoring</h3>
            <p>
              Track employee activity, device usage, and system events
              instantly.
            </p>
          </div>

          <div className="feature-card">
            <h3>Risk Scoring</h3>
            <p>
              Automatically calculate behavioral risk levels using intelligent
              analysis.
            </p>
          </div>

          <div className="feature-card">
            <h3>Alert System</h3>
            <p>
              Receive alerts for suspicious actions and abnormal activity
              patterns.
            </p>
          </div>

          <div className="feature-card">
            <h3>Secure Dashboard</h3>
            <p>Admin-only access with complete visibility and control.</p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-it-works">
        <h2>How It Works</h2>

        <div className="steps">
          <div className="step">
            <span>1</span>
            <p>Monitoring agent collects activity logs securely.</p>
          </div>

          <div className="step">
            <span>2</span>
            <p>Server processes logs and calculates risk scores.</p>
          </div>

          <div className="step">
            <span>3</span>
            <p>Admin dashboard displays insights and alerts.</p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
