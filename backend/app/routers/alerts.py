from fastapi import APIRouter, Depends, HTTPException
from app.services.supabase_service import supabase
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/")
def get_alerts(current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        response = supabase.table("alerts") \
            .select("""
                alert_id,
                severity,
                description,
                risk_score,
                status,
                created_at,
                employees(name)
            """) \
            .eq("company_id", current_user["company_id"]) \
            .order("created_at", desc=True) \
            .limit(50) \
            .execute()

        formatted = []

        for alert in response.data:
            formatted.append({
                "id": alert["alert_id"],
                "severity": alert["severity"],
                "description": alert["description"],
                "risk_score": alert["risk_score"],
                "status": alert["status"],
                "created_at": alert["created_at"],
                "employee_name": alert["employees"]["name"]
                if alert.get("employees") else "Unknown"
            })

        return formatted

    except Exception as e:
        print("Alert fetch error:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch alerts")