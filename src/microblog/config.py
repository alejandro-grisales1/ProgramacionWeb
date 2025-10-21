from __future__ import annotations
import os
import secrets
from urllib.parse import urlparse

class Config:
    """Application configuration loaded from environment variables."""
    SECRET_KEY: str = os.environ.get("SECRET_KEY", secrets.token_hex(32))

    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql+psycopg://microblog_user:12345@localhost/microblog")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security settings
    ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")
    
    # CSRF protection settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600  # 1 hour


def is_safe_url(target: str, host: str) -> bool:
    """Validate that a redirect URL is local/safe using urlparse."""
    if not target:
        return False
    ref = urlparse(host)
    test = urlparse(target)
    # Allow relative URLs
    return not test.netloc or (test.netloc == ref.netloc)

