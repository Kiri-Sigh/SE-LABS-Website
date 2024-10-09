from fastapi import APIRouter, Depends
from typing import Optional
from sqlalchemy.orm import Session

from ...dependency.database import get_db
from ...schemas.response.publication.PT01_publication_thumbnail import PT01
from ...schemas.response.publication.PIMG01_publication_image import PIMG01
from ...models.model import Publication


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
    publication = db.query(Publication)
    if laboratory_id:
        publication = publication.filter(Publication.lab_id == laboratory_id)
    offset = (page - 1) * amount
    publication = publication.offset(offset).limit(amount).all()
    return [PT01(publication) for publication in publication]

@router.get("/image-high", response_model=PIMG01)
async def get_publication_image_high(
        publication_id: str,
        db: Session = Depends(get_db)
        ):
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    return PIMG01(publication)

@router.get("/image-low", response_model=PIMG01)
async def get_publication_image_low(
        publication_id: str,
        db: Session = Depends(get_db)
        ):
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    return PIMG01(publication)