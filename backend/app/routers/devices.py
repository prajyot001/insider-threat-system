from fastapi import APIRouter, Depends, HTTPException
from app.services.supabase_service import supabase
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.get("/")
def get_devices(current_user: dict = Depends(get_current_user)):

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        response = (
        supabase.table("devices")
        .select("""
        device_id,
        device_name,
        os_type,
        ip_address,
        status,
        last_active,
        employee:employees!devices_employee_id_fkey(name)
        """)
        .eq("company_id", current_user["company_id"])
        .order("created_at", desc=True)
        .execute()
        )
        print(response.data)
        formatted = []

        for device in response.data:
            formatted.append({
            "id": device["device_id"],
            "device_name": device["device_name"],
            "os_type": device["os_type"],
            "ip_address": device["ip_address"],
            "status": device["status"],
            "last_active": device["last_active"],
            "employee_name": device["employee"]["name"]
            if device.get("employee") else "Unknown"
            })

        print(formatted)
        print("employee name:", formatted[0]["employee_name"])
        return formatted

    except Exception as e:
        print("Devices error:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch devices")