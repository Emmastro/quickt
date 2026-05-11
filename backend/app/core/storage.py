"""
File storage abstraction — dispatches to local filesystem or S3
depending on settings.storage_backend.
"""

import uuid
from pathlib import Path

import boto3
from botocore.config import Config as BotoConfig
from fastapi import UploadFile
from PIL import Image

from app.config import get_settings

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


class StorageError(Exception):
    pass


def _validate_image(file: UploadFile, max_mb: int) -> str:
    """Validate file type and size. Returns the cleaned extension."""
    if file.content_type not in ALLOWED_TYPES:
        raise StorageError(f"Invalid file type: {file.content_type}. Allowed: {', '.join(ALLOWED_TYPES)}")

    ext = Path(file.filename or "image.jpg").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        ext = ".jpg"
    return ext


def _generate_key(prefix: str, ext: str) -> str:
    return f"{prefix}/{uuid.uuid4().hex}{ext}"


async def save_image(file: UploadFile, prefix: str = "images") -> str:
    """Save an uploaded image and return its public URL."""
    settings = get_settings()
    ext = _validate_image(file, settings.upload_max_size_mb)

    content = await file.read()
    max_bytes = settings.upload_max_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise StorageError(f"File too large. Maximum size: {settings.upload_max_size_mb}MB")

    try:
        img = Image.open(file.file)
        img.verify()
        await file.seek(0)
    except Exception:
        raise StorageError("File is not a valid image")

    key = _generate_key(prefix, ext)

    if settings.storage_backend == "s3":
        return _save_to_s3(content, key, file.content_type, settings)
    else:
        return _save_to_local(content, key, settings)


def _save_to_local(content: bytes, key: str, settings) -> str:
    upload_root = Path(settings.upload_dir)
    file_path = upload_root / key
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_bytes(content)

    if settings.upload_base_url:
        return f"{settings.upload_base_url.rstrip('/')}/{key}"
    return f"/uploads/{key}"


def _save_to_s3(content: bytes, key: str, content_type: str, settings) -> str:
    client_kwargs = {
        "aws_access_key_id": settings.s3_access_key,
        "aws_secret_access_key": settings.s3_secret_key,
        "region_name": settings.s3_region or None,
    }
    if settings.s3_endpoint_url:
        client_kwargs["endpoint_url"] = settings.s3_endpoint_url

    s3 = boto3.client("s3", **client_kwargs, config=BotoConfig(signature_version="s3v4"))

    s3.put_object(
        Bucket=settings.s3_bucket,
        Key=key,
        Body=content,
        ContentType=content_type,
    )

    if settings.upload_base_url:
        return f"{settings.upload_base_url.rstrip('/')}/{key}"

    if settings.s3_endpoint_url:
        return f"{settings.s3_endpoint_url.rstrip('/')}/{settings.s3_bucket}/{key}"
    return f"https://{settings.s3_bucket}.s3.{settings.s3_region}.amazonaws.com/{key}"
