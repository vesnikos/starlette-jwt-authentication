import logging


def test_valid_jwt(client, get_valid_jwt, caplog):
    """Test valid JWT token in header"""
    caplog.set_level(logging.DEBUG)
    print(get_valid_jwt)
    response = client.get("/", headers={"token": get_valid_jwt})
    assert response.status_code == 200
    assert response.text == "Hello, nikos!"


def test_invalid_jwt(client, get_invalid_jwt, caplog):
    """Test invalid JWT token in header"""
    caplog.set_level(logging.DEBUG)
    response = client.get("/", headers={"token": get_invalid_jwt})
    assert response.status_code == 200
    assert response.text == "Hello, anonymous!"


def test_expired_jwt(client, get_expired_jwt, caplog):
    """Test expired JWT token in header"""
    caplog.set_level(logging.DEBUG)
    response = client.get("/", headers={"token": get_expired_jwt})
    assert response.status_code == 200
    assert response.text == "Hello, anonymous!"


def test_valid_jwt_param(client, get_valid_jwt, caplog):
    """Test valid JWT token in query param"""
    caplog.set_level(logging.DEBUG)
    response = client.get("/", params={"token": get_valid_jwt})
    assert response.status_code == 200
    assert response.text == "Hello, nikos!"


def test_invalid_jwt_param(client, get_invalid_jwt, caplog):
    """Test invalid JWT token in query param"""
    caplog.set_level(logging.DEBUG)
    response = client.get("/", params={"token": get_invalid_jwt})
    assert response.status_code == 200
    assert response.text == "Hello, anonymous!"


def test_expired_jwt_param(client, get_expired_jwt, caplog):
    """Test expired JWT token in query param"""
    caplog.set_level(logging.DEBUG)
    response = client.get("/", params={"token": get_expired_jwt})
    assert response.status_code == 200
    assert response.text == "Hello, anonymous!"


def test_no_jwt(client, caplog):
    """Test no JWT token"""
    caplog.set_level(logging.DEBUG)
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "Hello, anonymous!"
