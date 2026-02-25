# baseline_engine.py

from collections import defaultdict

# Store baseline per employee
employee_baseline = defaultdict(lambda: {
    "cpu_avg": 0,
    "network_avg": 0,
    "count": 0
})


role_baseline = defaultdict(lambda: {
    "cpu_avg": 0,
    "network_avg": 0,
    "count": 0
})

def update_baseline(employee_id, employee_role, cpu_usage, network_bytes):

    # --- Employee baseline ---
    emp = employee_baseline[employee_id]
    emp["count"] += 1
    emp["cpu_avg"] += (cpu_usage - emp["cpu_avg"]) / emp["count"]
    emp["network_avg"] += (network_bytes - emp["network_avg"]) / emp["count"]

    # --- Role baseline ---
    role = role_baseline[employee_role]
    role["count"] += 1
    role["cpu_avg"] += (cpu_usage - role["cpu_avg"]) / role["count"]
    role["network_avg"] += (network_bytes - role["network_avg"]) / role["count"]

def calculate_anomaly_score(employee_id, employee_role, cpu_usage, network_bytes):

    emp = employee_baseline[employee_id]
    role = role_baseline[employee_role]

    if emp["count"] < 5 or role["count"] < 5:
        return {
            "anomaly_score": 0,
            "employee_cpu_dev": 0,
            "role_cpu_dev": 0,
            "employee_net_dev": 0,
            "role_net_dev": 0
        }

    emp_cpu_dev = abs(cpu_usage - emp["cpu_avg"])
    role_cpu_dev = abs(cpu_usage - role["cpu_avg"])

    emp_net_dev = abs(network_bytes - emp["network_avg"])
    role_net_dev = abs(network_bytes - role["network_avg"])

    anomaly_score = 0

    if emp_cpu_dev > 30:
        anomaly_score += 20

    if role_cpu_dev > 40:
        anomaly_score += 30

    if emp_net_dev > emp["network_avg"] * 1.5:
        anomaly_score += 25

    if role_net_dev > role["network_avg"] * 2:
        anomaly_score += 35

    return {
        "anomaly_score": anomaly_score,
        "employee_cpu_dev": emp_cpu_dev,
        "role_cpu_dev": role_cpu_dev,
        "employee_net_dev": emp_net_dev,
        "role_net_dev": role_net_dev
    }