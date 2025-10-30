"""Authentication endpoints for the BlueSea API."""

from __future__ import annotations

import re
from typing import Any, Dict

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    current_user,
    get_jwt_identity,
    jwt_required,
)

from ..db import db
from ..models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

_USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{3,50}$")
_PASSWORD_MIN_LENGTH = 8


def _json_error(code: str, message: str, status: int):
    payload = {"error": code, "message": message}
    return jsonify(payload), status


def _validate_payload(data: Dict[str, Any]):
    if not isinstance(data, dict):
        return "invalid_payload", "Request payload must be a JSON object."

    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not username:
        return "username_required", "Username is required."
    if not _USERNAME_RE.match(username):
        return (
            "invalid_username",
            "Username must be 3-50 characters and contain only letters, numbers, dots, underscores, or hyphens.",
        )

    if not password:
        return "password_required", "Password is required."
    if len(password) < _PASSWORD_MIN_LENGTH:
        return "weak_password", "Password must be at least 8 characters long."

    return None


@auth_bp.post("/register")
def register():
    if not request.is_json:
        return _json_error("invalid_payload", "Request body must be JSON.", 415)

    data = request.get_json(silent=True) or {}
    validation_error = _validate_payload(data)
    if validation_error:
        code, message = validation_error
        return _json_error(code, message, 400)

    username = data["username"].strip()
    password = data["password"]

    existing_user = User.query.filter_by(email=username).first()
    if existing_user:
        return _json_error("conflict", "An account with that username already exists.", 409)

    user = User(email=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=user)
    response = {
        "user": {"id": user.id, "username": user.email, "is_admin": user.is_admin},
        "access_token": access_token,
    }
    return jsonify(response), 201


@auth_bp.post("/login")
def login():
    if not request.is_json:
        return _json_error("invalid_payload", "Request body must be JSON.", 415)

    data = request.get_json(silent=True) or {}
    validation_error = _validate_payload(data)
    if validation_error:
        code, message = validation_error
        return _json_error(code, message, 400)

    username = data["username"].strip()
    password = data["password"]

    user = User.query.filter_by(email=username).first()
    if not user or not user.check_password(password):
        return _json_error("invalid_credentials", "Invalid username or password.", 401)

    access_token = create_access_token(identity=user)
    response = {
        "user": {"id": user.id, "username": user.email, "is_admin": user.is_admin},
        "access_token": access_token,
    }
    return jsonify(response), 200


@auth_bp.get("/me")
@jwt_required()
def me():
    identity = get_jwt_identity()
    if not current_user:
        return _json_error("user_not_found", "The authenticated user could not be found.", 404)

    response = {
        "user": {
            "id": current_user.id,
            "username": current_user.email,
            "is_admin": current_user.is_admin,
            "identity": identity,
        }
    }
    return jsonify(response), 200
