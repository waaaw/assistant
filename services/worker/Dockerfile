FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml .
RUN pip install --no-cache-dir .
COPY worker_app ./worker_app
CMD ["celery", "-A", "worker_app.celery_app:celery_app", "worker", "--loglevel=INFO"]

