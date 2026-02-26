from fastapi import APIRouter, Depends, HTTPException
from app.services.supabase_service import supabase
from app.services.auth_service import get_current_user
from app.services.security import hash_password
from app.models.schemas import EmployeeCreate   
from datetime import datetime, timedelta
import secrets

router = APIRouter(prefix="/employees", tags=["Employees"])

@router.get("/")
def get_employees(current_user: dict = Depends(get_current_user)):
    try:
        if current_user["role"] != "admin":
         raise HTTPException(status_code=403, detail="Access denied")
        response = supabase.table("employees") \
            .select("*") \
            .eq("company_id", current_user["company_id"]) \
            .execute()
        
        return response.data

    except Exception as e:
        print("Get Employees Error:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch employees")
    
@router.post("/")
def create_employee(
    data: EmployeeCreate,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        
        hashed_password = hash_password(data.password)

        response = supabase.table("employees").insert({
            "company_id": current_user["company_id"],
            "name": data.name,
            "email": data.email,
            "role": data.role,
            "department": data.department,
            "status": data.status,
            "password": hashed_password
        }).execute()

        return {"message": "Employee created successfully"}

    except Exception as e:
        print("Create Employee Error:", e)
        raise HTTPException(status_code=500, detail="Failed to create employee")
    
@router.post("/{employee_id}/generate-token")
def generate_registration_token(
    employee_id: str,
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Access denied")

    try:
        # 1️⃣ Delete old unused tokens
        supabase.table("registration_tokens") \
            .delete() \
            .eq("employee_id", employee_id) \
            .eq("used", False) \
            .execute()

        # 2️⃣ Generate new secure token
        token_value = secrets.token_urlsafe(32)

        expires_at = datetime.utcnow() + timedelta(hours=24)

        response = supabase.table("registration_tokens").insert({
            "employee_id": employee_id,
            "token_value": token_value,
            "expires_at": expires_at.isoformat(),
            "used": False
        }).execute()

        return {
            "token": token_value,
            "expires_at": expires_at
        }

    except Exception as e:
        print("Generate Token Error:", e)
        raise HTTPException(status_code=500, detail="Failed to generate token")