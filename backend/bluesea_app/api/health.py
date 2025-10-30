"""Health check endpoint for the API."""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Return a simple JSON payload confirming the API is running."""

    return jsonify({"status": "ok"})
