from fastapi import APIRouter, Header

router = APIRouter(
    prefix="/lead-researcher/event",
    tags=["event"],
)

@router.get("/commit")
async def get_commit(
    laboratory_id: int,
    token: str = Header()
        ):
    return {"message": "Event committed"}

@router.patch("/")
async def update_event(
    event_id: int,
    approve: bool,
    token: str = Header()
        ):
    return {"message": "Event updated"}

@router.delete("/")
async def delete_event(
    event_id: int,
    token: str = Header()
        ):
    return {"message": "Event deleted"}