from fastapi import APIRouter
from ..schemas import LogCreate
from ..storage import add_log, get_logs, clear_logs
from ..services.risk_engine import calculate_risk
from ..services.feature_engineering import extract_features
from ..services.ai_escalation import should_escalate, build_ai_payload
from ..services.ai_service import call_ai, is_cooldown_active, update_cooldown
from ..services.baseline_engine import update_baseline, calculate_anomaly_score
router = APIRouter()

@router.post("/logs")
def receive_log(log: LogCreate):

    log_dict = log.model_dump()
    print("RECEIVED:", log_dict)

    # 1️⃣ Rule scoring
    risk_result = calculate_risk(log_dict)
    log_dict["risk_score"] = risk_result["risk_score"]
    log_dict["severity"] = risk_result["severity"]
    log_dict["reasons"] = risk_result["reasons"]

    # 2️⃣ Feature engineering
    log_dict["features"] = extract_features(log_dict)

    # 3️⃣ Baseline anomaly
    employee_id = log_dict["employee_id"]
    employee_role = log_dict["employee_role"]

    cpu_usage = log_dict["system_metrics"]["cpu_usage"]
    network_bytes = log_dict["network"]["bytes_sent"]

    baseline_result = calculate_anomaly_score(
        employee_id,
        employee_role,
        cpu_usage,
        network_bytes
    )

    anomaly_score = baseline_result["anomaly_score"]
    log_dict["anomaly_score"] = anomaly_score
    log_dict["baseline_deviation"] = {
        "employee_cpu_dev": baseline_result["employee_cpu_dev"],
        "role_cpu_dev": baseline_result["role_cpu_dev"],
        "employee_net_dev": baseline_result["employee_net_dev"],
        "role_net_dev": baseline_result["role_net_dev"]
    }

    update_baseline(
        employee_id,
        employee_role,
        cpu_usage,
        network_bytes
    )

    # 4️⃣ AI escalation decision (use rule + anomaly)
    pre_ai_score = max(log_dict["risk_score"], anomaly_score)

    device_id = log_dict["device_id"]

    if should_escalate(pre_ai_score) and not is_cooldown_active(device_id):

        all_logs = get_logs() + [log_dict]
        recent_logs = all_logs[-3:]

        ai_payload = build_ai_payload(recent_logs)
        print("AI PAYLOAD:", ai_payload)

        ai_result = call_ai(ai_payload)

        if ai_result["ai_score"] is not None:
            log_dict["ai_score"] = ai_result["ai_score"]
            log_dict["ai_reason"] = ai_result["reason"]
            log_dict["ai_severity"] = ai_result["severity"]

        update_cooldown(device_id)

    # 5️⃣ Final composite score
    final_score = max(
        log_dict["risk_score"],
        anomaly_score,
        log_dict.get("ai_score", 0)
    )

    log_dict["final_score"] = final_score

    # 6️⃣ Store
    add_log(log_dict)

    return {
        "status": "log received",
        "rule_score": log_dict["risk_score"],
        "anomaly_score": anomaly_score,
        "final_score": final_score
    }

@router.get("/logs")
def view_logs():
    return get_logs()


@router.delete("/logs")
def delete_logs():
    clear_logs()
    return {"status": "logs cleared"}