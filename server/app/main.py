from fastapi import FastAPI
from .config import APP_NAME
from .routes import health, logs

app = FastAPI(
    title=APP_NAME,
    docs_url=None,
    redoc_url=None
)

app.include_router(health.router, prefix="/health")
app.include_router(logs.router, prefix="/server")