"""File storage utilities for handling user uploads."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Final
from uuid import uuid4

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

__all__ = ["StorageError", "save_upload"]


class StorageError(RuntimeError):
    """Raised when a file cannot be saved to storage."""


_ALLOWED_MIME_TYPES: Final[frozenset[str]] = frozenset({"image/jpeg", "image/png"})
_MAX_FILE_SIZE: Final[int] = 10 * 1024 * 1024  # 10MB


def _validate_file(file_storage: FileStorage) -> None:
    if not file_storage:
        raise StorageError("No file provided for upload.")

    if not file_storage.mimetype:
        raise StorageError("Could not determine the file's MIME type.")

    if file_storage.mimetype not in _ALLOWED_MIME_TYPES:
        raise StorageError("Unsupported media type. Only JPEG and PNG images are allowed.")

    filename = secure_filename(file_storage.filename or "")
    if not filename:
        raise StorageError("The uploaded file must have a valid filename.")


def _enforce_size_limit(file_storage: FileStorage) -> None:
    current_position = file_storage.stream.tell()
    file_storage.stream.seek(0, os.SEEK_END)
    size = file_storage.stream.tell()
    file_storage.stream.seek(current_position)

    if size > _MAX_FILE_SIZE:
        raise StorageError("File exceeds the maximum allowed size of 10 MB.")


def save_upload(file_storage: FileStorage, upload_folder: str) -> str:
    """Persist an uploaded file to the configured storage location.

    Args:
        file_storage: The Werkzeug ``FileStorage`` instance to save.
        upload_folder: Absolute path to the directory where files are stored.

    Returns:
        The absolute path to the saved file.

    Raises:
        StorageError: If validation fails or the file cannot be saved.
    """

    _validate_file(file_storage)
    _enforce_size_limit(file_storage)

    upload_path = Path(upload_folder)
    try:
        upload_path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:  # pragma: no cover - unlikely but defensive
        raise StorageError("Unable to prepare the upload directory.") from exc

    original_name = secure_filename(file_storage.filename or "upload")
    extension = Path(original_name).suffix
    unique_name = f"{uuid4().hex}{extension}"
    destination = upload_path / unique_name

    try:
        file_storage.save(destination)
    except OSError as exc:
        raise StorageError("Failed to save the uploaded file.") from exc

    return str(destination)
