from app import schemas


def test_get_all_comments(comments, authorized_client):
    response = authorized_client.get("/comments/")
    assert response.status_code == 200
    data = response.json()
    all_comments = [schemas.CommentBase(**comment) for comment in comments]
    comments_response = [schemas.CommentBase(**comment) for comment in data]
    assert comments_response == all_comments


def test_get_all_comments_unauthorized_user(comments, client):
    response = client.get("/comments/")
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}