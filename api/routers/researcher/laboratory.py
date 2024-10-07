from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/researcher/laboratory",
    tags=["laboratory"],
)