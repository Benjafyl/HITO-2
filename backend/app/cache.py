import json
import logging
import os
from functools import lru_cache
from typing import Any

import redis

logger = logging.getLogger("skyconnect.cache")

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() in {"1", "true", "yes", "on"}
FLIGHTS_CACHE_KEY = "flights:all"
ROUTES_CACHE_KEY = "routes:all"
AIRCRAFT_CACHE_KEY = "aircraft:all"
FLIGHTS_TTL_SECONDS = int(os.getenv("FLIGHTS_CACHE_TTL", "60"))
CATALOG_TTL_SECONDS = int(os.getenv("CATALOG_CACHE_TTL", "300"))


@lru_cache(maxsize=1)
def get_redis_client() -> redis.Redis:
    return redis.Redis.from_url(
        REDIS_URL,
        decode_responses=True,
        socket_connect_timeout=0.5,
        socket_timeout=0.5,
    )


def get_cached_json(key: str) -> Any | None:
    if not CACHE_ENABLED:
        return None

    try:
        cached = get_redis_client().get(key)
    except redis.RedisError as exc:
        logger.warning("Redis read failed for key %s: %s", key, exc)
        return None

    if cached is None:
        return None
    return json.loads(cached)


def set_cached_json(key: str, value: Any, ttl_seconds: int) -> None:
    if not CACHE_ENABLED:
        return

    try:
        get_redis_client().setex(key, ttl_seconds, json.dumps(value))
    except redis.RedisError as exc:
        logger.warning("Redis write failed for key %s: %s", key, exc)


def invalidate_cache_keys(*keys: str) -> None:
    if not CACHE_ENABLED:
        return

    if not keys:
        return
    try:
        get_redis_client().delete(*keys)
    except redis.RedisError as exc:
        logger.warning("Redis delete failed for keys %s: %s", keys, exc)
