from fastapi import FastAPI

from app.auth import router as auth_router

app = FastAPI(title="AI Executive Assistant API", version="0.1.0")
app.include_router(auth_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok", "service": "api"}
