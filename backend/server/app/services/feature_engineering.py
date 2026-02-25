from datetime import datetime


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

    features = {
        "cpu_level": "high" if system["cpu_usage"] > 50 else "low",
        "network_level": "high" if network["bytes_sent"] > 50_000_000 else "low",
        "suspicious_count": len(log.get("suspicious_processes", [])),
        "after_hours": False,
        "rule_score": log.get("risk_score", 0)
    }

    hour = datetime.fromisoformat(system["timestamp"]).hour
    if hour < 7 or hour > 21:
        features["after_hours"] = True

    return features

def is_after_hours(timestamp):
    from datetime import datetime
    hour = datetime.fromisoformat(timestamp).hour
    return hour < 7 or hour > 21