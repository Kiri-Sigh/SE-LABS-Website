import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
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
from ....json_encoder import json_encode

# Load environment variables
load_dotenv()

# Constants
TEST_DATABASE_URL = os.getenv("URL_DATABASE_TEST")

# Test database setup
engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(class_=AsyncSession, expire_on_commit=False)
session_context = ContextVar("session_context", default=None)

async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

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

# Fixtures
@pytest.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def test_user(db_session):
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
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.fixture
def user_token(test_user):
    token = create_access_token(data={"sub": test_user.gmail})
    return token

@pytest.fixture
def authenticated_client(user_token):
    async def _authenticated_client(token=user_token):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            ac.headers["Authorization"] = f"Bearer {token}"
            yield ac
    return _authenticated_client

from ....schemas.request.event.readable.EventCreate import EventCreate
from ....schemas.request.event.unreadable.EC01_event_create import EC01

@pytest.fixture
def sample_event_data():
    event_data = EventCreate(
        Event=EC01(
            title="New Test Event",
            image_high=create_test_image_base64(),
            body="New body content for Test Event",
            location="New Test Location",
            date_start=datetime.now(),
            date_end=datetime.now() + timedelta(days=1),
            # Include other required fields here
        )
    )
    return event_data

@pytest.mark.asyncio
async def test_create_event_success(authenticated_client, sample_event_data, db_session):
    # Verify the user exists in the database
    user = await db_session.execute(db_session.query(Person).filter(Person.gmail == "test@example.com"))
    user = user.scalar_one_or_none()
    assert user is not None

    async for client in authenticated_client():
        response = await client.post("/researcher/event/", json=json_encode.prepare_json(sample_event_data))
    assert response.status_code == 200
    data = response.json()
    assert data["event_name"] == sample_event_data.Event.event_name
    assert "event_id" in data

@pytest.mark.asyncio
async def test_create_event_unauthenticated(sample_event_data):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/researcher/event/", json=json_encode.prepare_json(sample_event_data))
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_event_invalid_token(authenticated_client, sample_event_data):
    async for client in authenticated_client("invalid_token"):
        response = await client.post("/researcher/event/", json=json_encode.prepare_json(sample_event_data))
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_event_expired_token(authenticated_client, sample_event_data):
    expired_token = create_access_token(data={"sub": "test@example.com"}, expires_delta=timedelta(minutes=-1))
    async for client in authenticated_client(expired_token):
        response = await client.post("/researcher/event/", json=json_encode.prepare_json(sample_event_data))
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_create_event_invalid_data(authenticated_client):
    invalid_data = {
        "event_name": "Test Event",
        # Missing required fields
    }
    async for client in authenticated_client():
        response = await client.post("/researcher/event/", json=json_encode.prepare_json(invalid_data))
    assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.asyncio
async def test_create_event_invalid_dates(authenticated_client, sample_event_data):
    sample_event_data.Event.date_start = (datetime.now() + timedelta(days=2)).isoformat()
    sample_event_data.Event.date_end = (datetime.now() + timedelta(days=1)).isoformat()
    async for client in authenticated_client():
        response = await client.post("/researcher/event/", json=json_encode.prepare_json(sample_event_data))
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_create_event_missing_image(authenticated_client, sample_event_data):
    # Create a new dictionary from the original data, excluding image_high
    event_data_dict = sample_event_data.Event.dict(exclude={"Event": {"image_high"}})
    
    # change dict to EventCreate object
    event_data = EventCreate(Event=EC01(**event_data_dict))
    
    # Send the request with the modified data
    async for client in authenticated_client():
        response = await client.post("/researcher/event/", json=json_encode.prepare_json(event_data_dict))
    assert response.status_code == 422

# Add more tests as needed