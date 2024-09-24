from fastapi import APIRouter

router = APIRouter(
    prefix="/researcher/research",
    tags=["research"],
)