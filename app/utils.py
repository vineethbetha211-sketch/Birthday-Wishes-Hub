import secrets
from datetime import datetime, timezone

def generate_token(nbytes: int = 16) -> str:
    return secrets.token_urlsafe(nbytes)

def utcnow():
    return datetime.now(timezone.utc)
