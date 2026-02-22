WINDOW_SIZE = 3
ESCALATION_THRESHOLD = 50

def should_escalate(rule_score):
    return rule_score >= ESCALATION_THRESHOLD

def build_ai_payload(recent_logs, device_role="employee"):

    if not recent_logs:
        # fallback safe payload
        return {
            "device_role": device_role,
            "behavior_window": {
                "rule_scores": [],
                "risk_trend": "unknown",
                "cpu_levels": [],
                "network_levels": [],
                "suspicious_process_counts": [],
                "after_hours_flags": []
            },
            "max_rule_score": 0,
            "current_rule_score": 0
        }

    rule_scores = [log.get("risk_score", 0) for log in recent_logs]
    cpu_levels = [log.get("features", {}).get("cpu_level", "unknown") for log in recent_logs]
    network_levels = [log.get("features", {}).get("network_level", "unknown") for log in recent_logs]
    suspicious_counts = [log.get("features", {}).get("suspicious_count", 0) for log in recent_logs]
    after_hours_flags = [log.get("features", {}).get("after_hours", False) for log in recent_logs]

    trend = detect_trend(rule_scores)

    max_score = max(rule_scores) if rule_scores else 0
    current_score = rule_scores[-1] if rule_scores else 0

    return {
        "device_role": device_role,
        "behavior_window": {
            "rule_scores": rule_scores,
            "risk_trend": trend,
            "cpu_levels": cpu_levels,
            "network_levels": network_levels,
            "suspicious_process_counts": suspicious_counts,
            "after_hours_flags": after_hours_flags
        },
        "max_rule_score": max_score,
        "current_rule_score": current_score
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