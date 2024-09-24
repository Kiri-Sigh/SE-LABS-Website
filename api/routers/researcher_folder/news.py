from fastapi import APIRouter

router = APIRouter(
    prefix="/researcher/news",
    tags=["news"],
)