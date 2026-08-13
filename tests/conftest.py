import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault(
    "SECRET_KEY",
    "test-only-secret-key-with-more-than-32-characters",
)
os.environ.setdefault("DATABASE_URL", "sqlite://")
os.environ.setdefault("CORS_ORIGINS", "http://testserver")

from app.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def create_user(client):
    def _create_user(username: str):
        password = "Strong-password-123!"
        response = client.post(
            "/auth/register",
            json={
                "email": f"{username}@example.com",
                "username": username,
                "password": password,
            },
        )
        assert response.status_code == 201
        return response.json(), password

    return _create_user


@pytest.fixture
def auth_headers(client, create_user):
    def _auth_headers(username: str):
        user, password = create_user(username)
        response = client.post(
            "/auth/login",
            data={"username": username, "password": password},
        )
        assert response.status_code == 200
        token = response.json()["access_token"]
        return user, {"Authorization": f"Bearer {token}"}

    return _auth_headers
