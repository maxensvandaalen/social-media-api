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
