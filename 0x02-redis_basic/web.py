#!/usr/bin/env python3
"""
Web module.
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()


def data_caching(method: Callable) -> Callable:
    """Decorator that cache fetched data from url"""
    @wraps(method)
    def wrapper(url) -> str:
        """Function that cache the data"""
        redis_store.incr(f'count:{url}')
        result = redis_store.get(url)
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(url, 10, result)
        return result
    return wrapper


@data_caching
def get_page(url: str) -> str:
    """Function that get and return the html content of url"""
    return requests.get(url).text
