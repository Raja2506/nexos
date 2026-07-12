import json
import redis
from app.config import SETTINGS

# Single shared connection pool for the whole app
redis_client = redis.from_url(SETTINGS["REDIS_URL"], decode_responses=True)


def set_session_data(session_id: str, key: str, value: dict, ttl_seconds: int = 3600) -> None:
    """Store data for a session. Auto-expires after ttl_seconds (default 1 hour)."""
    redis_key = f"session:{session_id}:{key}"
    redis_client.set(redis_key, json.dumps(value), ex=ttl_seconds)


def get_session_data(session_id: str, key: str) -> dict | None:
    """Retrieve data for a session. Returns None if not found or expired."""
    redis_key = f"session:{session_id}:{key}"
    raw = redis_client.get(redis_key)
    return json.loads(raw) if raw else None


def delete_session_data(session_id: str, key: str) -> None:
    """Remove a specific key from a session."""
    redis_key = f"session:{session_id}:{key}"
    redis_client.delete(redis_key)


def clear_session(session_id: str) -> None:
    """Remove ALL keys belonging to a session (e.g., when conversation ends)."""
    pattern = f"session:{session_id}:*"
    keys = redis_client.keys(pattern)
    if keys:
        redis_client.delete(*keys)