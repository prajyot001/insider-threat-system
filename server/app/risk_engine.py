from datetime import datetime

def calculate_risk(log_data: dict) -> dict:
    risk_score = 0
    reasons = []

    system = log_data["system_metrics"]
    network = log_data["network"]
    suspicious_processes = log_data["suspicious_processes"]

    # 🔹 CPU Spike
    if system["cpu_usage"] > 50:
        risk_score += 20
        reasons.append("High CPU usage")

    # 🔹 RAM Spike
    if system["ram_usage"] > 85:
        risk_score += 15
        reasons.append("High RAM usage")

    # 🔹 Network Spike (simple threshold)
    if network["bytes_sent"] > 50_000_000:  # 50MB
        risk_score += 25
        reasons.append("High outbound network traffic")

    # 🔹 Suspicious Processes
    if len(suspicious_processes) > 0:
        risk_score += 40
        reasons.append("Suspicious process detected")

    # 🔹 After-hours activity
    hour = datetime.fromisoformat(system["timestamp"]).hour
    if hour < 7 or hour > 21:
        risk_score += 20
        reasons.append("After-hours activity")

    # Cap score at 100
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
    
