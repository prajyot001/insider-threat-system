import { Link } from "react-router-dom";
import "../styles/global.css";

function Home() {
  return (
    <div className="home-wrapper">
      
      {/* Hero Section */}
      <section className="hero">
        <h1>Employee Monitoring & Insider Threat Detection</h1>
        <p>
          Protect your organization with real-time activity monitoring,
          intelligent risk scoring, and advanced security insights.
        </p>

        <div className="hero-buttons">
          <Link to="/login" className="btn-primary">Sign In</Link>
          <Link to="/signup" className="btn-outline">Sign Up</Link>
        </div>
      </section>

      {/* Features Section */}
      <section className="features">
        <h2>Core Features</h2>

        <div className="feature-grid">
          <div className="feature-card">
            <h3>Real-Time Monitoring</h3>
            <p>Track employee activity, device usage, and system events instantly.</p>
          </div>

          <div className="feature-card">
            <h3>Risk Scoring</h3>
            <p>Automatically calculate behavioral risk levels using intelligent analysis.</p>
          </div>

          <div className="feature-card">
            <h3>Alert System</h3>
            <p>Receive alerts for suspicious actions and abnormal activity patterns.</p>
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