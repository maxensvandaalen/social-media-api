from app.utils import get_password_hash


def test_create_user(client):
    response = client.post(
        "/users/",
        json={"name": "JohnDoe", "email": "john_doe@doe.com",
              "password": "password1"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "JohnDoe"
    assert data["email"] == "john_doe@doe.com"


def test_create_user_existing_username(create_test_user, client):
    response = client.post(
        "/users/",
        json={"name": "John Doe", "email": "other@email.com",
              "password": "password456"}
    )
    assert response.status_code == 409
    assert response.json() == {"detail": "this username is already registered"}


def test_create_user_existing_email(create_test_user, client):
    response = client.post(
        "/users/",
        json={"name": "OtherUserName", "email": "john_doe@gmail.com",
              "password": "password123"}
    )
    assert response.status_code == 409
    assert response.json() == {
        "detail": "this emailadress is already registered"}
