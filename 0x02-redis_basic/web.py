#!/usr/bin/env python3
"""
Web module.
"""
import redis
import requests
from functools import wraps
from typing import Callable


redisStore = redis.Redis()


def data_caching(method: Callable) -> Callable:
    """Decorator that cache fetched data from url"""
    @wraps(method)
    def wrapper(url):
        """Function that cache the data"""
        cache_key = f"page:{url}"
        count_key = f"count:{url}"

        redisStore.incr(count_key)

        if redisStore.exists(cache_key):
            return redisStore.get(cache_key).decode()

        result = method(url)
        redisStore.setex(cache_key, 10, result)
        return result

    return wrapper


@data_caching
def get_page(url: str) -> str:
    """Function that get and return the html content of url"""
    html_content = requests.get(url).text
    return html_content
