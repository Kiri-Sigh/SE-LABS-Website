from fastapi import APIRouter, Header

from ...schemas.request.event.readable import EventCreate as schema

router = APIRouter(
    prefix="/researcher/event",
    tags=["event"],
)

@router.post("/")
async def create_event(
    body: schema.EventCreate,
    token: str = Header()
        ):
    return {"message": "Event posted"}