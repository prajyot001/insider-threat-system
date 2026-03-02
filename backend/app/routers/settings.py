from fastapi import APIRouter, Depends, HTTPException
from app.services.supabase_service import supabase
from app.services.auth_service import get_current_user
from app.services.security import hash_password

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("/")
def get_settings(current_user: dict = Depends(get_current_user)):
    try:
        company = supabase.table("companies") \
            .select("*") \
            .eq("company_id", current_user["company_id"]) \
            .single() \
            .execute()

        user = supabase.table("employees") \
            .select("name,email") \
            .eq("employee_id", current_user["user_id"]) \
            .single() \
            .execute()

        return {
            "company": company.data,
            "admin": user.data
        }

    except Exception as e:
        print("Settings Fetch Error:", e)
        raise HTTPException(status_code=500, detail="Failed to load settings")
    

from pydantic import BaseModel

class SettingsUpdate(BaseModel):
    company_name: str
    risk_threshold: int
    email_alerts: bool
    name: str
    email: str
    new_password: str | None = None


@router.put("/")
def update_settings(
    data: SettingsUpdate,
    current_user: dict = Depends(get_current_user)
):
    try:
        # Update company
        supabase.table("companies").update({
            "company_name": data.company_name,
            "risk_threshold": data.risk_threshold,
            "email_alerts": data.email_alerts
        }).eq("company_id", current_user["company_id"]).execute()

        # Update admin
        update_data = {
            "name": data.name,
            "email": data.email
        }

        if data.new_password:
            update_data["password"] = hash_password(data.new_password)

        supabase.table("employees").update(update_data) \
            .eq("employee_id", current_user["user_id"]) \
            .execute()

        return {"message": "Settings updated successfully"}

    except Exception as e:
        print("Settings Update Error:", e)
        raise HTTPException(status_code=500, detail="Update failed")