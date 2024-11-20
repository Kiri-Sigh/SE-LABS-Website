from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from typing import Optional
from uuid import UUID
import json
from pydantic import ValidationError

from ...dependencies import get_db, process_image
from ...model import *
from ...auth import get_current_active_lead_researcher
from ...schemas.auth_user import AuthUser
from ...schemas.laboratory_thumbnail import LaboratoryThumbnail, LT01
from ...schemas.laboratory_io import LaboratoryUpdate

router = APIRouter(
    prefix="/lead_researcher/laboratory",
    tags=["laboratory"],
)

@router.patch("/", response_model=LaboratoryThumbnail)
async def update_laboratory(
    laboratory: str,
    image: UploadFile = File(None),
    db = Depends(get_db),
    current_user: AuthUser = Depends(get_current_active_lead_researcher)
):
    """
    laboratory must come in this form
    {
        "LID": "UUID",
        "title": "string",
        "body": "string"
    }
    """
    if image is not None and image.content_type not in ["image/jpeg", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPEG images are allowed")
    
    try:
        laboratory_data = json.loads(laboratory)
        laboratory_object = LaboratoryUpdate.model_validate(laboratory_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in news field")
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    processed_images = await process_image(image) if image is not None else (None, None)
    high_res, low_res = processed_images

    lab = db.query(Laboratory).filter(Laboratory.lab_id == laboratory_object.LID).first()
    if lab is None:
        raise HTTPException(status_code=404, detail="Laboratory not found")
    lab.lab_name = laboratory_object.title
    lab.body = laboratory_object.body
    if high_res is not None:
        lab.image_high = high_res
    if low_res is not None:
        lab.image_low = low_res
    
    db.commit()
    db.refresh(lab)
    return LT01.to_laboratory_thumbnail(lab)