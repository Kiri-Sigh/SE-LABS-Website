from fastapi import APIRouter, Header, Depends, HTTPException

from ...schemas.request.laboratory.readable.LaboratoryCreate import LaboratoryCreate
from ...schemas.request.laboratory.readable.LaboratoryUpdate import LaboratoryUpdate
from ...dependency.get_current_user import get_current_user
from ...dependency.database import get_db
from ...models.model import Laboratory, Person

router = APIRouter(
    prefix="/admin/laboratory",
    tags=["laboratory"],
)

@router.post("/")
async def create_laboratory(
    body: LaboratoryCreate,
    current_user: Person = Depends(get_current_user),
    db = Depends(get_db)
        ):
    laboratory = Laboratory(
        title=body.title,
        body=body.body,
        image_high=body.image_high,
        image_low=body.image_low
    )
    db.add(laboratory)
    db.commit()
    db.refresh(laboratory)
    return laboratory

@router.delete("/")
async def delete_laboratory(
    laboratory_id: int,
    current_user: Person = Depends(get_current_user),
    db = Depends(get_db)
        ):
    laboratory = db.query(Laboratory).filter(Laboratory.id == laboratory_id).first()
    db.delete(laboratory)
    db.commit()
    return laboratory