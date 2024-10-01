import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from contextlib import contextmanager

from .dependency.database import get_db
from .main import app
from .database import Base
from .model import People

load_dotenv()

# Use a same database for testing just for now
TEST_DATABASE_URL = os.getenv("URL_DATABASE")
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_db():
    with get_test_db() as db:
        yield db

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(setup_db):
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_create_person(db_session: Session):
    new_person = People(
        user_id="testuser123",
        fullname="Test User",
        gmail="testuser@gmail.com",
        token="secrettoken",
        image_high=b'abc123',
        image_low=None
    )

    db_session.add(new_person)
    db_session.commit()

    created_person = db_session.query(People).filter(People.user_id == "testuser123").first()
    assert created_person is not None
    assert created_person.fullname == "Test User"
    assert created_person.gmail == "testuser@gmail.com"

def test_get_person(db_session: Session):
    # First, create a person
    new_person = People(
        user_id="testuser456",
        fullname="Another User",
        gmail="anotheruser@gmail.com",
        token="anothertoken",
        image_high=b'def456',
        image_low=None
    )
    db_session.add(new_person)
    db_session.commit()

    # Then test getting the person via API
    response = client.get("/people/testuser456")
    assert response.status_code == 200
    data = response.json()
    assert data["fullname"] == "Another User"
    assert data["gmail"] == "anotheruser@gmail.com"