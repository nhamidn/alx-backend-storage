#!/usr/bin/env python3
"""
Exercise module.
"""
import redis
from uuid import uuid4
from typing import Union


class Cache:
    """ Caching class
    """
    def __init__(self) -> None:
        """__init__ method."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes,  int,  float]) -> str:
        """Store data in Redis with a random key and return the key"""
        key = str(uuid4())
        client = self._redis
        client.set(key, data)
        return key
