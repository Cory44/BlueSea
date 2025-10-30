"""Database models for the BlueSea backend."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Iterable, List

from werkzeug.security import check_password_hash, generate_password_hash

from .db import db


class User(db.Model):
    """Represents an account within the BlueSea social network."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    posts = db.relationship("Post", back_populates="author", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:  # pragma: no cover - repr for debugging
        return f"<User {self.email}>"


class Post(db.Model):
    """Represents a post authored by a user."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    source = db.Column(db.String(50), nullable=False, default="community")
    tags = db.Column(db.Text, nullable=False, default="[]")
    image_path = db.Column(db.String(512))

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    author = db.relationship("User", back_populates="posts")

    def set_tags(self, tags: Iterable[str]) -> None:
        """Persist the provided collection of tags as a JSON array."""

        normalized = [tag for tag in tags if tag]
        self.tags = json.dumps(normalized)

    def get_tags(self) -> List[str]:
        """Return the list of tags associated with the post."""

        try:
            value = json.loads(self.tags or "[]")
        except (TypeError, json.JSONDecodeError):
            return []
        if not isinstance(value, list):
            return []
        return [str(tag) for tag in value if isinstance(tag, str)]

    def __repr__(self) -> str:  # pragma: no cover - repr for debugging
        return f"<Post {self.id} by user {self.user_id}>"
