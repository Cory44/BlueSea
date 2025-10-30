"""API blueprint registration for BlueSea."""

from flask import Blueprint

from .auth import auth_bp
from .health import health_bp
from .import_mock import import_bp
from .posts import posts_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")
api_bp.register_blueprint(health_bp)
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(posts_bp)
api_bp.register_blueprint(import_bp)

__all__ = ["api_bp"]
