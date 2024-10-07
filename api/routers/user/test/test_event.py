import base64
import os
import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from uuid import uuid4, UUID
from datetime import datetime, timedelta
from contextvars import ContextVar
from PIL import Image
import io

from ....main import app
from ....dependency.database import get_db
from ....models.model import Event, Laboratory, Research, Publication
from ....database.database import Base

# Load environment variables
load_dotenv()

# Constants
TEST_DATABASE_URL = os.getenv("URL_DATABASE_TEST")
SAMPLE_EVENT_COUNT = 15

# Test database setup
engine = create_async_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(class_=AsyncSession, expire_on_commit=False)
session_context = ContextVar("session_context", default=None)

# Helper functions
async def override_get_db():
    session = session_context.get()
    if session is None:
        async with TestingSessionLocal() as session:
            yield session
    else:
        yield session

def create_test_image():
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return buffer.getvalue()

# Override database dependency
app.dependency_overrides[get_db] = override_get_db

# Fixtures
@pytest.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal(bind=engine) as session:
        session_context.set(session)

        # Clear specific tables to ensure a clean state
        for model in [Event, Laboratory, Research, Publication]:
            await session.execute(model.__table__.delete())
        await session.commit()

        yield session

    session_context.set(None)
    await engine.dispose()

@pytest.fixture(scope="function")
async def sample_laboratory(db_session):
    laboratory = Laboratory(
        lab_id=uuid4(),
        lab_name="Test Laboratory",
        image_high=b"high_image_data",
        image_low=b"low_image_data",
        body="Test Laboratory Body"
    )
    db_session.add(laboratory)
    await db_session.commit()
    return laboratory

@pytest.fixture(scope="function")
async def sample_research(db_session, sample_laboratory):
    research = Research(
        research_id=uuid4(),
        research_name="Test Research",
        image_high=b"high_image_data",
        image_low=b"low_image_data",
        body="Test Research Body",
        lab_id=sample_laboratory.lab_id
    )
    db_session.add(research)
    await db_session.commit()
    return research

@pytest.fixture(scope="function")
async def sample_publication(db_session, sample_laboratory):
    publication = Publication(
        publication_id=uuid4(),
        publication_name="Test Publication",
        image_high=b"high_image_data",
        image_low=b"low_image_data",
        body="Test Publication Body",
        url="https://example.com",
        lab_id=sample_laboratory.lab_id
    )
    db_session.add(publication)
    await db_session.commit()
    return publication

@pytest.fixture(scope="function")
async def sample_events(db_session, sample_laboratory, sample_research, sample_publication):
    events = []
    for i in range(SAMPLE_EVENT_COUNT):
        event = Event(
            event_id=uuid4(),
            event_name=f"Test Event {i+1}",
            image_high=create_test_image(),
            image_low=create_test_image(),
            body=f"Body content for Test Event {i+1}",
            location=f"Test Location {i+1}",
            date_start=datetime.now() + timedelta(days=i),
            date_end=datetime.now() + timedelta(days=i+1),
            posted=True,
            lab_id=sample_laboratory.lab_id if i % 3 == 0 else None,
            research_id=sample_research.research_id if i % 3 == 1 else None,
            publication_id=sample_publication.publication_id if i % 3 == 2 else None,
        )
        events.append(event)
        db_session.add(event)
    
    await db_session.commit()
    return events

# Tests
@pytest.mark.asyncio
async def test_get_event_thumbnail(sample_events, db_session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user/event/thumbnail?amount=5&page=1")
        assert response.status_code == 200
        assert len(response.json()) == 5

        response = await ac.get("/user/event/thumbnail?amount=10&page=2")
        assert response.status_code == 200
        assert len(response.json()) == SAMPLE_EVENT_COUNT - 10  # Because we have 15 events in total

@pytest.mark.asyncio
async def test_get_event_thumbnail_with_filters(sample_events, db_session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        lab_id = sample_events[0].lab_id
        response = await ac.get(f"/user/event/thumbnail?laboratory_id={lab_id}")
        assert response.status_code == 200
        assert len(response.json()) > 0

        research_id = sample_events[1].research_id
        response = await ac.get(f"/user/event/thumbnail?research_id={research_id}")
        assert response.status_code == 200
        assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_get_event_image_high(sample_events, db_session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        event_id = sample_events[0].event_id
        response = await ac.get(f"/user/event/image-high?event_id={event_id}")
        await assert_valid_image_response(response, event_id)

@pytest.mark.asyncio
async def test_get_event_image_low(sample_events, db_session):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        event_id = sample_events[0].event_id
        response = await ac.get(f"/user/event/image-low?event_id={event_id}")
        await assert_valid_image_response(response, event_id)

@pytest.mark.asyncio
async def test_get_event_image_high_not_found(db_session):
    await assert_image_not_found("/user/event/image-high")

@pytest.mark.asyncio
async def test_get_event_image_low_not_found(db_session):
    await assert_image_not_found("/user/event/image-low")

# Helper assertion functions
async def assert_valid_image_response(response, event_id):
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    
    data = response.json()
    assert "image" in data
    assert "eid" in data["image"]
    assert "image" in data["image"]
    assert data["image"]["eid"] == str(event_id)
    assert isinstance(data["image"]["image"], str)
    
    try:
        image_data = base64.b64decode(data["image"]["image"])
        assert image_data[:2] == b'\xFF\xD8', "Image is not a JPEG"
    except:
        pytest.fail("Image data is not valid base64")

async def assert_image_not_found(endpoint):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        non_existent_id = UUID('00000000-0000-0000-0000-000000000000')
        response = await ac.get(f"{endpoint}?event_id={non_existent_id}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Event not found"