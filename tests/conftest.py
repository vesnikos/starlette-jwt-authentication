from datetime import datetime, timedelta, timezone

import jwt
import pytest
from starlette.testclient import TestClient

from src.starlette_swt_authentication.app import app


@pytest.fixture(scope="function")
def get_jwt_key():
    return "secret"


@pytest.fixture(scope="function")
def get_valid_jwt(get_jwt_key):
    token = jwt.encode(
        payload={
            "user_id": "1",
            "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=30),
            "iat": datetime.now(tz=timezone.utc),
            "nbf": datetime.now(tz=timezone.utc),
        },
        key=get_jwt_key,
        algorithm="HS256",
    )
    return token


@pytest.fixture(scope="function")
def get_expired_jwt(get_jwt_key):
    token = jwt.encode(
        payload={
            "user_id": "1",
            "exp": datetime.now(tz=timezone.utc) - timedelta(seconds=29),
            "iat": datetime.now(tz=timezone.utc) - timedelta(seconds=30),
            "nbf": datetime.now(tz=timezone.utc) - timedelta(seconds=30),
        },
        key=get_jwt_key,
        algorithm="HS256",
    )
    return token


@pytest.fixture(scope="function")
def get_invalid_jwt():
    token = jwt.encode(
        payload={
            "user_id": "1",
            "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=30),
            "iat": datetime.now(tz=timezone.utc),
            "nbf": datetime.now(tz=timezone.utc),
        },
        key="invalid",
        algorithm="HS256",
    )
    return token


@pytest.fixture(scope="function")
def client():

    return TestClient(app)
