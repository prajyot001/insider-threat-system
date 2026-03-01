from urllib import response

from fastapi import APIRouter, Depends, HTTPException
from app.services.supabase_service import supabase
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("/")
def get_logs(current_user: dict = Depends(get_current_user)):
    try:
        
        logs_response = (
        supabase.table("activity_logs")
        .select("""
            log_id,
            employee_id,
            device_id,
            event_type,
            event_data,
            risk_score,
            created_at
        """)
        .eq("company_id", current_user["company_id"])
        .order("created_at", desc=True)
        .limit(100)
        .execute()
         )

        logs = logs_response.data
        employee_ids = list({log["employee_id"] for log in logs})
        device_ids = list({log["device_id"] for log in logs})
        employees_response = (
        supabase.table("employees")
        .select("employee_id, name")
        .in_("employee_id", employee_ids)
        .execute()
        )

        employee_map = {
            e["employee_id"]: e["name"]
            for e in employees_response.data
        }
        
        devices_response = (
        supabase.table("devices")
        .select("device_id, device_name")
        .in_("device_id", device_ids)
        .execute()
        )

        device_map = {
            d["device_id"]: d["device_name"]
            for d in devices_response.data
        }
       
        formatted = []

        for log in logs:
            formatted.append({
                "log_id": log["log_id"],
                "employee_name": employee_map.get(log["employee_id"], "Unknown"),
                "device_name": device_map.get(log["device_id"], "Unknown"),
                "event_type": log["event_type"],
                "risk_score": log["risk_score"],
                "created_at": log["created_at"],
                "event_data": log["event_data"]
            })

        return formatted

    except Exception as e:
        print("Logs Error:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch logs")