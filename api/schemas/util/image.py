from pydantic import BaseModel, model_validator
from PIL import Image
import io
import base64

class ImageInterface(BaseModel):
    image_high: bytes
    image_low: bytes = None

    @model_validator(mode='before')
    @classmethod
    def validate_and_process_image(cls, values):
        if 'image_high' in values:
            jpg_bytes = cls._ensure_jpg(values['image_high'])
            low_res_bytes = cls._create_low_resolution(jpg_bytes)
            values['image_low'] = low_res_bytes
        return values

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

    @property
    def image_high_bytes(self) -> bytes:
        return self._base64_to_bytes(self.image_high)

    @property
    def image_low_bytes(self) -> bytes:
        return self._base64_to_bytes(self.image_low) if self.image_low else None