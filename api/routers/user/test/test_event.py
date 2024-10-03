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

    yield session

    session_context.set(None)
    session.close()
    transaction.rollback()
    connection.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def sample_Laboratory(db_session):
    # Correction: Change 'Laboratory' to 'laboratory' for consistency
    laboratory = Laboratory(
        lab_id=uuid4(),  # Changed from Laboratory_id to lab_id
        lab_name="Test Laboratory",  # Changed from Laboratory_name to lab_name
        body="Test Laboratory Body"
    )
    db_session.add(laboratory)
    db_session.commit()
    return laboratory

@pytest.fixture(scope="function")
def sample_Research(db_session):
    # Correction: Change 'Research' to 'research' for consistency
    research = Research(
        research_id=uuid4(),  # Changed from Research_id to research_id
        research_name="Test Research",
        body="Test Research Body"
    )
    db_session.add(research)
    db_session.commit()
    return research

@pytest.fixture(scope="function")
def sample_publication(db_session):
    publication = Publication(
        publication_id=uuid4(),  # Changed from str(uuid4()) to uuid4()
        publication_name="Test Publication",
        body="Test Publication Body"
    )
    db_session.add(publication)
    db_session.commit()
    return publication

@pytest.fixture(scope="function")
def sample_Event(db_session, sample_Laboratory, sample_Research, sample_publication):
    # Correction: Change 'Event' to 'events' for consistency
    events = [
        Event(
            event_id=uuid4(),  # Changed from str(uuid4()) to uuid4()
            event_name=f"Event {i}",
            image_high=b"high_image_data",
            image_low=b"low_image_data",
            body=f"Body content for Event {i}",
            location=f"Location {i}",
            date_start=datetime.now(),
            date_end=datetime.now() + timedelta(days=1),
            posted=True,
            lab_id=sample_Laboratory.lab_id,  # Changed from Laboratory_id to lab_id
            research_id=sample_Research.research_id,
            publication_id=sample_publication.publication_id,
        ) for i in range(15)
    ]
    db_session.add_all(events)
    db_session.commit()
    return events

def test_get_event_thumbnail(sample_Event, db_session):
    response = client.get("/user/event/thumbnail?amount=5&page=1")
    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get("/user/event/thumbnail?amount=10&page=2")
    assert response.status_code == 200
    assert len(response.json()) == 5

def test_get_event_thumbnail_with_filters(sample_Event, db_session):
    lab_id = sample_Event[0].lab_id  # Changed from Laboratory_id to lab_id
    response = client.get(f"/user/event/thumbnail?lab_id={lab_id}")  # Changed from Laboratoryoratory_id to lab_id
    assert response.status_code == 200
    assert len(response.json()) == 1

    research_id = sample_Event[1].research_id
    response = client.get(f"/user/event/thumbnail?research_id={research_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_event_image_high(sample_Event, db_session):
    event_id = sample_Event[0].event_id
    response = client.get(f"/user/event/image-high?event_id={event_id}")
    assert response.status_code == 200
    assert response.json()["image_url"] == sample_Event[0].image_high

def test_get_event_image_high_not_found(db_session):
    non_existent_id = uuid4()
    response = client.get(f"/user/event/image-high?event_id={non_existent_id}")
    assert response.status_code == 404

def test_get_event_image_low(sample_Event, db_session):
    event_id = sample_Event[0].event_id
    response = client.get(f"/user/event/image-low?event_id={event_id}")
    assert response.status_code == 200
    assert response.json()["image_url"] == sample_Event[0].image_low

def test_get_event_image_low_not_found(db_session):
    non_existent_id = uuid4()
    response = client.get(f"/user/event/image-low?event_id={non_existent_id}")
    assert response.status_code == 404

# The following async tests are commented out. If you want to use them, 
# you'll need to adjust your test setup to support async testing.

# @pytest.mark.asyncio
# async def test_get_event_thumbnail_async(sample_Event, db_session):
#     response = await client.get("/user/event/thumbnail?amount=5&page=1")
#     assert response.status_code == 200
#     assert len(response.json()) == 5

# @pytest.mark.asyncio
# async def test_get_event_image_high_async(sample_Event, db_session):
#     event_id = sample_Event[0].event_id
#     response = await client.get(f"/user/event/image-high?event_id={event_id}")
#     assert response.status_code == 200
#     assert response.json()["image_url"] == sample_Event[0].image_high

# @pytest.mark.asyncio
# async def test_get_event_image_low_async(sample_Event, db_session):
#     event_id = sample_Event[0].event_id
#     response = await client.get(f"/user/event/image-low?event_id={event_id}")
#     assert response.status_code == 200
#     assert response.json()["image_url"] == sample_Event[0].image_low