import os
from fastapi.testclient import TestClient
from loguru import logger
from app.main import app
from app.config import settings

client = TestClient(app, raise_server_exceptions=False)


def test_custom_exception_a():
    response = client.get("/test/a/-5")
    assert response.status_code == 409
    data = response.json()
    assert data["error_type"] == "CustomAError"
    assert "X-Request-ID" in response.headers


def test_custom_exception_b():
    response = client.get("/test/b/200")
    assert response.status_code == 404
    data = response.json()
    assert data["error_type"] == "CustomBError"


def test_http_exception():
    response = client.get("/non-existent-route")
    assert response.status_code == 404
    data = response.json()
    assert data["error_type"] == "HTTPException"


def test_validation_error_problem_details():
    response = client.post(
        "/users/register",
        json={
            "username": "a",
            "age": 15,
            "email": "bad-email",
            "password": "weakpassword",
        },
    )
    assert response.status_code == 422
    assert response.headers["content-type"] == "application/problem+json"
    data = response.json()
    assert data["title"] == "Validation Error"
    assert len(data["errors"]) >= 4


def test_unexpected_exception_and_log_file():
    response = client.get("/test/boom")
    assert response.status_code == 500
    data = response.json()
    assert data["error_type"] == "InternalServerError"

    # Ждём завершения асинхронной записи (enqueue=True) в файл лога
    logger.complete()

    assert os.path.exists(settings.log_file)
    with open(settings.log_file, "r", encoding="utf-8") as f:
        logs = f.read()
    assert "Unexpected internal error" in logs
