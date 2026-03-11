"""Security dependencies for API key auth and basic in-memory rate limiting."""

from collections import defaultdict, deque
import threading
import time
from typing import Deque
from typing import Optional

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from . import config

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
_request_history: dict[str, Deque[float]] = defaultdict(deque)
_request_lock = threading.Lock()


def get_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """Validate X-API-Key from request headers."""
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key in X-API-Key header",
        )

    if api_key != config.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return api_key


def rate_limit(api_key: str = Depends(get_api_key)) -> None:
    """Reject requests that exceed the configured per-key request window."""
    now = time.time()
    window_seconds = float(config.RATE_LIMIT_WINDOW_SECONDS)
    max_requests = int(config.RATE_LIMIT_REQUESTS)

    with _request_lock:
        history = _request_history[api_key]

        while history and now - history[0] > window_seconds:
            history.popleft()

        if len(history) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=(
                    f"Rate limit exceeded: max {max_requests} requests "
                    f"in {int(window_seconds)} seconds"
                ),
            )

        history.append(now)
