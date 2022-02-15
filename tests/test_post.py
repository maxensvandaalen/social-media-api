from pytest import mark


def test_get_all_posts(authorized_client):
    response = authorized_client.get("/posts/")
    assert response.status_code == 200


def test_get_post_by_id(first_test_post, authorized_client):
    response = authorized_client.get("/posts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Some title"
    assert data["content"] == "Some content"


def test_get_post_non_exist(first_test_post, authorized_client):
    response = authorized_client.get("/posts/12345")
    assert response.status_code == 404
    assert response.json() == {"detail": "post with id: 12345 does not exist"}


@mark.parametrize("title, content, is_published", [
    ("a title", "some content", True),
    ("another title", "other content", False), ])
def test_create_post(first_test_user, authorized_client, title, content, is_published):
    response = authorized_client.post(
        "/posts/",
        json={"title": title, "content": content, "is_published": is_published}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == title
    assert data["content"] == content
    assert data["is_published"] == is_published


def test_delete_post(first_test_post, authorized_client):
    response = authorized_client.delete("/posts/1")
    assert response.status_code == 200


def test_delete_post_non_exist(first_test_user, authorized_client):
    response = authorized_client.delete("/posts/1234")
    assert response.status_code == 404


def test_delete_post_other_user_post(first_test_post, second_test_post, authorized_client):
    response = authorized_client.delete("/posts/2")
    assert response.status_code == 403


def test_update_post(first_test_post, authorized_client):
    response = authorized_client.put(
        "/posts/1",
        json={"title": "updated title",
              "content": "updated content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "updated title"
    assert data["content"] == "updated content"


def test_update_post_non_exist(first_test_user, authorized_client):
    response = authorized_client.put(
        "/posts/1",
        json={"title": "updated title",
              "content": "updated content"}
    )
    assert response.status_code == 404


def test_update_post_other_user_post(first_test_post, second_test_post, authorized_client):
    response = authorized_client.put(
        "/posts/2",
        json={"title": "updated title",
              "content": "updated content"}
    )
    assert response.status_code == 403
