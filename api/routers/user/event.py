from fastapi import APIRouter

router = APIRouter(
    prefix="/user/event",
    tags=["event"],
)