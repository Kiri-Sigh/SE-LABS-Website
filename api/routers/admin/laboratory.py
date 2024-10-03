from fastapi import APIRouter, Header

from ...schemas.request.laboratory.readable import LaboratoryCreate as readable

router = APIRouter(
    prefix="/admin/laboratory",
    tags=["laboratory"],
)

@router.post("/")
async def create_laboratory(
    body: readable.LaboratoryCreate,
    token: str = Header()
        ):
    return {"message": "Laboratory created"}

@router.delete("/")
async def delete_laboratory(
    laboratory_id: int,
    token: str = Header()
        ):
    return {"message": "Laboratory deleted"}