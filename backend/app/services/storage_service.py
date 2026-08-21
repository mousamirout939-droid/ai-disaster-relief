"""
Abstraction over object storage (S3-compatible) with a local-filesystem
fallback for development. Keeps upload/inference-path logic out of route
handlers and services that just need "give me a URL" / "give me a local path".
"""
import logging
import os
import uuid
from pathlib import Path

import aioboto3

from app.core.config import settings

logger = logging.getLogger("app.services.storage")


class StorageService:
    def __init__(self):
        self.backend = settings.STORAGE_BACKEND

    async def upload_file(self, content: bytes, filename: str, folder: str = "uploads") -> str:
        ext = Path(filename).suffix
        key = f"{folder}/{uuid.uuid4().hex}{ext}"

        if self.backend == "s3":
            session = aioboto3.Session()
            async with session.client(
                "s3",
                region_name=settings.S3_REGION,
                endpoint_url=settings.S3_ENDPOINT_URL,
                aws_access_key_id=settings.S3_ACCESS_KEY,
                aws_secret_access_key=settings.S3_SECRET_KEY,
            ) as s3:
                await s3.put_object(Bucket=settings.S3_BUCKET_NAME, Key=key, Body=content)
            return f"https://{settings.S3_BUCKET_NAME}.s3.{settings.S3_REGION}.amazonaws.com/{key}"

        # local fallback
        local_dir = Path(settings.LOCAL_UPLOAD_DIR) / folder
        local_dir.mkdir(parents=True, exist_ok=True)
        local_path = local_dir / Path(key).name
        local_path.write_bytes(content)
        return f"/media/{folder}/{Path(key).name}"

    async def get_local_path_for_inference(self, url_or_path: str) -> str:
        """YOLO inference needs a local file path; download from S3 if needed."""
        if self.backend != "s3":
            return str(Path(settings.LOCAL_UPLOAD_DIR) / url_or_path.replace("/media/", ""))

        key = url_or_path.split(".amazonaws.com/")[-1]
        tmp_path = f"/tmp/{uuid.uuid4().hex}{Path(key).suffix}"
        session = aioboto3.Session()
        async with session.client(
            "s3",
            region_name=settings.S3_REGION,
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
        ) as s3:
            obj = await s3.get_object(Bucket=settings.S3_BUCKET_NAME, Key=key)
            body = await obj["Body"].read()
        with open(tmp_path, "wb") as f:
            f.write(body)
        return tmp_path
