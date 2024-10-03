from pydantic import BaseModel

from ..unreadable import PT01_publication_tranform as unreadable

class PublicationTranform(BaseModel):
    Publication: unreadable.PT01