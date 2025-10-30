"""Endpoints for creating and retrieving posts."""

from __future__ import annotations

import json
import os
from typing import Iterable, List, Optional

from flask import Blueprint, current_app, jsonify, request, url_for
from flask_jwt_extended import current_user, jwt_required

from ..db import db
from ..models import Post
from ..services.storage import StorageError, save_upload

posts_bp = Blueprint("posts", __name__)


def _normalize_tags(raw: Optional[Iterable[str] | str]) -> List[str]:
    """Normalize incoming tag values to a deterministic list."""

    items: List[str]
    if raw is None:
        items = []
    elif isinstance(raw, (list, tuple, set)):
        items = [str(item) for item in raw]
    elif isinstance(raw, str):
        candidate = raw.strip()
        if not candidate:
            items = []
        else:
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                tokens = [token.strip() for token in candidate.replace(";", ",").split(",")]
                items = [token for token in tokens if token]
            else:
                if isinstance(parsed, list):
                    items = [str(item) for item in parsed]
                elif isinstance(parsed, str):
                    items = [parsed]
                else:
                    items = []
    else:
        items = []

    normalized: List[str] = []
    seen = set()
    for item in items:
        tag = item.strip().lower()
        if not tag or tag in seen:
            continue
        seen.add(tag)
        normalized.append(tag)
    return normalized


def _serialize_post(post: Post) -> dict:
    """Convert a :class:`Post` instance into a serializable dictionary."""

    upload_folder = current_app.config.get("UPLOAD_FOLDER")
    image_url: Optional[str] = None
    if post.image_path:
        normalized_path = post.image_path.replace("\\", "/")
        if normalized_path.lower().startswith(("http://", "https://")):
            image_url = normalized_path
        else:
            filename = normalized_path
            if upload_folder and os.path.isabs(post.image_path):
                try:
                    filename = os.path.relpath(post.image_path, upload_folder)
                except ValueError:
                    filename = os.path.basename(post.image_path)
            image_url = url_for("serve_upload", filename=filename, _external=True)

    author = None
    if post.author:
        author = {
            "id": post.author.id,
            "username": post.author.email,
            "is_admin": post.author.is_admin,
        }

    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "source": post.source,
        "tags": post.get_tags(),
        "image_url": image_url,
        "created_at": post.created_at.isoformat() if post.created_at else None,
        "updated_at": post.updated_at.isoformat() if post.updated_at else None,
        "user": author,
    }


@posts_bp.post("/posts")
@jwt_required()
def create_post():
    """Create a new post using multipart form data."""

    title = (request.form.get("title") or "").strip()
    body = (request.form.get("body") or "").strip()
    source = (request.form.get("source") or "community").strip().lower() or "community"

    if not title:
        return jsonify({"error": "title_required", "message": "Title is required."}), 400
    if not body:
        return jsonify({"error": "body_required", "message": "Body is required."}), 400

    tags_input = request.form.getlist("tags")
    if not tags_input:
        tags_input = request.form.getlist("tags[]")
    if not tags_input:
        single_tag = request.form.get("tags")
        tags_input = single_tag if single_tag is not None else []
    tags = _normalize_tags(tags_input)

    post = Post(title=title, body=body, source=source, author=current_user)
    post.set_tags(tags)

    upload_folder = current_app.config.get("UPLOAD_FOLDER")
    image = request.files.get("image")
    if image:
        try:
            saved_path = save_upload(image, upload_folder)
        except StorageError as exc:
            return jsonify({"error": "upload_failed", "message": str(exc)}), 400
        relative_path = saved_path
        if upload_folder:
            try:
                relative_path = os.path.relpath(saved_path, upload_folder)
            except ValueError:
                relative_path = os.path.basename(saved_path)
        post.image_path = relative_path.replace("\\", "/")

    db.session.add(post)
    db.session.commit()

    return jsonify({"post": _serialize_post(post)}), 201


@posts_bp.get("/posts")
def list_posts():
    """Return a paginated list of posts."""

    source = request.args.get("source")
    limit_param = request.args.get("limit", type=int)
    offset_param = request.args.get("offset", type=int)

    limit = 20 if limit_param is None else max(1, min(limit_param, 50))
    offset = 0 if offset_param is None else max(0, offset_param)

    query = Post.query.order_by(Post.created_at.desc())
    if source:
        query = query.filter(Post.source == source.strip().lower())

    items = query.offset(offset).limit(limit + 1).all()
    has_more = len(items) > limit
    posts = items[:limit]

    next_offset = offset + len(posts) if has_more else None

    return jsonify(
        {
            "items": [_serialize_post(post) for post in posts],
            "nextOffset": next_offset,
            "limit": limit,
            "offset": offset,
        }
    )


@posts_bp.get("/posts/<int:post_id>")
def get_post(post_id: int):
    """Return a single post by its identifier."""

    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "not_found", "message": "Post not found."}), 404

    return jsonify({"post": _serialize_post(post)})
