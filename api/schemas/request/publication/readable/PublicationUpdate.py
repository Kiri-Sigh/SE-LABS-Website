from pydantic import BaseModel

from ..unreadable import PU01_publication_update as unreadable

class PublicationUpdate(BaseModel):
    Publication: unreadable.PU01