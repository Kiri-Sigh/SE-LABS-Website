from fastapi import APIRouter

from ...schemas.request.laboratory.readable import LaboratoryCreate as readable

router = APIRouter(
    prefix="/admin/laboratory",
    tags=["laboratory"],
)

@router.post("/")
async def create_laboratory(
    body: readable.LaboratoryCreate
        ):
    return {"message": "Laboratory created"}

@router.delete("/")
async def delete_laboratory(
    laboratory_id: int
        ):
    return {"message": "Laboratory deleted"}