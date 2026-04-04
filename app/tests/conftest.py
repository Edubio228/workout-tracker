import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from app.main import app as fastapi_app
from app.db.seed import seed_exercises
import app.models.user      # noqa
import app.models.workout   # noqa
import app.models.exercise  # noqa

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

fastapi_app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    """Create all tables and seed exercises before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    # Pass the test session so seeded data is visible to the test
    db = TestingSessionLocal()
    seed_exercises(db)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(fastapi_app)

@pytest.fixture
def registered_user(client):
    client.post("/auth/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    return {"username": "testuser", "password": "password123"}

@pytest.fixture
def auth_client(client, registered_user):
    response = client.post("/auth/login", data={
        "username": registered_user["username"],
        "password": registered_user["password"],
    })
    token = response.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client