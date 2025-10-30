"""BlueSea Flask application factory and extensions."""

from __future__ import annotations

import os
from typing import Any, Mapping, Optional, Union

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .config import Config
from .db import db

jwt = JWTManager()


def _load_config(app: Flask, config_object: Optional[Union[str, Mapping[str, Any]]]) -> None:
    app.config.from_object(Config)
    if not config_object:
        return
    if isinstance(config_object, str):
        app.config.from_object(config_object)
    else:
        app.config.from_mapping(config_object)


def create_app(config_object: Optional[Union[str, Mapping[str, Any]]] = None) -> Flask:
    """Create and configure the Flask application."""

    app = Flask(__name__, instance_relative_config=True)

    os.makedirs(app.instance_path, exist_ok=True)

    _load_config(app, config_object)

    upload_folder = app.config.get("UPLOAD_FOLDER")
    if upload_folder:
        os.makedirs(upload_folder, exist_ok=True)

    db.init_app(app)
    jwt.init_app(app)

    cors_origins = app.config.get("CORS_ORIGINS", ["*"])
    if isinstance(cors_origins, str):
        cors_origins = [cors_origins]
    resources = {
        r"/api/*": {
            "origins": cors_origins if cors_origins != ["*"] else "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    }
    CORS(app, resources=resources, supports_credentials=True)

    register_error_handlers(app)
    register_jwt_handlers()
    register_routes(app)

    with app.app_context():
        db.create_all()

    return app


def register_error_handlers(app: Flask) -> None:
    """Register JSON error handlers for the application."""

    @app.errorhandler(404)
    def handle_not_found(error):  # type: ignore[override]
        return jsonify({"error": "not_found", "message": str(error)}), 404

    @app.errorhandler(500)
    def handle_internal_error(error):  # type: ignore[override]
        return jsonify({"error": "internal_error", "message": str(error)}), 500


def register_jwt_handlers() -> None:
    """Configure JWT error handlers to return JSON payloads."""

    from .models import User

    @jwt.user_identity_loader
    def user_identity_lookup(user: User):
        return str(user.id) if isinstance(user, User) else str(user)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data.get("sub")
        if identity is None:
            return None
        return User.query.get(int(identity))

    @jwt.user_lookup_error_loader
    def user_lookup_error_callback(_jwt_header, _jwt_data):
        return jsonify({"error": "user_not_found", "message": "The authenticated user could not be found."}), 404

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):  # pragma: no cover - thin wrapper
        return jsonify({"error": "token_expired", "message": "The access token has expired."}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(message):  # pragma: no cover - thin wrapper
        return jsonify({"error": "token_invalid", "message": message}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(message):  # pragma: no cover - thin wrapper
        return jsonify({"error": "authorization_required", "message": message}), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header, jwt_data):  # pragma: no cover - thin wrapper
        return jsonify({"error": "fresh_token_required", "message": "Fresh token required."}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_data):  # pragma: no cover - thin wrapper
        return jsonify({"error": "token_revoked", "message": "The token has been revoked."}), 401


def register_routes(app: Flask) -> None:
    """Register blueprints and utility routes for the application."""

    from .api import api_bp

    @app.route("/uploads/<path:filename>")
    def serve_upload(filename: str):
        upload_folder = app.config.get("UPLOAD_FOLDER")
        return send_from_directory(upload_folder, filename)

    app.register_blueprint(api_bp)


__all__ = ["create_app", "db", "jwt"]
