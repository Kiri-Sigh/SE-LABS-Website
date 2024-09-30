# def test_get_person(db_setup):
#     # Create a person in the database first
#     new_person = People(
#         user_id="testuser123",
#         fullname="Test User",
#         gmail="testuser@gmail.com",
#         token="secrettoken",
#         image_high=b'abc123',
#         image_low=None
#     )

#     db = TestingSessionLocal()
#     db.add(new_person)
#     db.commit()

#     # Then, get that person by user_id
#     response = client.get("/people/testuser123")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["user_id"] == "testuser123"
#     assert data["fullname"] == "Test User"

import os
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from .dependency.database import get_db
from .main import app
from .database import Base
from .sqlalchemy.people import People

load_dotenv()
engine = create_engine(os.getenv("URL_DATABASE"))
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
client = TestClient(app)

@pytest.fixture(scope="module")
def db_setup():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_person(db_setup):
    # Create a new person instance using the SQLAlchemy model
    print("Creating a person...")
    new_person = People(
        user_id="testuser123",
        fullname="Test User",
        gmail="testuser@gmail.com",
        token="secrettoken",
        image_high=b'abc123',  # Correctly mock bytes input
        image_low=None
    )

    # Add the new person to the database session
    print("Person created, checking response...")
    db = TestingSessionLocal()
    db.add(new_person)
    db.commit()
    db.refresh(new_person)  # Refresh to get the latest state

    # Test to verify creation
    response = client.get(f"/people/{new_person.user_id}")
    print("Response received:", response.status_code)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "testuser123"
    assert data["fullname"] == "Test User"