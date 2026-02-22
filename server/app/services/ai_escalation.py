WINDOW_SIZE = 3
ESCALATION_THRESHOLD = 50

def should_escalate(rule_score):
    return rule_score >= ESCALATION_THRESHOLD

def build_ai_payload(recent_logs):

    latest = recent_logs[-1]

    payload = {
        "employee_role": latest["employee_role"],
        "rule_score": latest["risk_score"],
        "anomaly_score": latest["anomaly_score"],
        "trend": detect_trend([l["risk_score"] for l in recent_logs]),

        "cpu_usage": latest["system_metrics"]["cpu_usage"],
        "network_bytes": latest["network"]["bytes_sent"],

        "employee_cpu_deviation": latest["baseline_deviation"]["employee_cpu_dev"],
        "role_cpu_deviation": latest["baseline_deviation"]["role_cpu_dev"],
        "employee_network_deviation": latest["baseline_deviation"]["employee_net_dev"],
        "role_network_deviation": latest["baseline_deviation"]["role_net_dev"],

        "after_hours": latest["features"]["after_hours"],
        "suspicious_process_count": latest["features"]["suspicious_count"]
    }

    return payload

def detect_trend(scores):
    if not scores:
        return "unknown"

    if len(scores) == 1:
        return "stable"

    if scores[-1] > scores[0]:
        return "increasing"
    elif scores[-1] < scores[0]:
        return "decreasing"

    return "stable"