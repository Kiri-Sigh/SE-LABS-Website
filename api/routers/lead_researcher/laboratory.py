from fastapi import APIRouter, Header

from ...schemas.request.laboratory.readable import LaboratoryUpdate as readable

router = APIRouter(
    prefix="/lead-researcher/laboratory",
    tags=["laboratory"],
)

@router.patch("/")
async def update_laboratory(
    laboratory_id: int,
    body: readable.LaboratoryUpdate,
    token: str = Header()
        ):
    return {"message": "Laboratory updated"}