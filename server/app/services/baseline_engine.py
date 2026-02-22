# baseline_engine.py

from collections import defaultdict

# Store baseline per employee
employee_baseline = defaultdict(lambda: {
    "cpu_avg": 0,
    "network_avg": 0,
    "count": 0
})


def update_baseline(employee_id, cpu_usage, network_bytes):
    baseline = employee_baseline[employee_id]

    baseline["count"] += 1

    # Running average update
    baseline["cpu_avg"] += (cpu_usage - baseline["cpu_avg"]) / baseline["count"]
    baseline["network_avg"] += (network_bytes - baseline["network_avg"]) / baseline["count"]


def calculate_anomaly_score(employee_id, cpu_usage, network_bytes):

    baseline = employee_baseline[employee_id]

    if baseline["count"] < 5:
        # Not enough data to compare yet
        return 0

    cpu_deviation = abs(cpu_usage - baseline["cpu_avg"])
    network_deviation = abs(network_bytes - baseline["network_avg"])

    anomaly_score = 0

    # CPU deviation scoring
    if cpu_deviation > 30:
        anomaly_score += 25

    # Network deviation scoring
    if network_deviation > (baseline["network_avg"] * 1.5):
        anomaly_score += 35

    return anomaly_score