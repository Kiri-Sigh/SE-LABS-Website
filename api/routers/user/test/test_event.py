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

from ....main import app  # Replace with your actual app import
from ....dependency.database import get_db
from ....models.model import Events, Lab, Project, Publication  # Assuming Events is your model
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
def sample_lab(db_session):
    lab = Lab(
        lab_id=str(uuid4()),
        lab_name="Test Lab",
        body="Test Lab Body"
    )
    db_session.add(lab)
    db_session.commit()
    return lab

@pytest.fixture(scope="function")
def sample_project(db_session):
    project = Project(
        project_id=str(uuid4()),
        project_name="Test Project",
        body="Test Project Body"
    )
    db_session.add(project)
    db_session.commit()
    return project

@pytest.fixture(scope="function")
def sample_publication(db_session):
    publication = Publication(
        publication_id=str(uuid4()),
        publication_name="Test Publication",
        body="Test Publication Body"
    )
    db_session.add(publication)
    db_session.commit()
    return publication

@pytest.fixture(scope="function")
def sample_events(db_session, sample_lab, sample_project, sample_publication):
    events = [
        Events(
            event_id=str(uuid4()),
            event_name=f"Event {i}",
            image_high=b"high_image_data",
            image_low=b"low_image_data",
            body=f"Body content for Event {i}",
            location=f"Location {i}",
            date_start=datetime.now(),
            date_end=datetime.now() + timedelta(days=1),
            posted=True,
            lab_id=sample_lab.lab_id,
            project_id=sample_project.project_id,
            publication_id=sample_publication.publication_id,
        ) for i in range(15)
    ]
    db_session.add_all(events)
    db_session.commit()
    return events


def test_get_event_thumbnail(sample_events, db_session):
    response = client.get("/user/event/thumbnail?amount=5&page=1")
    assert response.status_code == 200
    assert len(response.json()) == 5

    response = client.get("/user/event/thumbnail?amount=10&page=2")
    assert response.status_code == 200
    assert len(response.json()) == 5

def test_get_event_thumbnail_with_filters(sample_events, db_session):
    lab_id = sample_events[0].lab_id
    response = client.get(f"/user/event/thumbnail?laboratory_id={lab_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1

    research_id = sample_events[1].research_id
    response = client.get(f"/user/event/thumbnail?research_id={research_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_get_event_image_high(sample_events, db_session):
    event_id = sample_events[0].event_id
    response = client.get(f"/user/event/image-high?event_id={event_id}")
    assert response.status_code == 200
    assert response.json()["image_url"] == sample_events[0].image_high

def test_get_event_image_high_not_found(db_session):
    non_existent_id = uuid4()
    response = client.get(f"/user/event/image-high?event_id={non_existent_id}")
    assert response.status_code == 404

def test_get_event_image_low(sample_events, db_session):
    event_id = sample_events[0].event_id
    response = client.get(f"/user/event/image-low?event_id={event_id}")
    assert response.status_code == 200
    assert response.json()["image_url"] == sample_events[0].image_low

def test_get_event_image_low_not_found(db_session):
    non_existent_id = uuid4()
    response = client.get(f"/user/event/image-low?event_id={non_existent_id}")
    assert response.status_code == 404

# @pytest.mark.asyncio
# async def test_get_event_thumbnail_async(sample_events, db_session):
#     response = await client.get("/user/event/thumbnail?amount=5&page=1")
#     assert response.status_code == 200
#     assert len(response.json()) == 5

# @pytest.mark.asyncio
# async def test_get_event_image_high_async(sample_events, db_session):
#     event_id = sample_events[0].event_id
#     response = await client.get(f"/user/event/image-high?event_id={event_id}")
#     assert response.status_code == 200
#     assert response.json()["image_url"] == sample_events[0].image_high

# @pytest.mark.asyncio
# async def test_get_event_image_low_async(sample_events, db_session):
#     event_id = sample_events[0].event_id
#     response = await client.get(f"/user/event/image-low?event_id={event_id}")
#     assert response.status_code == 200
#     assert response.json()["image_url"] == sample_events[0].image_low