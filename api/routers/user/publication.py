from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from ...dependency.database import get_db
from ...pydantic.response.publication.PT01_publication_thumbnail import PT01
from ...pydantic.response.publication.PIMG01_publication_image import PIMG01

router = APIRouter(
    prefix="/user/publication",
    tags=["publication"],
)

@router.get("/thumbnail", response_model=list[PT01])
async def get_publication_thumbnail(
        laboratory_id: Optional[str] = None,
        amount: Optional[int] = 0,
        page: Optional[int] = 1,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get publication thumbnail"}

@router.get("/image-high", response_model=PIMG01)
async def get_publication_image_high(
        publication_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get publication image high"}

@router.get("/image-low", response_model=PIMG01)
async def get_publication_image_low(
        publication_id: str,
        db: Session = Depends(get_db)
        ):
    return {"message": "Get publication image low"}