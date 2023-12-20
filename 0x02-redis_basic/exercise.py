#!/usr/bin/env python3
"""
Exercise module.
"""
import redis
from uuid import uuid4
from typing import Union


class Cache:
    """Cache class."""
    def __init__(self) -> None:
        """Init method of the Cache class."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store data in Redis with a random key and return the key"""
        rand_key = str(uuid4())
        self._redis.set(rand_key, data)
        return rand_key
