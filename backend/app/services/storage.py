"""Storage abstraction layer for report files.

Supports local filesystem storage (default) and S3-compatible storage (optional).
Configure via STORAGE_BACKEND environment variable: 'local' or 's3'.
"""

import os
from abc import ABC, abstractmethod
from io import BytesIO
from typing import BinaryIO

from app.core.config import settings


class StorageService(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    def save(self, content: bytes, filename: str) -> str:
        """Save content and return storage location identifier."""
        pass

    @abstractmethod
    def open(self, location: str) -> BinaryIO:
        """Open and return a file-like object for reading."""
        pass

    @abstractmethod
    def exists(self, location: str) -> bool:
        """Check if a file exists at the given location."""
        pass

    @abstractmethod
    def delete(self, location: str) -> None:
        """Delete a file at the given location."""
        pass

    @abstractmethod
    def get_download_url(self, location: str, filename: str) -> str | None:
        """Get a download URL for the file. Returns None for local storage."""
        pass


class LocalStorage(StorageService):
    """Local filesystem storage implementation."""

    def __init__(self, base_path: str = "/data/reports"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, content: bytes, filename: str) -> str:
        """Save content to local filesystem and return file path."""
        file_path = os.path.join(self.base_path, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(content)

        return file_path

    def open(self, location: str) -> BinaryIO:
        """Open a local file for reading."""
        return open(location, "rb")

    def exists(self, location: str) -> bool:
        """Check if local file exists."""
        return os.path.exists(location)

    def delete(self, location: str) -> None:
        """Delete a local file."""
        if os.path.exists(location):
            os.remove(location)

    def get_download_url(self, location: str, filename: str) -> str | None:
        """Local storage doesn't use presigned URLs."""
        return None


class S3Storage(StorageService):
    """S3-compatible storage implementation."""

    def __init__(
        self,
        bucket: str,
        region: str = "us-east-1",
        access_key: str | None = None,
        secret_key: str | None = None,
        endpoint_url: str | None = None,
    ):
        try:
            import boto3  # type: ignore[import-not-found]
        except ImportError:
            raise ImportError(
                "boto3 is required for S3 storage. Install with: poetry add boto3"
            )

        self.bucket = bucket
        self.region = region

        session_kwargs = {}
        if access_key and secret_key:
            session_kwargs["aws_access_key_id"] = access_key
            session_kwargs["aws_secret_access_key"] = secret_key

        if region:
            session_kwargs["region_name"] = region

        self.s3_client = boto3.client("s3", endpoint_url=endpoint_url, **session_kwargs)  # type: ignore[call-overload]

    def save(self, content: bytes, filename: str) -> str:
        """Save content to S3 and return S3 URI."""
        key = f"reports/{filename}"
        self.s3_client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=content,
            ContentType="application/pdf",
        )
        return f"s3://{self.bucket}/{key}"

    def open(self, location: str) -> BinaryIO:
        """Open an S3 object for reading."""
        if not location.startswith("s3://"):
            raise ValueError(f"Invalid S3 location: {location}")

        parts = location.replace("s3://", "").split("/", 1)
        bucket = parts[0]
        key = parts[1] if len(parts) > 1 else ""

        response = self.s3_client.get_object(Bucket=bucket, Key=key)
        return BytesIO(response["Body"].read())

    def exists(self, location: str) -> bool:
        """Check if an S3 object exists."""
        if not location.startswith("s3://"):
            return False

        try:
            parts = location.replace("s3://", "").split("/", 1)
            bucket = parts[0]
            key = parts[1] if len(parts) > 1 else ""

            self.s3_client.head_object(Bucket=bucket, Key=key)
            return True
        except Exception:
            return False

    def delete(self, location: str) -> None:
        """Delete an S3 object."""
        if not location.startswith("s3://"):
            raise ValueError(f"Invalid S3 location: {location}")

        parts = location.replace("s3://", "").split("/", 1)
        bucket = parts[0]
        key = parts[1] if len(parts) > 1 else ""

        self.s3_client.delete_object(Bucket=bucket, Key=key)

    def get_download_url(self, location: str, filename: str) -> str | None:
        """Generate a presigned URL for downloading."""
        if not location.startswith("s3://"):
            return None

        parts = location.replace("s3://", "").split("/", 1)
        bucket = parts[0]
        key = parts[1] if len(parts) > 1 else ""

        url: str = self.s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket,
                "Key": key,
                "ResponseContentDisposition": f'attachment; filename="{filename}"',
            },
            ExpiresIn=3600,
        )
        return url


def get_storage_service() -> StorageService:
    """Get the configured storage service instance."""
    backend = getattr(settings, "STORAGE_BACKEND", "local").lower()

    if backend == "s3":
        bucket = getattr(settings, "S3_BUCKET", None)
        if not bucket:
            raise ValueError("S3_BUCKET must be set when STORAGE_BACKEND=s3")

        return S3Storage(
            bucket=bucket,
            region=getattr(settings, "S3_REGION", "us-east-1"),
            access_key=getattr(settings, "AWS_ACCESS_KEY_ID", None),
            secret_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", None),
            endpoint_url=getattr(settings, "S3_ENDPOINT_URL", None),
        )
    else:
        reports_dir = getattr(settings, "REPORTS_DIR", "/data/reports")
        return LocalStorage(base_path=reports_dir)


storage_service = get_storage_service()
