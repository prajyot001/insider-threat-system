from .supabase_client import supabase
from datetime import datetime

def insert_activity_log(log_dict):
    employee_id = log_dict["employee_id"]

    # 🔹 Step 1: Fetch company_id from employees table
    emp_response = supabase.table("employees") \
        .select("company_id") \
        .eq("id", employee_id) \
        .single() \
        .execute()

    if not emp_response.data:
        raise Exception("Employee not found")

    company_id = emp_response.data["company_id"]
    data = {
        "company_id": company_id,
        "employee_id": log_dict["employee_id"],
        "device_id": log_dict["device_id"],
        "event_type": "behavior_snapshot",
        "event_data": log_dict,
        "risk_score": log_dict["final_score"],
        "created_at": datetime.utcnow().isoformat(),
        
    }

    supabase.table("activity_logs").insert(data).execute()
    
def insert_telemetry_snapshot(log_dict):

    snapshot = {
        "device_id": log_dict["device_id"],
        "employee_id": log_dict["employee_id"],
        "cpu_usage": log_dict["system_metrics"]["cpu_usage"],
        "ram_usage": log_dict["system_metrics"]["ram_usage"],
        "bytes_sent": log_dict["network"]["bytes_sent"],
        "bytes_received": log_dict["network"]["bytes_received"],
        "suspicious_count": log_dict["features"]["suspicious_count"],
        "snapshot_time": log_dict["system_metrics"]["timestamp"]
    }

    supabase.table("telemetry_snapshots").insert(snapshot).execute()
    
    
def insert_alert(log_dict):

    alert = {
        "employee_id": log_dict["employee_id"],
        "risk_score": log_dict["final_score"],
        "severity": log_dict.get("ai_severity", log_dict["severity"]),
        "description": log_dict.get("ai_reason", "Rule-based alert"),
        "status": "open",
        "created_at": datetime.utcnow().isoformat()
    }

    supabase.table("alerts").insert(alert).execute()