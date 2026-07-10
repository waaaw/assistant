import os

from celery import Celery

celery_app = Celery(
    "assistant-worker",
    broker=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    backend=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
)


@celery_app.task(name="assistant.healthcheck")
def healthcheck() -> str:
    return "ok"

