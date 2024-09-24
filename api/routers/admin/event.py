from fastapi import APIRouter

router = APIRouter(
    prefix="/admin/event",
    tags=["event"],
)