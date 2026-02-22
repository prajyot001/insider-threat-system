def map_cpu_level(cpu):
    if cpu < 50:
        return "low"
    elif cpu < 80:
        return "medium"
    else:
        return "critical"


def map_network_level(bytes_sent):
    if bytes_sent < 5_000_000:
        return "low"
    elif bytes_sent < 50_000_000:
        return "medium"
    else:
        return "high"


def extract_features(log):
    system = log["system_metrics"]
    network = log["network"]

    return {
        "cpu_level": map_cpu_level(system["cpu_usage"]),
        "network_level": map_network_level(network["bytes_sent"]),
        "suspicious_count": len(log["suspicious_processes"]),
        "after_hours": is_after_hours(system["timestamp"]),
        "rule_score": log.get("risk_score", 0)
    }


def is_after_hours(timestamp):
    from datetime import datetime
    hour = datetime.fromisoformat(timestamp).hour
    return hour < 7 or hour > 21