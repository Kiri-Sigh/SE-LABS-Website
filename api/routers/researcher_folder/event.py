from fastapi import APIRouter

router = APIRouter(
    prefix="/researcher/event",
    tags=["event"],
)