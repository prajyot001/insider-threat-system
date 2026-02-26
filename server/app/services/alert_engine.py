def generate_alert(log_dict):

    return {
        "employee_id": log_dict["employee_id"],
        "severity": log_dict["ai_severity"],
        "threat_type": log_dict.get("ai_threat_type"),
        "reason": log_dict.get("ai_reason"),
        "final_score": log_dict["final_score"],
        "timestamp": log_dict["system_metrics"]["timestamp"]
    }