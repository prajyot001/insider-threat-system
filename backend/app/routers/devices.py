from fastapi import APIRouter, Depends, HTTPException
from app.services.supabase_service import supabase
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.get("/")
def get_devices(current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        devices_response = (
        supabase.table("devices")
        .select("""
            device_id,
            device_name,
            os_type,
            ip_address,
            status,
            last_active,
            employee_id
        """)
        .eq("company_id", current_user["company_id"])
        .order("created_at", desc=True)
        .execute()
        )

        devices = devices_response.data
        employee_ids = list({d["employee_id"] for d in devices})
        employees_response = (
        supabase.table("employees")
        .select("employee_id, name")
        .in_("employee_id", employee_ids)
        .execute()
         )

        employees = employees_response.data
        employee_map = {e["employee_id"]: e["name"] for e in employees}
        formatted = []

        for device in devices:
            formatted.append({
                "id": device["device_id"],
                "device_name": device["device_name"],
                "os_type": device["os_type"],
                "ip_address": device["ip_address"],
                "status": device["status"],
                "last_active": device["last_active"],
                "employee_name": employee_map.get(device["employee_id"], "Unknown")
            })

        
        
        return formatted

    except Exception as e:
        print("Devices error:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch devices")