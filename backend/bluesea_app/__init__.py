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
    resources = {r"/api/*": {"origins": cors_origins if cors_origins != ["*"] else "*"}}
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
        return jsonify({"error": "Not Found", "message": str(error)}), 404

    @app.errorhandler(500)
    def handle_internal_error(error):  # type: ignore[override]
        return jsonify({"error": "Internal Server Error", "message": str(error)}), 500


def register_jwt_handlers() -> None:
    """Configure JWT error handlers to return JSON payloads."""

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):  # pragma: no cover - thin wrapper
        return jsonify({"error": "token_expired", "description": "The access token has expired."}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(message):  # pragma: no cover - thin wrapper
        return jsonify({"error": "token_invalid", "description": message}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(message):  # pragma: no cover - thin wrapper
        return jsonify({"error": "authorization_required", "description": message}), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header, jwt_data):  # pragma: no cover - thin wrapper
        return jsonify({"error": "fresh_token_required", "description": "Fresh token required."}), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_data):  # pragma: no cover - thin wrapper
        return jsonify({"error": "token_revoked", "description": "The token has been revoked."}), 401


def register_routes(app: Flask) -> None:
    """Register blueprints and utility routes for the application."""

    from .api import api_bp

    @app.route("/uploads/<path:filename>")
    def serve_upload(filename: str):
        upload_folder = app.config.get("UPLOAD_FOLDER")
        return send_from_directory(upload_folder, filename)

    app.register_blueprint(api_bp)


__all__ = ["create_app", "db", "jwt"]
