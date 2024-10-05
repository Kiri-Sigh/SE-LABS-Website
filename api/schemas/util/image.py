from pydantic import BaseModel, model_validator
from PIL import Image
import io


class ImageInterface(BaseModel):
    image_high: bytes
    image_low: bytes = None

    @model_validator(mode='before')
    @classmethod
    def validate_and_process_image(cls, values):
        if 'image_high' in values:
            values['image_high'] = cls._ensure_jpg(values['image_high'])
            values['image_low'] = cls._create_low_resolution(values['image_high'])
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