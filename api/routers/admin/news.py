from fastapi import APIRouter

router = APIRouter(
    prefix="/admin/news",
    tags=["news"],
)