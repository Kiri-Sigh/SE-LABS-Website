from fastapi import APIRouter, Header

from ...schemas.request.publication.readable import PublicationUpdate as readable

router = APIRouter(
    prefix="/lead-researcher/publication",
    tags=["publication"],
)

@router.patch("/")
async def update_publication(
    publication_id: int,
    body: readable.PublicationUpdate,
    token: str = Header()
        ):
    return {"message": "Publication updated"}

@router.delete("/")
async def delete_publication(
    publication_id: int,
    token: str = Header()
        ):
    return {"message": "Publication deleted"}