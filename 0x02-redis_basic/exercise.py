#!/usr/bin/env python3
"""
Exercise module.
"""
import redis
from functools import wraps
from uuid import uuid4
from typing import Union, Callable, Optional, Any


def count_calls(method: Callable) -> Callable:
    """Function that track the number of redis methods calls"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Function that increment call count of a method"""
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """ Caching class
    """
    def __init__(self) -> None:
        """__init__ method."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes,  int,  float]) -> str:
        """Store data in Redis with a random key and return the key"""
        key = str(uuid4())
        client = self._redis
        client.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """Get value data from Redis cache storage"""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, data: bytes) -> str:
        """Converts bytes to string"""
        return data.decode('utf-8')

    def get_int(self, data: bytes) -> int:
        """Converts bytes to integer"""
        return int(data)
