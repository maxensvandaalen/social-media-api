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


def test_create_comment(first_test_post, authorized_client):
    response = authorized_client.post(
        "/comments/",
        json={"post_id": 1, "content": "a comment"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["post_id"] == 1
    assert data["owner_id"] == 1
    assert data["content"] == "a comment"


def test_create_comment_non_existing_post(authorized_client):
    response = authorized_client.post(
        "/comments/",
        json={"post_id": 1, "content": "a comment"}
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "post with id: 1 does not exist"}


def test_create_comment_unauthorized_user(first_test_post, client):
    response = client.post(
        "/comments/",
        json={"post_id": 1, "content": "a comment"}
    )
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_comment(comments, authorized_client):
    response = authorized_client.delete("/comments/2")
    assert response.status_code == 200


def test_delete_comment_other_user(comments, authorized_client):
    response = authorized_client.delete("/comments/1")
    assert response.status_code == 403


def test_delete_comment_non_existing_comment(comments, authorized_client):
    response = authorized_client.delete("/comments/9999")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "comment with id: 9999 does not exist"}


def test_delete_comment_unauthorized_user(comments, client):
    response = client.delete("/comments/1")
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}
