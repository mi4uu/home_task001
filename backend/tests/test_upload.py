from http import HTTPStatus
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_upload():
    response = client.post(
        "/files/", files={"file": open("tests/users_posts_audience.csv", "rb")}
    )
    assert response.status_code == HTTPStatus.CREATED
