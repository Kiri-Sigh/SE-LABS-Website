from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import Optional
from uuid import UUID, uuid4
import json
from pydantic import ValidationError

from ...dependencies import get_db, process_image
from ...auth import get_current_active_admin
from ...schemas.auth_user import AuthUser
from ...schemas.laboratory_thumbnail import LaboratoryThumbnail, LT01
from ...schemas.laboratory_io import LaboratoryCreate
from ...schemas.ult.position import Position
from ...model import Laboratory, Event, News, Publication, Research, person_lab, person_research, Researcher

router = APIRouter(
    prefix="/admin/laboratory",
    tags=["laboratory"],
)

@router.post("/", response_model=LaboratoryThumbnail)
async def create_laboratory(
    laboratory: str,
    image: UploadFile = File(...),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_admin)
    ):
    """
    laboratory must come in this form
    {
        "title": "string",
        "body": "string"
    }
    """
    if image.content_type not in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG images are allowed")

    try:
        laboratory_data = json.loads(laboratory)
        laboratory_object = LaboratoryCreate.model_validate(laboratory_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in news field")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    processed_images = await process_image(image)
    high_res, low_res = processed_images

    new_lab = Laboratory(
        lab_id=uuid4(),
        lab_name=laboratory_object.title,
        image_high=high_res,
        image_low=low_res,
        body=laboratory_object.body
    )

    db.add(new_lab)

    all_admin = db.query(Researcher).filter(Researcher.admin == True).all()
    for admin in all_admin:
        db.add(person_lab(user_id=admin.user_id, lab_id=new_lab.lab_id, role=Position.Admin))

    db.commit()
    db.refresh(new_lab)
    return LT01.to_laboratory_thumbnail(new_lab)

@router.delete("/", response_model=LaboratoryThumbnail)
def delete_laboratory(
    laboratory_id: UUID,
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_admin)
):
    lab = db.query(Laboratory).filter(Laboratory.lab_id == laboratory_id).first()
    if lab is None:
        raise HTTPException(status_code=404, detail="Laboratory not found")
    
    result = LT01.to_laboratory_thumbnail(lab)

    # Delete associated events
    db.query(Event).filter(Event.lab_id == laboratory_id).delete()

    # Delete associated news
    db.query(News).filter(News.lab_id == laboratory_id).delete()

    # Delete associated publications
    db.query(Publication).filter(Publication.lab_id == laboratory_id).delete()

    # Get all research IDs associated with this lab
    research_ids = [research.research_id for research in lab.researches]

    # Delete person_research entries
    db.query(person_research).filter(person_research.research_id.in_(research_ids)).delete(synchronize_session='fetch')

    # Delete person_lab entries
    db.query(person_lab).filter(person_lab.lab_id == laboratory_id).delete(synchronize_session='fetch')

    # Delete associated researches
    db.query(Research).filter(Research.lab_id == laboratory_id).delete()

    # Delete the laboratory
    db.delete(lab)

    db.commit()
    return result