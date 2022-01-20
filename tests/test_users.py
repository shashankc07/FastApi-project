from app import schemas
import pytest


def test_create_user(client):
    res = client.post("/users/", json={"email": "test@example.com", "password": "test123"})
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ("shanky@example.com", "test123", 403),
    ("test@example.com", "wrong_pass", 403),
    ("test@example.com", "test123", 200)
])
def test_wrong_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
