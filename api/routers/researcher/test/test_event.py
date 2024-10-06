import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime, timedelta
from contextvars import ContextVar
import os
from dotenv import load_dotenv
from uuid import uuid4
import io
from PIL import Image
import base64

from ....main import app
from ....database.database import Base
from ....dependency.database import get_db
from ....models.model import Person, Event, UserCredentials, Laboratory, Research, Publication
from ....token.token import create_access_token, SECRET_KEY, ALGORITHM

# Load environment variables
load_dotenv()

# Constants
TEST_DATABASE_URL = os.getenv("URL_DATABASE_TEST")

# Test database setup
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
session_context = ContextVar("session_context", default=None)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_test_image():
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue()

def create_test_image_base64():
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# Override database dependency
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Fixtures
@pytest.fixture(scope="function")
def db_session():
    db = next(override_get_db())
    yield db
    db.close()

@pytest.fixture
def test_user(db_session):
    user = Person(
        user_id=uuid4(), 
        full_name="Test User",
        image_high=create_test_image(),
        image_low=create_test_image(),
        gmail="test@example.com",
        highest_role="Researcher",
        admin=False
    )
    credentials = UserCredentials(password_hash="hashed_password", user_id=user.user_id)
    db_session.add(user)
    db_session.add(credentials)
    db_session.commit()
    print(f"Test user created: {user.user_id}, {user.gmail}")
    db_session.refresh(user)
    return user

@pytest.fixture
def user_token(test_user):
    token = create_access_token(data={"sub": test_user.gmail})
    print(f"Generated token for user {test_user.gmail}: {token}")
    return token

@pytest.fixture
def authenticated_client(user_token):
    def _authenticated_client(token=user_token):
        return TestClient(app, headers={"Authorization": f"Bearer {token}"})
    return _authenticated_client

@pytest.fixture
def sample_event_data():
    inner_data = {
        "event_name": "Test Event",
        "body": "This is a test event",
        "location": "Test Location",
        "date_start": (datetime.now() + timedelta(days=1)).isoformat(),
        "date_end": (datetime.now() + timedelta(days=2)).isoformat(),
        "image_high": create_test_image_base64(),
        "image_low": None  # or provide a lower resolution image if needed
    }
    return {"Event": inner_data}

def test_create_event_success(authenticated_client, sample_event_data, db_session):
    # Verify the user exists in the database
    user = db_session.query(Person).filter(Person.gmail == "test@example.com").first()
    print(f"User in database: {user.user_id if user else 'Not found'}")

    response = authenticated_client().post("/researcher/event/", json=sample_event_data)
    print(f"Response status code: {response.status_code}")
    print(f"Response content: {response.content}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["event_name"] == sample_event_data["Event"]["event_name"]
    assert "event_id" in data

def test_create_event_unauthenticated(sample_event_data):
    response = client.post("/researcher/event/", json=sample_event_data)
    assert response.status_code == 401

def test_create_event_invalid_token(authenticated_client, sample_event_data):
    response = authenticated_client("invalid_token").post("/researcher/event/", json=sample_event_data)
    assert response.status_code == 401

def test_create_event_expired_token(authenticated_client, sample_event_data):
    expired_token = create_access_token(data={"sub": "test@example.com"}, expires_delta=timedelta(minutes=-1))
    response = authenticated_client(expired_token).post("/researcher/event/", json=sample_event_data)
    assert response.status_code == 401

def test_create_event_invalid_data(authenticated_client):
    invalid_data = {
        "event_name": "Test Event",
        # Missing required fields
    }
    response = authenticated_client().post("/researcher/event/", json=invalid_data)
    assert response.status_code == 422  # Unprocessable Entity

def test_create_event_invalid_dates(authenticated_client, sample_event_data):
    sample_event_data["date_start"] = (datetime.now() + timedelta(days=2)).isoformat()
    sample_event_data["date_end"] = (datetime.now() + timedelta(days=1)).isoformat()
    response = authenticated_client().post("/researcher/event/", json=sample_event_data)
    assert response.status_code == 422

def test_create_event_missing_image(authenticated_client, sample_event_data):
    del sample_event_data["image_high"]
    response = authenticated_client().post("/researcher/event/", json=sample_event_data)
    assert response.status_code == 422

# Add more tests as needed