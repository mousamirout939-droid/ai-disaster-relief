"""Image preprocessing utilities shared by the YOLO inference pipeline."""
from io import BytesIO

from PIL import Image, ImageOps

MAX_DIMENSION = 1280


def normalize_image(raw_bytes: bytes) -> bytes:
    """Auto-orient (EXIF), downscale oversized images, and re-encode as JPEG
    to keep inference latency and storage costs predictable."""
    img = Image.open(BytesIO(raw_bytes))
    img = ImageOps.exif_transpose(img)
    img = img.convert("RGB")

    if max(img.size) > MAX_DIMENSION:
        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION))

    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return buffer.getvalue()


def validate_image_bytes(raw_bytes: bytes, max_size_mb: int = 15) -> None:
    if len(raw_bytes) > max_size_mb * 1024 * 1024:
        raise ValueError(f"Image exceeds max size of {max_size_mb}MB")
    try:
        Image.open(BytesIO(raw_bytes)).verify()
    except Exception as exc:
        raise ValueError("Uploaded file is not a valid image") from exc
