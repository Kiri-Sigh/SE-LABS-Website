from fastapi import APIRouter

router = APIRouter(
    prefix="/admin/laboratory",
    tags=["laboratory"],
)