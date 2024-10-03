from fastapi import APIRouter

from ...schemas.request.laboratory.readable import LaboratoryUpdate as readable

router = APIRouter(
    prefix="/lead-researcher/laboratory",
    tags=["laboratory"],
)

@router.patch("/")
async def update_laboratory(
    laboratory_id: int,
    body: readable.LaboratoryUpdate
        ):
    return {"message": "Laboratory updated"}