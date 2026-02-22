from collections import defaultdict
from datetime import datetime

daily_store = defaultdict(lambda: {
    "total_logs": 0,
    "cpu_sum": 0,
    "cpu_max": 0,
    "network_sum": 0,
    "network_max": 0,
    "usb_events": 0,
    "after_hours_sessions": 0,
    "rule_score_sum": 0,
    "anomaly_score_sum": 0
})


def update_daily_summary(log_dict):

    employee_id = log_dict["employee_id"]
    today = datetime.utcnow().date().isoformat()

    key = f"{employee_id}_{today}"
    summary = daily_store[key]

    cpu = log_dict["system_metrics"]["cpu_usage"]
    network = log_dict["network"]["bytes_sent"]
    rule_score = log_dict["risk_score"]
    anomaly_score = log_dict["anomaly_score"]

    summary["total_logs"] += 1
    summary["cpu_sum"] += cpu
    summary["cpu_max"] = max(summary["cpu_max"], cpu)

    summary["network_sum"] += network
    summary["network_max"] = max(summary["network_max"], network)

    summary["rule_score_sum"] += rule_score
    summary["anomaly_score_sum"] += anomaly_score

    if log_dict["features"]["after_hours"]:
        summary["after_hours_sessions"] += 1
        
        
def get_daily_summary(employee_id):

    today = datetime.utcnow().date().isoformat()
    key = f"{employee_id}_{today}"

    summary = daily_store.get(key)

    if not summary or summary["total_logs"] == 0:
        return None

    return {
        "employee_id": employee_id,
        "date": today,
        "avg_cpu": summary["cpu_sum"] / summary["total_logs"],
        "max_cpu": summary["cpu_max"],
        "avg_network": summary["network_sum"] / summary["total_logs"],
        "max_network": summary["network_max"],
        "avg_rule_score": summary["rule_score_sum"] / summary["total_logs"],
        "avg_anomaly_score": summary["anomaly_score_sum"] / summary["total_logs"],
        "after_hours_sessions": summary["after_hours_sessions"],
        "total_logs": summary["total_logs"]
    }