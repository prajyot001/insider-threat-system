from fastapi import FastAPI
from .config import APP_NAME
from .routes import health, logs

app = FastAPI(title=APP_NAME)

app.include_router(health.router)
app.include_router(logs.router)