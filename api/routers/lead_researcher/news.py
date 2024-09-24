from fastapi import APIRouter

router = APIRouter(
    prefix="/lead-researcher/news",
    tags=["news"],
)