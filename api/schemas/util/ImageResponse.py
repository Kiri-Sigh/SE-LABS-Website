from pydantic import BaseModel

from ..response.event.EIMGH01_event_image_high import EIMGH01
from ..response.event.EIMGL01_event_image_low import EIMGL01

class ImageResponse(BaseModel):
    image: EIMGH01 | EIMGL01