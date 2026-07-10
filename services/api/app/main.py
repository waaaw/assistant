from fastapi import FastAPI

from app.auth import router as auth_router
from app.dashboard import empty_dashboard
from app.ops import RequestIdMiddleware
from datetime import date

app = FastAPI(title="AI Executive Assistant API", version="0.1.0")
app.include_router(auth_router)
app.add_middleware(RequestIdMiddleware)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "api"}


@app.get("/ready", tags=["system"])
def ready() -> dict[str, str]:
    return {"status": "ready", "service": "api"}


@app.get("/dashboard/summary", tags=["dashboard"])
def dashboard_summary() -> dict:
    return empty_dashboard(date.today().isoformat()).model_dump(mode="json")
