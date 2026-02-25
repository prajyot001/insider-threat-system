import random
from datetime import datetime, timedelta

otp_storage = {}

def generate_otp():
    return str(random.randint(100000, 999999))

def save_otp(email: str, otp: str):
    otp_storage[email] = {
        "otp": otp,
        "expiry": datetime.utcnow() + timedelta(minutes=5)
    }

def verify_otp(email: str, user_otp: str):
    record = otp_storage.get(email)

    if not record:
        return False, "No OTP found"

    if datetime.utcnow() > record["expiry"]:
        return False, "OTP expired"

    if record["otp"] != user_otp:
        return False, "Invalid OTP"

    return True, "OTP verified"