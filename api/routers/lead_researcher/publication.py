from fastapi import APIRouter

from ...schemas.request.publication.readable import PublicationUpdate as readable

router = APIRouter(
    prefix="/lead-researcher/publication",
    tags=["publication"],
)

@router.patch("/")
async def update_publication(
    publication_id: int,
    body: readable.PublicationUpdate
        ):
    return {"message": "Publication updated"}

@router.delete("/")
async def delete_publication(
    publication_id: int
        ):
    return {"message": "Publication deleted"}