from datetime import datetime
from datetime import datetime

def calculate_risk(log_data: dict) -> dict:
    risk_score = 0
    reasons = []

    system = log_data["system_metrics"]
    network = log_data["network"]
    suspicious_processes = log_data.get("suspicious_processes", [])

    # 🔹 External USB
    if log_data.get("external_devices", {}).get("usb_connected_count", 0) > 0:
        risk_score += 20
        reasons.append("External storage connected")

    # 🔹 File Activity
    if log_data.get("file_activity", {}).get("recent_file_access_count", 0) > 0:
        risk_score += 10
        reasons.append("Recent file access detected")

    # 🔹 Screenshot Activity
    if log_data.get("screen_activity", {}).get("screenshot_taken", False):
        risk_score += 5
        reasons.append("Screen capture capability detected")

    # 🔹 CPU Spike
    if system["cpu_usage"] > 50:
        risk_score += 20
        reasons.append("High CPU usage")

    # 🔹 RAM Spike
    if system["ram_usage"] > 85:
        risk_score += 15
        reasons.append("High RAM usage")

    # 🔹 Network Spike
    if network["bytes_sent"] > 50_000_000:
        risk_score += 25
        reasons.append("High outbound network traffic")

    # 🔹 Suspicious Processes
    if len(suspicious_processes) > 0:
        risk_score += 40
        reasons.append("Suspicious process detected")

    # 🔹 After-hours
    hour = datetime.fromisoformat(system["timestamp"]).hour
    if hour < 7 or hour > 21:
        risk_score += 20
        reasons.append("After-hours activity")

    risk_score = min(risk_score, 100)

    return {
        "risk_score": risk_score,
        "reasons": reasons,
        "severity": get_severity(risk_score)
    }


def get_severity(score: int) -> str:
    if score < 30:
        return "low"
    elif score < 70:
        return "medium"
    else:
        return "high"

def get_severity(score: int) -> str:
    if score < 30:
        return "low"
    elif score < 70:
        return "medium"
    else:
        return "high"
    
