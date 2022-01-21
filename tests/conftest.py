from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pytest import fixture
from app.config import settings
from app.main import app
from app.database import Base, get_db

testdatabase = f"{settings.SQLALCHEMY_DATABASE_URL}_test"

engine = create_engine(testdatabase)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@fixture
def client():
    yield TestClient(app)
