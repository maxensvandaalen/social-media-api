
from datetime import datetime, timedelta
from jose import jwt
from pytest import approx
from app.config import settings


def test_login_for_access_token(client, first_test_user):
    res = client.post(
        "/token", data={"username": "John Doe", "password": "verygoodpassword"})
    login_res = res.json()
    payload = jwt.decode(login_res["access_token"],
                         settings.SECRET_KEY, settings.ALGORITHM)
    timestamp = (datetime.utcnow(
    ) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
    assert res.status_code == 200
    assert login_res["token_type"] == "bearer"
    assert payload["sub"] == "John Doe"
    assert payload["exp"] == approx(timestamp, 1)


def test_login_for_access_token_wrong_credentials(client, first_test_user):
    res = client.post(
        "/token", data={"username": "John Doe", "password": "wrong_password"})
    login_res = res.json()

    assert res.status_code == 401
    assert login_res["detail"] == "Incorrect username or password"
