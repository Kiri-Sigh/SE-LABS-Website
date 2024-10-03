from pydantic import BaseModel

from ..unreadable import RC01_researcher_create as unreadable

class ResearcherCreate(BaseModel):
    Researcher: unreadable.RC01