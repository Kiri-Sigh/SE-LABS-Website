from pydantic import BaseModel, model_validator
from PIL import Image
import io
from typing import Optional

class ImageInterface(BaseModel):
    image_high: bytes
    image_low: Optional[bytes] = None

    @model_validator(mode='before')  # Use 'before' mode to manipulate values before validation
    def generate_image_low(cls, values):
        if 'image_high' in values and not values.get('image_low'):
            values['image_low'] = cls._create_low_resolution(values['image_high'])
        return values

    @classmethod
    def _create_low_resolution(cls, image: bytes) -> bytes:
        try:
            with Image.open(io.BytesIO(image)) as img:
                width, height = img.size
                new_width = width // 2
                new_height = height // 2

                low_res_img = img.resize((new_width, new_height), Image.LANCZOS)

                buffer = io.BytesIO()
                low_res_img.save(buffer, format=img.format)
                return buffer.getvalue()
        except Exception as e:
            raise ValueError("Invalid image data provided") from e
