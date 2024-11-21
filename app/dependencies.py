from fastapi import Depends, UploadFile, File
from PIL import Image
import io
from typing import Tuple
from .database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def process_image(image: UploadFile = File(...)) -> Tuple[bytes, bytes]:
    contents = await image.read()
    img = Image.open(io.BytesIO(contents))

    # Create high resolution version (1080x720)
    high_res = img.resize((1080, 720), Image.LANCZOS)
    high_res_bytes = io.BytesIO()
    high_res.save(high_res_bytes, format='JPEG')
    high_res_bytes = high_res_bytes.getvalue()

    # Create low resolution version (540x360, half of the high res)
    low_res = img.resize((540, 360), Image.LANCZOS)
    low_res_bytes = io.BytesIO()
    low_res.save(low_res_bytes, format='JPEG')
    low_res_bytes = low_res_bytes.getvalue()

    return high_res_bytes, low_res_bytes

def get_processed_images(image: UploadFile = File(...)):
    return process_image(image)