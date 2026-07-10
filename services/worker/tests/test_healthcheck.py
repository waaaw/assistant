from worker_app.celery_app import healthcheck


def test_healthcheck_task() -> None:
    assert healthcheck.run() == "ok"

