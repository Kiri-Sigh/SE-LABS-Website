from fastapi import APIRouter

router = APIRouter(
    prefix="/researcher/publication",
    tags=["publication"],
)