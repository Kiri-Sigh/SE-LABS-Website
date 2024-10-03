from pydantic import BaseModel, ConfigDict
from uuid import UUID
from abc import ABC

from ..util.image import ImageInterface

class LabInterface(BaseModel, ABC, ImageInterface): 
    lab_name: str
    body: str

    def __new__(cls, *args, **kwargs):
        if cls is LabInterface:
            raise TypeError(f"{cls.__name__} is an abstract class and cannot be instantiated directly.")
        return super().__new__(cls)

class LabCreate(LabInterface):
    pass

class LabDB(LabInterface):
    lab_id: UUID
    researches: list[UUID]
    publications: list[UUID]
    news: list[UUID]
    events: list[UUID]

    model_config = ConfigDict(from_attributes=True)