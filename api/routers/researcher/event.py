from fastapi import APIRouter

from ...schemas.request.event.readable import EventCreate as schema

router = APIRouter(
    prefix="/researcher/event",
    tags=["event"],
)

@router.post("/")
async def create_event(
    body: schema.EventCreate
        ):
    return {"message": "Event posted"}