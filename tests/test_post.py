def test_get_all_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 200


def test_get_post_by_id(create_test_post, client):
    response = client.get("/posts/1")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Some title"
    assert data["content"] == "Some content"
