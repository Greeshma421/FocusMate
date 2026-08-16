"""Database package helpers
Expose get_db dependency for convenience imports: from app.db import get_db
"""
from .session import get_db  # noqa: F401