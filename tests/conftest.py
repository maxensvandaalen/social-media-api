from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pytest import fixture
from app.config import settings
from app.main import app
from app.database import Base, get_db
from app.models import Post, User
from app.utils import get_password_hash

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


@fixture
def create_test_user(session):
    hashed_password = get_password_hash("verygoodpassword")
    user = {
        "name": "John Doe",
        "email": "john_doe@gmail.com",
        "password": hashed_password
    }

    db_user = User(**user)
    session.add(db_user)
    session.commit()
    return db_user

@fixture
def create_test_post(create_test_user, session):
    post = {
        "title": "Some title",
        "content": "Some content",
        "owner_id": 1
    }

    db_post = Post(**post)
    session.add(db_post)
    session.commit()

    
