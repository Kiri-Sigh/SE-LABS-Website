from pydantic import BaseModel

from ..unreadable import NC01_news_create as unreadable

class NewsCreate(BaseModel):
    News: unreadable.NC01