from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pytest import fixture
from app.config import settings
from app.main import app
from app.database import Base, get_db
from app.models import Post, User, Comment
from app.utils import get_password_hash
from app.oauth2 import create_access_token

testdatabase = f"{settings.SQLALCHEMY_DATABASE_URL}_test"

engine = create_engine(testdatabase)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


def create_test_user(user, session):
    user["password"] = get_password_hash(user["password"])
    db_user = User(**user)
    session.add(db_user)
    session.commit()
    return db_user


@fixture
def first_test_user(session):
    user = {
        "id": 1,
        "name": "John Doe",
        "email": "john_doe@gmail.com",
        "password": "verygoodpassword"
    }
    return create_test_user(user, session)


@fixture
def second_test_user(session):
    user = {
        "id": 2,
        "name": "Jane Doe",
        "email": "janedoe@outlook.com",
        "password": "1234567890"
    }
    return create_test_user(user, session)


@fixture
def first_test_post(first_test_user, session):
    post = {
        "id": 1,
        "title": "Some title",
        "content": "Some content",
        "owner_id": first_test_user.id
    }

    db_post = Post(**post)
    session.add(db_post)
    session.commit()
    return db_post


@fixture
def second_test_post(second_test_user, session):
    post = {
        "id": 2,
        "title": "second post",
        "content": "Some content",
        "owner_id": second_test_user.id
    }

    db_post = Post(**post)
    session.add(db_post)
    session.commit()
    return db_post


@fixture
def authorized_client(first_test_user, client):
    access_token = create_access_token(
        data={"sub": first_test_user.name}
    )
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {access_token}"
    }
    return client


@fixture
def comments(first_test_user, second_test_user, first_test_post, second_test_post, session):
    comments = [
        {
            "id": 1,
            "content": "First! Nice post, John!",
            "post_id": first_test_post.id,
            "owner_id": second_test_user.id
        },
        {
            "id": 2,
            "content": "Great content!",
            "post_id": second_test_post.id,
            "owner_id": first_test_user.id
        }
    ]

    for comment in comments:
        db_comment = Comment(**comment)
        session.add(db_comment)
    session.commit()
    return comments
