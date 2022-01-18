def test_get_all_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 200
