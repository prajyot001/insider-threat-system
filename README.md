# 🛡️ SecureMonitor

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-blue)
![Supabase](https://img.shields.io/badge/Supabase-Database-green)
![AI Powered](https://img.shields.io/badge/AI-Enabled-purple)
![Status](https://img.shields.io/badge/Project-Production--Ready-success)


🛡️ SecureMonitor

AI-Powered Insider Threat Detection & Behavioral Risk Intelligence Platform

---

📌 Overview

**SecureMonitor** is an AI-driven insider threat detection system designed to monitor employee behavior, detect anomalies, and generate intelligent risk alerts in real time.

The system uses:

* Rule-based risk analysis
* Role-aware behavioral baselines
* AI-powered anomaly interpretation
* Daily behavioral aggregation
* Secure cloud storage (Supabase)

It is built as a scalable SaaS-ready cybersecurity platform.

---

# 🏗️ Architecture

SecureMonitor is designed with **two separate backend servers** to handle scalability and reduce load after deployment (e.g., on Render).

---

## 🔹 1️⃣ Main Application Server

**Frontend + Backend + Supabase**

Handles:

* Company signup & login
* Admin dashboard
* Risk engine
* AI escalation
* Baseline modeling
* Alert generation
* Supabase database integration

Tech:

* FastAPI
* React
* Supabase
* AI API

---

## 🔹 2️⃣ Device Server (Monitoring Agent Server)

**Device → Analysis → Database**

Handles:

* Device telemetry collection
* CPU, RAM monitoring
* Network monitoring
* External device detection
* File activity
* Screenshot events
* Suspicious process tracking
* Sending logs to Main Server

This separation:

* Reduces load on main server
* Improves scalability
* Allows horizontal scaling
* Enables production-ready deployment

---

# 🔄 System Flow

```
Employee Device
     ↓
Device Monitoring Agent
     ↓
Device Server (Analysis)
     ↓
Main Application Server
     ↓
Risk Engine + Baseline Engine
     ↓
AI Escalation Layer
     ↓
Supabase Database
     ↓
Admin Dashboard
```

---

# 🧠 Intelligence Layers

## 🔹 Rule-Based Risk Engine

Evaluates:

* High CPU usage
* High RAM usage
* Network spikes
* Suspicious processes
* After-hours activity
* USB/external device usage
* File access events

Outputs:

* Risk Score (0–100)
* Severity (Low / Medium / High)
* Reasons

---

## 🔹 Role-Aware Baseline Engine

Maintains:

* Employee baseline
* Role baseline
* CPU deviation
* Network deviation

Calculates:

* Behavioral anomaly score
* Baseline deviation metrics

---

## 🔹 AI Escalation Layer

Triggered when:

* Risk score crosses threshold
* Suspicious activity pattern appears

AI analyzes:

* Current activity
* Daily behavior summary
* Role baseline deviation
* Historical behavior trend

Returns:

* AI score
* AI severity
* AI explanation

Final Score =
`max(rule_score, anomaly_score, ai_score)`

---

## 🔹 Daily Behavior Aggregator

Collects:

* Daily average CPU usage
* Daily average network usage
* Suspicious activity frequency
* After-hours activity frequency

Detects:

* Behavior drift
* Gradual data exfiltration
* Long-term risk buildup

---

# 🗄️ Database (Supabase)

Tables:

* `companies`
* `employees`
* `devices`
* `activity_logs`
* `telemetry_snapshots`
* `alerts`
* `registration_tokens`

Security:

* Row-Level Security (RLS)
* UUID-based identifiers
* Multi-tenant ready structure

---

# 🌐 Admin Dashboard (Frontend)

Built using:

* React
* Supabase Auth
* Lottie animations
* Modern dashboard layout

Features:

* Company Signup
* Admin Login
* Employee monitoring
* Alert dashboard
* Risk visualization

---

# ⚙️ Tech Stack

### Backend

* FastAPI
* Python
* Uvicorn
* Supabase (PostgreSQL)
* AI API integration

### Frontend

* React
* React Router
* Supabase JS
* Lottie-react

### Monitoring Agent

* Python
* psutil
* Scheduler
* HTTP log sender

---

# 🚀 Running the Project

## 🔹 Run Backend Server

From project root:

```bash
python run.py
```

This starts the FastAPI main server.

---

## 🔹 Run Device Monitoring Agent

```bash
python run.py
```

(Inside device/agent directory if separated)

---

## 🔹 Run Frontend

```bash
cd frontend
npm install
npm start
```

---

# 🔐 Privacy Design

SecureMonitor does NOT:

* Log keystrokes
* Capture file content
* Upload private documents
* Record screen content

It only stores:

* Behavioral metadata
* System telemetry
* Aggregated activity patterns

Designed to balance:
Security + Privacy

---

# 📊 Example Risk Output

```json
{
  "rule_score": 25,
  "anomaly_score": 16,
  "ai_score": 40,
  "final_score": 40,
  "severity": "medium",
  "ai_reason": "Network usage significantly higher than role baseline."
}
```

---

# 📦 Deployment

Designed for deployment on:

* Render (Backend)
* Supabase (Database)
* Static Hosting / Render (Frontend)

Dual-server architecture ensures:

* Load distribution
* Better scalability
* Production readiness

---

# 🎯 Future Improvements

* WebSocket real-time dashboard updates
* Advanced ML anomaly detection
* Insider risk heatmaps
* Automated response system
* Role-based AI fine-tuning
* SaaS subscription billing model

---

# 🏆 Project Vision

SecureMonitor aims to become a next-generation insider threat detection SaaS platform that:

* Uses AI for behavioral intelligence
* Scales for enterprise use
* Protects company data
* Respects employee privacy

---


