from fastapi import APIRouter, Header, Depends, HTTPException

from ...schemas.request.laboratory.readable import LaboratoryUpdate as readable
from ...dependency.get_current_user import get_current_user
from ...dependency.database import get_db
from ...models.model import Laboratory, Person

router = APIRouter(
    prefix="/lead-researcher/laboratory",
    tags=["laboratory"],
)

@router.patch("/")
async def update_laboratory(
    laboratory_id: int,
    body: readable.LaboratoryUpdate,
    current_user: Person = Depends(get_current_user),
    db = Depends(get_db)
        ):
    laboratory = db.query(Laboratory).filter(Laboratory.id == laboratory_id).first()
    laboratory.title = body.title
    laboratory.body = body.body
    laboratory.image_high = body.image_high
    laboratory.image_low = body.image_low
    db.commit()
    db.refresh(laboratory)
    return laboratory
