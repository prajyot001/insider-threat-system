from fastapi import FastAPI
from app.routers import auth
from dotenv import load_dotenv
from app.routers import dashboard
from app.routers import employees
import os

load_dotenv()
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

app.include_router(employees.router)
app.include_router(dashboard.router)