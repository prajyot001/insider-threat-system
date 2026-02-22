from fastapi import APIRouter
from ..schemas import LogCreate
from ..storage import add_log, get_logs, clear_logs
from ..services.risk_engine import calculate_risk
from ..services.feature_engineering import extract_features
from ..services.ai_escalation import should_escalate, build_ai_payload
from ..services.ai_service import call_ai, is_cooldown_active, update_cooldown

router = APIRouter()


@router.post("/logs")
def receive_log(log: LogCreate):

    log_dict = log.model_dump()

    # 1️⃣ Rule-based scoring
    risk_result = calculate_risk(log_dict)

    log_dict["risk_score"] = risk_result["risk_score"]
    log_dict["severity"] = risk_result["severity"]
    log_dict["reasons"] = risk_result["reasons"]

    # 2️⃣ Feature engineering
    features = extract_features(log_dict)
    log_dict["features"] = features

    # 3️⃣ Default final score = rule score
    final_score = log_dict["risk_score"]

    # 4️⃣ Escalation logic
    device_id = log_dict["device_id"]

    if should_escalate(final_score):

        if not is_cooldown_active(device_id):

            all_logs = get_logs()
            if len(all_logs) >= 2:
                recent_logs = all_logs[-3:]
            else:
                recent_logs = all_logs

            ai_payload = build_ai_payload(recent_logs)

            print("AI PAYLOAD:", ai_payload)

            ai_result = call_ai(ai_payload)

            if ai_result["ai_score"] is not None:
                log_dict["ai_score"] = ai_result["ai_score"]
                log_dict["ai_reason"] = ai_result["reason"]
                log_dict["ai_severity"] = ai_result["severity"]

                # Combine scores safely
                final_score = max(final_score, ai_result["ai_score"])

            update_cooldown(device_id)

    # 5️⃣ Store final score
    log_dict["final_score"] = final_score

    # 6️⃣ Store enriched log
    add_log(log_dict)

    return {
        "status": "log received",
        "rule_score": log_dict["risk_score"],
        "final_score": final_score,
        "severity": log_dict["severity"]
    }


@router.get("/logs")
def view_logs():
    return get_logs()


@router.delete("/logs")
def delete_logs():
    clear_logs()
    return {"status": "logs cleared"}