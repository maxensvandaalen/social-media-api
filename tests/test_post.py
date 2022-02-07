def test_get_all_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 200


def test_get_post_by_id(create_test_post, client):
    response = client.get("/posts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Some title"
    assert data["content"] == "Some content"


def test_get_post_non_exist(create_test_post, client):
    response = client.get("/posts/12345")
    assert response.status_code == 404
    assert response.json() == {"detail": "post with id: 12345 does not exist"}


def test_create_post(create_test_user, client):
    response = client.post(
        "/posts/?user_id=1",
        json={"title": "a title", "content": "some content"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "a title"
    assert data["content"] == "some content"
