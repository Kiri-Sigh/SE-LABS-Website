from pydantic import BaseModel

from ..unreadable import RL01_researcher_login as unreadable

class ResearcherLogin(BaseModel):
    Researcher: unreadable.RL01