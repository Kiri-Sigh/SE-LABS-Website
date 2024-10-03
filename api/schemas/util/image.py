from pydantic import BaseModel, model_validator
from PIL import Image
import io
from abc import ABC

class ImageInterface(BaseModel, ABC):
    image_high: bytes
    image_low: bytes

    def __new__(cls, *args, **kwargs):
        if cls is ImageInterface:
            raise TypeError(f"{cls.__name__} is an abstract class and cannot be instantiated directly.")
        return super().__new__(cls)

    @model_validator(mode='before')
    def generate_image_low(cls, values):
        if 'image_high' in values:
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
