from fastapi import APIRouter, HTTPException
from ...pydantic.event import Event
from ...fake_db.event import fake_db_event

router = APIRouter(
    prefix="/user/event",
    tags=["event"],
)

@router.get("/thumbnail", response_model=list[Event])
def get_thumbnail(amount: int, laboratory_id: int | None = None, research_id: int | None = None):
    if amount < 0:
        raise HTTPException(status_code=400, detail="Amount must be a positive integer")
    if amount > len(fake_db_event):
        raise HTTPException(status_code=400, detail="Amount exceeds the number of events in the database")

    filtered_events = fake_db_event
    if laboratory_id is not None:
        filtered_events = [event for event in filtered_events if event["laboratory_id"] == laboratory_id]
    if research_id is not None:
        filtered_events = [event for event in filtered_events if event["research_id"] == research_id]

    return filtered_events[:amount]

