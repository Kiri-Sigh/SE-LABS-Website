from fastapi import APIRouter

router = APIRouter(
    prefix="/admin/publication",
    tags=["publication"],
)