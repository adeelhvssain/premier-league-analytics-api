"""Simple API key auth and in-memory rate limiting dependencies."""

from collections import deque
from threading import Lock
import time
from typing import Deque
from typing import Optional

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from . import config


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
_request_history: dict[str, Deque[float]] = {}
_history_lock = Lock()


def get_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """Validate API key from X-API-Key header."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    if api_key != config.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return api_key


def rate_limit(api_key: str = Security(get_api_key)) -> None:
    """Apply simple in-memory fixed-window style rate limiting per API key."""
    now = time.time()
    window_start = now - config.RATE_LIMIT_WINDOW_SECONDS

    with _history_lock:
        history = _request_history.setdefault(api_key, deque())
        while history and history[0] <= window_start:
            history.popleft()

        if len(history) >= config.RATE_LIMIT_REQUESTS:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )

        history.append(now)
