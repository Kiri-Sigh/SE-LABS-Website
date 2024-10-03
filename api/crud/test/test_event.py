import os
import pytest
from dotenv import load_dotenv
from uuid import uuid4
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import IntegrityError
from contextvars import ContextVar
from pydantic import ValidationError

from ...models.model import Event, Laboratory, Research, Publication
from ...schemas.core.event import EventsCreate, EventsDB
from ..event import get_event, get_event_list, create_event, delete_event
from ...database.database import Base

load_dotenv()

# Use a same database for testing just for now
TEST_DATABASE_URL = os.getenv("URL_DATABASE")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

session_context = ContextVar("session_context", default=None)

@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def sample_laboratory(db_session: Session):
    laboratory = Laboratory(
        lab_id=uuid4(),
        lab_name="Test Laboratory",
        body="Test Laboratory Body"
    )
    db_session.add(laboratory)
    db_session.commit()
    return laboratory

@pytest.fixture(scope="function")
def sample_research(db_session: Session):
    research = Research(
        research_id=uuid4(),
        research_name="Test Research",
        body="Test Research Body"
    )
    db_session.add(research)
    db_session.commit()
    return research

@pytest.fixture(scope="function")
def sample_publication(db_session: Session):
    publication = Publication(
        publication_id=uuid4(),
        publication_name="Test Publication",
        body="Test Publication Body"
    )
    db_session.add(publication)
    db_session.commit()
    return publication

@pytest.fixture(scope="function")
def sample_event(db_session: Session, sample_laboratory, sample_research, sample_publication):
    event = Event(
        event_id=str(uuid4()),
        event_name="Test Event",
        image_high=b"high_image_data",
        image_low=b"low_image_data",
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
def test_get_existing_event(db_session: Session, sample_event):
    retrieved_event = get_event(db_session, sample_event.event_id)
    assert retrieved_event is not None
    assert retrieved_event.event_id == sample_event.event_id
    assert retrieved_event.event_name == sample_event.event_name

def test_get_non_existent_event(db_session: Session):
    non_existent_id = str(uuid4())
    retrieved_event = get_event(db_session, non_existent_id)
    assert retrieved_event is None

# Tests for get_event_list function
def test_get_event_list_with_results(db_session: Session, sample_event):
    events = get_event_list(db_session, skip=0, limit=10)
    assert len(events) >= 1
    assert any(event.event_id == sample_event.event_id for event in events)

def test_get_event_list_empty(db_session: Session):
    # Clear all events from the database
    db_session.query(Event).delete()
    db_session.commit()
    
    events = get_event_list(db_session, skip=0, limit=10)
    assert len(events) == 0

def test_get_event_list_pagination(db_session: Session):
    # Create 15 events
    for i in range(15):
        event = Event(event_id=str(uuid4()), event_name=f"Event {i}")
        db_session.add(event)
    db_session.commit()

    # Test first page
    first_page = get_event_list(db_session, skip=0, limit=10)
    assert len(first_page) == 10

    # Test second page
    second_page = get_event_list(db_session, skip=10, limit=10)
    assert len(second_page) == 5

# Tests for create_event function
def test_create_event_success(db_session: Session, sample_laboratory, sample_research, sample_publication):
    event_data = EventsCreate(
        event_name="New Test Event",
        image_high=b"new_high_image_data",
        image_low=b"new_low_image_data",
        body="New body content for Test Event",
        location="New Test Location",
        date_start=datetime.now(),
        date_end=datetime.now() + timedelta(days=1),
        posted=True,
        lab_id=sample_laboratory.lab_id,
        research_id=sample_research.research_id,
        publication_id=sample_publication.publication_id,
    )
    new_event = create_event(db_session, event_data)
    assert new_event.event_name == "New Test Event"
    assert new_event.body == "New body content for Test Event"
    assert new_event.lab_id == sample_laboratory.lab_id

def test_create_event_missing_required_field(db_session: Session):
    with pytest.raises(ValidationError) as exc_info:
        event_data = EventsCreate(
            # Missing required fields
            event_name="Incomplete Event",
        )
        create_event(db_session, event_data)
    
    # Check the specific validation errors if needed
    errors = exc_info.value.errors()
    assert len(errors) == 6  # Expecting 6 validation errors
    assert errors[0]["loc"] == ("image_high",)
    assert errors[1]["loc"] == ("image_low",)
    assert errors[2]["loc"] == ("body",)
    assert errors[3]["loc"] == ("location",)
    assert errors[4]["loc"] == ("date_start",)
    assert errors[5]["loc"] == ("date_end",)

# Tests for delete_event function
def test_delete_existing_event(db_session: Session, sample_event):
    result = delete_event(db_session, sample_event.event_id)
    assert result == {"message": "Event deleted successfully."}
    
    deleted_event = get_event(db_session, sample_event.event_id)
    assert deleted_event is None

def test_delete_non_existent_event(db_session: Session):
    non_existent_id = str(uuid4())
    result = delete_event(db_session, non_existent_id)
    assert result == {"message": "Event deleted successfully."}  # This might need to be adjusted based on your error handling