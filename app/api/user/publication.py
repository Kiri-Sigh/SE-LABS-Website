from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from uuid import UUID

from ...dependencies import get_db
from ...model import *
from ...schemas.publication_thumbnail import PublicationThumbnail

router = APIRouter(
    prefix="/user/publication",
    tags=["publication"],
)

@router.get("/thumbnail", response_model=List[PublicationThumbnail])
def get_publication_thumbnail(
    laboratory_id: Optional[UUID] = Query(),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db = Depends(get_db)
):
    publication = db.query(Publication).filter(Publication.posted == True)
    if laboratory_id:
        publication = publication.filter(Publication.lab_id == laboratory_id)
    offset = (page - 1) * amount
    return publication.offset(offset).limit(amount).all()

@router.get("/image-high")
def get_publication_image_high(publication_id: UUID, db = Depends(get_db)):
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication.image_high

@router.get("/image-low")
def get_publication_image_low(publication_id: UUID, db = Depends(get_db)):
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return publication.image_low