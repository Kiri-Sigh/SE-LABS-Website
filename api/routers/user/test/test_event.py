from fastapi.exceptions import RequestValidationError
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from ..event import router
from ....fake_db.event import fake_db_event

client = TestClient(router)

def test_get_thumbnail():
    response = client.get("/user/event/thumbnail?amount=5")
    assert response.status_code == 200
    assert response.json() == fake_db_event[:5]

def test_get_thumbnail_partial_events():
    response = client.get("/user/event/thumbnail?amount=3")
    assert response.status_code == 200
    assert response.json() == fake_db_event[:3]

def test_get_thumbnail_negative_amount():
    with pytest.raises(HTTPException) as excinfo:
        client.get("/user/event/thumbnail?amount=-1")
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Amount must be a positive integer"

def test_get_thumbnail_zero_amount():
    response = client.get("/user/event/thumbnail?amount=0")
    assert response.status_code == 200
    assert response.json() == []

def test_get_thumbnail_too_much_amount():
    with pytest.raises(HTTPException) as excinfo:
        client.get("/user/event/thumbnail?amount=100")
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Amount exceeds the number of events in the database"

def test_get_thumbnail_with_laboratory_id():
    response = client.get("/user/event/thumbnail?amount=2&laboratory_id=1")
    assert response.status_code == 200
    assert len(response.json()) <= 2
    for event in response.json():
        assert event["laboratory_id"] == 1

def test_get_thumbnail_with_research_id():
    response = client.get("/user/event/thumbnail?amount=2&research_id=1")
    assert response.status_code == 200
    assert len(response.json()) <= 2
    for event in response.json():
        assert event["research_id"] == 1

def test_get_thumbnail_with_laboratory_and_research_id():
    response = client.get("/user/event/thumbnail?amount=2&laboratory_id=1&research_id=1")
    assert response.status_code == 200
    assert len(response.json()) <= 2
    for event in response.json():
        assert event["laboratory_id"] == 1 and event["research_id"] == 1

def test_get_thumbnail_no_matching_events():
    response = client.get("/user/event/thumbnail?amount=2&laboratory_id=999")
    assert response.status_code == 200
    assert response.json() == []

def test_get_thumbnail_string_amount():
    with pytest.raises(RequestValidationError) as excinfo:
        client.get("/user/event/thumbnail?amount=abc")
    exception = excinfo.value
    errors = exception.errors()
    assert len(errors) == 1
    assert errors[0]['type'] == 'int_parsing'
    assert errors[0]['loc'] == ('query', 'amount')
    assert 'unable to parse' in errors[0]['msg']
    assert errors[0]['input'] == 'abc'

def test_get_thumbnail_float_amount():
    with pytest.raises(RequestValidationError) as excinfo:
        client.get("/user/event/thumbnail?amount=1.5")
    exception = excinfo.value
    errors = exception.errors()
    assert len(errors) == 1
    assert errors[0]['type'] == 'int_parsing'
    assert errors[0]['loc'] == ('query', 'amount')
    assert 'unable to parse' in errors[0]['msg']
    assert errors[0]['input'] == '1.5'

def test_get_thumbnail_no_amount():
    with pytest.raises(RequestValidationError) as excinfo:
        client.get("/user/event/thumbnail")
    exception = excinfo.value
    errors = exception.errors()
    assert len(errors) == 1
    assert errors[0]['type'] == 'missing'
    assert errors[0]['loc'] == ('query', 'amount')
    assert 'Field required' in errors[0]['msg']
    assert errors[0]['input'] == None