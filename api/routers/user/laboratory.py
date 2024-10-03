from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from ...dependency.database import get_db
from ...schemas.response.laboratory.LT01_laboratory_thumbnail import LT01
from ...schemas.response.laboratory.LIMG01_laboratory_image import LIMG01

router = APIRouter(
    prefix="/user/laboratory",
    tags=["laboratory"],
)

@router.get("/thumbnail", response_model=list[LT01])
async def get_laboratory_thumbnail(
        laboratory_id: Optional[str] = None,
        amount: Optional[int] = 0,
        page: Optional[int] = 1,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get laboratory thumbnail"}

@router.get("/image-high", response_model=LIMG01)
async def get_laboratory_image_high(
        laboratory_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get laboratory image high"}

@router.get("/image-low", response_model=LIMG01)
async def get_laboratory_image_low(
        laboratory_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get laboratory image low"}