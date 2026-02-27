from fastapi import APIRouter
from ..schemas import LogCreate
from ..storage import add_log, get_logs, clear_logs
from ..services.risk_engine import calculate_risk
from ..services.feature_engineering import extract_features
from ..services.ai_escalation import build_behavioral_ai_payload, should_escalate, build_ai_payload
from ..services.ai_service import call_ai, is_cooldown_active, update_cooldown
from ..services.baseline_engine import update_baseline, calculate_anomaly_score
from ..services.daily_aggregator import update_daily_summary
from ..services.daily_aggregator import get_daily_summary


router = APIRouter()

@router.post("/")
def receive_log(log: LogCreate):

    log_dict = log.model_dump()
    # print("RECEIVED:", log_dict)

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
    log_dict["ai_called"] = False
    if should_escalate(pre_ai_score) and not is_cooldown_active( device_id):
        

        all_logs = get_logs() + [log_dict]
        recent_logs = all_logs[-5:]
        log_dict["ai_called"] = True
        daily_summary = get_daily_summary(employee_id)

        ai_payload = build_behavioral_ai_payload(
            log_dict,
            daily_summary,
            recent_logs
        )

        ai_result = call_ai(ai_payload)
        print("AI RESULT:", ai_result)
        print("🧠 AI CALLED")
        print("AI PAYLOAD:", ai_payload)
        print("AI RESULT:", ai_result)
        if ai_result["ai_score"] is not None:

            log_dict["ai_score"] = ai_result["ai_score"]
            log_dict["ai_confidence"] = ai_result.get("confidence")
            log_dict["ai_threat_type"] = ai_result.get("threat_type")
            log_dict["ai_reason"] = ai_result["reason"]

            if ai_result.get("alert_required"):
                log_dict["alert"] = True
            else:
                log_dict["alert"] = False
        else:
            log_dict["ai_score"] = None
            log_dict["ai_reason"] = "AI call failed"
        update_cooldown(device_id)
        

    # 5️⃣ Final composite score
    
    rule_score = log_dict["risk_score"]
    ai_score = log_dict.get("ai_score", 0)
    all_logs = get_logs()

    if len(all_logs) >= 1:
        last_score = all_logs[-1]["final_score"]
        velocity = rule_score - last_score
    else:
        velocity = 0

    if velocity > 20:
        velocity_boost = 10
    else:
        velocity_boost = 0
        
    final_score = int(
        (0.4 * rule_score) +
        (0.35 * anomaly_score) +
        (0.25 * ai_score)
    ) + velocity_boost
    
    log_dict["risk_velocity"] = velocity
    log_dict["velocity_boost"] = velocity_boost

    log_dict["final_score"] = final_score
    
    if final_score >= 70:
        severity = "high"
    elif final_score >= 40:
        severity = "medium"
    else:
        severity = "low"

    log_dict["final_severity"] = severity
    from ..database.log_repository import (
    insert_activity_log,
    insert_telemetry_snapshot,
    insert_alert
    )
    insert_activity_log(log_dict)
    insert_telemetry_snapshot(log_dict)

    if log_dict.get("alert"):
        insert_alert(log_dict)
    #daily summary update
    update_daily_summary(log_dict)
    
    daily_summary = get_daily_summary(employee_id)
    # 6️⃣ Store
    add_log(log_dict)
    
    return {
        "status": "log received",
        "rule_score": log_dict["risk_score"],
        "anomaly_score": anomaly_score,
        "final_score": final_score
    }

@router.get("/")
def view_logs():
    return get_logs()


@router.delete("/")
def delete_logs():
    clear_logs()
    return {"status": "logs cleared"}

@router.get("/dashboard")
def dashboard():
    return {
        "logs": get_logs(),
        "daily_summary": get_daily_summary("EMP-001")
    }