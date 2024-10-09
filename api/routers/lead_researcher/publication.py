from fastapi import APIRouter, Header, Depends

from ...schemas.request.publication.readable import PublicationUpdate as readable
from ...dependency.database import get_db
from ...dependency.get_current_user import get_current_user

from ...models.model import Person, Publication

router = APIRouter(
    prefix="/lead-researcher/publication",
    tags=["publication"],
)

@router.patch("/")
async def update_publication(
    publication_id: int,
    body: readable.PublicationUpdate,
    current_user: Person = Depends(get_current_user),
    db = Depends(get_db)
        ):
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    publication.title = body.title
    publication.body = body.body
    publication.lab_id = body.lab_id
    publication.image_high = body.image_high
    publication.image_low = body.image_low
    db.commit()
    db.refresh(publication)
    return publication


@router.delete("/")
async def delete_publication(
    publication_id: int,
    current_user: Person = Depends(get_current_user),
    db = Depends(get_db)
        ):
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    db.delete(publication)
    db.commit()
    return publication