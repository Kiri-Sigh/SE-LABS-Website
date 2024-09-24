from fastapi import APIRouter

router = APIRouter(
    prefix="/user/publication",
    tags=["publication"],
)