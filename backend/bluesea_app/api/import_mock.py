"""Endpoints for ingesting mock imported posts."""

from __future__ import annotations

from typing import Dict, List, Optional

from flask import Blueprint, current_app, jsonify, request
from flask.typing import ResponseReturnValue

from ..db import db
from ..models import Post, User
from ..services import is_marine

import_bp = Blueprint("import", __name__, url_prefix="/import")


def _normalize_tags(raw_tags: Optional[List[str]]) -> List[str]:
    if not raw_tags:
        return []
    normalized: List[str] = []
    seen = set()
    for tag in raw_tags:
        if not isinstance(tag, str):
            continue
        cleaned = tag.strip().lower()
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        normalized.append(cleaned)
    return normalized


def _collect_candidates(payload: Dict) -> List[Dict]:
    posts = payload.get("posts")
    if not isinstance(posts, list):
        raise ValueError("Payload must include a list of posts under the 'posts' key.")

    candidates: List[Dict] = []
    for index, item in enumerate(posts):
        if not isinstance(item, dict):
            raise ValueError(f"Post at index {index} must be an object.")

        title = item.get("title")
        body = item.get("body")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"Post at index {index} is missing a valid title.")
        if not isinstance(body, str) or not body.strip():
            raise ValueError(f"Post at index {index} is missing a valid body.")

        source = item.get("source")
        if source is not None and not isinstance(source, str):
            raise ValueError(f"Post at index {index} has an invalid source.")

        image_url = item.get("image_url")
        if image_url is not None and not isinstance(image_url, str):
            raise ValueError(f"Post at index {index} has an invalid image_url.")

        tags_raw = item.get("tags")
        if tags_raw is not None and not isinstance(tags_raw, list):
            raise ValueError(f"Post at index {index} must declare tags as a list when provided.")

        summary_value = item.get("summary")
        summary = summary_value.strip() if isinstance(summary_value, str) else ""
        description_value = item.get("description")
        description = description_value.strip() if isinstance(description_value, str) else ""

        candidates.append(
            {
                "title": title.strip(),
                "body": body.strip(),
                "source": (source or "imported").strip().lower() or "imported",
                "image_url": image_url.strip() if isinstance(image_url, str) else None,
                "tags": _normalize_tags(tags_raw),
                "summary": summary,
                "description": description,
            }
        )

    return candidates


def _determine_author() -> User:
    email = current_app.config.get("ADMIN_EMAIL", "admin@bluesea.local")
    password = current_app.config.get("ADMIN_PASSWORD", "bluesea123")

    author = User.query.filter_by(email=email).first()
    if author:
        return author

    author = User(email=email, is_admin=True)
    author.set_password(password)
    db.session.add(author)
    db.session.flush()
    return author


@import_bp.post("/mock")
def import_mock() -> ResponseReturnValue:
    """Import posts from a mock payload when they relate to marine topics."""

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return (
            jsonify({"error": "invalid_payload", "message": "JSON body must be an object."}),
            400,
        )

    try:
        candidates = _collect_candidates(payload)
    except ValueError as exc:
        return jsonify({"error": "invalid_payload", "message": str(exc)}), 400

    marine_candidates: List[Dict] = []
    for candidate in candidates:
        combined_text = " ".join(
            part
            for part in [
                candidate["title"],
                candidate["summary"],
                candidate["description"],
                candidate["body"],
                " ".join(candidate["tags"]),
            ]
            if part
        )
        if is_marine(combined_text):
            marine_candidates.append(candidate)

    if not marine_candidates:
        return "", 204

    author = _determine_author()

    for candidate in marine_candidates:
        post = Post(
            title=candidate["title"],
            body=candidate["body"],
            source=candidate["source"],
            author=author,
        )
        post.set_tags(candidate["tags"])
        if candidate["image_url"]:
            post.image_path = candidate["image_url"]
        db.session.add(post)

    db.session.commit()

    return jsonify({"imported": len(marine_candidates)}), 201


__all__ = ["import_bp", "import_mock"]
