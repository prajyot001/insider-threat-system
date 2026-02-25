import os
from fastapi import APIRouter
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timedelta
from collections import defaultdict


router = APIRouter()

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@router.get("/dashboard/overview")
def get_dashboard_overview():

    # Total Employees
    employees = supabase.table("employees").select("*", count="exact").execute()
    total_employees = employees.count

    # Active Devices
    devices = supabase.table("devices").select("*", count="exact").eq("status", "active").execute()
    active_devices = devices.count

    # Open Alerts
    alerts = supabase.table("alerts").select("*", count="exact").eq("status", "open").execute()
    open_alerts = alerts.count

    # High Risk Users (risk_score > 70)
    high_risk = supabase.table("employees").select("*", count="exact").gt("risk_score", 70).execute()
    high_risk_users = high_risk.count

    return {
        "totalEmployees": total_employees,
        "activeDevices": active_devices,
        "openAlerts": open_alerts,
        "highRiskUsers": high_risk_users
    }
    


@router.get("/dashboard/charts")
def get_dashboard_charts():

    # --- Risk Trend (Last 7 Days) ---
    seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()

    logs = supabase.table("activity_logs") \
        .select("created_at,risk_score") \
        .gte("created_at", seven_days_ago) \
        .execute()

    daily_risk = defaultdict(int)

    for log in logs.data:
        date = log["created_at"][:10]  # YYYY-MM-DD
        daily_risk[date] += log.get("risk_score", 0)

    risk_trend = [
        {"day": date, "risk": value}
        for date, value in sorted(daily_risk.items())
    ]


    # --- Alerts by Severity ---
    alerts = supabase.table("alerts") \
        .select("severity") \
        .execute()

    severity_count = defaultdict(int)

    for alert in alerts.data:
        severity = alert["severity"]
        severity_count[severity] += 1

    alerts_severity = [
        {"name": key, "value": value}
        for key, value in severity_count.items()
    ]

    return {
        "riskTrend": risk_trend,
        "alertsSeverity": alerts_severity
    }