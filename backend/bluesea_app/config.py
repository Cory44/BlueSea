"""Application configuration for the BlueSea backend."""

from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_INSTANCE_PATH = BASE_DIR / "instance"
DEFAULT_DATABASE_PATH = DEFAULT_INSTANCE_PATH / "bluesea.db"


class Config:
    """Base configuration loading values from environment variables."""

    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", SECRET_KEY)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.getenv('SQLITE_PATH', DEFAULT_DATABASE_PATH)}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_EXPIRES_MINUTES", "30")))
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    JSON_SORT_KEYS = False
    PREFERRED_URL_SCHEME = os.getenv("PREFERRED_URL_SCHEME", "http")
    SERVER_NAME = os.getenv("SERVER_NAME", None)

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@bluesea.local")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "bluesea123")


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)
