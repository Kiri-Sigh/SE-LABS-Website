from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from uuid import UUID
from fastapi.responses import Response

from dependencies import get_db
from model import *
from schemas.publication_thumbnail import PublicationThumbnail, PT01

router = APIRouter(
    prefix="/user/publication",
    tags=["publication"],
)

@router.get("/thumbnail", response_model=List[PublicationThumbnail])
def get_publication_thumbnail(
    laboratory_id: Optional[UUID] = Query(None),
    amount: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
    db = Depends(get_db)
):
    publication = db.query(Publication)
    if laboratory_id:
        publication = publication.filter(Publication.lab_id == laboratory_id)
    offset = (page - 1) * amount
    publications = publication.offset(offset).limit(amount).all()
    return [PT01.to_publication_thumbnail(publication) for publication in publications]

@router.get("/thumbnail/{publication_id}", response_model=PublicationThumbnail)
def get_publication_thumbnail_by_id(publication_id: UUID, db = Depends(get_db)):
    publication = db.query(Publication).filter(Publication.publication_id == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return PT01.to_publication_thumbnail(publication)

@router.get("/image-high")
def get_publication_image_high(publication_id: UUID, db = Depends(get_db)):
    publication = db.query(Publication).filter(Publication.publication_id == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return Response(content=publication.image_high, media_type="image/jpeg")

@router.get("/image-low")
def get_publication_image_low(publication_id: UUID, db = Depends(get_db)):
    publication = db.query(Publication).filter(Publication.publication_id == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return Response(content=publication.image_low, media_type="image/jpeg")