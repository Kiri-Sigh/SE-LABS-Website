# Original test code with inline comments and corrections

import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
from datetime import datetime, timedelta
from contextvars import ContextVar
from uuid import UUID

from ....main import app  # Ensure this import path is correct for your project structure
from ....dependency.database import get_db
from ....models.model import Event, Laboratory, Research, Publication
from ....database.database import Base

load_dotenv()

# Use a same database for testing just for now
TEST_DATABASE_URL = os.getenv("URL_DATABASE")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

session_context = ContextVar("session_context", default=None)

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

@pytest.fixture(scope="function")
def sample_laboratory(db_session):
    laboratory = Laboratory(
        lab_id=uuid4(),
        lab_name="Test Laboratory",
        image_high=b"high_image_data",
        image_low=b"low_image_data",
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
        image_high=b"high_image_data",
        image_low=b"low_image_data",
        body="Test Research Body",
        lab_id=sample_laboratory.lab_id  # Ensure this is passed correctly
    )
    db_session.add(research)
    db_session.commit()
    return research

@pytest.fixture(scope="function")
def sample_publication(db_session, sample_laboratory):
    publication = Publication(
        publication_id=uuid4(),
        publication_name="Test Publication",
        image_high=b"high_image_data",
        image_low=b"low_image_data",
        body="Test Publication Body",
        url="https://example.com",
        lab_id=sample_laboratory.lab_id  # Ensure this is passed correctly
    )
    db_session.add(publication)
    db_session.commit()
    return publication

@pytest.fixture(scope="function")
def sample_events(db_session, sample_laboratory, sample_research, sample_publication):
    events = []
    for i in range(15):  # Create 15 events
        event = Event(
            event_id=uuid4(),
            event_name=f"Test Event {i+1}",
            image_high=b"high_image_data",
            image_low=b"low_image_data",
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
    
    db_session.commit()
    return events


def test_get_event_thumbnail(sample_events, db_session):
    response = client.get("/user/event/thumbnail?amount=5&page=1")
    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get("/user/event/thumbnail?amount=10&page=2")
    assert response.status_code == 200
    assert len(response.json()) == 5  # Because we have 15 events in total

def test_get_event_thumbnail_with_filters(sample_events, db_session):
    lab_id = sample_events[0].lab_id
    response = client.get(f"/user/event/thumbnail?laboratory_id={lab_id}")
    assert response.status_code == 200
    assert len(response.json()) > 0

    research_id = sample_events[1].research_id
    response = client.get(f"/user/event/thumbnail?research_id={research_id}")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_event_image_high(sample_events, db_session):
    event_id = sample_events[0].event_id
    response = client.get(f"/user/event/image-high?event_id={event_id}")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    
    data = response.json()
    assert "image" in data
    assert "eid" in data["image"]
    assert "image" in data["image"]
    assert data["image"]["eid"] == str(event_id)
    assert isinstance(data["image"]["image"], str)  # Base64 encoded image data

def test_get_event_image_low(sample_events, db_session):
    event_id = sample_events[0].event_id
    response = client.get(f"/user/event/image-low?event_id={event_id}")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    
    data = response.json()
    assert "image" in data
    assert "eid" in data["image"]
    assert "image" in data["image"]
    assert data["image"]["eid"] == str(event_id)
    assert isinstance(data["image"]["image"], str)  # Base64 encoded image data

def test_get_event_image_high_not_found(db_session):
    non_existent_id = UUID('00000000-0000-0000-0000-000000000000')
    response = client.get(f"/user/event/image-high?event_id={non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

def test_get_event_image_low_not_found(db_session):
    non_existent_id = UUID('00000000-0000-0000-0000-000000000000')
    response = client.get(f"/user/event/image-low?event_id={non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"