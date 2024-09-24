from fastapi import APIRouter

router = APIRouter(
    prefix="/lead-researcher/event",
    tags=["event"],
)