"""Redis caching configuration for FastAPI application."""

import os
import pickle
from functools import wraps
from typing import Any, Optional

import redis
from redis import Redis

# Redis connection
REDIS_URL = os.getenv("REDIS_URL", "redis://:redis@redis:6379/0")

redis_client: Optional[Redis] = None


def init_redis() -> Redis:
    """Initialize Redis connection."""
    global redis_client
    redis_client = redis.from_url(REDIS_URL, decode_responses=False)
    return redis_client


def get_redis() -> Redis:
    """Get Redis client instance."""
    if redis_client is None:
        init_redis()
    return redis_client


def cache_key(*args, prefix: str = "cache", **kwargs) -> str:
    """Generate cache key from arguments."""
    key_parts = [prefix]
    key_parts.extend(str(arg) for arg in args)
    key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    return ":".join(key_parts)


def cached(prefix: str = "cache", ttl: int = 300):
    """Decorator to cache function results in Redis.

    Args:
        prefix: Cache key prefix
        ttl: Time to live in seconds (default: 5 minutes)

    Example:
        @cached(prefix="users", ttl=600)
        def get_user(user_id: int):
            return db.query(User).filter(User.id == user_id).first()
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            redis = get_redis()
            key = cache_key(*args, prefix=prefix, **kwargs)

            # Try to get from cache
            try:
                cached_value = redis.get(key)
                if cached_value:
                    return pickle.loads(cached_value)
            except Exception as e:
                print(f"Cache get error: {e}")

            # Call function and cache result
            result = func(*args, **kwargs)
            try:
                redis.setex(key, ttl, pickle.dumps(result))
            except Exception as e:
                print(f"Cache set error: {e}")

            return result

        return wrapper

    return decorator


def clear_cache(pattern: str = "*") -> int:
    """Clear cache entries matching pattern.

    Args:
        pattern: Redis key pattern (default: "*" clears all)

    Returns:
        Number of keys deleted
    """
    redis = get_redis()
    keys = redis.keys(pattern)
    if keys:
        return redis.delete(*keys)
    return 0


def cache_set(key: str, value: Any, ttl: int = 300) -> bool:
    """Manually set a cache value.

    Args:
        key: Cache key
        value: Value to cache
        ttl: Time to live in seconds
    """
    redis = get_redis()
    try:
        redis.setex(key, ttl, pickle.dumps(value))
        return True
    except Exception as e:
        print(f"Cache set error: {e}")
        return False


def cache_get(key: str) -> Optional[Any]:
    """Manually get a cache value.

    Args:
        key: Cache key

    Returns:
        Cached value or None
    """
    redis = get_redis()
    try:
        value = redis.get(key)
        return pickle.loads(value) if value else None
    except Exception as e:
        print(f"Cache get error: {e}")
        return None
