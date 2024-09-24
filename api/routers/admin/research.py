from fastapi import APIRouter

router = APIRouter(
    prefix="/admin/research",
    tags=["research"],
)