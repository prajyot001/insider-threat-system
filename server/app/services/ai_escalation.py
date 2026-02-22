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
def build_behavioral_ai_payload(current_log, daily_summary, recent_logs):

    return {
        "employee_role": current_log["employee_role"],

        # Current snapshot
        "current_activity": {
            "cpu_usage": current_log["system_metrics"]["cpu_usage"],
            "network_bytes": current_log["network"]["bytes_sent"],
            "rule_score": current_log["risk_score"],
            "anomaly_score": current_log["anomaly_score"],
            "risk_velocity": current_log.get("risk_velocity", 0)
        },

        # Daily behavior summary
        "daily_summary": daily_summary,

        # Recent trend
        "recent_scores": [
            l["risk_score"] for l in recent_logs
        ],

        # Baseline deviation
        "role_cpu_deviation": current_log["baseline_deviation"]["role_cpu_dev"],
        "role_network_deviation": current_log["baseline_deviation"]["role_net_dev"],

        "after_hours": current_log["features"]["after_hours"],
        "suspicious_process_count": current_log["features"]["suspicious_count"]
    }
    
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