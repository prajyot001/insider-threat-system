from fastapi import APIRouter
from ..schemas import LogCreate
from ..storage import add_log, get_logs, clear_logs
from ..risk_engine import calculate_risk

router = APIRouter()


@router.post("/logs")
def receive_log(log: LogCreate):
    log_dict = log.model_dump()

    # 🔥 Calculate risk
    risk_result = calculate_risk(log_dict)

    log_dict["risk_score"] = risk_result["risk_score"]
    log_dict["severity"] = risk_result["severity"]
    log_dict["reasons"] = risk_result["reasons"]
    print(f"Calculated risk: {risk_result}")    
    print(f"Storing log with risk score: {log_dict['risk_score']} and severity: {log_dict['severity']}")
    add_log(log_dict)
    # Store in Supabase here (or memory for now)
    if risk_result["risk_score"] >= 70:
    # insert into alerts table
        pass

    return {
        "status": "log received",
        "risk_score": risk_result["risk_score"],
        "severity": risk_result["severity"]
    }
    

@router.get("/logs")
def view_logs():
    return get_logs()


@router.delete("/logs")
def delete_logs():
    clear_logs()
    return {"status": "logs cleared"}