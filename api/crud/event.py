from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List, Optional
from uuid import UUID

from ..models.model import Event
from ..schemas.core.event import EventCreate, EventDB

def get_event(db: Session, event_id: UUID) -> Optional[EventDB]:
    """
    Retrieve a single event by its ID.

    Args:
        db (Session): The database session.
        event_id (UUID): The ID of the event to retrieve.

    Returns:
        Optional[EventDB]: The event if found, None otherwise.

    Raises:
        HTTPException: If a database error occurs.
    """
    try:
        return db.query(Event).filter(Event.event_id == event_id).first()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def get_event_list(db: Session, skip: int = 0, limit: int = 100) -> List[EventDB]:
    """
    Retrieve a list of events with pagination.

    Args:
        db (Session): The database session.
        skip (int): Number of records to skip (default: 0).
        limit (int): Maximum number of records to return (default: 100).

    Returns:
        List[EventDB]: A list of events.

    Raises:
        HTTPException: If a database error occurs.
    """
    try:
        return db.query(Event).offset(skip).limit(limit).all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def create_event(db: Session, event: EventCreate) -> EventDB:
    """
    Create a new event in the database.

    Args:
        db (Session): The database session.
        event (EventCreate): The event data to create.

    Returns:
        EventDB: The created event.

    Raises:
        HTTPException: If a database error occurs.
    """
    try:
        db_event = Event(**event.model_dump())
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def delete_event(db: Session, event_id: UUID) -> dict:
    """
    Delete an event from the database by its ID.

    Args:
        db (Session): The database session.
        event_id (UUID): The ID of the event to delete.

    Returns:
        dict: A message indicating successful deletion.

    Raises:
        HTTPException: If the event is not found or if a database error occurs.
    """
    try:
        event = db.query(Event).filter(Event.event_id == event_id).first()
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        db.delete(event)
        db.commit()
        return {"message": "Event deleted successfully."}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")