"""Seed script for creating initial application data."""

from __future__ import annotations

from typing import Optional

from flask import Flask, current_app

from . import create_app
from .db import db
from .models import User


def ensure_admin_user() -> User:
    """Ensure an administrator account exists using configured credentials."""

    email = current_app.config["ADMIN_EMAIL"]
    password = current_app.config["ADMIN_PASSWORD"]

    admin = User.query.filter_by(email=email).first()
    if admin:
        if not admin.is_admin:
            admin.is_admin = True
            db.session.commit()
        return admin

    admin = User(email=email, is_admin=True)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    return admin


def seed_app(app: Optional[Flask] = None) -> None:
    """Run the seed process, creating the administrator user."""

    app = app or create_app()
    with app.app_context():
        db.create_all()
        ensure_admin_user()


if __name__ == "__main__":
    seed_app()
