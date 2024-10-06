import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4
from datetime import datetime, timedelta
from contextvars import ContextVar
from pydantic import ValidationError
from PIL import Image
import io
from fastapi import HTTPException
import base64

from ...main import app
from ...dependency.database import get_db
from ...models.model import Event, Laboratory, Research, Publication
from ...schemas.core.event import EventCreate, EventDB
from ...database.database import Base
from ...crud.event import get_event, get_event_list, create_event, delete_event

# Load environment variables
load_dotenv()

# Set up test database
TEST_DATABASE_URL = os.getenv("URL_DATABASE_TEST")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

session_context = ContextVar("session_context", default=None)

# Override database dependency for testing
def override_get_db():
    session = session_context.get()
    if session is None:
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()
    else:
        yield session

client = TestClient(app)

# Fixture to create a database session for each test
@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    session_context.set(session)

    # Clear specific tables to ensure a clean state
    session.query(Event).delete()
    session.query(Laboratory).delete()
    session.query(Research).delete()
    session.query(Publication).delete()
    session.commit()

    yield session

    session_context.set(None)
    session.close()
    transaction.rollback()
    connection.close()

app.dependency_overrides[get_db] = override_get_db

# Utility function to create a test image
def create_test_image():
    img = Image.new("RGB", (10, 10), color=(255, 0, 0))  # Red pixel
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")  # Save as PNG format
    return buffer.getvalue()

def create_test_image_base64():
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

# Fixtures for sample data
@pytest.fixture(scope="function")
def sample_laboratory(db_session):
    laboratory = Laboratory(
        lab_id=uuid4(),
        lab_name="Test Laboratory",
        image_high=create_test_image(),
        image_low=create_test_image(),
        body="Test Laboratory Body"
    )
    db_session.add(laboratory)
    db_session.commit()
    return laboratory

@pytest.fixture(scope="function")
def sample_research(db_session, sample_laboratory):
    research = Research(
        research_id=uuid4(),
        research_name="Test Research",
        image_high=create_test_image(),
        image_low=create_test_image(),
        body="Test Research Body",
        lab_id=sample_laboratory.lab_id
    )
    db_session.add(research)
    db_session.commit()
    return research

@pytest.fixture(scope="function")
def sample_publication(db_session, sample_laboratory):
    publication = Publication(
        publication_id=uuid4(),
        publication_name="Test Publication",
        image_high=create_test_image(),
        image_low=create_test_image(),
        body="Test Publication Body",
        url="https://example.com",
        lab_id=sample_laboratory.lab_id
    )
    db_session.add(publication)
    db_session.commit()
    return publication

@pytest.fixture(scope="function")
def sample_event(db_session, sample_laboratory, sample_research, sample_publication):
    event = Event(
        event_id=uuid4(),
        event_name="Test Event",
        image_high=create_test_image(),
        image_low=create_test_image(),
        body="Body content for Test Event",
        location="Test Location",
        date_start=datetime.now(),
        date_end=datetime.now() + timedelta(days=1),
        posted=True,
        lab_id=sample_laboratory.lab_id,
        research_id=sample_research.research_id,
        publication_id=sample_publication.publication_id,
    )
    db_session.add(event)
    db_session.commit()
    return event

# Tests for get_event function
def test_get_existing_event(db_session, sample_event):
    retrieved_event = get_event(db_session, sample_event.event_id)
    assert retrieved_event is not None
    assert retrieved_event.event_id == sample_event.event_id
    assert retrieved_event.event_name == sample_event.event_name

def test_get_non_existent_event(db_session):
    non_existent_id = str(uuid4())
    retrieved_event = get_event(db_session, non_existent_id)
    assert retrieved_event is None

# Tests for get_event_list function
def test_get_event_list_with_results(db_session, sample_event):
    events = get_event_list(db_session, skip=0, limit=10)
    assert len(events) >= 1
    assert any(event.event_id == sample_event.event_id for event in events)

def test_get_event_list_empty(db_session):
    db_session.query(Event).delete()
    db_session.commit()
    
    events = get_event_list(db_session, skip=0, limit=10)
    assert len(events) == 0

def test_get_event_list_pagination(db_session):
    # Create 15 events
    for i in range(15):
        event = Event(
            event_id=str(uuid4()),
            event_name=f"Event {i}",
            image_high=create_test_image(),
            image_low=create_test_image(),
            body="Body content",
            location="Test Location",
            date_start=datetime.now(),
            date_end=datetime.now() + timedelta(days=1),
            posted=True,
            lab_id=None,
            research_id=None,
            publication_id=None,
        )
        db_session.add(event)
    db_session.commit()

    # Test first page
    first_page = get_event_list(db_session, skip=0, limit=10)
    assert len(first_page) == 10

    # Test second page
    second_page = get_event_list(db_session, skip=10, limit=10)
    assert len(second_page) == 5

# Tests for create_event function
def test_create_event_success(db_session, sample_laboratory, sample_research, sample_publication):
    event_data = EventCreate(
        event_name="New Test Event",
        image_high=create_test_image(),
        body="New body content for Test Event",
        location="New Test Location",
        date_start=datetime.now(),
        date_end=datetime.now() + timedelta(days=1),
        lab_id=sample_laboratory.lab_id,
        research_id=sample_research.research_id,
        publication_id=sample_publication.publication_id,
    )
    new_event = create_event(db_session, event_data)
    assert new_event.event_name == "New Test Event"
    assert new_event.body == "New body content for Test Event"
    assert new_event.lab_id == sample_laboratory.lab_id

def test_create_event_missing_required_field(db_session):
    with pytest.raises(ValidationError) as exc_info:
        event_data = EventCreate(
            event_name="Incomplete Event",
            # Missing required fields
        )
        create_event(db_session, event_data)
    
    # Check the specific validation errors
    errors = exc_info.value.errors()
    assert len(errors) == 5
    assert errors[0]["loc"] == ("image_high",)
    assert errors[1]["loc"] == ("body",)
    assert errors[2]["loc"] == ("location",)
    assert errors[3]["loc"] == ("date_start",)
    assert errors[4]["loc"] == ("date_end",)

# Tests for delete_event function
def test_delete_existing_event(db_session, sample_event):
    result = delete_event(db_session, sample_event.event_id)
    assert result == {"message": "Event deleted successfully."}
    
    deleted_event = get_event(db_session, sample_event.event_id)
    assert deleted_event is None

def test_delete_non_existent_event(db_session):
    non_existent_id = str(uuid4())
    with pytest.raises(HTTPException) as exc_info:
        delete_event(db_session, non_existent_id)
    
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Event not found"