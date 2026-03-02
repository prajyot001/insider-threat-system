from fastapi import FastAPI
from app.routers import auth
from dotenv import load_dotenv
from app.routers import dashboard
from app.routers import employees
from app.routers import reports
from app.routers import auth, employees, alerts, devices ,logs, settings
import os


load_dotenv()
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://insider-threat-seven.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

app.include_router(employees.router)
app.include_router(dashboard.router)
app.include_router(reports.router)
app.include_router(auth.router)
app.include_router(alerts.router)
app.include_router(devices.router)
app.include_router(logs.router)
app.include_router(settings.router)