from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ...schemas.request.event.readable.EventCreate import EventCreate
from ...schemas.core.event import EventDB
from ...dependency.get_current_user import get_current_user
from ...dependency.database import get_db
from ...models.model import Person
from ...crud.event import create_event

router = APIRouter(
    prefix="/researcher/event",
    tags=["event"],
)

@router.post("/", response_model=EventDB)
async def create_event(
    body: EventCreate,
    current_user: Person = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new event in the database.

    Args:
        body (EventCreate): The event data to create.
        token (str): The JWT token.
        current_user (Person): The current user.
        db (Session): The database session.

    Returns:
        EventDB: The created event.
    """
    event = create_event(db, body)
    return event