def test_get_all_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 200


def test_get_post_by_id(client):
    response = client.get("/posts/1")
    assert response.status_code == 200
    