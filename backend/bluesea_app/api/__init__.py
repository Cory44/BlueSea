"""API blueprint registration for BlueSea."""

from flask import Blueprint

from .health import health_bp

api_bp = Blueprint("api", __name__, url_prefix="/api")
api_bp.register_blueprint(health_bp)

__all__ = ["api_bp"]
