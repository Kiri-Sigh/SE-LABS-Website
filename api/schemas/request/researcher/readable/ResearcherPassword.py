from pydantic import BaseModel

from ..unreadable import RP01_researcher_password as unreadable

class ResearcherPassword(BaseModel):
    Researcher: unreadable.RP01