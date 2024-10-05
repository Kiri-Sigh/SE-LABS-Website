from fastapi import APIRouter, Header

router = APIRouter(
    prefix="/admin/researcher",
    tags=["researcher"],
)

@router.patch("/")
async def assign_to_lead_researcher(
    laboratory_id: int,
    researcher_id: int,
    token: str = Header()
        ):
    return {"message": "Researcher updated"}

@router.delete("/")
async def delete_researcher_out_of_laboratory(
    laboratory_id: int,
    researcher_id: int,
    token: str = Header()
        ):
    return {"message": "Researcher deleted"}