from urllib import response

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.otp_service import generate_otp, save_otp, verify_otp,otp_storage
from app.services.email_service import send_otp_email
from app.services.supabase_service import supabase
from app.services.security import hash_password
from jose import jwt
from datetime import datetime, timedelta
import os

router = APIRouter()

class SignupRequest(BaseModel):
    companyName: str
    companyEmail: str
    adminName: str
    adminEmail: str
    password: str

class OTPVerifyRequest(BaseModel):
    adminEmail: str
    otp: str


@router.post("/signup")
def signup(data: SignupRequest):

    otp = generate_otp()

    save_otp(data.adminEmail, otp, data.dict())

    send_otp_email(data.adminEmail, otp)

    return {"message": "OTP sent to admin email"}


from pydantic import BaseModel
from app.services.security import verify_password

class LoginRequest(BaseModel):
    email: str
    password: str

from dotenv import load_dotenv
import bcrypt

load_dotenv()

@router.post("/login")
def login(data: LoginRequest):
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    # temp hardcoded admin credentials for testing
  
    # Find user by email
    response = supabase.table("employees").select("*").eq("email", data.email).execute()
    print("Supabase response:", response)  # Debugging line
    if not response.data:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
   
    # Verify password
    if not verify_password(data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
        
    
    token_data = {
    "user_id": user["employee_id"],
    "company_id": user["company_id"],
    "role": user["role"],
    "exp": datetime.utcnow() + timedelta(hours=2)
    }
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {
    "access_token": access_token,
    "token_type": "bearer"

    }
    
    
    
@router.post("/verify-otp")
def verify(data: OTPVerifyRequest):

    success, message = verify_otp(data.adminEmail, data.otp)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    signup_data = otp_storage.get(data.adminEmail)

    if not signup_data:
        raise HTTPException(status_code=400, detail="Signup data missing")

    # Hash password
    hashed_password = hash_password(signup_data["password"])

    # STEP 1: Insert company and get response
    company_response = supabase.table("companies").insert({
        "company_name": signup_data["companyName"],
        "company_email": signup_data["companyEmail"],
        "plan_type": "free"
    }).execute()

    company_id = company_response.data[0]["company_id"]

    # STEP 2: Insert admin with correct company_id
    supabase.table("employees").insert({
        "name": signup_data["adminName"],
        "email": signup_data["adminEmail"],
        "password": hashed_password,
        "role": "admin",
        "company_id": company_id
    }).execute()

    return {"message": "Account created successfully"}