from fastapi.testclient import TestClient
from app.main import app
import pytest
from app import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.oauth2 import create_token
from app.database import get_db, Base


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:shashank007@localhost:8080/test_FastApi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(bind=engine)  # drop all tables
    Base.metadata.create_all(bind=engine)  # create all tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture(scope="function")
def test_user(client):
    user = {"email": "test@example.com", "password": "test123"}
    res = client.post("/users/", json=user)
    assert res.status_code == 201
    return user


@pytest.fixture(scope="function")
def token(test_user):
    return create_token({"user_id": 1})


@pytest.fixture()
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture()
def test_posts(test_user, session):
    posts_data = [{
        "title": "First Post",
        "content": "testing first post",
        "user_id": 1
    }, {
        "title": "Second Post",
        "content": "testing second post",
        "user_id": 1
    }, {
        "title": "Third Post",
        "content": "testing third post",
        "user_id": 1
    }]

    def create_post_model(post):
        return models.Post(**post)

    posts = list(map(create_post_model, posts_data))
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
