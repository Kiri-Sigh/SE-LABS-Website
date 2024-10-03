from pydantic import model_validator
from PIL import Image
import io

class ImageInterface:
    image_high: bytes
    image_low: bytes

    @model_validator(mode='before')
    @staticmethod
    def generate_image_low(values):
        if 'image_high' in values:
            values['image_low'] = ImageInterface._create_low_resolution(values['image_high'])
        return values

    @staticmethod
    def _create_low_resolution(image: bytes) -> bytes:
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