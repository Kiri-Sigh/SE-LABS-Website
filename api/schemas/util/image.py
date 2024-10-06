from pydantic import BaseModel, model_validator, field_validator
from PIL import Image
import io
import base64

class ImageInterface(BaseModel):
    image_high: bytes
    image_low: bytes = None

    @field_validator('image_high', mode='before')
    @classmethod
    def validate_image_high(cls, value):
        if isinstance(value, str):
            return cls._base64_to_bytes(value)
        return value

    @model_validator(mode='after')
    def validate_and_process_image(self):
        if self.image_high:
            jpg_bytes = self._ensure_jpg(self.image_high)
            low_res_bytes = self._create_low_resolution(jpg_bytes)
            self.image_high = jpg_bytes
            self.image_low = low_res_bytes
        return self

    @staticmethod
    def _ensure_jpg(image: bytes) -> bytes:
        try:
            with Image.open(io.BytesIO(image)) as img:
                if img.format != 'JPEG':
                    buffer = io.BytesIO()
                    img = img.convert('RGB')
                    img.save(buffer, format='JPEG')
                    return buffer.getvalue()
                return image
        except Exception as e:
            raise ValueError("Invalid image data provided") from e

    @staticmethod
    def _create_low_resolution(image: bytes) -> bytes:
        try:
            with Image.open(io.BytesIO(image)) as img:
                width, height = img.size
                new_width = width // 2
                new_height = height // 2

                low_res_img = img.resize((new_width, new_height), Image.LANCZOS)

                buffer = io.BytesIO()
                low_res_img.save(buffer, format='JPEG')
                return buffer.getvalue()
        except Exception as e:
            raise ValueError("Invalid image data provided") from e

    @staticmethod
    def _base64_to_bytes(base64_string: str) -> bytes:
        try:
            return base64.b64decode(base64_string)
        except Exception as e:
            raise ValueError("Invalid base64 encoded string") from e

    @property
    def image_high_bytes(self) -> bytes:
        return self.image_high

    @property
    def image_low_bytes(self) -> bytes:
        return self.image_low