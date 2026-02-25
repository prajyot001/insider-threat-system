from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.otp_service import generate_otp, save_otp, verify_otp
from app.services.email_service import send_otp_email

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
    save_otp(data.adminEmail, otp)

    send_otp_email(data.adminEmail, otp)

    return {"message": "OTP sent to admin email"}


@router.post("/verify-otp")
def verify(data: OTPVerifyRequest):
    success, message = verify_otp(data.adminEmail, data.otp)

    if not success:
        raise HTTPException(status_code=400, detail=message)

    return {"message": "OTP verified successfully"}