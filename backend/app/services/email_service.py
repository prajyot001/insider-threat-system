import os
from dotenv import load_dotenv
import resend

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

def send_otp_email(to_email: str, otp: str):
    print(f"OTP for {to_email} is: {otp}")
    resend.Emails.send({
        "from": "SecureMonitor <onboarding@resend.dev>",  # temporary sender
        "to": to_email,
        "subject": "OTP Verification - SecureMonitor",
        "html": f"""
        <div style="font-family: Arial;">
            <h2>Your OTP Code</h2>
            <p>Your verification code is:</p>
            <h1>{otp}</h1>
            <p>This OTP will expire in 5 minutes.</p>
        </div>
        """
    })