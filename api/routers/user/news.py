from fastapi import APIRouter

router = APIRouter(
    prefix="/user/news",
    tags=["news"],
)