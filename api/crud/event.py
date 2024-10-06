from sqlalchemy.orm import Session
from ..models.model import Event
from ..schemas.core.event import EventsCreate, EventsDB

def get_event(db: Session, event_id: int) -> EventsDB:
    """
    Retrieve a single event by its ID.
    """
    return db.query(Event).filter(Event.event_id == event_id).first()

def get_event_list(db: Session, skip: int = 0, limit: int = 100) -> list[EventsDB]:
    """
    Retrieve a list of events with pagination.
    """
    return db.query(Event).offset(skip).limit(limit).all()

def create_event(db: Session, event: EventsCreate) -> EventsDB:
    """
    Create a new event in the database.
    """
    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

def delete_event(db: Session, event_id: int):
    """
    Delete an event from the database by its ID.
    """
    db.query(Event).filter(Event.event_id == event_id).delete()
    db.commit()
    return {"message": "Event deleted successfully."}