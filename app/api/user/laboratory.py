from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from uuid import UUID
from fastapi.responses import Response

from ...dependencies import get_db
from ...model import *
from ...schemas.laboratory_thumbnail import LaboratoryThumbnail, LT01

router = APIRouter(
    prefix="/user/laboratory",
    tags=["laboratory"],
)

@router.get("/thumbnail", response_model=List[LaboratoryThumbnail])
def get_laboratory_thumbnail(
    laboratory_id: Optional[UUID] = Query(None),
    amount: Optional[int] = Query(3),
    page: Optional[int] = Query(1),
    db = Depends(get_db)
):
    laboratory = db.query(Laboratory)
    if laboratory_id:
        laboratory = laboratory.filter(Laboratory.lab_id== laboratory_id)
    offset = (page - 1) * amount
    laboratories = laboratory.offset(offset).limit(amount).all()
    return [LT01.to_laboratory_thumbnail(lab) for lab in laboratories]

@router.get("/image-high")
def get_laboratory_image_high(laboratory_id: UUID, db = Depends(get_db)):
    laboratory = db.query(Laboratory).filter(Laboratory.lab_id == laboratory_id).first()
    if not laboratory:
        raise HTTPException(status_code=404, detail="Laboratory not found")
    return Response(content=laboratory.image_high, media_type="image/jpeg")

@router.get("/image-low")
def get_laboratory_image_low(laboratory_id: UUID, db = Depends(get_db)):
    laboratory = db.query(Laboratory).filter(Laboratory.lab_id == laboratory_id).first()
    if not laboratory:
        raise HTTPException(status_code=404, detail="Laboratory not found")
    return Response(content=laboratory.image_low, media_type="image/jpeg")